import argparse
import ast
from pathlib import Path
import re
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent
WATCH_POLL_SECONDS = 60
SAVE_QUIET_SECONDS = 5
PUSH_RETRY_SECONDS = 60


def has_implementation(statement: ast.stmt) -> bool:
    if isinstance(statement, ast.Pass):
        return False
    if (
        isinstance(statement, ast.Expr)
        and isinstance(statement.value, ast.Constant)
        and isinstance(statement.value.value, str)
    ):
        return False

    suites = [
        child
        for attribute in ("body", "orelse", "finalbody")
        for child in getattr(statement, attribute, [])
        if isinstance(child, ast.stmt)
    ]
    if isinstance(statement, (ast.Try, ast.TryStar)):
        suites.extend(
            child
            for handler in statement.handlers
            for child in handler.body
            if isinstance(child, ast.stmt)
        )
    if suites:
        return any(has_implementation(child) for child in suites)
    return True


def completed_solutions() -> tuple[list[tuple[int, Path, str]], list[str]]:
    completed = []
    invalid_files = []
    solution_files = sorted(
        ROOT.glob("solutions/q[0-9][0-9][0-9]_*.py"),
        key=lambda path: int(path.stem[1:4]),
    )
    for path in solution_files:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            invalid_files.append(path.name)
            continue

        docstring = ast.get_docstring(tree) or ""
        title_match = (
            re.match(r"Question \d+:\s*(.+)", docstring.splitlines()[0])
            if docstring
            else None
        )
        title = title_match.group(1) if title_match else path.stem
        if any(has_implementation(statement) for statement in tree.body):
            number = int(path.stem[1:4])
            completed.append((number, path, title))
    return completed, invalid_files


def update_progress_readme() -> None:
    completed, invalid_files = completed_solutions()
    solution_files = sorted(
        ROOT.glob("solutions/q[0-9][0-9][0-9]_*.py"),
        key=lambda path: int(path.stem[1:4]),
    )
    completed_numbers = {number for number, _, _ in completed}
    next_solution = next(
        (
            path
            for path in solution_files
            if int(path.stem[1:4]) not in completed_numbers
        ),
        None,
    )

    progress_rows = [
        "| Milestone | Status |",
        "|---|---:|",
        f"| Questions organized and linked to solution files | {len(solution_files)} / 100 |",
        f"| Solutions containing executable code | {len(completed)} / {len(solution_files)} |",
    ]
    if next_solution is None:
        progress_rows.append("| Next exercise | All listed exercises have code |")
    else:
        next_number = int(next_solution.stem[1:4])
        next_tree = ast.parse(next_solution.read_text(encoding="utf-8"))
        next_docstring = ast.get_docstring(next_tree) or ""
        next_title_match = (
            re.match(r"Question \d+:\s*(.+)", next_docstring.splitlines()[0])
            if next_docstring
            else None
        )
        next_title = (
            next_title_match.group(1) if next_title_match else next_solution.stem
        )
        progress_rows.append(
            f"| Next exercise | [Question {next_number} — {next_title}]"
            f"(solutions/{next_solution.name}) |"
        )

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    section = "\n".join(
        [
            "<!-- AUTO_PROGRESS_START -->",
            *progress_rows,
            "<!-- AUTO_PROGRESS_END -->",
        ]
    )
    updated_readme, replacements = re.subn(
        r"<!-- AUTO_PROGRESS_START -->.*?<!-- AUTO_PROGRESS_END -->",
        lambda _: section,
        readme,
        count=1,
        flags=re.DOTALL,
    )
    if replacements != 1:
        raise RuntimeError("README.md is missing the automatic progress markers.")
    if updated_readme != readme:
        readme_path.write_text(updated_readme, encoding="utf-8")
        print(
            f"Updated README progress: {len(completed)} of "
            f"{len(solution_files)} solution files contain executable code."
        )
    if invalid_files:
        print(
            "Not counted due to Python syntax errors: "
            + ", ".join(invalid_files),
            file=sys.stderr,
        )


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

        update_progress_readme()
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
