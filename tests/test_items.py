
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