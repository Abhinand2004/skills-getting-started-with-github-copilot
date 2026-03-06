"""Tests for GET /activities endpoint.

Each test is structured using Arrange-Act-Assert for readability.
"""
import pytest


def test_get_activities_returns_200(client):
    """Test that GET /activities returns a 200 status code."""
    # Arrange
    # no setup required

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200


def test_get_activities_returns_dict(client):
    """Test that GET /activities returns a dictionary."""
    # Arrange
    # nothing to set up

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert isinstance(data, dict)


def test_get_activities_contains_expected_fields(client):
    """Test that each activity has required fields."""
    # Arrange
    # endpoint ready with default data

    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert len(activities) > 0, "Should have at least one activity"
    for activity_name, activity_details in activities.items():
        assert isinstance(activity_name, str)
        assert "description" in activity_details
        assert "schedule" in activity_details
        assert "max_participants" in activity_details
        assert "participants" in activity_details
        assert isinstance(activity_details["participants"], list)


def test_get_activities_includes_known_activities(client):
    """Test that the response includes expected activities."""
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Basketball Team",
        "Music Band"
    ]

    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity in expected_activities:
        assert activity in activities, f"{activity} not found in activities"


def test_get_activities_participants_are_lists(client):
    """Test that participants field is always a list."""
    # Arrange
    # no special setup

    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_details in activities.items():
        assert isinstance(activity_details["participants"], list)
