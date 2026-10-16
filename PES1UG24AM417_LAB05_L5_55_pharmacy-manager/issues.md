# Lab 5: Static Code Analysis

## Issue Documentation

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe eval() | Security | 48 | Arbitrary expression execution | Replaced eval() with safe AST-based arithmetic evaluation |
| Hardcoded password | Security | 11 | Password stored directly in source code | Used an environment variable |
| Weak MD5 hash | Security | 51 | Weak hashing algorithm | Replaced MD5 with SHA-256 |
| Unsafe pickle | Security | 64 | Deserialization can execute malicious code | Replaced pickle with JSON |
| Shell command execution | Security | 68 | os.system() can allow command injection | Replaced it with print() |
| Mutable default argument | Code quality | 13 | Shared list between function calls | Used None and initialized a new list |
| Bare exception | Code quality | 27 | Catches exceptions without specifying a type | Added explicit validation and appropriate errors |
| Unused imports | Code quality | 2, 6 | Imports were not used | Removed unused imports |
| Long lines | Formatting | 87 | Lines exceeded style limits | Reformatted long lines |
| Missing final newline | Formatting | 297 | File did not end with a newline | Added a final newline |

## Verification

- Pylint final score: 9.80/10
- Bandit: No issues identified
- Flake8: No issues reported