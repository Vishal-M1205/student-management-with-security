def test_create_subject_success(client):
    response = client.post("/subjects/", json={"name": "Mathematics"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Mathematics"
    assert "id" in data


def test_create_subject_validation_failure(client):

    response = client.post("/subjects/", json={"name": "M"})
    assert response.status_code == 422


def test_get_all_subjects(client):

    client.post("/subjects/", json={"name": "Physics"})
    client.post("/subjects/", json={"name": "Chemistry"})

    response = client.get("/subjects/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    subject_names = [s["name"] for s in data]
    assert "Physics" in subject_names
    assert "Chemistry" in subject_names


def test_get_subject_by_id_success(client):
    created = client.post("/subjects/", json={"name": "Biology"}).json()
    subject_id = created["id"]

    response = client.get(f"/subjects/{subject_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Biology"


def test_get_subject_by_id_not_found(client):
    response = client.get("/subjects/20000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Subject Not Found"


def test_update_subject_success(client):
    created = client.post("/subjects/", json={"name": "History"}).json()
    subject_id = created["id"]

    response = client.put(f"/subjects/{subject_id}", json={"name": "World History"})
    assert response.status_code == 200
    assert response.json()["name"] == "World History"


def test_patch_subject_success(client):
    created = client.post("/subjects/", json={"name": "Computer Science"}).json()
    subject_id = created["id"]

    response = client.patch(f"/subjects/{subject_id}", json={"name": "Data Science"})
    assert response.status_code == 200
    assert response.json()["name"] == "Data Science"


def test_delete_subject_success(client):
    created = client.post("/subjects/", json={"name": "Geography"}).json()
    subject_id = created["id"]

    delete_response = client.delete(f"/subjects/{subject_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/subjects/{subject_id}")
    assert get_response.status_code == 404
