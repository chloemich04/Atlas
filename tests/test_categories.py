
def test_create_category(client):
    # the client will create a new category called "work"
    response = client.post("/categories/", json={"name": "work"})

    # verify the response status code is 200
    assert response.status_code == 200

    # verify that "work" is in the response body
    data = response.json()
    assert data["name"] == "work"
    assert "id" in data

def test_list_categories(client):
    # client will create categories
    client.post("/categories/", json={"name": "work"})
    client.post("/categories/", json={"name": "personal"})

    # client will request to see all the categories
    response = client.get("/categories/")
    assert response.status_code == 200

    data = response.json()
    names = {item["name"] for item in data}
    # verify if the categories the client created are there
    assert "work" in names
    assert "personal" in names

def test_get_category(client):
    created = client.post("/categories/", json={"name": "work"}).json()
    category_id = created["id"]
    
    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == "work"

def test_get_category_not_found(client):
    # client will input a crazy category id
    response = client.get("/categories/9999")
    # the request should not be accepted
    assert response.status_code == 404
    # verify to see if the not found message shows up
    assert response.json()["detail"] == "Category not found"