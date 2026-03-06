"""Tests for POST /activities/{activity_name}/signup endpoint.

All tests use the Arrange-Act-Assert pattern to make intentions clear.
"""
import pytest


def test_signup_valid_activity_and_email(client, sample_email):
    """Test successful signup for a valid activity."""
    # Arrange
    url = f"/activities/Chess Club/signup?email={sample_email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert sample_email in data["message"]


def test_signup_adds_participant_to_activity(client, sample_email):
    """Test that signup adds the participant to the activity's list."""
    # Arrange
    signup_url = f"/activities/Chess Club/signup?email={sample_email}"

    # Act
    client.post(signup_url)

    # Assert
    response = client.get("/activities")
    activities = response.json()
    assert sample_email in activities["Chess Club"]["participants"]


def test_signup_nonexistent_activity_returns_404(client, sample_email):
    """Test that signing up for a non-existent activity returns 404."""
    # Arrange
    url = f"/activities/Nonexistent Club/signup?email={sample_email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_multiple_people_same_activity(client):
    """Test that multiple people can sign up for the same activity."""
    # Arrange
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    url1 = f"/activities/Chess Club/signup?email={email1}"
    url2 = f"/activities/Chess Club/signup?email={email2}"

    # Act
    response1 = client.post(url1)
    response2 = client.post(url2)

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    response = client.get("/activities")
    activities = response.json()
    assert email1 in activities["Chess Club"]["participants"]
    assert email2 in activities["Chess Club"]["participants"]


def test_signup_duplicate_signup_same_person(client, sample_email):
    """Test that the same person can sign up multiple times (creates duplicates in list)."""
    # Arrange
    url = f"/activities/Chess Club/signup?email={sample_email}"

    # Act
    response1 = client.post(url)
    response2 = client.post(url)

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    response = client.get("/activities")
    activities = response.json()
    count = activities["Chess Club"]["participants"].count(sample_email)
    assert count == 2


def test_signup_returns_success_message(client, sample_email):
    """Test that signup returns a success message."""
    # Arrange
    url = f"/activities/Chess Club/signup?email={sample_email}"

    # Act
    response = client.post(url)
    data = response.json()

    # Assert
    assert "Signed up" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_to_different_activities(client, sample_email):
    """Test that a person can sign up for multiple different activities."""
    # Arrange
    url1 = f"/activities/Chess Club/signup?email={sample_email}"
    url2 = f"/activities/Programming Class/signup?email={sample_email}"

    # Act
    response1 = client.post(url1)
    response2 = client.post(url2)

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    response = client.get("/activities")
    activities = response.json()
    assert sample_email in activities["Chess Club"]["participants"]
    assert sample_email in activities["Programming Class"]["participants"]
