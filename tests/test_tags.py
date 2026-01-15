def test_create_tag(auth_client):
    response = auth_client.post("/tags/", json={"name": "urgent"})
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "urgent"
    assert "id" in data

def test_list_tags(auth_client):
    auth_client.post("/tags/", json={"name": "urgent"})
    auth_client.post("/tags/", json={"name": "later"})

    response = auth_client.get("/tags/")
    assert response.status_code == 200
    names = {item["name"] for item in response.json()}
    assert "urgent" in names
    assert "later" in names

def test_get_tag(auth_client):
    created = auth_client.post("/tags/", json={"name": "urgent"}).json()
    tag_id = created["id"]

    response = auth_client.get(f"/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "urgent"

def test_update_tag(auth_client):
    created = auth_client.post("/tags/", json={"name": "urgent"}).json()
    tag_id = created["id"]

    response = auth_client.put(f"/tags/{tag_id}", json={"name": "high"})
    assert response.status_code == 200
    assert response.json()["name"] == "high"

def test_delete_tag(auth_client):
    created = auth_client.post("/tags/", json={"name": "urgent"}).json()
    tag_id = created["id"]

    response = auth_client.delete(f"/tags/{tag_id}")
    assert response.status_code == 200

    get_response = auth_client.get(f"/tags/{tag_id}")
    assert get_response.status_code == 404