# def test_get_all_students(client):
#     client.post("/students/", json={"name": "Charlie Brown", "age": 20, "gender": "M"})
#     client.post("/students/", json={"name": "Diana Prince", "age": 22, "gender": "F"})

#     response = client.get("/students/")
#     assert response.status_code == 200

#     data = response.json()
#     assert "students" in data
#     assert data["total"] >= 2
#     assert data["page"] == 1
#     assert data["limit"] == 5
#     assert data["total_pages"] >= 1

#     student_names = [s["name"] for s in data["students"]]
#     assert "Charlie Brown" in student_names
#     assert "Diana Prince" in student_names


# def test_get_all_students_with_filtering(client):
#     client.post("/students/", json={"name": "Edward Norton", "age": 25, "gender": "M"})
#     client.post(
#         "/students/", json={"name": "Fiona Gallagher", "age": 25, "gender": "F"}
#     )
#     client.post("/students/", json={"name": "George Clark", "age": 19, "gender": "M"})

#     # Filter by gender
#     res_gender = client.get("/students/?gender=F")
#     assert res_gender.status_code == 200
#     f_students = res_gender.json()["students"]
#     assert all(s["gender"] == "F" for s in f_students)

#     # Filter by age
#     res_age = client.get("/students/?age=25")
#     assert res_age.status_code == 200
#     age_students = res_age.json()["students"]
#     assert all(s["age"] == 25 for s in age_students)
