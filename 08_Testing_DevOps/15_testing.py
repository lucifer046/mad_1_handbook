# Testing with pytest

import pytest

# The function we want to test
def add_marks(current, increment):
    if increment < 0:
        raise ValueError("Increment cannot be negative")
    return current + increment

# 1. Simple Test Case
def test_add_marks_success():
    assert add_marks(80, 5) == 85

# 2. Testing for Exceptions
def test_add_marks_negative():
    with pytest.raises(ValueError):
        add_marks(80, -5)

# 3. Using Fixtures
@pytest.fixture
def sample_student():
    return {"name": "Alice", "marks": 80}

def test_student_marks(sample_student):
    new_marks = add_marks(sample_student["marks"], 10)
    assert new_marks == 90

# 4. Parametrized Testing
@pytest.mark.parametrize("current, inc, expected", [
    (10, 20, 30),
    (0, 0, 0),
    (99, 1, 100)
])
def test_add_marks_multiple(current, inc, expected):
    assert add_marks(current, inc) == expected
