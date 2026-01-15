
def create_category(auth_client, name="work"):
    response = auth_client.post("/categories/", json={"name": name})
    assert response.status_code == 200
    return response.json()

def test_create_item(auth_client):
    category = create_category(auth_client)
    response = auth_client.post(
        '/items/',
        json={
            "name": "Task 1",
            "description": "in category",
            "category_id": category["id"]
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Task 1"
    assert data["description"] == "in category"
    assert data["category_id"] == category["id"]
    assert "id" in data

def test_list_items(auth_client):
    auth_client.post("/items/", json={"name": "A", "description": "one"})
    auth_client.post("/items/", json={"name": "B", "description": "two"})

    response = auth_client.get("/items/")
    assert response.status_code == 200

    data = response.json()
    names = {item["name"] for item in data}
    assert "A" in names
    assert "B" in names

def test_get_item(auth_client):
    created = auth_client.post("/items/", json={"name": "Task 1", "description": "one"}).json()
    item_id = created["id"]
    
    response = auth_client.get(f"/items/{item_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Task 1"

def test_get_item_not_found(auth_client):
    response = auth_client.get("/items/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_update_item(auth_client):
    created = auth_client.post("/items/", json={"name": "Task 1", "description": "one"}).json()
    item_id = created["id"]

    response = auth_client.put(
        f"/items/{item_id}",
        json={"name": "Task 1 Updated",
              "description": "two"},
    )

    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Task 1 Updated"
    assert data["description"] == "two"

def test_delete_item(auth_client):
    created = auth_client.post("/items/", json={"name": "Task 1", "description": "one"}).json()
    item_id = created["id"]

    response = auth_client.delete(f"/items/{item_id}")
    assert response.status_code == 200

    get_response = auth_client.get(f"/items/{item_id}")
    assert get_response.status_code == 404

def test_search_items(auth_client):
    auth_client.post("/items/", json={"name": "Alpha task", "description": "one"})
    auth_client.post("/items/", json={"name": "Beta task", "description": "two"})

    response = auth_client.get("/items/", params={"q": "Alpha"})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Alpha task"

def test_filter_items_by_category(auth_client):
    work = create_category(auth_client, name="work")
    personal = create_category(auth_client, name="personal")

    auth_client.post(
        "/items/",
        json={"name": "Work task", "description": "one", "category_id": work["id"]},
    )
    auth_client.post(
        "/items/",
        json={"name": "Personal task", "description": "two", "category_id": personal["id"]},
    )

    response = auth_client.get("/items/", params={"category_id": work["id"]})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Work task"

def test_list_items_pagination(auth_client):
    for i in range(5):
        auth_client.post("/items/", json={"name": f"Task {i}", "description": "x"})
    
    response = auth_client.get("/items/", params={"skip": 1, "limit": 2})

    assert response.status_code == 200

    # should skip Task 1 and return only Task 2 and Task 3
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Task 1"
    assert data[1]["name"] == "Task 2"

def test_update_item_category_id(auth_client):
    cat1 = create_category(auth_client, "work")
    cat2 = create_category(auth_client, "personal")

    created = auth_client.post(
        "/items/",
        json={"name": "Task 1", "description": "one", "category_id": cat1["id"]},
    ).json()
    item_id = created["id"]

    response = auth_client.put(
        f"/items/{item_id}",
        json={"category_id": cat2["id"]},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["category_id"] == cat2["id"]

def test_cannot_access_other_users_items(client):
    # User A
    client.post("/auth/register", json={"email": "a@example.com", "password": "password123"}),
    login_a = client.post("/auth/login", data={"username": "a@example.com", "password": "password123"})
    token_a = login_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # User B
    client.post("/auth/register", json={"email": "b@example.com", "password": "password123"}),
    login_b = client.post("/auth/login", data={"username": "b@example.com", "password": "password123"})
    token_b = login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User A creates an item
    created = client.post(
        "/items/",
        headers=headers_a,
        json={"name": "A item", "description": "owned by A"},
    ).json()
    item_id = created["id"]

    # User B tries to access User A's item
    response = client.get(f"/items/{item_id}", headers=headers_b)
    assert response.status_code == 404 # no bueno :) 

def test_create_item_with_tags(auth_client):
    tag1 = auth_client.post("/tags/", json={"name": "urgent"}).json()
    tag2 = auth_client.post("/tags/", json={"name": "backend"}).json()

    response = auth_client.post(
        "/items/",
        json={
            "name": "Tagged items",
            "description": "has tags",
            "tag_ids": [tag1["id"], tag2["id"]],
        },
    )
    assert response.status_code == 200
    data = response.json()
    tag_names = {t["name"] for t in data["tags"]}
    assert tag_names == {"urgent", "backend"}

def test_update_item_tags(auth_client):
    tag1 = auth_client.post("/tags/", json={"name": "urgent"}).json()
    tag2 = auth_client.post("/tags/", json={"name": "backend"}).json()

    created = auth_client.post("/items/", json={"name": "Item", "description": "x"}).json()
    item_id = created["id"]

    response = auth_client.put(
        f"/items/{item_id}",
        json={"tag_ids": [tag1["id"], tag2["id"]]},
    )
    assert response.status_code == 200
    tag_names = {t["name"] for t in response.json()["tags"]}
    assert tag_names == {"urgent", "backend"}

def test_create_item_with_invalid_tag_id(auth_client):
    response = auth_client.post(
        "/items/",
        json={"name": "Bad item", "description": "x", "tag_ids": [9999]},
    )    
    assert response.status_code == 400
    assert response.json()["detail"] == "One or more tags not found"