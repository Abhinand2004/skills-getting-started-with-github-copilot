"""Tests for DELETE /activities/{activity_name}/unregister endpoint.

Each test follows Arrange-Act-Assert to clearly delineate steps.
"""
import pytest


def test_unregister_registered_participant(client, sample_email):
    """Test successful unregistration of a registered participant."""
    # Arrange
    signup_url = f"/activities/Chess Club/signup?email={sample_email}"
    unregister_url = f"/activities/Chess Club/unregister?email={sample_email}"
    client.post(signup_url)
    
    # Act
    response = client.delete(unregister_url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]


def test_unregister_removes_participant_from_activity(client, sample_email):
    """Test that unregister removes the participant from the activity's list."""
    # Arrange
    signup_url = f"/activities/Chess Club/signup?email={sample_email}"
    unregister_url = f"/activities/Chess Club/unregister?email={sample_email}"
    client.post(signup_url)
    response = client.get("/activities")
    activities = response.json()
    assert sample_email in activities["Chess Club"]["participants"]
    
    # Act
    client.delete(unregister_url)
    
    # Assert
    response = client.get("/activities")
    activities = response.json()
    assert sample_email not in activities["Chess Club"]["participants"]


def test_unregister_nonexistent_activity_returns_404(client, sample_email):
    """Test that unregistering from a non-existent activity returns 404."""
    # Arrange
    url = f"/activities/Nonexistent Club/unregister?email={sample_email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_non_registered_participant_returns_400(client, sample_email):
    """Test that unregistering a non-registered participant returns 400."""
    # Arrange
    url = f"/activities/Chess Club/unregister?email={sample_email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_then_signup_again(client, sample_email):
    """Test that a participant can signup again after unregistering."""
    # Arrange
    signup_url = f"/activities/Chess Club/signup?email={sample_email}"
    unregister_url = f"/activities/Chess Club/unregister?email={sample_email}"
    client.post(signup_url)
    
    # Act
    client.delete(unregister_url)
    response = client.post(signup_url)

    # Assert
    assert response.status_code == 200
    response = client.get("/activities")
    activities = response.json()
    assert sample_email in activities["Chess Club"]["participants"]


def test_unregister_one_of_many_participants(client):
    """Test unregistering one participant from an activity with multiple."""
    # Arrange
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    signup1 = f"/activities/Chess Club/signup?email={email1}"
    signup2 = f"/activities/Chess Club/signup?email={email2}"
    unregister1 = f"/activities/Chess Club/unregister?email={email1}"
    client.post(signup1)
    client.post(signup2)
    
    # Act
    response = client.delete(unregister1)

    # Assert
    assert response.status_code == 200
    response = client.get("/activities")
    activities = response.json()
    assert email1 not in activities["Chess Club"]["participants"]
    assert email2 in activities["Chess Club"]["participants"]


def test_unregister_returns_success_message(client, sample_email):
    """Test that unregister returns a success message."""
    # Arrange
    signup_url = f"/activities/Chess Club/signup?email={sample_email}"
    unregister_url = f"/activities/Chess Club/unregister?email={sample_email}"
    client.post(signup_url)
    
    # Act
    response = client.delete(unregister_url)
    data = response.json()

    # Assert
    assert "Unregistered" in data["message"]
    assert sample_email in data["message"]
