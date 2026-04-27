
def test_create(objects_api):
    # Фикстура objects_api уже создала клиент и сервис!
    payload = {"name": "Test", "value": 42}

    # Создаем
    # create_resp = objects_api.create_object(payload)
    # assert create_resp.status_code == 200
    # obj_id = create_resp.json()["id"]

    # Получаем
    get_resp = objects_api.get_object_by_id("1")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Test"

    # # Чистим
    # objects_api.delete_object(obj_id)



