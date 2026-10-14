# 100-Python-coding-questions-solved-from-basic-to-advanced-by-PRANAJIT
100 Python coding questions solved from basic to advanced by PRANAJIT

## Questions and solutions

The complete question list is in [`questions/README.md`](questions/README.md).
Each question links to its Python file in [`solutions/`](solutions/README.md).
Write your answer in that file and save it.

## Automatic publishing in VS Code

Open this repository as a folder in VS Code and allow the
**Watch and publish solution saves** task to run. It watches `solutions/`;
after a file has been unchanged for three seconds, it commits the solution
change and pushes `main` to `origin`. The task retries the push if GitHub is
temporarily unavailable.

If VS Code does not start the task automatically (for example, the folder was
already open when setup was completed), start it with **Terminal → Run Task →
Watch and publish solution saves**.

The watcher only stages files under `solutions/`; it does not stage question
materials or other project files. You can also publish manually from the
repository root with:

```sh
python3 push_solution.py
```

Git command-line authentication must be configured for the account that can
push to `origin`. VS Code sign-in alone may not configure Git authentication.
Do not put passwords or access tokens in this repository.
