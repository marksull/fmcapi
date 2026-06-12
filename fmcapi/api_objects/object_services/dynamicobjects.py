from fmcapi.api_objects.apiclasstemplate import APIClassTemplate
import fnmatch
import glob as glob_module
import ipaddress
import logging
import os
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    _WATCHDOG_AVAILABLE = True
except ImportError:
    _WATCHDOG_AVAILABLE = False


class DynamicObject(APIClassTemplate):
    """The Dynamic Object in the FMC."""

    VALID_JSON_DATA = ["id", "name", "description", "type", "objectType"]
    VALID_FOR_KWARGS = VALID_JSON_DATA + []
    URL_SUFFIX = "/object/dynamicobjects"
    VALID_CHARACTERS_FOR_NAME = """[.\w\d_\- ]"""

    VALID_GET_FILTERS = [
        "unusedOnly",
        "ids" "nameStartsWith",
    ]  # unusedOnly:Bool, "ids:id1,id2,..." ,nameStartsWith:String

    def __init__(self, fmc, **kwargs):
        """
        Initialize Dynamic Object.

        Set self.type to "DynamicObject" and parse the kwargs.

        :param fmc: (object) FMC object
        :param kwargs: Any other values passed during instantiation.
        :return: None
        """
        super().__init__(fmc, **kwargs)
        logging.debug("In __init__() for Dynamic Object class.")
        self.parse_kwargs(**kwargs)
        self.type = "DynamicObject"

    def _parse_ip_file(self, filepath):
        """
        Read a file and return a list of valid IPv4/IPv6 host addresses.

        Lines that are empty, whitespace-only, or not parseable as an IP address
        are silently ignored.

        :param filepath: (str) Path to the file to parse.
        :return: (list) Valid IP address strings.
        """
        ips = []
        try:
            with open(filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        addr = ipaddress.ip_address(line)
                        ips.append(str(addr))
                    except ValueError:
                        logging.debug(f"Skipping invalid IP address line: {line!r}")
        except OSError as exc:
            logging.warning(f"Cannot read file {filepath}: {exc}")
        return ips

    def _sync_file(self, filepath, create=False):
        """
        Sync the contents of a single file to the FMC as a Dynamic Object.

        The Dynamic Object name is derived from the file's stem (filename without
        extension). The file is expected to contain one IP address per line.

        :param filepath: (str) Absolute or relative path to the IP list file.
        :param create: (bool) Create the Dynamic Object on the FMC if it does not exist.
        :return: None
        """
        # Lazy import to avoid circular dependency (dynamicobjectmappings imports DynamicObject)
        from .dynamicobjectmappings import DynamicObjectMappings

        name = Path(filepath).stem
        new_ips = set(self._parse_ip_file(filepath))

        if not new_ips:
            logging.info(f"No valid IPs found in '{filepath}'. Skipping '{name}'.")
            return

        # Resolve the Dynamic Object on the FMC
        dyn_obj = DynamicObject(fmc=self.fmc, name=name)
        response = dyn_obj.get()

        if not response or 'id' not in response:
            if not create:
                logging.warning(
                    f"Dynamic Object '{name}' not found on FMC and create=False. Skipping."
                )
                return
            dyn_obj.objectType = "IP"
            dyn_obj.post()
            response = dyn_obj.get()
            if not response or 'id' not in response:
                logging.error(f"Failed to create Dynamic Object '{name}'. Skipping.")
                return
            logging.info(f"Created Dynamic Object '{name}'.")

        obj_id = response["id"]

        # Retrieve current IP mappings
        dom = DynamicObjectMappings(fmc=self.fmc, id=obj_id)
        current_response = dom.get()
        current_ips = set()
        if current_response and "items" in current_response:
            current_ips = {item["mapping"] for item in current_response["items"] if "mapping" in item}

        to_add = list(new_ips - current_ips)
        to_remove = list(current_ips - new_ips)

        if not to_add and not to_remove:
            logging.info(f"Dynamic Object '{name}' is already up to date.")
            return

        print(f"TO ADD : {to_add}")
        print(f"TO REMOVE : {to_remove}")
        mapping = DynamicObjectMappings(fmc=self.fmc)
        if to_add:
            mapping.handle_mappings(action="add", value=to_add, name=name)
        if to_remove:
            mapping.handle_mappings(action="remove", value=to_remove, name=name)
        mapping.post()
        logging.info(
            f"Synced Dynamic Object '{name}': +{len(to_add)} added, -{len(to_remove)} removed."
        )

    def watch_and_sync(self, path=".", create=False, initial_sync=False):
        """
        Long-running blocking method that watches a directory for file changes
        and syncs them as Dynamic Objects on the FMC.

        Each file maps to one Dynamic Object: the object name is the file stem
        (filename without extension). Each line in the file must be a valid IPv4
        or IPv6 host address; all other lines are ignored.

        This method blocks indefinitely until interrupted (KeyboardInterrupt).
        The watchdog is NOT limited to a single read cycle — it stays alive and
        re-syncs the corresponding Dynamic Object every time a watched file is
        created or modified.

        Requires the ``watchdog`` package (``pip install watchdog``).

        :param path: (str) Directory path or glob pattern (e.g. ``'/path/*.txt'``).
                     Defaults to the current working directory.
        :param create: (bool) Create the Dynamic Object on the FMC when it is not
                       already present. Defaults to False.
        :param initial_sync: (bool) Force-sync all matching files immediately on
                             startup before entering the watch loop.
                             Defaults to False.
        :return: None
        """
        if not _WATCHDOG_AVAILABLE:
            raise ImportError(
                "The 'watchdog' package is required for watch_and_sync(). "
                "Install it with: pip install watchdog"
            )

        glob_pattern = None
        if any(c in path for c in ("*", "?", "[")):
            watch_dir = str(Path(path).resolve().parent)
            glob_pattern = Path(path).name
        else:
            watch_dir = str(Path(path).resolve())

        # Optionally sync all existing matching files before entering the watch loop
        if initial_sync:
            files = (
                glob_module.glob(path)
                if glob_pattern
                else glob_module.glob(os.path.join(path, "*"))
            )
            for filepath in files:
                if os.path.isfile(filepath):
                    logging.info(f"Initial sync: {filepath}")
                    self._sync_file(filepath, create=create)

        sync_file = self._sync_file

        class _DynamicObjectFileHandler(FileSystemEventHandler):
            """Watchdog handler that syncs changed files to FMC Dynamic Objects."""

            def __init__(self, pattern, create_flag):
                """
                Initialize the handler.

                :param pattern: (str or None) Glob pattern to restrict which files trigger a sync.
                :param create_flag: (bool) Passed through to _sync_file.
                """
                super().__init__()
                self._pattern = pattern
                self._create_flag = create_flag

            def _handle(self, event):
                """
                Process a filesystem event.

                :param event: watchdog FileSystemEvent
                """
                if event.is_directory:
                    return
                filepath = event.src_path
                filename = Path(filepath).name
                # Ignore editor temporary/backup files (e.g. file~, .file.swp)
                if filename.endswith("~") or filename.startswith("."):
                    return
                # event.src_path is always absolute; match only the filename
                # against the glob pattern (e.g. "*.txt" or "*")
                if self._pattern and not fnmatch.fnmatch(filename, self._pattern):
                    return
                logging.info(f"File event detected: {filepath}")
                sync_file(filepath, create=self._create_flag)

            def on_modified(self, event):
                """Handle file modification events."""
                self._handle(event)

            def on_created(self, event):
                """Handle file creation events."""
                self._handle(event)

        handler = _DynamicObjectFileHandler(pattern=glob_pattern, create_flag=create)
        observer = Observer()
        observer.schedule(handler, watch_dir, recursive=False)
        observer.start()
        logging.info(
            f"Watching '{watch_dir}' for Dynamic Object file changes. Press Ctrl+C to stop."
        )
        try:
            while observer.is_alive():
                observer.join(timeout=1)
        except KeyboardInterrupt:
            logging.info("Stopping Dynamic Object file watcher.")
            observer.stop()
        observer.join()
