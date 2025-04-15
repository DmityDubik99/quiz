from games.conector import Conector
import asyncio

async def main():
    connector = Conector("bd/fill_in_the_blank/english_quiz_a1.json")
    connector.connect_to_fill_in_blank(topic="Travel", subtopic="Directions")

if __name__ == "__main__":
    asyncio.run(main())
