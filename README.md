<div align="center">

# Python Problem-Solving Portfolio

### 100 programming exercises · structured practice · solutions in progress

**Pranajit Das** · Python · Git · GitHub

</div>

---

## About this project

This repository is my structured journey through 100 programming exercises,
starting with input, output, and basic arithmetic and progressing to strings,
lists, number problems, and small menu-driven programs.

I use each prompt to practise breaking a problem into steps, implementing a
solution in Python, and refining it as I learn. Progress below is refreshed
automatically from the numbered solution files; the code-presence count does
not assess correctness.

## Progress

| Milestone | Status |
|---|---:|
| Questions organized and linked to solution files | 100 / 100 |
<!-- AUTO_PROGRESS_START -->
| Milestone | Status |
|---|---:|
| Questions organized and linked to solution files | 100 / 100 |
| Solutions containing executable code | 5 / 100 |
| Next exercise | [Question 6 — Swap Using a Third Variable](solutions/q006_swap_using_third_variable.py) |
<!-- AUTO_PROGRESS_END -->

## Browse the work

- **[All 100 questions](questions/README.md)** — prompts grouped in their
  original sequence, each linked to its solution file.
- **[Solution index](solutions/README.md)** — a direct route to every Python
  exercise.
- **[Completed example: Hello, World!](solutions/q001_hello_world.py)** —
  the first exercise in the collection.

## How I work through an exercise

1. Read the prompt and identify the inputs, expected output, and edge cases.
2. Implement the solution in its numbered Python file.
3. Run it with representative inputs and check the result.
4. Save the work and continue to the next exercise.

The exercise set builds practice across:

- Variables, input/output, arithmetic, and conditionals
- Loops, numeric properties, and digit manipulation
- Series and pattern generation
- String processing
- Lists, searching, sorting, and functions

These are the topics covered by the roadmap; my completed solutions and
progress are reflected in the repository rather than implied by the topic list.

## Repository layout

```text
.
├── questions/
│   └── README.md          # Numbered prompts and links
├── solutions/
│   ├── README.md          # Solution index
│   ├── q001_hello_world.py
│   └── qNNN_*.py          # One editable file per exercise
├── .vscode/tasks.json     # Optional save-and-publish task
└── push_solution.py       # Small Git publishing helper
```

## Version control

I use Git and GitHub to keep the project history and publish completed
solutions. An optional VS Code task checks the whole project once a minute and
publishes Git-visible changes after they have settled. This is a convenience
for routine commits and pushes, not part of the exercise solutions. The same
helper can be run manually with `python3 push_solution.py`.

The watcher uses the Git command-line credentials configured on this machine.
Git-ignored files are excluded; do not add secrets to the repository.

## Maintainer

**Pranajit Das**
Project owner and author of the solutions as they are completed.
