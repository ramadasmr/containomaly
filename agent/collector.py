"""
Collect docker `ps -a --format json` output and return structured list.
This module attempts to be defensive: if docker is missing or output is empty it returns an empty list.
"""
import subprocess
import json
from typing import List, Dict
from .logger import get_logger

logger = get_logger(__name__)

def collect_docker_snapshots() -> List[Dict]:
    """Run `docker ps -a --format '{{json .}}'` and parse each line as JSON."""
    cmd = [
        "docker",
        "ps",
        "-a",
        "--format",
        "{{json .}}",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError:
        logger.error("docker command not found on PATH")
        return []

    if result.returncode != 0:
        logger.error(
            "docker command failed: returncode=%s stderr=%s",
            result.returncode,
            result.stderr.strip(),
        )
        return []

    stdout = result.stdout.strip()
    if not stdout:
        logger.info("docker ps returned no containers")
        return []

    containers = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            containers.append(json.loads(line))
        except json.JSONDecodeError:
            logger.warning("Skipping non-json line from docker ps: %s", line)

    return containers
