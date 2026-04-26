# Assignment 1 – Lab 1

## Work Distribution
Person 1: Task 1, Task 3  
Person 2: Task 2  

---

## Task 2: Boundary Value Analysis and Equivalence Partitioning

### 1. Explanation of BVA and EP

**Equivalence Partitioning (EP)** is a test design technique where the input domain is divided into groups (partitions) that are expected to behave similarly. Instead of testing every possible value, one representative value from each partition is selected.

**Boundary Value Analysis (BVA)** focuses on testing values at the boundaries of input ranges. Errors often occur at these boundaries, making them especially important to test.

---

### 2. Comparison of their usability

Equivalence Partitioning helps reduce the number of test cases by grouping inputs that should produce the same behavior. This makes testing more efficient.

Boundary Value Analysis complements EP by focusing on edge cases. Since many defects occur at boundaries, BVA increases the likelihood of finding errors that EP alone might miss.

Together, they provide a structured and effective approach to test design.

---

### 3. Application to the age validation scenario

#### Equivalence Partitions

- EP1: age < 0 → invalid (impossible)
- EP2: 0 ≤ age < 18 → underage
- EP3: 18 ≤ age ≤ 120 → valid
- EP4: age > 120 → invalid (impossible)

---

#### Boundary Values

The critical boundaries are: 0, 18, and 120.

Test values:

- Around 0: -1, 0, 1  
- Around 18: 17, 18, 19  
- Around 120: 119, 120, 121  

These values ensure that behavior at and around the boundaries is correctly handled.