# debug_path.py
import miniwob
import os

path = os.path.dirname(miniwob.__file__)
html_path = os.path.join(path, "html")

print(f"MiniWoB is installed at: {path}")
print(f"HTML files should be at: {html_path}")

if os.path.exists(os.path.join(html_path, "miniwob", "click-test-2.html")):
    print("\n[OK] The HTML file exists!")
    print(f"Set this in your environment variables:\nMINIWOB_URL=file://{html_path}")
else:
    print("\n[ERROR] HTML files not found in the expected location.")