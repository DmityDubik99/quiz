import sqlite3 as sq
import random


class Connect:
    def __init__(self):
        self.base = sq.connect('words.db')
        self.cur = self.base.cursor()
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS statistics (
                         user_id INTEGER,
                         user_name TEXT,
                         right INTEGER,
                         wrong INTEGER,
                         level INTEGER DEFAULT 1
        )""")
        self.base.commit()

    

    def create_user(self, user_id, name: str):
        self.cur.execute("""INSERT INTO statistics VALUES (?, ?, 0, 0, 1)""", (user_id, name))  # Start at level 1
        self.base.commit()

    def update_right(self, user_id):
        self.cur.execute("UPDATE statistics SET right = right + 1 WHERE user_id = ?", (user_id,))
        self.base.commit()
        
        # Обновляем уровень пользователя
        self.update_level(user_id)

        
    def update_wrong(self, user_id):
        self.cur.execute("""UPDATE statistics SET wrong = wrong+1 WHERE user_id = '{}'""".format(user_id))
        self.base.commit()

    def clear_stat(self, user_id):
        self.cur.execute("""UPDATE statistics SET right = 0, wrong = 0, level = 1 WHERE user_id = '{}'""".format(user_id))  # Reset to level 1
        self.base.commit()

    def get_words(self):
        self.words = self.cur.execute("SELECT * FROM eng_words WHERE id IN (?, ?, ?, ?)", random.sample(range(1, 5001), 4)).fetchall()
        random.shuffle(self.words)
        return self.words
    
    def get_stat(self, user_id):
        result = self.cur.execute("SELECT right, wrong, level FROM statistics WHERE user_id = ?", (user_id,)).fetchone()
        if result:
            return result
        return (0, 0, 1)  # если данных нет, возвращаем значения по умолчанию



    def update_level(self, user_id):
        # Получаем количество правильных ответов
        right_answers = self.cur.execute("SELECT right FROM statistics WHERE user_id = ?", (user_id,)).fetchone()[0]
        
        # Начальный порог для каждого уровня
        level_threshold = 2  # Для первого уровня нужно 10 правильных ответов
        
        # Вычисляем уровень на основе правильных ответов с умножением на 2 для каждого уровня
        level = 1
        while right_answers >= level_threshold:
            level_threshold *= 2  # Увеличиваем порог для следующего уровня (умножаем на 2)
            level += 1  # Переходим на следующий уровень

        # Максимальный уровень 10, если уровень больше 10, то устанавливаем его равным 10
        if level > 10:
            level = 10
        
        # Обновляем уровень пользователя в базе данных
        current_level = self.cur.execute("SELECT level FROM statistics WHERE user_id = ?", (user_id,)).fetchone()[0]
        
        # Если уровень изменился, обновляем его и отправляем уведомление
        if current_level != level:
            self.cur.execute("UPDATE statistics SET level = ? WHERE user_id = ?", (level, user_id))
            self.base.commit()
            return True, level  # Возвращаем True, если уровень изменился
        return False, current_level  # Возвращаем False, если уровень не изменился



