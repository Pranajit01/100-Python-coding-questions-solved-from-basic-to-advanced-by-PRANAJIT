# 100-Python-coding-questions-solved-from-basic-to-advanced-by-PRANAJIT
100 Python coding questions solved from basic to advanced by PRANAJIT

## Solutions

Store each Python answer as a descriptively named file under `solutions/`,
for example `solutions/q001_even_or_odd.py`. Question materials can remain
under `questions/`.

## Add and publish a solution

1. Add or update a solution file under `solutions/`.
2. From the repository root, run:

   ```sh
   python3 push_solution.py
   ```

The script stages changes under `solutions/`, creates a descriptive commit,
and pushes the `main` branch to `origin`. It does not stage changes elsewhere
in the repository. Make sure `origin` points to your GitHub repository and
that Git authentication is already configured; credentials should not be
stored in this project.

If there are no solution changes, the script exits without creating a commit.
