"""Tests for GET / (root) endpoint.

Using the Arrange-Act-Assert pattern for clarity in each test.
"""
import pytest


def test_root_redirect_status(client):
    """Test that GET / returns a redirect status code."""
    # Arrange
    # no setup required for this endpoint

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in [301, 302, 303, 307, 308]


def test_root_redirect_location(client):
    """Test that GET / redirects to /static/index.html."""
    # Arrange
    # nothing to prepare

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert "location" in response.headers or "Location" in response.headers
    location = response.headers.get("location") or response.headers.get("Location")
    assert "/static/index.html" in location


def test_root_following_redirect(client):
    """Test that following the redirect from GET / works."""
    # Arrange
    # no preconditions

    # Act
    response = client.get("/", follow_redirects=True)

    # Assert
    assert response.status_code == 200
