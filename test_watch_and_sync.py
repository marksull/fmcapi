"""
Manual integration test for DynamicObject.watch_and_sync().

Steps performed:
  1. Connect to FMC
  2. List all existing Dynamic Objects
  3. List all current mappings for the "servers" Dynamic Object (if it exists)
  4. Start watch_and_sync() pointed at test_watchdog/servers.txt

To trigger a sync while the watcher is running, edit and save the file:
  echo "10.99.99.99" >> test_watchdog/servers.txt

Press Ctrl+C to stop the watcher.

Usage
-----
  # Edit the credentials below, then run:
  python test_watch_and_sync.py

Local package setup (run once):
  pip install -e .       # editable install — uses this source tree directly
  pip install watchdog   # required for watch_and_sync()

Verify local package is active:
  python -c "import fmcapi; print(fmcapi.__file__)"
  # Should print .../fmcapi/fmcapi/__init__.py
"""

import logging
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Ensure the LOCAL fmcapi source tree is used even if another version is
# installed system-wide.  Remove this block if you rely on pip install -e .
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))

import fmcapi  # noqa: E402

# ===========================================================================
# *** SET THESE TO MATCH YOUR FMC ENVIRONMENT ***
# ===========================================================================

# Path to the directory (or glob) that watch_and_sync() will monitor.
# The filename stem becomes the Dynamic Object name, so servers.txt -> "servers"
WATCH_PATH = str(Path(__file__).resolve().parent / "test_watchdog")
# ===========================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("test_watch_and_sync.log"),
    ],
)


def get_all_dynamic_objects(fmc):
    """Fetch and log every Dynamic Object currently on the FMC."""
    logging.info("--- Step 1: Fetching all Dynamic Objects ---")
    result = fmcapi.DynamicObject(fmc=fmc).get()
    items = result.get("items", [])
    if not items:
        logging.info("  No Dynamic Objects found on FMC.")
    for obj in items:
        logging.info(f"  [{obj.get('id')}]  {obj.get('name')}  type={obj.get('objectType')}")
    return items


def get_mappings_for_object(fmc, name):
    """
    Fetch and log the current IP mappings for a named Dynamic Object.

    :param fmc: (object) Active FMC session.
    :param name: (str) Dynamic Object name to look up.
    """
    logging.info(f"--- Step 2: Fetching mappings for Dynamic Object '{name}' ---")

    # Look up the object to get its ID
    dyn = fmcapi.DynamicObject(fmc=fmc, name=name)
    response = dyn.get()

    if not response:
        logging.info(f"  Dynamic Object '{name}' does not exist on FMC yet.")
        return

    obj_id = response["id"]
    logging.info(f"  Found '{name}' with id={obj_id}")

    # Fetch its mappings
    mappings_obj = fmcapi.DynamicObjectMappings(fmc=fmc, id=obj_id)
    mapping_response = mappings_obj.get()

    ips = []
    if mapping_response:
        ips = mapping_response.get("items", [])

    if ips:
        logging.info(f"  Current mappings ({len(ips)} IPs):")
        for ip in ips:
            logging.info(f"    {ip}")
    else:
        logging.info(f"  No mappings currently set for '{name}'.")


def main():
    logging.info("Connecting to FMC at %s ...", FMC_HOST)

    with fmcapi.FMC(
        host="svldmz2-cp-corp-fmc1.cisco.com",
        username="dcn_firewall.gen",
        password= "BtqWL8734K22NpGidZ.",
    ).__enter__() as fmc:

        # Step 1 — list all existing dynamic objects
        get_all_dynamic_objects(fmc)

        # Step 2 — show current mappings for the "servers" object
        # (derived from servers.txt — change this name if you rename the file)
        get_mappings_for_object(fmc, name="servers")

        # Step 3 — start the long-running watcher
        logging.info("--- Step 3: Starting watch_and_sync() ---")
        logging.info("  Watching : %s", WATCH_PATH)
        logging.info("  create   : True  (will create 'servers' on FMC if missing)")
        logging.info("  initial_sync: True  (syncs servers.txt immediately on start)")
        logging.info("  Edit test_watchdog/servers.txt to trigger a live sync.")
        logging.info("  Press Ctrl+C to stop.")

        dyn = fmcapi.DynamicObject(fmc=fmc)
        dyn.watch_and_sync(
            path=WATCH_PATH,
            create=True,
            initial_sync=True,
        )


if __name__ == "__main__":
    main()
