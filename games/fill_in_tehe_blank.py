import os
import json
import random

class FillInBlanck:
    def __init__(self, folder_path: str):
        """
        Инициализация класса подключения к квизам.
        :param folder_path: Путь к папке с JSON-файлами квизов.
        """
        self.folder_path = folder_path
        self.quiz_loader = FillInBlanck(folder_path)

    def load_all_data(self):
        """
        Загружает все JSON-файлы из папки в память.
        :return: Список всех квизов.
        """
        all_quizzes = []
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".json"):
                with open(os.path.join(self.folder_path, filename), "r", encoding="utf-8") as file:
                    try:
                        quizzes = json.load(file)
                        if isinstance(quizzes, list):
                            all_quizzes.extend(quizzes)
                        else:
                            all_quizzes.append(quizzes)
                    except json.JSONDecodeError as e:
                        print(f"Ошибка чтения {filename}: {e}")
        return all_quizzes

    def get_quiz(self, level: str = None, topic: str = None, subtopic: str = None):
        """
        Получает случайный квиз по фильтрам: уровень, топик и подтопик.
        :param level: Уровень сложности (A1–C2)
        :param topic: Основная тема (например, Travel)
        :param subtopic: Подтема (например, Directions)
        :return: Один подходящий квиз (dict) или None
        """
        # Фильтруем по условиям
        filtered = self.data

        if level:
            filtered = [q for q in filtered if q.get("level") == level]

        if topic:
            filtered = [q for q in filtered if q.get("topic") == topic]

        if subtopic:
            filtered = [q for q in filtered if q.get("subtopic") == subtopic]

        # Возвращаем случайный квиз из отфильтрованных
        if filtered:
            return random.choice(filtered)
        else:
            return None