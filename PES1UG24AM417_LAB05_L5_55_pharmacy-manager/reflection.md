# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis?

Static code analysis examines source code without executing the program.
It helps identify programming mistakes, security vulnerabilities, and
formatting problems.

## 2. What did Pylint, Bandit, and Flake8 identify?

Pylint identified code quality problems such as mutable default
arguments, missing docstrings, naming convention violations, and
unnecessary imports.

Bandit identified security risks such as eval(), weak hashing,
hardcoded passwords, unsafe pickle deserialization, and shell command
execution.

Flake8 identified formatting problems, unused imports, missing blank
lines, and lines that exceeded the recommended length.

## 3. How did you fix the identified problems?

I replaced eval() with safe AST-based arithmetic evaluation, replaced
pickle with JSON, used SHA-256 instead of MD5, moved the password to
an environment variable, and removed shell command execution.

I also corrected naming conventions, removed unused imports, improved
exception handling, fixed formatting problems, and added documentation.

## 4. How does static analysis improve software quality?

Static analysis helps detect problems early, improves code readability,
reduces security risks, and makes programs easier to maintain. Using
multiple tools provides different perspectives on code quality and
security.