from app import create_app

import sys
import os

# Get the directory of the current file (wsgi.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (containing 'app') to sys.path
sys.path.insert(0, os.path.dirname(current_dir))

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, use_reloader=True)

