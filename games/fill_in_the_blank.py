import os
import json
import random

class FillInBlanck:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        """
        Загружает один JSON-файл с квизами.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                quizzes = json.load(file)
                if isinstance(quizzes, list):
                    return quizzes
                else:
                    return [quizzes]
        except Exception as e:
            print(f"❌ Ошибка загрузки файла {self.file_path}: {e}")
            return []

    def get_quiz(self, level: str = None, topic: str = None, subtopic: str = None):
        """
        Возвращает случайный квиз по фильтрам.
        """
        filtered = self.data

        if topic:
            filtered = [q for q in filtered if q.get("topic") == topic]

        if subtopic:
            filtered = [q for q in filtered if q.get("subtopic") == subtopic]

        if filtered:
            return random.choice(filtered)
        return None
