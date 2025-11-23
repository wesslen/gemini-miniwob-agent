# serve_miniwob.py
import miniwob
import os
import http.server
import socketserver
import threading
import time

# 1. Find the MiniWoB HTML directory
package_path = os.path.dirname(miniwob.__file__)
web_dir = os.path.join(package_path, "html")

os.chdir(web_dir)

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

# 2. Start the server in a thread
class ThreadedHTTPServer(threading.Thread):
    def run(self):
        with socketserver.TCPServer(("", PORT), Handler) as self.httpd:
            print(f"\n[SERVER] Serving MiniWoB at http://localhost:{PORT}")
            print(f"[SERVER] Mapped to directory: {web_dir}")
            self.httpd.serve_forever()

    def stop(self):
        if hasattr(self, 'httpd'):
            self.httpd.shutdown()
            self.httpd.server_close()

if __name__ == "__main__":
    server = ThreadedHTTPServer()
    server.start()
    
    print("\n[INSTRUCTIONS]")
    print(f"1. Keep this script running.")
    print(f"2. Update your .env file to:")
    print(f"   MINIWOB_URL=http://localhost:{PORT}")
    print("3. Run 'uv run main.py' in a separate terminal.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.stop()