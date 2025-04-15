from games.fill_in_the_blank import FillInBlanck

class Conector:
    def __init__(self, file_path: str):
        print("🟢 Инициализация Conector")
        self.quiz_loader = FillInBlanck(file_path)

    def connect_to_fill_in_blank(self, level=None, topic=None, subtopic=None):
        quiz = self.quiz_loader.get_quiz(topic=topic, subtopic=subtopic)

        if quiz:
            print("🔹 Question:", quiz["question"])
            for option in quiz["options"]:
                print(f"  {option} [{quiz['option_transcriptions'][option]}] 🔊 {quiz['option_audio'][option]}")
            print("✅ Answer:", quiz["answer"])
            print("ℹ️ Explanation:", quiz["explanation"])
        else:
            print("❌ Не удалось найти подходящий квиз.")
