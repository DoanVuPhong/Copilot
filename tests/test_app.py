import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200  # OK with redirect
    assert response.url.path == "/static/index.html"

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities

def test_signup_success():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    # Verify the student was actually added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate():
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already registered
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_nonexistent_activity():
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"