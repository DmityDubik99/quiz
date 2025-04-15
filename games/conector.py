from games.fill_in_the_blank import FillInBlanck
import random

class Conector:
    def __init__(self, file_path: str):
        print("🟢 Инициализация Conector")
        self.quiz_loader = FillInBlanck(file_path)

    def quizFiilTheBlank(self):
        connector = Conector("bd/fill_in_the_blank/english_quiz_a1.json")
        connector.connect_to_fill_in_blank(topic="Travel", subtopic="Directions")


    def connect_to_fill_in_blank(self, level="rnd", topic=None, subtopic=None):
        if level == "rnd":
            level = random.choice(["A1", "A2", "B1", "B2", "C1", "C2"])

        quiz = self.quiz_loader.get_quiz(topic=topic, subtopic=subtopic)

        if quiz:
            print("🔹 Question:", quiz["question"])
            for option in quiz["options"]:
                print(f"  {option} [{quiz['option_transcriptions'][option]}] 🔊 {quiz['option_audio'][option]}")
            print("✅ Answer:", quiz["answer"])
            print("ℹ️ Explanation:", quiz["explanation"])
        else:
            print("❌ Не удалось найти подходящий квиз.")
