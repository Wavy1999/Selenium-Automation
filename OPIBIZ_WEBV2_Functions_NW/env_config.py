"""
env_config.py
==============
Single source of truth for environment-specific settings (currently just
BASE_URL). All Selenium modules should import BASE_URL from here instead of
hardcoding URLs.

Why this exists:
-----------------
Previously, each module (WHouse.py, MOrder.py, AnotherBank.py, etc.) had its
own hardcoded copy of the environment URL (e.g. "http://vm-app-dev01:9001").
When the environment changed, every file had to be edited individually and
it was easy to miss one.

Now, the URL lives in a single ".env" file at the project root. To point the
whole automation suite at a new environment, edit ONLY the .env file:

    BASE_URL=http://172.16.40.154:9000

Usage in any module:
---------------------
    from env_config import BASE_URL

    driver.get(f"{BASE_URL}/ShopManagement/Warehouse")

Setup (one-time):
------------------
    pip install python-dotenv

Place the .env file in the same directory this file resolves its path from
(project root), or set BASE_URL as a real OS/CI environment variable — real
env vars always take precedence over the .env file.
"""

import os
from dotenv import load_dotenv

# Resolve the .env file relative to this file's location so it's found
# regardless of the current working directory the tests are launched from.
_ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

# override=False -> if BASE_URL is already set as a real OS/CI env var,
# that value wins over whatever is in the .env file.
load_dotenv(dotenv_path=_ENV_PATH, override=False)

# ---- Base URL used by every module ----
# Falls back to the current default environment if .env is missing entirely.
BASE_URL = os.getenv("BASE_URL", "http://172.16.40.154:9000").rstrip("/")
