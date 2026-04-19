# Software Testing

## Why Do We Test?

Imagine you built a calculator app. You show it to your teacher and she types `5 + 3`. The app shows `9`. That's a bug!

Now imagine this calculator controls the autopilot of an airplane.

**Testing** is how we catch these bugs before our users do. It's also how we make sure that when we fix one bug, we don't accidentally create another.

---

## The Testing Pyramid: From Fast to Slow

Think of testing like checking your homework:

```

                            ACCEPTANCE TESTING ← Teacher checks
                           (Slow, Expensive, Few) your final work
                        /\
                       / \
                      / \
                     / INTEGRATION TESTING \
                    / (Medium speed, some) \
                   / \
                  / \
                 / \
                / UNIT TESTING \
               / (Fast, Cheap, Many — run always) \
              / \
```

### Level 1: Unit Testing (The Foundation)

Test one small, isolated piece of code — usually one function.

```
Testing: "Does the is_passing() function work correctly?"

NOT testing: Does the database connection work?
NOT testing: Does the login form look right?
NOT testing: Does the whole app flow correctly?

Just this ONE function.
```

```python
# The function we want to test (in app.py)
def is_passing(marks):
    """Returns True if marks >= 40, otherwise False."""
    return marks >= 40
```

```python
# The test file (in test_app.py)
import pytest
from app import is_passing

# Each test function starts with "test_"
def test_passing_marks():
    """Test that a student with 85 marks is considered passing."""
    assert is_passing(85) == True # assert = "I am claiming this is true"

def test_failing_marks():
    """Test that a student with 35 marks is considered failing."""
    assert is_passing(35) == False

def test_exact_boundary():
    """Test the exact boundary: 40 marks = passing."""
    assert is_passing(40) == True

def test_zero_marks():
    """Edge case: 0 marks should fail."""
    assert is_passing(0) == False
```

Run with: `pytest test_app.py`

### Level 2: Integration Testing

Test that **multiple components** work correctly when connected together.

```
Testing: "Does the /login route work end-to-end?"
        → Does it read from the request?
        → Does it query the database correctly?
        → Does it redirect on success?
        → Does it return an error on failure?
```

### Level 3: Acceptance Testing

The entire app is tested by a real user or client to verify it meets requirements. The slowest and most expensive.

---

## Testing Methodologies

### Black-Box Testing

You test the function **without looking at the code**. You only know: "What goes in? What should come out?"

```
  Black Box Test:

    Input: marks = 85

  85 > ??? > Expected Output: True
          (code
           hidden)


  You don't care HOW it calculates. Just that it returns True.
```

### White-Box Testing

You test the function **with full access to the code**. You verify every possible code path is covered.

```python
def classify_student(marks):
    if marks >= 80: # ← Path A
        return "Distinction"
    elif marks >= 40: # ← Path B
        return "Pass"
    else: # ← Path C
        return "Fail"
```

For 100% coverage, you MUST test all 3 paths (A, B, and C).

### Regression Testing

After you fix a bug or add a new feature, you run ALL your tests again to make sure nothing broke.

```
  Old Code (works) → Add new feature → Bug appears in OLD feature!
                                                            ↑
                                               This is a REGRESSION.
                                               Run ALL tests to catch it.
```

---

## Writing Tests with pytest

**pytest** is the most popular Python testing library:

```python
import pytest
from app import StudentModel

# FIXTURE: A function that sets up data for tests
# (Like preparing ingredients before cooking)
@pytest.fixture
def sample_model():
    """Creates a fresh StudentModel with test data before each test."""
    model = StudentModel()
    model.add_student("Alice", 85)
    model.add_student("Bob", 35)
    return model

# Tests that USE the fixture (pytest injects it automatically)
def test_count_students(sample_model):
    assert len(sample_model.get_all_students()) == 2

def test_alice_is_passing(sample_model):
    alice = sample_model.get_by_name("Alice")
    assert alice["marks"] >= 40

def test_bob_is_failing(sample_model):
    bob = sample_model.get_by_name("Bob")
    assert bob["marks"] < 40

# PARAMETRIZE: Run the same test with different inputs
@pytest.mark.parametrize("marks, expected", [
    (100, True), # test case 1
    (85, True), # test case 2
    (40, True), # test case 3 — boundary
    (39, False), # test case 4 — just below boundary
    (0, False), # test case 5
])
def test_passing_boundary(marks, expected):
    from app import is_passing
    assert is_passing(marks) == expected
    # This runs 5 separate tests from one function!
```

---

## Test-Driven Development (TDD): Tests First!

TDD flips the order — you write the **test BEFORE the code**:

```
  STEP 1 (RED): Write a test for a feature that doesn't exist yet.
                    Run it → It FAILS (of course, the code isn't written!)

  STEP 2 (GREEN): Write the MINIMUM code needed to make that test pass.
                    Run it → It PASSES.

  STEP 3 (REFACTOR):Clean up the code without breaking any tests.
                    Run all tests → Still PASSING.

  Repeat for the next feature.
```

```python
# STEP 1 (RED): Write the test first
def test_calculate_grade():
    assert calculate_grade(95) == "A+" # calculate_grade doesn't exist yet!
    assert calculate_grade(85) == "A"
    assert calculate_grade(70) == "B"

# → Run: FAILS with "NameError: calculate_grade not defined" ← That's okay!

# STEP 2 (GREEN): Write the code to make it pass
def calculate_grade(marks):
    if marks >= 90: return "A+"
    if marks >= 80: return "A"
    if marks >= 70: return "B"
    return "C"

# → Run: ALL PASS

# STEP 3 (REFACTOR): The code is clean, nothing to change here.
```

[TIP]
TDD seems slow at first, but it **saves time** in the long run. You spend less time debugging mysterious errors because every piece of code has a test from the start!
[/CALLOUT]

[NOTE]
**Code Coverage**: 100% coverage (every line of code is run by at least one test) sounds perfect, but it doesn't mean 0 bugs. Coverage measures if the code was RUN, not if it was tested with the RIGHT inputs.
[/CALLOUT]

---

## Glossary

| Term | Meaning |
|:---|:---|
| **Unit Test** | A test for a single, isolated function or class |
| **Integration Test** | A test for multiple components working together |
| **Acceptance Test** | A final test by the user/client that the app meets requirements |
| **pytest** | The most popular Python testing framework |
| **Fixture** | Code that prepares the environment before each test runs |
| **Parametrize** | Running the same test with multiple sets of input data |
| **TDD** | Test-Driven Development — write tests before writing code |
| **Coverage** | The percentage of code lines executed during testing |
| **Regression** | A bug in existing code that appears after making a new change |
