# Assignment 3 – Integration Testing

## Work Distribution

Person 1: Task 1  
Person 2: Task 2  

---

## Task 2: Integration Testing

### 1. Test cases

The following test cases were derived using the test design technique:

1. Valid user data  
→ Expected: Object is successfully created  

2. Missing required field  
→ Expected: WriteError is raised  

3. Wrong data type  
→ Expected: WriteError is raised  

4. Invalid data structure (e.g., wrong type for tasks)  
→ Expected: WriteError is raised  

---

### 2. Pytest fixture

A pytest fixture was implemented to allow safe interaction with the database without affecting production data.  
The fixture creates a fresh DAO instance and clears the collection before and after each test:

```python
import pytest
from src.util.dao import DAO

@pytest.fixture
def user_dao():
    dao = DAO("user")
    dao.drop()

    dao = DAO("user")
    yield dao

    dao.drop()
``` 
This ensures that each test runs in isolation and does not interfere with other tests or existing data.

### 3. Implementation

The test cases were implemented using pytest in the following file:

backend/tests/test_dao.py

The tests verify that valid input data results in successful object creation, while invalid input data leads to errors as enforced by the MongoDB validator.

### 4. Test execution result and evaluation

The integration tests were executed with:

pytest tests/test_dao.py

The result was:

4 passed in 0.58s

The tests confirm that the DAO correctly communicates with the MongoDB database.
Valid data is accepted and stored, while invalid data is rejected according to the validator rules.

The coverage report shows that approximately 52% of the DAO code is covered.
This is expected since only the create() method was tested, while other methods such as find, update, and delete are outside the scope of this assignment.

Overall, the integration tests demonstrate that the interaction between the DAO and the MongoDB database works as intended.