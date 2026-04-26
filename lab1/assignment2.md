# Assignment 2 – Unit Testing

## Work Distribution

Person 1: Task 2  
Person 2: Task 1  

---

## Task 1: Mocking

### 1. Explanation of mocking

Mocking is a testing technique where real dependencies are replaced with controlled fake objects. These fake objects are called mocks.

A mock can simulate the behavior of a real dependency, such as a database, an API, a file system, or another class. Instead of using the real dependency during the test, the test uses the mock to control what should be returned or how the dependency should behave.

For example, if a function normally reads data from a database, the database can be replaced with a mock that returns predefined data.

### 2. Purpose of mocking in unit testing

The purpose of mocking in unit testing is to isolate the unit that is being tested. A unit test should focus on one small part of the system, such as one function or one method.

Mocking helps make unit tests:

- faster, because they do not need real external systems
- more predictable, because the test controls the mock behavior
- more isolated, because only the unit under test is tested
- easier to use for error cases, because the mock can simulate failures

Mocking is especially useful when the real dependency is slow, unreliable, difficult to set up, or outside the scope of the unit test.

In unit testing, mocking makes it possible to test the logic of one unit without depending on other parts of the system.