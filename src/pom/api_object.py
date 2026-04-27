from httpx import Response

from src.api_client import ApiClient
from src.routes import Routes

class ObjectsApi:
    def __init__(self, client: ApiClient):
        self.client = client

    # POST
    def create_object(self, payload: dict) -> Response:
        return self.client.post(Routes.OBJECTS, json=payload)

    def update_object(self, obj_id: int, payload: dict) -> Response:
        url = f"{Routes.OBJECTS}/{obj_id}"
        return self.client.put(url, json=payload)

    def delete_object(self, obj_id: int) -> Response:
        url = f"{Routes.OBJECTS}/{obj_id}"
        return self.client.delete(url)

    def get_all_objects(self) -> Response:
        return self.client.get(Routes.OBJECTS)

    def get_object_by_id(self, obj_id: int) -> Response:
        url = f"{Routes.OBJECTS}/{obj_id}"
        return self.client.get(url)

