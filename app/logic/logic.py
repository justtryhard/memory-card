import json
import random
from typing import List, Dict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent # константа для поднятия на 2 уровня выше (в корень)
DATA_DIR = BASE_DIR / "data"
QUESTIONS_PATH = DATA_DIR / "questions.json"


class QuestionDatabase:
    """
    Класс, с которым работает UI
    """

    def __init__(self):
        loader = QuestionLoader()
        questions = loader.load()
        self.manager = QuestionManager(questions)

    def get_question(self) -> Dict | None:
        return self.manager.get_random_question()

    def check_answer(self, question: Dict, index: int) -> bool:
        return self.manager.check_answer(question, index)


class QuestionLoader:
    def load(self) -> List[Dict]:
        """Загрузка вопросов из json с постоянным путём"""
        with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)


class QuestionManager:
    def __init__(self, questions: List[Dict]):
        self.questions = questions
        self.used_ids = set()

    def get_random_question(self) -> Dict | None:
        """Возврат случайного вопроса без повторений.
        Вопросы не повторяются до полного прохождения списка.
        Если вопросы закончатся - происходит обнуление used_ids и начинается сначала.
        """
        if not self.questions:
            return None

        available = [elem for elem in self.questions if elem["id"] not in self.used_ids]
        if not available:
            self.used_ids.clear()
            available = self.questions

        question = random.choice(available)
        self.used_ids.add(question["id"])
        return question

    def check_answer(self, question: Dict, answer_index: int) -> bool:
        """Проверка правильности ответа"""
        return question["correct"] == answer_index
