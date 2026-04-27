qingchencloud/clawpanel contains a path traversal vulnerability (ZIP Slip, CWE-22) in the `download_frontend_update` extraction logic. The application joins attacker-controlled ZIP entry names to the update directory without proper path normalization and boundary validation, allowing write outside the intended `web-update` directory. This can result in arbitrary file write under the current user context and may lead to code execution depending on the targeted write location.
Affected Product and Version
- Product: qingchencloud/clawpanel
- Observed affected release: `v0.14.0`
- Audit baseline commit: `09fe9c601dfef928a1d771cc65d888639f63e766`
- 
An attacker must be able to make the client process a malicious frontend update ZIP via the `download_frontend_update` path. Realistic vectors include:
1. Compromise of update delivery input (update manifest/domain/CDN/object storage).
2. Any in-app webview context that can invoke the Tauri command `download_frontend_update` with attacker-controlled URL.
No administrator privileges are required.
