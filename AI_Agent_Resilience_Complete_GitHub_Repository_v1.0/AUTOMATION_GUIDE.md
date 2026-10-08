# RVPI Cyber Range Automation Guide — v1.1

## Chosen execution stack

The canonical YAML remains hypervisor-neutral, but the first executable adapter is:

- **Proxmox VE** for VM lifecycle, snapshots, NIC assignment, and isolated virtual switching.
- **pfSense CE** for FW-20 and FW-21 policy enforcement.
- **Ansible + pfsensible.core** for repeatable pfSense configuration.
- **Python + proxmoxer** for Proxmox discovery/restore/NIC operations.
- **Linux `tc` mirroring** on the Proxmox node for passive Zeek observation points.

This keeps research definitions separate from implementation while making the first lab platform reproducible.

## 1. Install controller dependencies

From `automation/`:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml
```

Copy the example files:

```bash
cp .env.example .env
cp inventory/hosts.example.yml inventory/hosts.yml
```

Do **not** store real Proxmox token secrets in Git.

## 2. Create the Proxmox lab bridges

Review:

```text
platform/proxmox/interfaces.snippet
```

Add the two isolated bridges to the Proxmox node:

- `vmbr-lab`: VLAN-aware experimental bridge
- `vmbr-mirror`: isolated destination for Zeek mirror NICs

Apply the network change during a maintenance window using your normal Proxmox network procedure.

## 3. Verify canonical configuration

```bash
cd automation
./rvpi-lab validate
```

The run must not proceed if validation fails.

## 4. Render the Proxmox NIC plan

```bash
./rvpi-lab render-proxmox
```

This writes:

```text
automation/generated/proxmox-plan.yaml
```

The plan uses:

- VLAN 10 — Management
- VLAN 20 — N0 / Red
- VLAN 30 — N1 / DMZ
- VLAN 40 — N2 / Internal
- VLAN 50 — N3 / Protected
- VLAN 60 — S1 / Backup
- VLAN 70 — Telemetry

Zeek monitor NICs use `vmbr-mirror` and have no routable IP.

## 5. Configure Proxmox API authentication

Use a scoped, revocable Proxmox API token. Export the values listed in `.env.example`, for example:

```bash
export PROXMOX_HOST=...
export PROXMOX_NODE=...
export PROXMOX_USER=...
export PROXMOX_TOKEN_ID=...
export PROXMOX_TOKEN_SECRET=...
```

The automation intentionally does not contain real credentials.

## 6. Discover existing VMs by name

The adapter does **not** invent VMIDs. It discovers them by the agreed VM names:

```bash
./rvpi-lab discover-vms
```

Review:

```text
automation/generated/discovered-vms.yaml
```

Every required VM name must resolve exactly once.

## 7. Apply NIC assignments

First inspect the dry run:

```bash
./rvpi-lab apply-nics
```

Only after reviewing it:

```bash
./rvpi-lab apply-nics --apply
```

The fixed firewall NIC order is important because telemetry mirroring refers to firewall NIC indexes.

## 8. Verify pfSense interface assignment

The intended logical interface maps are in:

```text
platform/pfsense/pfsense.yaml
```

### FW-20

| Logical network | pfSense interface |
|---|---|
| N0 External | `wan` |
| N1 DMZ | `lan` |
| Management | `opt1` |

### FW-21

| Logical network | pfSense interface |
|---|---|
| N1 DMZ | `wan` |
| N2 Internal | `lan` |
| N3 Protected | `opt1` |
| S1 Backup | `opt2` |
| Management | `opt3` |

Confirm these assignments in pfSense before applying experiment rules.

## 9. Prepare Ansible access to pfSense

The pfsensible modules need privileged access on pfSense. Use a dedicated automation account and the minimum required privileges. Update:

```text
automation/inventory/hosts.yml
```

The package does not contain passwords or SSH private keys.

## 10. Render a defensive architecture

Example for D2:

```bash
./rvpi-lab render-pfsense --profile D2
```

Outputs:

```text
automation/generated/pfsense-D2.yml
automation/generated/pfsense-D2.manifest.yaml
```

Then review the playbook before applying it:

```bash
ansible-playbook --check generated/pfsense-D2.yml
ansible-playbook generated/pfsense-D2.yml
```

Render D0, D1, D2, or D3 by changing the profile argument.

### Important D2/D3 distinction

The generated pfSense playbook applies the **network policy**. D2/D3 also contain identity/privilege controls. Those controls are preserved in the profile manifest but require separate AD/GPO automation. They are not silently represented as firewall rules.

## 11. Restore the baseline

The restore process uses the snapshots defined in:

```text
restore/baseline.yaml
```

Dry run:

```bash
./rvpi-lab restore
```

Apply:

```bash
./rvpi-lab restore --apply
```

The adapter resolves VM names to actual Proxmox VMIDs before rollback.

## 12. Configure passive monitoring

Once the discovered VM map exists:

```bash
./rvpi-lab render-mirror
```

This creates:

```text
automation/generated/apply-mirror.sh
```

Run that script as root on the Proxmox node **after the relevant VMs are running**.

It mirrors:

- FW-20 N0-facing NIC → ZEEK-01 monitor NIC
- FW-21 N3-facing NIC → ZEEK-02 monitor NIC

The Zeek monitor interfaces remain on the isolated `vmbr-mirror` bridge and should have no IP address.

## 13. Resolve an experiment manifest

```bash
./rvpi-lab resolve-experiment ../experiments/exp1-template.yaml
```

This writes a resolved, self-contained experiment description that should be copied into the run-results directory before execution.

## Recommended pre-run sequence

```text
validate
→ discover VMs
→ restore baseline
→ apply/verify NIC plan
→ verify pfSense interface map
→ render + apply D0/D1/D2/D3
→ start VMs/telemetry
→ apply mirror configuration
→ run preflight reachability tests
→ save resolved experiment manifest
→ start experiment
```

## Deliberate safeguards

- Management and Telemetry are blocked from the attack plane in all profiles.
- Firewall automation uses `RVPI-` rule names.
- Existing non-RVPI firewall policy is not intentionally purged.
- Proxmox changes require an explicit `--apply`.
- Secrets are referenced through environment variables, not embedded in YAML.
- VMIDs are discovered rather than assumed.
- D2/D3 identity policy is not falsely claimed to be enforced by pfSense.
