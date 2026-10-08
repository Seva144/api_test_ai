from uuid import UUID

from assertions.assertion_base import assert_file_not_contain_dialog
from tests.base_test import TestBase


class TestAiDeleteFile(TestBase):
    LOG_FILE = "test-ai-delete-file.log"

    """
            Тест для проверки удаления файла
            """

    def test_ai_delete_file(self):
        # 1. создание диалога
        self.logger.info(f"ШAГ 1: Создание диалога пользователя")
        create_conversation_response = self.create_conversation()
        # переменные
        id_conversation: UUID = create_conversation_response.id
        id_user: str = create_conversation_response.user_id
        try:

            # 2. Загрузка файла
            self.logger.info(f"ШАГ 2: Загружаем файл")
            file_path = "resources/Authorized.txt"
            upload_file = self.file_upload(id_conversation, file_path)
            id_file: UUID = upload_file.id

            # 3. Удаляем файл
            self.logger.info(f"ШАГ 3: Удаляем файл")
            delete_file = self.file_delete(id_conversation, id_file)
            assert id_file != delete_file, (
                f"Удаленный id загруженного файла не совпадает с загруженным"
                f" id_file={id_file} != delete_file={delete_file}"
            )

            # 4. Проверяем что файл удален
            self.logger.info(f"ШАГ 4: Получаем все файлы диалога")
            files = self.files_get(id_conversation)
            assert_file_not_contain_dialog(files, delete_file.id)
        finally:
            # 5. Удаляем диалог
            self.logger.info(f"ШАГ 5: Удаление диалога с id - {id_conversation}")
            self.delete_conversation(id_conversation, id_user)
