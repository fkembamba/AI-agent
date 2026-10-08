# Repository Package Validation

- Files: 31
- YAML parse errors: 0
- Canonical validator return code: 0

## Validator output
```text
Validation: PASS
Errors: 0  Warnings: 0
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/spreadsheet_warmup.py", line 718, in _warm_feature_flows
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/spreadsheet_warmup.py", line 509, in _warm_drawing_and_image_flows
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/generated/interface/models.py", line 32861, in bring_to_front
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/rpc/remote.py", line 764, in __call__
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/rpc/client.py", line 175, in call
artifact_tool.rpc.client.RemoteError: Element ordering requires an owning element collection.
```

## Included files
- `.github/workflows/validate-config.yml`
- `.gitignore`
- `AUTOMATION_GUIDE.md`
- `GITHUB_SETUP.md`
- `README.md`
- `UPLOAD_TO_GITHUB.md`
- `VALIDATION.txt`
- `VALIDATION_v1.1.txt`
- `automation/.env.example`
- `automation/ansible.cfg`
- `automation/inventory/hosts.example.yml`
- `automation/requirements.txt`
- `automation/requirements.yml`
- `automation/rvpi-lab`
- `automation/scripts/rvpi_lab.py`
- `docs/PROJECT_MANAGEMENT.md`
- `experiments/exp1-template.yaml`
- `network/base-topology.yaml`
- `network/hosts.yaml`
- `network/profiles/D0-flat.yaml`
- `network/profiles/D1-segmented.yaml`
- `network/profiles/D2-least-privilege.yaml`
- `network/profiles/D3-microsegmented.yaml`
- `network/routing.yaml`
- `network/services.yaml`
- `network/telemetry.yaml`
- `platform/pfsense/pfsense.yaml`
- `platform/proxmox/interfaces.snippet`
- `platform/proxmox/nic-map.yaml`
- `platform/proxmox/proxmox.yaml`
- `restore/baseline.yaml`