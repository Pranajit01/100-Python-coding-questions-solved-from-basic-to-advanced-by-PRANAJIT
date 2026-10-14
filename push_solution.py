from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


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


def main() -> int:
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

        run_git("add", "-A", "--", "solutions")
        changed_files = run_git(
            "diff", "--cached", "--name-only", capture_output=True
        ).splitlines()
        if not changed_files:
            print("No solution changes to commit.")
            return 0

        if len(changed_files) == 1:
            message = f"Completed solution: {Path(changed_files[0]).name}"
        else:
            message = f"Updated solutions ({len(changed_files)} files)"

        run_git("commit", "-m", message)
        try:
            run_git("push", "origin", "main")
        except RuntimeError as error:
            print(
                f"{error}\nThe commit is saved locally; push it with "
                "'git push origin main' after resolving the issue.",
                file=sys.stderr,
            )
            return 1
    except RuntimeError as error:
        print(error, file=sys.stderr)
        return 1

    print(f"Committed and pushed: {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
