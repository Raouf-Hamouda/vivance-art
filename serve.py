#!/usr/bin/env python3
"""Local server for VIVANCE_SITE. Clean URLs like the live site: /portfolio -> portfolio.html, 404 -> 404.html. Port 8774."""
import http.server, os, sys, socketserver
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8774
ROOT = os.path.dirname(os.path.abspath(__file__))
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def translate_path(self, path):
        p = path.split("?")[0].split("#")[0]
        if p == "/": return os.path.join(ROOT, "index.html")
        full = os.path.join(ROOT, p.lstrip("/"))
        if os.path.isdir(full): return os.path.join(full, "index.html")
        if not os.path.exists(full) and os.path.exists(full + ".html"): return full + ".html"
        return full
    def send_error(self, code, message=None, explain=None):
        page = os.path.join(ROOT, "404.html")
        if code == 404 and os.path.exists(page):
            data = open(page, "rb").read(); self.send_response(404); self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data); return
        super().send_error(code, message, explain)
    def end_headers(self): self.send_header("Cache-Control", "no-store"); self.send_header("Accept-Ranges", "bytes"); super().end_headers()
    def send_head(self):
        """Range support (206) so video seeking works like on a real host."""
        rng = self.headers.get("Range"); path = self.translate_path(self.path)
        if not rng or not os.path.isfile(path): return super().send_head()
        try:
            size = os.path.getsize(path); a, b = rng.replace("bytes=", "").split("-"); a = int(a) if a else 0; b = int(b) if b else size - 1; b = min(b, size - 1)
            if a > b or a >= size: self.send_response(416); self.send_header("Content-Range", f"bytes */{size}"); self.end_headers(); return None
            f = open(path, "rb"); f.seek(a)
            self.send_response(206); self.send_header("Content-Type", self.guess_type(path)); self.send_header("Content-Range", f"bytes {a}-{b}/{size}")
            self.send_header("Content-Length", str(b - a + 1)); self.end_headers()
            class Part:
                def __init__(s, fh, n): s.fh, s.n = fh, n
                def read(s, k=-1):
                    if s.n <= 0: return b""
                    d = s.fh.read(s.n if k < 0 else min(k, s.n)); s.n -= len(d); return d
                def close(s): s.fh.close()
            return Part(f, b - a + 1)
        except Exception: return super().send_head()
    def log_message(self, *a): pass
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", PORT), H) as s:
    print(f"VIVANCE_SITE  http://localhost:{PORT}/DESIGN_SYSTEM.html"); s.serve_forever()
