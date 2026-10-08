# AI Agent Resilience Cyber-Range Project

This repository is the **live IT project-management and technical implementation workspace** for the Coordinated Autonomous AI Agent Resilience Study.

It combines:

- GitHub-native project management;
- network configuration-as-code;
- D0-D3 defensive architecture profiles;
- cyber-range host and routing definitions;
- restore/baseline definitions;
- experiment manifests;
- Proxmox/pfSense adapter work;
- automation and validation scripts;
- GitHub issue / pull-request templates.

## Repository map

```text
.
├── README.md
├── GITHUB_SETUP.md
├── AUTOMATION_GUIDE.md
├── docs/
│   └── PROJECT_MANAGEMENT.md
├── network/
│   ├── base-topology.yaml
│   ├── hosts.yaml
│   ├── routing.yaml
│   ├── services.yaml
│   ├── telemetry.yaml
│   └── profiles/
│       ├── D0-flat.yaml
│       ├── D1-segmented.yaml
│       ├── D2-least-privilege.yaml
│       └── D3-microsegmented.yaml
├── restore/
│   └── baseline.yaml
├── experiments/
│   └── exp1-template.yaml
├── platform/
│   ├── proxmox/
│   └── pfsense/
├── automation/
│   ├── rvpi-lab
│   ├── scripts/
│   │   └── rvpi_lab.py
│   ├── inventory/
│   ├── requirements.txt
│   └── requirements.yml
└── .github/
    ├── ISSUE_TEMPLATE/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        └── validate-config.yml
```

## Start here

1. Read [`docs/PROJECT_MANAGEMENT.md`](docs/PROJECT_MANAGEMENT.md).
2. Read [`GITHUB_SETUP.md`](GITHUB_SETUP.md).
3. Confirm the actual remote virtualization platform before treating the Proxmox adapter as authoritative.
4. Export and reconcile the real VM/IP/NIC inventory.
5. Run local configuration validation:

```bash
python3 -m pip install PyYAML
python3 automation/scripts/rvpi_lab.py validate
```

## Important

The current Proxmox/pfSense platform adapter is **provisional** until the team confirms what virtualization platform is actually used on the remote infrastructure.

The files under `network/`, `restore/`, and `experiments/` are the canonical research definitions and should remain platform-neutral where practical.

## Repository privacy

Use a **private repository** if this project contains infrastructure topology, security controls, host configuration, experiment details, or other non-public lab information.

Never commit passwords, private keys, API tokens, `.env` files, or other secrets.
