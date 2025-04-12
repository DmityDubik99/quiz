from games.fill_in_tehe_blank import FillInBlanck


class Conector:

    def connect_to_fill_in_blank(self, level="A1", topic="Travel", subtopic="Directions"):
        """
        Получает и выводит квиз по заданным параметрам.
        :param level: Уровень сложности.
        :param topic: Основная тема.
        :param subtopic: Подтема.
        """
        quiz = self.quiz_loader.get_quiz(level=level, topic=topic, subtopic=subtopic)

        if quiz:
            print("🔹 Question:", quiz["question"])
            for option in quiz["options"]:
                print(f"  {option} [{quiz['option_transcriptions'][option]}] 🔊 {quiz['option_audio'][option]}")
            print("✅ Answer:", quiz["answer"])
            print("ℹ️ Explanation:", quiz["explanation"])
        else:
            print("❌ Не удалось найти подходящий квиз.")
