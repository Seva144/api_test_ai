from api import routes


def post_conversation(client, **kwargs):
    return client.post(routes.Routes.CONVERSATION, **kwargs)


def delete_conversation(client, id_conversation):
    return client.delete(routes.Routes.CONVERSATION_BY_ID.format(id_conversation))