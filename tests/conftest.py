import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for making HTTP requests to the FastAPI app."""
    return TestClient(app)


# Store original activities data
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state before each test to prevent state pollution."""
    # Reset to original state
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Cleanup after test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


@pytest.fixture
def sample_email():
    """Provide a sample email for signup tests."""
    return "student@mergington.edu"
