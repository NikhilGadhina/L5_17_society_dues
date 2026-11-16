# Lab 5 — Reflection

> The repository README asks for four reflection answers, but the provided handout does not include a separate list of questions. These responses address four prompts based on the handout's learning outcomes; adjust them if the instructor provides a different question list.

## 1. What is static analysis, and how did it help with this program?

Static analysis examines source code without executing it. Pylint, Bandit, and Flake8 each highlighted a different kind of risk: code quality and correctness, security, and formatting. Together they revealed dangerous patterns in the dues ledger that were not obvious from its short successful demo.

## 2. Which important issues did you find and how did you fix them?

Bandit identified SQL built by interpolating input values and the use of `eval` to calculate a late fee. I replaced the SQL construction with parameterized queries and replaced `eval` with a direct numeric calculation that validates non-negative inputs. I also removed an unused hard-coded password. Pylint identified a shared mutable history default, broad exception handling, inconsistent returns, unclear naming, and missing documentation. I used a `None` default with a new list per call, removed the broad catch, made missing dues return `None` explicitly, and added documentation and a main guard. Flake8's line length, spacing, and `None`-comparison issues were fixed.

## 3. Which tool was most useful, and why?

Bandit was especially useful because it drew attention to the highest-risk patterns: SQL injection and arbitrary code execution via `eval`. Pylint helped improve the design and make edge cases clearer, while Flake8 quickly identified style issues. I needed all three to get a broader picture than any single tool could provide.

## 4. What are static analysis limitations, and how would you use it in future?

Static analysis cannot prove that a program is correct, and it may not understand how code is used at runtime. It does not replace tests or human review. I would run these tools during development and in CI, prioritize findings by severity, and add tests for core behavior. In this lab, focused runtime assertions complemented the tool reports by checking payment status, pending balances, parameterized handling of injection-like input, and the late-fee rules.
