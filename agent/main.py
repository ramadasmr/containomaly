"""
CLI entrypoint for the agent.
Can run once (--once) or loop continuously with an interval (--interval).
"""
import argparse
import time
from datetime import datetime
from .collector import collect_docker_snapshots
from .sender import Sender
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

def run_once(dry_run: bool = False):
    containers = collect_docker_snapshots()
    payload = Sender().build_payload(containers)
    payload["timestamp"] = datetime.utcnow().isoformat() + "Z"

    if dry_run:
        logger.info("Dry run payload: %s", payload)
        return payload

    resp = Sender().send(payload)
    return resp.json()

def run_loop(interval: int):
    logger.info("Starting agent loop with interval=%s seconds", interval)
    try:
        while True:
            try:
                run_once(dry_run=False)
            except Exception as exc:
                logger.exception("Error during collection/send: %s", exc)
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Agent interrupted by user, shutting down")

def parse_args():
    parser = argparse.ArgumentParser("agent")
    parser.add_argument("--once", action="store_true", help="Run collection and send once")
    parser.add_argument("--dry-run", action="store_true", help="Build payload but do not send")
    parser.add_argument("--interval", type=int, default=settings.collect_interval_seconds, help="Polling interval seconds")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.once:
        run_once(dry_run=args.dry_run)
        return
    run_loop(args.interval)

if __name__ == "__main__":
    main()