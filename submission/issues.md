# Lab 5 — Static Analysis Findings

Line numbers refer to the original `society_dues.py` from the assigned repository. Findings are ordered by severity where applicable. Baseline and final tool output are saved under [`reports/before/`](reports/before/) and [`reports/after/`](reports/after/).

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| SQL constructed with interpolated values | Security — Medium (Bandit B608) | 8–9 | Flat and month values were interpolated into an SQL statement, allowing crafted input to alter the query. | Replaced interpolation with SQLite placeholders and a parameter tuple. Added a primary key for one flat/month bill and an upsert to avoid duplicate records. |
| `eval` on a rule string | Security — Medium (Bandit B307; Pylint W0123) | 19–24 | `eval` executes arbitrary Python code from the supplied string. | Removed expression evaluation. `calculate_penalty(days_late, daily_fee)` now uses numeric arguments and rejects negative values. |
| Hard-coded password-like constant | Security — Low (Bandit B105) | 5 | `TREASURER_PASSWORD` was embedded in source and unused. | Removed the unused secret. |
| Mutable default history list | Bug / quality (Pylint W0102) | 8–11 | `history=[]` caused calls that omitted history to share the same list. | Changed the default to `None` and create a new list for each call. |
| Inconsistent return for missing dues | Bug / quality (Pylint R1710) | 12–17 | `collect` returned the amount for a matching due but implicitly returned `None` otherwise. | It now explicitly returns `None` when the flat/month pair is absent and returns the amount after marking a match paid. |
| Broad exception handling | Quality / robustness (Pylint W0718) | 19–24 | Catching every `Exception` hid programming errors and turned all failures into a zero fee. | Removed the broad `try/except`; fee inputs are validated and invalid negative values raise `ValueError`. |
| Incorrect comparison to `None` | Quality (Pylint C0121; Flake8 E711) | 29 | The code checked `rows != None`; `fetchall()` already returns a list, so the condition was unnecessary and used non-idiomatic `None` comparison. | Removed the redundant condition and directly return the flat identifiers from the result rows. |
| Naming and missing documentation | Maintainability (Pylint C0103, C0114, C0116) | 1, 8–42 | The module and functions lacked docstrings and used camelCase names. | Added module/function docstrings and renamed functions to `snake_case`. Added a main guard so importing the module does not run the demonstration. |
| Long lines and missing blank line | Style (Pylint C0301; Flake8 E501, E302) | 4, 12–15 | SQL statements exceeded the configured line width and a top-level function lacked the required separation. | Split SQL across adjacent string literals and formatted top-level definitions consistently. |
| Inline comment spacing | Style (Flake8 E261) | 38 | The inline comment did not have two spaces before `#`. | Added the required spacing. |

## Verification summary

- **Pylint:** 10.00/10.
- **Bandit:** 0 findings (High, Medium, Low all 0).
- **Flake8:** no violations (exit status 0).
- Focused runtime checks passed for parameterized SQL handling of injection-like text, independent history defaults, missing dues, payment/pending transitions, upserts, and penalty validation.
