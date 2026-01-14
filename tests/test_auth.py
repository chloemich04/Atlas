def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "new@example.com", "password": "password123"},
    )
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert data["is_active"] is True

def test_register_duplicate_user(client):
    client.post("/auth/register", json={"email": "dup@example.com", "password": "password123"})
    response = client.post("/auth/register", json={"email": "dup@example.com", "password": "password123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_user(client):
    client.post("/auth/register", json={"email": "login@example.com", "password": "password123"})
    response = client.post("/auth/login", data={"username": "login@example.com", "password": "password123"})
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_me_requires_auth(client):
    response = client.get("/auth/me")
    assert response.status_code == 401

def test_me_with_auth(client):
    client.post("/auth/register", json={"email": "me@example.com", "password": "password123"})
    login = client.post("/auth/login", data={"username": "me@example.com", "password": "password123"})
    token = login.json()["access_token"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"