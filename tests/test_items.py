
def create_category(client, name="work"):
    response = client.post("/categories/", json={"name": name})
    assert response.status_code == 200
    return response.json()

def test_create_item(client):
    category = create_category(client)
    response = client.post(
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

def test_list_items(client):
    client.post("/items/", json={"name": "A", "description": "one"})
    client.post("/items/", json={"name": "B", "description": "two"})

    response = client.get("/items/")
    assert response.status_code == 200

    data = response.json()
    names = {item["name"] for item in data}
    assert "A" in names
    assert "B" in names

def test_get_item(client):
    created = client.post("/items/", json={"name": "Task 1", "description": "one"}).json()
    item_id = created["id"]
    
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Task 1"

def test_get_item_not_found(client):
    response = client.get("/items/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_update_item(client):
    created = client.post("/items/", json={"name": "Task 1", "description": "one"}).json()
    item_id = created["id"]

    response = client.put(
        f"/items/{item_id}",
        json={"name": "Task 1 Updated",
              "description": "two"},
    )

    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Task 1 Updated"
    assert data["description"] == "two"

def test_delete_item(client):
    created = client.post("/items/", json={"name": "Task 1", "description": "one"}).json()
    item_id = created["id"]

    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200

    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404

def test_search_items(client):
    client.post("/items/", json={"name": "Alpha task", "description": "one"})
    client.post("/items/", json={"name": "Beta task", "description": "two"})

    response = client.get("/items/", params={"q": "Alpha"})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Alpha task"

def test_filter_items_by_category(client):
    work = create_category(client, name="work")
    personal = create_category(client, name="personal")

    client.post(
        "/items/",
        json={"name": "Work task", "description": "one", "category_id": work["id"]},
    )
    client.post(
        "/items/",
        json={"name": "Personal task", "description": "two", "category_id": personal["id"]},
    )

    response = client.get("/items/", params={"category_id": work["id"]})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Work task"
