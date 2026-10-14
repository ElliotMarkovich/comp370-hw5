# Conceptual Answers: Homework 6

## 1. Refactoring and Refactoring Techniques
* **What is refactoring?** Refactoring is the process of restructuring existing code without altering its external behavior, with the goal of improving code readability, maintainability, and reducing technical debt.
* **Three examples of refactoring techniques:**
    * **Extract Function:** Taking a distinct block of code and turning it into a separate, well-named function to eliminate duplication and clarify execution flow.
    * **Extract Variable:** Assigning the result of a complex expression to a descriptive variable to make the intent of the computation immediately obvious.
    * **Guard Clauses (Replacing Nested Conditionals):** Using early returns to handle edge cases or invalid states upfront, reducing deep indentation and nesting in conditional logic.

---

## 2. Phases of Messiness in Data Science Projects
* **Why does code naturally go through "phases" of messiness?** Data science projects begin as exploratory research where data structures, anomalies, and analytical paths are initially unknown.
* **Exploratory Prototyping:** Early experimentation prioritizes speed of discovery over clean software design, resulting in ad-hoc, linear scripts.
* **Shifting Requirements and Pivots:** As intermediate results or stakeholder feedback emerge, analytical goals change, leading to rapid, incremental patches on existing code rather than clean redesigns.
* **The Refactoring Need:** Clean code in data science is rarely achieved on the first pass; it requires a deliberate post-exploration refactoring phase to transition raw notebooks or scripts into structured pipelines.

---

## 3. Techniques for Creating More Modular Code
* **Three techniques for creating more modular code:**
    * **Single Responsibility Principle (SRP):** Designing functions and modules so that each has only one clear responsibility or reason to change (e.g., separating data parsing, statistical aggregation, and plotting).
    * **Encapsulation & Explicit Parameters:** Avoiding reliance on mutable global variables by passing all necessary inputs explicitly into functions and returning defined outputs.
    * **Separation of Concerns via Modular File Structure:** Decomposing large, monolithic scripts into logical, reusable modules and helper scripts.
