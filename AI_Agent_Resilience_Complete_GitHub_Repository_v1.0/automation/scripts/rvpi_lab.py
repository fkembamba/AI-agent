#!/usr/bin/env python3
"""
RVPI cyber-range orchestration helper.

Safe defaults:
- validation/rendering are local only;
- Proxmox-changing operations require --apply;
- firewall playbooks are rendered, not silently executed;
- management and telemetry networks are protected in every profile.
"""
from __future__ import annotations
import argparse, os, sys, time, ipaddress, subprocess, json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

def yload(p):
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ydump(obj, p):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        yaml.safe_dump(obj, f, sort_keys=False)

def path_for_profile(pid):
    m = {
        "D0": ROOT/"network/profiles/D0-flat.yaml",
        "D1": ROOT/"network/profiles/D1-segmented.yaml",
        "D2": ROOT/"network/profiles/D2-least-privilege.yaml",
        "D3": ROOT/"network/profiles/D3-microsegmented.yaml",
    }
    if pid not in m:
        raise SystemExit(f"Unknown profile: {pid}")
    return m[pid]

def resolve_profile(pid):
    obj = yload(path_for_profile(pid))
    parent = obj.get("extends")
    if not parent:
        return obj
    base = resolve_profile(parent)
    # Keep inherited blocks and overlay child blocks. For D3, microsegmentation
    # is intentionally authoritative for east-west rules.
    merged = dict(base)
    for k, v in obj.items():
        if k == "extends":
            continue
        if isinstance(v, dict) and isinstance(merged.get(k), dict):
            z = dict(merged[k]); z.update(v); merged[k] = z
        else:
            merged[k] = v
    merged["_inheritance"] = [parent] + base.get("_inheritance", [])
    return merged

def validate():
    errors, warnings = [], []
    topo = yload(ROOT/"network/base-topology.yaml")
    hosts = yload(ROOT/"network/hosts.yaml")["hosts"]
    services = yload(ROOT/"network/services.yaml")["services"]
    nicmap = yload(ROOT/"platform/proxmox/nic-map.yaml")["vms"]
    pfs = yload(ROOT/"platform/pfsense/pfsense.yaml")

    nets = {}
    for n, cfg in topo["networks"].items():
        try:
            nets[n] = ipaddress.ip_network(cfg["subnet"])
        except Exception as e:
            errors.append(f"Network {n}: {e}")

    seen = {}
    for h, cfg in hosts.items():
        for ifn, iface in cfg.get("interfaces", {}).items():
            ip = iface.get("ip")
            net = iface.get("network")
            if net not in nets:
                errors.append(f"{h}.{ifn}: unknown network {net}")
                continue
            if ip:
                try:
                    a = ipaddress.ip_address(ip)
                    if a not in nets[net]:
                        errors.append(f"{h}.{ifn}: {ip} not inside {nets[net]}")
                    if ip in seen:
                        errors.append(f"Duplicate IP {ip}: {seen[ip]} and {h}.{ifn}")
                    seen[ip] = f"{h}.{ifn}"
                except Exception as e:
                    errors.append(f"{h}.{ifn}: invalid IP {ip}: {e}")

    for h in hosts:
        if h not in nicmap:
            warnings.append(f"{h}: no Proxmox NIC map entry")
    for h in nicmap:
        if h not in hosts:
            warnings.append(f"{h}: Proxmox NIC map has no canonical host entry")

    # profile checks
    valid_targets = set(hosts)
    valid_networks = set(nets)
    for pid in ["D0","D1","D2","D3"]:
        p = resolve_profile(pid)
        for block in [p.get("policy",{}).get("rules",[]),
                      p.get("microsegmentation",{}).get("allowed_flows",[])]:
            for r in block:
                for key in ["from","to"]:
                    v = r.get(key)
                    if isinstance(v, str) and v not in valid_networks and v != "*":
                        warnings.append(f"{pid}:{r.get('id')}: {key}={v} is not a canonical network")
                for key in ["from_host","to_host","source","destination"]:
                    v = r.get(key)
                    if isinstance(v, str) and v not in valid_targets and v not in valid_networks and v != "*":
                        warnings.append(f"{pid}:{r.get('id')}: {key}={v} is not a canonical host/network")
                svcs = r.get("services",[])
                for s in svcs:
                    if s not in services:
                        errors.append(f"{pid}:{r.get('id')}: unknown service {s}")

    # protect control planes
    for pnet in ["management","telemetry"]:
        if topo["networks"][pnet].get("attack_plane") is not False:
            errors.append(f"{pnet} must have attack_plane: false")

    print(f"Validation: {'PASS' if not errors else 'FAIL'}")
    print(f"Errors: {len(errors)}  Warnings: {len(warnings)}")
    for x in errors: print("ERROR:", x)
    for x in warnings: print("WARN :", x)
    return 1 if errors else 0

def proxmox_plan(out):
    plat = yload(ROOT/"platform/proxmox/proxmox.yaml")
    nmap = plat["network_map"]
    vmmap = yload(ROOT/"platform/proxmox/nic-map.yaml")
    plan = {"bridge": plat["switching"], "vms": {}, "mirrors": vmmap.get("mirrors", [])}
    for lname, v in vmmap["vms"].items():
        plan["vms"][lname] = {"proxmox_name": v["proxmox_name"], "nics": {}}
        for netx, nic in v["nics"].items():
            nw = nic["network"]
            m = nmap[nw]
            value = f"{nic.get('model','virtio')},bridge={m['bridge']}"
            if m.get("vlan_tag") is not None:
                value += f",tag={m['vlan_tag']}"
            plan["vms"][lname]["nics"][netx] = value
    ydump(plan, out)
    print(f"Wrote Proxmox NIC/bridge plan: {out}")

def aliases():
    topo = yload(ROOT/"network/base-topology.yaml")
    hosts = yload(ROOT/"network/hosts.yaml")["hosts"]
    services = yload(ROOT/"network/services.yaml")["services"]
    result = []
    for n,cfg in topo["networks"].items():
        result.append(dict(name=f"RVPI_{n.upper()}", type="network",
                           address=cfg["subnet"], descr=f"RVPI network {n}"))
    for h,cfg in hosts.items():
        # choose first attack-plane/data IP
        for iface in cfg.get("interfaces",{}).values():
            if iface.get("ip") and iface.get("network") not in ("management","telemetry"):
                result.append(dict(name=f"RVPI_HOST_{h.upper()}", type="host",
                                   address=iface["ip"], descr=f"RVPI host {h}"))
                break
    for s,cfg in services.items():
        result.append(dict(name=f"RVPI_PORT_{s.upper()}", type="port",
                           address=" ".join(str(x) for x in cfg["ports"]),
                           descr=f"RVPI service {s}"))
    return result

def target_alias(x):
    if x in ("any","*"): return "any"
    hosts = yload(ROOT/"network/hosts.yaml")["hosts"]
    topo = yload(ROOT/"network/base-topology.yaml")["networks"]
    if x in hosts: return f"RVPI_HOST_{x.upper()}"
    if x in topo: return f"RVPI_{x.upper()}"
    return x

def service_cfg(s):
    return yload(ROOT/"network/services.yaml")["services"][s]

def source_zone_for_host(host):
    h = yload(ROOT/"network/hosts.yaml")["hosts"][host]
    for iface in h.get("interfaces",{}).values():
        if iface.get("network") not in ("management","telemetry") and iface.get("ip"):
            return iface["network"]
    raise ValueError(f"No data/attack-plane network for host {host}")

def pick_firewall(source_zone):
    if source_zone == "n0_external":
        return "fw20"
    if source_zone in ("n1_dmz","n2_internal","n3_protected","s1_backup"):
        return "fw21"
    raise ValueError(f"No firewall routing source zone {source_zone}")

def collect_flows(pid):
    p = resolve_profile(pid)
    flows = []
    # perimeter treatment from inherited D0/D1 policy structures
    perimeter = p.get("policy",{}).get("perimeter",{})
    for r in perimeter.get("rules",[]):
        rr = dict(r)
        rr.setdefault("id", f"{pid}-PER-{len(flows)+1:03d}")
        flows.append(rr)

    # D1/D2 explicit rules
    if pid in ("D1","D2"):
        flows.extend(p.get("policy",{}).get("rules",[]))

    # D3: retain inherited perimeter but use microsegmentation for east-west
    if pid == "D3":
        flows.extend(p.get("microsegmentation",{}).get("allowed_flows",[]))

    return flows

def normalize_rule_sources(r):
    if "from_host" in r:
        return [(source_zone_for_host(r["from_host"]), r["from_host"])]
    if "source" in r:
        s = r["source"]
        if s in yload(ROOT/"network/hosts.yaml")["hosts"]:
            return [(source_zone_for_host(s), s)]
        return [(s, s)]
    if "sources" in r:
        return [(source_zone_for_host(h), h) for h in r["sources"]]
    if "from" in r:
        return [(r["from"], r["from"])]
    raise ValueError(f"Cannot determine source: {r}")

def normalize_rule_destinations(r):
    if "to_host" in r: return [r["to_host"]]
    if "to_hosts" in r: return r["to_hosts"]
    if "destination" in r: return [r["destination"]]
    if "destinations" in r: return r["destinations"]
    if "to" in r: return [r["to"]]
    return ["any"]

def rule_registry():
    names = set()
    for pid in ["D0","D1","D2","D3"]:
        if pid == "D0":
            for fw in ["fw20","fw21"]:
                for iface in ["wan","lan","opt1","opt2","opt3"]:
                    names.add(f"RVPI-{pid}-{fw}-{iface}-BLOCK-MGMT")
                    names.add(f"RVPI-{pid}-{fw}-{iface}-BLOCK-TELEM")
                    names.add(f"RVPI-{pid}-{fw}-{iface}-ALLOW-ENTERPRISE")
        for r in collect_flows(pid):
            for _, src in normalize_rule_sources(r):
                for dst in normalize_rule_destinations(r):
                    for svc in r.get("services",["any"]):
                        names.add(f"RVPI-{pid}-{r.get('id','FLOW')}-{src}-{dst}-{svc}"[:120])
    return sorted(names)

def render_pfsense(pid, out):
    pf = yload(ROOT/"platform/pfsense/pfsense.yaml")["firewalls"]
    topo = yload(ROOT/"network/base-topology.yaml")["networks"]
    managed_prefix = "RVPI-"
    tasks_by_fw = {"fw20": [], "fw21": []}

    # Alias tasks on both firewalls
    alias_tasks = [{
        "name": f"Alias {a['name']}",
        "pfsensible.core.pfsense_alias": {
            "name": a["name"], "type": a["type"], "address": a["address"],
            "descr": a["descr"], "state": "present"
        }
    } for a in aliases()]

    # Remove previously managed RVPI rules by known names. Ignore names absent.
    cleanup_names = rule_registry()

    # Create ordered rule task helper
    order = {"fw20": {}, "fw21": {}}
    def add_rule(fw, iface, name, action, source, destination,
                 protocol="any", destination_port=None, log=True):
        key = (fw, iface)
        prev = order[fw].get(iface)
        spec = {
            "name": name,
            "action": action,
            "interface": iface,
            "ipprotocol": "inet",
            "protocol": protocol,
            "source": source,
            "destination": destination,
            "log": log,
            "state": "present",
        }
        if destination_port:
            spec["destination_port"] = destination_port
        if prev:
            spec["after"] = prev
        else:
            spec["after"] = "top"
        tasks_by_fw[fw].append({"name": name, "pfsensible.core.pfsense_rule": spec})
        order[fw][iface] = name

    # Apply control-plane blocks on every attack-facing interface.
    for fw, zones in [("fw20",["n0_external","n1_dmz"]),
                      ("fw21",["n1_dmz","n2_internal","n3_protected","s1_backup"])]:
        for zone in zones:
            iface = pf[fw]["interfaces"][zone]
            add_rule(fw, iface, f"RVPI-{pid}-{fw}-{iface}-BLOCK-MGMT",
                     "block", "any", "RVPI_MANAGEMENT", log=True)
            add_rule(fw, iface, f"RVPI-{pid}-{fw}-{iface}-BLOCK-TELEM",
                     "block", "any", "RVPI_TELEMETRY", log=True)

    if pid == "D0":
        # Perimeter remains constrained to declared public services.
        for r in collect_flows("D0"):
            for sz, src in normalize_rule_sources(r):
                fw = pick_firewall(sz); iface = pf[fw]["interfaces"][sz]
                for dst in normalize_rule_destinations(r):
                    for svc in r.get("services",["any"]):
                        sc = service_cfg(svc)
                        add_rule(fw, iface, f"RVPI-{pid}-{r.get('id','PER')}-{src}-{dst}-{svc}"[:120],
                                 "pass", target_alias(src), target_alias(dst),
                                 protocol=sc["protocol"],
                                 destination_port=f"RVPI_PORT_{svc.upper()}")

        # Flat enterprise: broad routed connectivity only among N1/N2/N3/S1.
        enterprise_alias = "RVPI_ENTERPRISE_ATTACK_PLANE"
        enterprise_nets = " ".join(topo[n]["subnet"] for n in ["n1_dmz","n2_internal","n3_protected","s1_backup"])
        alias_tasks.append({
            "name": f"Alias {enterprise_alias}",
            "pfsensible.core.pfsense_alias": {
                "name": enterprise_alias, "type": "network", "address": enterprise_nets,
                "descr": "D0 enterprise attack plane", "state": "present"
            }
        })
        for zone in ["n1_dmz","n2_internal","n3_protected","s1_backup"]:
            fw = "fw21"; iface = pf[fw]["interfaces"][zone]
            add_rule(fw, iface, f"RVPI-{pid}-{fw}-{iface}-ALLOW-ENTERPRISE",
                     "pass", target_alias(zone), enterprise_alias, protocol="any")
    else:
        for r in collect_flows(pid):
            for sz, src in normalize_rule_sources(r):
                fw = pick_firewall(sz); iface = pf[fw]["interfaces"][sz]
                for dst in normalize_rule_destinations(r):
                    for svc in r.get("services",["any"]):
                        if svc == "any":
                            proto, port = "any", None
                        else:
                            sc = service_cfg(svc)
                            proto, port = sc["protocol"], f"RVPI_PORT_{svc.upper()}"
                        add_rule(fw, iface, f"RVPI-{pid}-{r.get('id','FLOW')}-{src}-{dst}-{svc}"[:120],
                                 "pass", target_alias(src), target_alias(dst),
                                 protocol=proto, destination_port=port)

    plays = []
    for fw in ["fw20","fw21"]:
        cleanup = [{
            "name": f"Remove previous managed rule {n}",
            "pfsensible.core.pfsense_rule": {
                "name": n,
                "interface": "floating",
                "state": "absent"
            },
            "ignore_errors": True
        } for n in []]  # intentionally disabled: rule deletion requires original interface
        plays.append({
            "name": f"Apply RVPI {pid} profile to {fw}",
            "hosts": fw,
            "gather_facts": False,
            "become": True,
            "tasks": alias_tasks + tasks_by_fw[fw]
        })
    ydump(plays, out)

    # Human-readable manifest with identity controls not implemented by pfSense.
    manifest = {
        "profile": pid,
        "playbook": str(out),
        "note": "Only RVPI-prefixed rules are created. Existing non-RVPI rules are preserved.",
        "identity_controls": resolve_profile(pid).get("identity_policy"),
        "privilege_controls": resolve_profile(pid).get("privilege_policy"),
        "warning": "D2/D3 identity/privilege controls require separate AD/GPO automation; this playbook applies the network/firewall portion."
    }
    ydump(manifest, Path(out).with_suffix(".manifest.yaml"))
    print(f"Wrote pfSense playbook: {out}")
    print(f"Wrote manifest: {Path(out).with_suffix('.manifest.yaml')}")

def proxmox_client():
    try:
        from proxmoxer import ProxmoxAPI
    except ImportError:
        raise SystemExit("Install automation/requirements.txt first (proxmoxer missing).")
    host = os.getenv("PROXMOX_HOST")
    user = os.getenv("PROXMOX_USER")
    tid = os.getenv("PROXMOX_TOKEN_ID")
    sec = os.getenv("PROXMOX_TOKEN_SECRET")
    if not all([host,user,tid,sec]):
        raise SystemExit("Set PROXMOX_HOST, PROXMOX_USER, PROXMOX_TOKEN_ID, PROXMOX_TOKEN_SECRET.")
    verify = os.getenv("PROXMOX_VERIFY_SSL","true").lower() not in ("0","false","no")
    return ProxmoxAPI(host, user=user, token_name=tid, token_value=sec, verify_ssl=verify)

def discover_vms(out):
    p = proxmox_client()
    resources = p.cluster.resources.get(type="vm")
    wanted = yload(ROOT/"platform/proxmox/nic-map.yaml")["vms"]
    by_name = {}
    for r in resources:
        if r.get("type") == "qemu":
            by_name.setdefault(r.get("name"), []).append(r)
    result = {}
    errors=[]
    for logical,cfg in wanted.items():
        name = cfg["proxmox_name"]
        found = by_name.get(name,[])
        if len(found) != 1:
            errors.append(f"{logical}: expected exactly one VM named {name}, found {len(found)}")
        else:
            result[logical] = {"name": name, "vmid": found[0]["vmid"], "node": found[0]["node"]}
    ydump({"vms": result, "errors": errors}, out)
    print(f"Wrote discovered VM map: {out}")
    if errors:
        for e in errors: print("ERROR:", e)
        return 1
    return 0

def wait_task(p, node, upid, timeout=600):
    deadline=time.time()+timeout
    while time.time() < deadline:
        st = p.nodes(node).tasks(upid).status.get()
        if st.get("status") == "stopped":
            if st.get("exitstatus") not in (None,"OK"):
                raise RuntimeError(f"Task failed: {upid}: {st}")
            return
        time.sleep(2)
    raise TimeoutError(f"Timed out waiting for {upid}")

def restore(dmap_path, apply=False):
    base = yload(ROOT/"restore/baseline.yaml")
    dmap = yload(dmap_path)
    if dmap.get("errors"):
        raise SystemExit("Discovered VM map contains errors; fix before restore.")
    actions=[]
    for phase in base["restore_order"]:
        for h in phase["hosts"]:
            if h not in dmap["vms"]:
                actions.append(("SKIP",h,"not in discovered VM map"))
                continue
            vm = dmap["vms"][h]
            snap = base["snapshot_map"][h]
            actions.append(("ROLLBACK",h,vm["node"],vm["vmid"],snap))
    if not apply:
        for a in actions: print(*a)
        print("Dry run only. Re-run with --apply to execute snapshot rollback.")
        return 0
    p=proxmox_client()
    for a in actions:
        if a[0] != "ROLLBACK":
            print(*a); continue
        _,h,node,vmid,snap=a
        print(f"Rolling back {h} ({vmid}) -> {snap}")
        upid=p.nodes(node).qemu(vmid).snapshot(snap).rollback.post()
        wait_task(p,node,upid)
    print("Snapshot rollback completed.")
    return 0

def apply_nics(dmap_path, apply=False):
    dmap=yload(dmap_path)
    plan_path=ROOT/"automation/generated/proxmox-plan.yaml"
    if not plan_path.exists():
        proxmox_plan(plan_path)
    plan=yload(plan_path)
    actions=[]
    for logical,v in plan["vms"].items():
        if logical not in dmap.get("vms",{}):
            continue
        vm=dmap["vms"][logical]
        actions.append((logical,vm,v["nics"]))
    if not apply:
        for logical,vm,nics in actions:
            print(logical, vm["vmid"], nics)
        print("Dry run only. Re-run with --apply to modify VM NIC definitions.")
        return 0
    p=proxmox_client()
    for logical,vm,nics in actions:
        print(f"Updating NICs: {logical} ({vm['vmid']})")
        p.nodes(vm["node"]).qemu(vm["vmid"]).config.put(**nics)
    print("NIC updates submitted.")
    return 0

def render_mirror(dmap_path, out):
    dmap=yload(dmap_path)["vms"]
    mirrors=yload(ROOT/"platform/proxmox/nic-map.yaml").get("mirrors",[])
    lines=["#!/bin/sh","set -eu","","# Run as root on the Proxmox node after VMs are started.",""]
    for m in mirrors:
        s=dmap[m["source_vm"]]["vmid"]; d=dmap[m["destination_vm"]]["vmid"]
        sidx=int(m["source_nic"].replace("net","")); didx=int(m["destination_nic"].replace("net",""))
        sdev=f"tap{s}i{sidx}"; ddev=f"tap{d}i{didx}"
        lines += [
            f"# {m['id']}: {m['source_vm']} {m['source_nic']} -> {m['destination_vm']} {m['destination_nic']}",
            f"tc qdisc replace dev {sdev} clsact",
        ]
        if "ingress" in m["directions"]:
            lines.append(f"tc filter replace dev {sdev} ingress pref 10 matchall action mirred egress mirror dev {ddev}")
        if "egress" in m["directions"]:
            lines.append(f"tc filter replace dev {sdev} egress pref 10 matchall action mirred egress mirror dev {ddev}")
        lines.append("")
    Path(out).write_text("\n".join(lines)+"\n", encoding="utf-8")
    os.chmod(out,0o755)
    print(f"Wrote mirror configuration script: {out}")

def resolve_experiment(exp_path, out):
    exp=yload(exp_path)
    arch=Path(exp["experiment"]["configuration"]["architecture_profile"]).name
    pid=arch.split("-")[0]
    resolved={
        "experiment": exp["experiment"],
        "resolved_profile": resolve_profile(pid),
        "base_topology": yload(ROOT/"network/base-topology.yaml"),
        "hosts": yload(ROOT/"network/hosts.yaml"),
        "services": yload(ROOT/"network/services.yaml"),
        "routing": yload(ROOT/"network/routing.yaml"),
        "telemetry": yload(ROOT/"network/telemetry.yaml"),
    }
    ydump(resolved,out)
    print(f"Wrote resolved experiment: {out}")

def main():
    ap=argparse.ArgumentParser()
    sp=ap.add_subparsers(dest="cmd",required=True)

    sp.add_parser("validate")

    p=sp.add_parser("render-proxmox"); p.add_argument("--out", default=str(ROOT/"automation/generated/proxmox-plan.yaml"))
    p=sp.add_parser("render-pfsense"); p.add_argument("--profile", choices=["D0","D1","D2","D3"], required=True); p.add_argument("--out")
    p=sp.add_parser("discover-vms"); p.add_argument("--out", default=str(ROOT/"automation/generated/discovered-vms.yaml"))
    p=sp.add_parser("restore"); p.add_argument("--vm-map", default=str(ROOT/"automation/generated/discovered-vms.yaml")); p.add_argument("--apply",action="store_true")
    p=sp.add_parser("apply-nics"); p.add_argument("--vm-map", default=str(ROOT/"automation/generated/discovered-vms.yaml")); p.add_argument("--apply",action="store_true")
    p=sp.add_parser("render-mirror"); p.add_argument("--vm-map", default=str(ROOT/"automation/generated/discovered-vms.yaml")); p.add_argument("--out", default=str(ROOT/"automation/generated/apply-mirror.sh"))
    p=sp.add_parser("resolve-experiment"); p.add_argument("experiment"); p.add_argument("--out", default=str(ROOT/"automation/generated/resolved-experiment.yaml"))

    a=ap.parse_args()
    if a.cmd=="validate": return validate()
    if a.cmd=="render-proxmox": return proxmox_plan(a.out) or 0
    if a.cmd=="render-pfsense":
        out=a.out or str(ROOT/f"automation/generated/pfsense-{a.profile}.yml")
        return render_pfsense(a.profile,out) or 0
    if a.cmd=="discover-vms": return discover_vms(a.out)
    if a.cmd=="restore": return restore(a.vm_map,a.apply)
    if a.cmd=="apply-nics": return apply_nics(a.vm_map,a.apply)
    if a.cmd=="render-mirror": return render_mirror(a.vm_map,a.out) or 0
    if a.cmd=="resolve-experiment": return resolve_experiment(a.experiment,a.out) or 0

if __name__=="__main__":
    raise SystemExit(main())
