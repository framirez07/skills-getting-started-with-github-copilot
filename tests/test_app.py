"""
Unit tests for the Mergington High School Activities API.
Tests follow the AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_200(self, client: TestClient):
        """Arrange: Setup already done by fixture
        Act: Make GET request to /activities
        Assert: Response status is 200"""
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client: TestClient):
        """Arrange: Setup already done by fixture
        Act: Make GET request to /activities
        Assert: Response contains a dictionary"""
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, dict)

    def test_get_activities_contains_expected_fields(self, client: TestClient):
        """Arrange: Setup already done by fixture
        Act: Make GET request to /activities
        Assert: Each activity has required fields"""
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data

    def test_get_activities_participants_is_list(self, client: TestClient):
        """Arrange: Setup already done by fixture
        Act: Make GET request to /activities
        Assert: Participants field is a list"""
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_contains_chess_club(self, client: TestClient):
        """Arrange: Setup already done by fixture
        Act: Make GET request to /activities
        Assert: Chess Club is in the activities"""
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert "Chess Club" in data


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful_returns_200(self, client: TestClient):
        """Arrange: Prepare email and activity name
        Act: POST to signup endpoint
        Assert: Response status is 200"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200

    def test_signup_successful_returns_message(self, client: TestClient):
        """Arrange: Prepare email and activity name
        Act: POST to signup endpoint
        Assert: Response contains success message"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_duplicate_returns_400(self, client: TestClient):
        """Arrange: Use an email already in Chess Club
        Act: POST to signup endpoint
        Assert: Response status is 400"""
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400

    def test_signup_duplicate_error_message(self, client: TestClient):
        """Arrange: Use an email already in Chess Club
        Act: POST to signup endpoint
        Assert: Response contains appropriate error message"""
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_signup_nonexistent_activity_returns_404(self, client: TestClient):
        """Arrange: Prepare non-existent activity name
        Act: POST to signup endpoint
        Assert: Response status is 404"""
        # Arrange
        email = "student@mergington.edu"
        activity_name = "NonExistent Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404

    def test_signup_nonexistent_activity_error_message(self, client: TestClient):
        """Arrange: Prepare non-existent activity name
        Act: POST to signup endpoint
        Assert: Response contains appropriate error message"""
        # Arrange
        email = "student@mergington.edu"
        activity_name = "NonExistent Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "Activity not found" in data["detail"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_successful_returns_200(self, client: TestClient):
        """Arrange: Use an email already in an activity
        Act: DELETE from unregister endpoint
        Assert: Response status is 200"""
        # Arrange
        email = "michael@mergington.edu"  # In Chess Club
        activity_name = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200

    def test_unregister_successful_returns_message(self, client: TestClient):
        """Arrange: Use an email already in an activity
        Act: DELETE from unregister endpoint
        Assert: Response contains success message"""
        # Arrange
        email = "michael@mergington.edu"  # In Chess Club
        activity_name = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_nonparticipant_returns_400(self, client: TestClient):
        """Arrange: Use an email not in the activity
        Act: DELETE from unregister endpoint
        Assert: Response status is 400"""
        # Arrange
        email = "notinactivity@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400

    def test_unregister_nonparticipant_error_message(self, client: TestClient):
        """Arrange: Use an email not in the activity
        Act: DELETE from unregister endpoint
        Assert: Response contains appropriate error message"""
        # Arrange
        email = "notinactivity@mergington.edu"
        activity_name = "Chess Club"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "not registered" in data["detail"]

    def test_unregister_nonexistent_activity_returns_404(self, client: TestClient):
        """Arrange: Prepare non-existent activity name
        Act: DELETE from unregister endpoint
        Assert: Response status is 404"""
        # Arrange
        email = "student@mergington.edu"
        activity_name = "NonExistent Club"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404

    def test_unregister_nonexistent_activity_error_message(self, client: TestClient):
        """Arrange: Prepare non-existent activity name
        Act: DELETE from unregister endpoint
        Assert: Response contains appropriate error message"""
        # Arrange
        email = "student@mergington.edu"
        activity_name = "NonExistent Club"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert "Activity not found" in data["detail"]
