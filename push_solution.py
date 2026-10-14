import argparse
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent
WATCH_POLL_SECONDS = 60
SAVE_QUIET_SECONDS = 5
PUSH_RETRY_SECONDS = 60


def run_git(*args: str, capture_output: bool = False) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(
            f"git {' '.join(args)} failed with exit code "
            f"{result.returncode}: {detail}"
        )
    return result.stdout.strip() if capture_output else ""


def publish_project_changes() -> int:
    try:
        git_root = Path(run_git("rev-parse", "--show-toplevel", capture_output=True))
        if git_root.resolve() != ROOT:
            print(
                f"Refusing to continue: expected repository root {ROOT}, "
                f"but Git reports {git_root.resolve()}.",
                file=sys.stderr,
            )
            return 1

        branch = run_git("branch", "--show-current", capture_output=True)
        if branch != "main":
            print(
                f"Refusing to continue: expected branch 'main', found {branch!r}.",
                file=sys.stderr,
            )
            return 1

        remotes = run_git("remote", capture_output=True).splitlines()
        if "origin" not in remotes:
            print(
                "Refusing to continue: configure the GitHub repository as "
                "'origin' first.",
                file=sys.stderr,
            )
            return 1

        staged = run_git("diff", "--cached", "--name-only", capture_output=True)
        if staged:
            print(
                "Refusing to continue: the Git index already contains staged "
                "changes. Commit or unstage them before running this script.",
                file=sys.stderr,
            )
            return 1

        run_git("add", "-A")
        changed_files = run_git(
            "diff", "--cached", "--name-only", capture_output=True
        ).splitlines()
        message = ""
        if changed_files:
            message = f"Auto-publish project updates ({len(changed_files)} files)"
            run_git("commit", "-m", message)
        else:
            print("No project changes to commit.")

        try:
            run_git("push", "origin", "main")
        except RuntimeError as error:
            print(
                f"{error}\nAny commit is saved locally; push it with "
                "'git push origin main' after resolving the issue.",
                file=sys.stderr,
            )
            return 1
    except RuntimeError as error:
        print(error, file=sys.stderr)
        return 1

    if message:
        print(f"Committed and pushed: {message}")
    else:
        print("Pushed any pending commits.")
    return 0


def watch_solutions() -> int:
    print(
        "Watching the project for changes every 60 seconds. "
        "Stable changes are committed and pushed automatically.",
        flush=True,
    )
    last_status = ""
    stable_since = time.monotonic()
    handled_status = ""
    next_retry = 0.0

    try:
        while True:
            try:
                status = run_git(
                    "status",
                    "--porcelain=v1",
                    "--untracked-files=all",
                    capture_output=True,
                )
            except RuntimeError as error:
                print(error, file=sys.stderr, flush=True)
                time.sleep(WATCH_POLL_SECONDS)
                continue

            now = time.monotonic()
            if status != last_status:
                last_status = status
                stable_since = now
                handled_status = ""

            if status and status != handled_status:
                if now - stable_since >= SAVE_QUIET_SECONDS:
                    print("Project changes are stable; publishing.", flush=True)
                    publish_project_changes()
                    handled_status = status
                    next_retry = time.monotonic() + PUSH_RETRY_SECONDS

            if now >= next_retry:
                if not status or status == handled_status:
                    publish_project_changes()
                    next_retry = time.monotonic() + PUSH_RETRY_SECONDS

            time.sleep(WATCH_POLL_SECONDS)
    except KeyboardInterrupt:
        print("\nStopped watching solutions/.", flush=True)
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Commit and push project files, or watch for saved changes."
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="watch the whole project and publish stable changes automatically",
    )
    args = parser.parse_args()
    if args.watch:
        return watch_solutions()
    return publish_project_changes()


if __name__ == "__main__":
    raise SystemExit(main())
