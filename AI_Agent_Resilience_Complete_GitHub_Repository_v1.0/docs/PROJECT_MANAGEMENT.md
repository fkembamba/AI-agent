# Coordinated Autonomous AI Agent Resilience Study

## IT Project Management Plan

**Project type:** Cybersecurity / AI research infrastructure project  
**Project status:** Planning-to-implementation transition  
**Primary platform:** Cyber range with versioned configuration-as-code  
**Document purpose:** Provide a GitHub-native project-management and technical-readiness document that can be used with GitHub Issues, Milestones, Projects, Pull Requests, and versioned infrastructure files.

---

## 1. Project Team

| Code | Team member | IT project role | Primary responsibility |
|---|---|---|---|
| **FK** | Fred Kembamba | Research / Experiment Owner | Experiment design, integration, automation, data collection, analysis, documentation |
| **DER** | Derrick | Team Leader | Overall coordination, priorities, cross-domain decisions, readiness review, escalation |
| **ANA** | Anatol | Advanced AI Expert | A1/A2/A3 agent design, coordination logic, model/tool behavior, AI validation |
| **GAS** | Gashugi | Cybersecurity & Infrastructure Expert | Virtualization, networking, firewalls, VM/IP inventory, snapshots, telemetry, restore |
| **MAU** | Maurice | Cybersecurity & Infrastructure Expert | Virtualization, networking, firewalls, VM/IP inventory, snapshots, telemetry, restore |

**Responsibility rule:** The first code listed for a task is the primary owner. Derrick is the escalation and accountability point for cross-workstream IT decisions.

---

## 2. Project Charter

| Charter item | Definition |
|---|---|
| **Current phase** | Planning-to-implementation transition; VMs exist, while inventory reconciliation, baseline restore validation, telemetry, agent integration, and pilots remain to be completed. |
| **Primary objective** | Build a reproducible cyber range that compares A1 single-agent, A2 independent multi-agent, and A3 coordinated multi-agent conditions across D0-D3 defensive architectures. |
| **In scope** | Virtualization inventory; N0/N1/N2/N3/S1 networking; firewall/security profiles; AD/identity; Zeek/logging; CALDERA; AI-agent orchestration; snapshots/restore; configuration-as-code; pilots; experiments; analysis artifacts. |
| **Out of scope** | Unauthorized testing of external systems, production changes outside the approved lab, and uncontrolled Internet-facing agent activity. |
| **Primary research comparison** | A3 vs A2 isolates the effect of coordination beyond parallelism. |
| **Project success condition** | A run can be restored, configured, preflight-validated, executed, logged, measured, archived, and reset using versioned artifacts and documented ownership. |

---

## 3. GitHub Project Operating Model

The GitHub repository is the **live implementation record**. Formal reports can still be maintained in Word/PDF, but GitHub should be used for day-to-day IT execution, configuration management, task ownership, evidence, technical review, and experiment versioning.

### Recommended GitHub Project fields

| Field | Values / use |
|---|---|
| **Status** | Backlog, Ready, In Progress, Blocked, Technical Review, Done |
| **Priority** | P0, P1, P2 |
| **Work Package** | WP1-WP10 |
| **Milestone** | M0-M10 |
| **Area** | Infrastructure, Network, Identity, Telemetry, Automation, AI Agent, CALDERA, Experiment, Analysis, Governance |
| **Owner** | FK, DER, ANA, GAS, MAU |
| **Evidence** | Link to config, PR, command output, screenshot, log, dataset, or experiment artifact |
| **Target Date** | Enter only when agreed by the team |
| **Percent Complete** | Optional management field |

### Recommended workflow

`Backlog -> Ready -> In Progress -> Blocked/Technical Review -> Done`

A work item is **Done only when evidence demonstrates the expected state**. Attempting a configuration is not sufficient.

---

## 4. Work Breakdown Structure

| WBS | Work package | Primary deliverable | Owner(s) | Depends on | Status |
|---|---|---|---|---|---|
| **WP1** | Governance & scope | Charter, roles, authorization boundary, change process | DER + FK | None | In Progress |
| **WP2** | Virtualization & asset inventory | Platform/version, VM/IP/NIC inventory, snapshots | GAS + MAU | WP1 | In Progress |
| **WP3** | Network & security profiles | N0-N3/S1, D0-D3, routing/firewall, preflight | GAS + MAU + FK | WP2 | In Progress |
| **WP4** | Identity & host configuration | AD/DNS, GPO, users/groups, least privilege, software/service state | GAS + MAU + FK | WP2, WP3 | TODO |
| **WP5** | Telemetry & logging | Zeek sensors, firewall/host/CALDERA logs, run IDs, UTC synchronization | GAS + MAU + FK | WP2, WP3 | TODO |
| **WP6** | Automation & restore | Platform adapter, snapshot restore, manifest capture, baseline verification | FK + GAS + MAU | WP2, WP3 | In Progress |
| **WP7** | AI-agent & CALDERA integration | A1/A2/A3 modes, coordination bus, action allowlist, controller integration | ANA + FK | WP3, WP5 | TODO |
| **WP8** | Functional pilots | P0 single-agent, P1 independent, P2 coordinated pilot evidence | FK + ANA + GAS + MAU | WP4-WP7 | TODO |
| **WP9** | Experiment pilot matrix | Randomized A1/A2/A3 x D0-D3 pilot matrix and raw artifacts | FK | WP8 | TODO |
| **WP10** | Analysis & reporting | Pilot variance, sample-size decision, findings, limitations, final documentation | FK + DER + ANA | WP9 | TODO |

> **Scheduling rule:** Do not invent dates simply to populate a Gantt chart. Add start/target dates when the remote virtualization platform, actual VM/IP inventory, and team availability are confirmed.

---

## 5. RACI Matrix

| Workstream | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Project governance / priorities | DER | DER | FK, ANA, GAS, MAU | All |
| Research & experimental design | FK | DER | ANA | GAS, MAU |
| Virtualization / VM inventory | GAS, MAU | DER | FK | ANA |
| Network / firewall / segmentation | GAS, MAU | DER | FK | ANA |
| Identity / AD / least privilege | GAS, MAU | DER | FK | ANA |
| Telemetry / logging / time sync | GAS, MAU, FK | DER | ANA | All |
| Automation / restore / manifests | FK, GAS, MAU | DER | ANA | All |
| AI-agent A1/A2/A3 design | ANA, FK | DER | GAS, MAU | All |
| CALDERA / action interface | FK, ANA | DER | GAS, MAU | All |
| Pilot execution P0/P1/P2 | FK, ANA, GAS, MAU | DER | All | All |
| Experiment execution | FK | DER | ANA, GAS, MAU | All |
| Analysis & technical reporting | FK | DER | ANA | GAS, MAU |
| Risk / issue / change control | FK | DER | ANA, GAS, MAU | All |

---

## 6. Milestones and Stage Gates

| ID | Milestone / Gate | Acceptance criterion | Owner | Status |
|---|---|---|---|---|
| **M0** | Project direction agreed | Roles, objective, and experiment direction documented | DER + FK | Done |
| **M1** | Infrastructure inventory gate | Platform confirmed; VM/IP/NIC/snapshot inventory reconciled | GAS + MAU | TODO |
| **M2** | Baseline recovery gate | Restore returns all systems to verified baseline | GAS + MAU + FK | TODO |
| **M3** | Network baseline gate | D0 and D1 implemented; allowed/denied paths and control-plane isolation pass preflight | GAS + MAU + FK | TODO |
| **M4** | Advanced architecture gate | D2/D3 identity, least-privilege, and microsegmentation controls validated | GAS + MAU + FK | TODO |
| **M5** | Telemetry readiness gate | Zeek + firewall + host + CALDERA + agent logs correlate by run ID with acceptable clock drift | GAS + MAU + FK | TODO |
| **M6** | P0 gate | Single-agent functional pilot passes action, telemetry, measurement, and reset checks | FK + ANA | TODO |
| **M7** | P1/P2 gate | Independent and coordinated multi-agent pilots run under equal budgets with complete logs | FK + ANA | TODO |
| **M8** | Experiment readiness review | P0 tasks closed, major risks controlled, runbook approved | DER + Team | TODO |
| **M9** | 12-cell pilot complete | Randomized A1/A2/A3 x D0-D3 pilot matrix completed and archived | FK | TODO |
| **M10** | Full experiment authorization | Pilot variance reviewed; repetitions and analysis plan frozen | DER + FK | TODO |

---

## 7. Risk Register

| ID | Risk | Likelihood | Impact | Owner | Mitigation / control | State |
|---|---|---:|---:|---|---|---|
| R1 | Remote platform differs from assumed adapter | Medium | High | GAS + MAU | Confirm platform/version first; keep YAML hypervisor-neutral; build the correct adapter | Open |
| R2 | VM/IP/NIC inventory incomplete or inconsistent | Medium | High | GAS + MAU | Export from hypervisor/guests and reconcile before changes | Open |
| R3 | Snapshot/restore baseline is unreliable | Medium | High | GAS + MAU + FK | Repeat restore tests; record snapshot IDs; health checks; abort on failure | Open |
| R4 | Firewall/profile misconfiguration changes treatment | Medium | High | GAS + MAU + FK | Configuration-as-code; preflight connectivity matrix; preserve resolved profile per run | Open |
| R5 | Management or Telemetry becomes an attack shortcut | Low | Critical | GAS + MAU | Out-of-band isolation; default deny; explicit route/connectivity preflight | Open |
| R6 | Clock drift or missing telemetry corrupts response-window metrics | Medium | High | GAS + MAU + FK | UTC sync, drift threshold, run-ID correlation, telemetry readiness gate | Open |
| R7 | CPU/RAM/storage contention biases timing | Medium | Medium | GAS + MAU | Stable allocations, resource monitoring, log host utilization | Open |
| R8 | Software/configuration drift across runs | Medium | High | FK + GAS + MAU | Snapshots, manifests, versioned YAML, software inventory, change control | Open |
| R9 | AI-agent nondeterminism obscures coordination effect | High | Medium | ANA + FK | Equal budgets, fixed tools/conditions, seeds where supported, repeated trials, full logs | Open |
| R10 | Unintended external connectivity / scope escape | Low | Critical | DER + GAS + MAU | Restricted/disabled Internet, scope boundary, emergency stop, preflight reachability check | Open |

---

## 8. Current Issue Log

| Issue | Description | Owner | Status | Next action |
|---|---|---|---|---|
| **I-001** | Remote virtualization platform/version not yet confirmed | GAS + MAU | Open | Confirm platform and management access |
| **I-002** | Actual VM/IP/NIC inventory not reconciled with planned table | GAS + MAU + FK | Open | Export inventory and resolve mismatches |
| **I-003** | D2/D3 identity/privilege automation not implemented | GAS + MAU + FK | Open | Define AD/GPO implementation and tests |
| **I-004** | A1/A2/A3 agent modes not implemented end-to-end | ANA + FK | Open | Implement P0 first, then A2/A3 |
| **I-005** | Telemetry not verified end-to-end for all event sources | GAS + MAU + FK | Open | Complete telemetry readiness gate |

---

## 9. Decision Log

| Decision | Statement | State | Owner / approver |
|---|---|---|---|
| **D-001** | Use versioned YAML/configuration-as-code as the canonical experimental definition | Accepted | FK + DER |
| **D-002** | Keep Management and Telemetry outside the attack graph | Accepted | Team |
| **D-003** | Reuse one base topology for D0-D3; vary policies/controls | Accepted | Team |
| **D-004** | Compare A1 vs A2 vs A3 under comparable resource budgets; A3-vs-A2 isolates coordination | Accepted | FK + ANA + DER |
| **D-005** | Reuse the existing VM set and add controllers/containers only where needed | Accepted | Team |
| **D-006** | Select/build the executable platform adapter only after the actual remote virtualization platform is confirmed | Pending | DER + GAS + MAU + FK |

---

## 10. Configuration / Baseline Register

| Artifact | Version | Owner | Status | Configuration-management note |
|---|---|---|---|---|
| Network configuration | v1.0 | FK | Created / validated | Topology, hosts, routes, telemetry, D0-D3 profiles |
| Automation package | v1.1 | FK | Created; platform pending | Current Proxmox/pfSense adapter is provisional |
| Architecture diagram | Current | FK | Created | Includes experiment, AI, restore controllers and agent cluster |
| VM/IP/NIC inventory | TBD | GAS + MAU | Pending | Must reflect actual running environment |
| Baseline snapshots | TBD | GAS + MAU | Pending verification | Snapshot IDs/names must be tested and recorded |
| Experiment manifest | Template | FK | Created | Resolve and archive one copy per run |
| D0-D3 deployed profiles | TBD | GAS + MAU + FK | Pending | Archive effective firewall/identity configuration with each version |

---

## 11. GitHub Issue Conventions

### Issue title format

Use:

`[AREA] Short action-oriented title`

Examples:

- `[INFRA] Export actual VM/IP/NIC inventory`
- `[NET] Validate D1 segmented connectivity matrix`
- `[IDENTITY] Implement D2 least-privilege GPO`
- `[TELEM] Verify Zeek N0-N1 observation point`
- `[AI] Implement A2 independent multi-agent mode`
- `[EXP] Run P0 single-agent functional pilot`
- `[RISK] Validate attack-plane isolation from Management`

### Required issue content

Every implementation issue should contain:

**Work package:** WP#  
**Milestone:** M#  
**Owner(s):** team codes  
**Priority:** P0/P1/P2  
**Dependencies:** issue numbers or work packages  
**Acceptance criteria:** measurable completion conditions  
**Evidence required:** config, command output, log, screenshot, test result, or experiment artifact  
**Change impact:** none / network / identity / agent / experiment baseline  
**Status:** tracked by GitHub Project

---

## 12. GitHub Labels

Use consistent labels:

| Label | Purpose |
|---|---|
| `area:infrastructure` | Hypervisor, VMs, snapshots, storage |
| `area:network` | VLANs, routing, firewall, D0-D3 |
| `area:identity` | AD, DNS, GPO, privileges |
| `area:telemetry` | Zeek, SIEM/logging, time sync |
| `area:automation` | Restore, configuration generation, validation |
| `area:ai-agent` | A1/A2/A3, coordination, agent controller |
| `area:caldera` | CALDERA integration and allowed action mapping |
| `area:experiment` | Pilots and experiment execution |
| `area:analysis` | Metrics, statistics, result processing |
| `area:governance` | RACI, decisions, risks, scope |
| `priority:P0` | Blocking / experiment-critical |
| `priority:P1` | Important |
| `priority:P2` | Enhancements / non-blocking |
| `type:task` | Implementation work |
| `type:risk` | Project or technical risk |
| `type:issue` | Active blocker/problem |
| `type:decision` | Architecture/project decision |
| `type:experiment` | Experimental run or pilot |
| `status:blocked` | Waiting on dependency or decision |

---

## 13. Pull Request and Change-Control Rules

A Pull Request is required for changes to:

- canonical YAML topology or D0-D3 profiles;
- automation scripts;
- AD/GPO or identity policy;
- AI agent configuration;
- CALDERA mappings;
- experiment manifests or metrics;
- baseline snapshot/configuration references.

Every PR should identify:

**Related issue:** `#<issue>`  
**Work package:** `WP#`  
**Change type:** Infrastructure / Network / Identity / AI / Experiment / Documentation  
**Reason:** why the change is required  
**Validation performed:** commands/tests  
**Baseline impact:** Yes/No  
**Experimental comparability impact:** Yes/No  
**Approver(s):** relevant RACI owner(s)

Do not merge a baseline-changing PR until the change has been reviewed and the resulting version is recorded.

---

## 14. Technical Readiness Checklist

### A. Research Question and Experimental Design

- [x] **Central research question defined** — Owner: FK + DER
- [x] **A1/A2/A3 conditions defined** — Owner: FK + ANA
- [x] **D0-D3 architectures defined** — Owner: FK + GAS + MAU
- [x] **Primary metrics defined** — Owner: FK + DER
- [ ] **Freeze inclusion/exclusion and termination rules** — Priority: P0
- [ ] **Freeze statistical analysis plan** — Priority: P1
- [ ] **Pilot-based power/sample-size analysis** — Priority: P1

### B. Virtualization, VM Inventory, and Addressing

- [x] Existing VMs created — GAS + MAU
- [ ] Confirm remote virtualization platform/version — **P0** — GAS + MAU
- [ ] Retrieve actual VM/IP/NIC inventory — **P0** — GAS + MAU
- [ ] Reconcile actual IPs with planned IP table — **P0** — FK + GAS + MAU
- [ ] Document multi-homed firewall NIC ordering — **P0** — GAS + MAU
- [ ] Create and verify baseline snapshots — **P0** — GAS + MAU

### C. Network Configuration and Architecture Switching

- [x] Network architecture designed — FK
- [x] Canonical network YAML v1.0 created — FK
- [ ] Confirm/build adapter for actual hypervisor — **P0** — FK + GAS + MAU
- [ ] Implement and verify D0 — **P0**
- [ ] Implement and verify D1 — **P0**
- [ ] Implement and verify D2 — **P1**
- [ ] Implement and verify D3 — **P1**
- [ ] Implement automated network preflight — **P0**

### D. Identity, Host State, and Reproducibility

- [x] Domain Controller included in design — FK
- [ ] AD/GPO automation for D2/D3 — **P1**
- [ ] Freeze domain membership and user roles — **P1**
- [ ] Freeze software/service state — **P1**
- [ ] Verify one-command baseline restore — **P0**
- [ ] Store baseline hashes/configuration manifest — **P1**

### E. Telemetry and Measurement

- [x] Telemetry architecture designed — FK
- [ ] Deploy/verify Zeek perimeter sensor — **P0**
- [ ] Deploy/verify Zeek internal sensor — **P0**
- [ ] Centralize firewall, host, CALDERA, and controller logs — **P0**
- [ ] Enforce UTC/time synchronization — **P0**
- [ ] Validate extraction of t0, tD, tC, and tI — **P0**

### F. AI Agent and CALDERA Integration

- [x] Agent-control architecture designed — FK + ANA
- [ ] Implement A1 single-agent controller — **P0** — ANA + FK
- [ ] Implement A2 independent multi-agent mode — **P0** — ANA + FK
- [ ] Implement A3 coordinated multi-agent mode — **P0** — ANA + FK
- [ ] Enforce equal A2/A3 resource budgets — **P0** — FK + ANA
- [ ] Define coordination-message schema — **P1** — ANA + FK
- [ ] Define action allowlist / CALDERA mapping — **P0** — FK + ANA

### G. Pilot Experiments

- [ ] P0 single-agent functional pilot — **P0**
- [ ] P1 independent multi-agent pilot — **P0**
- [ ] P2 coordinated multi-agent pilot — **P0**
- [ ] Randomized 12-cell pilot matrix — **P1**
- [ ] Pilot variance / sample-size decision — **P1**
- [ ] Freeze full Experiment 1 runbook — **P0**

### H. Safety, Integrity, and Documentation

- [ ] Document authorized scope boundary — **P0**
- [ ] Verify unintended Internet access is controlled — **P0**
- [ ] Verify abort/emergency-stop mechanism — **P0**
- [ ] Define raw artifact retention policy — **P1**
- [ ] Maintain threats-to-validity log — **P1**
- [ ] Maintain experiment change log/versioning — **P1**

---

## 15. Immediate Next Actions

| Order | Action | Owner(s) | Priority | GitHub issue |
|---:|---|---|---|---|
| 1 | Confirm remote virtualization platform and version | GAS + MAU | P0 | Create |
| 2 | Export actual VM/IP/NIC inventory | GAS + MAU | P0 | Create |
| 3 | Reconcile actual addressing/interface order with canonical YAML | FK + GAS + MAU | P0 | Create |
| 4 | Create/test baseline snapshots | GAS + MAU | P0 | Create |
| 5 | Adapt automation to the actual hypervisor if needed | FK + GAS + MAU | P0 | Create |
| 6 | Implement and verify D0/D1 | GAS + MAU + FK | P0 | Create |
| 7 | Deploy/verify telemetry and UTC synchronization | GAS + MAU + FK | P0 | Create |
| 8 | Implement A1 controller and CALDERA interface | ANA + FK | P0 | Create |
| 9 | Run P0 and validate full reset | FK + ANA + GAS + MAU | P0 | Create |
| 10 | Implement A2/A3 and run P1/P2 after P0 passes | ANA + FK + Team | P0 | Create |

---

## 16. Weekly Project Status

Use a GitHub Discussion, Issue, or Project update with this format:

### Reporting week
`YYYY-MM-DD`

### Overall status
`Green / Amber / Red`

### Completed
- Link completed issues/PRs.

### In progress
- Link current issues/PRs.

### Blockers
- Link blocked issues.

### Risks requiring leadership attention
- Reference risk IDs.

### Decisions required
- Reference decision or issue IDs.

### Milestones at risk
- Reference M#.

### Changes approved
- Link PRs or decision records.

---

## 17. Versioning and Experiment Baselines

Use Git tags/releases for reproducible experimental checkpoints.

Suggested naming:

- `range-baseline-v1.0`
- `network-d0-v1.0`
- `network-d1-v1.0`
- `network-d2-v1.0`
- `network-d3-v1.0`
- `p0-baseline-v1.0`
- `p1-baseline-v1.0`
- `p2-baseline-v1.0`
- `exp1-pilot-v1.0`

Every experimental run should record the Git commit SHA or release/tag used for its configuration.

---

## 18. Definition of Done

A task is considered **Done** only when:

1. the implementation/configuration exists;
2. the expected technical state has been tested;
3. required acceptance criteria pass;
4. evidence is attached or linked to the GitHub issue;
5. related documentation/configuration is committed;
6. required review/approval is complete;
7. baseline or experiment-version impact is recorded.

This definition applies to infrastructure, networking, telemetry, identity, automation, AI-agent, and experiment tasks.
