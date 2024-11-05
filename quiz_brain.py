import html
import random
import requests
from question_model import Question  # Replace 'question' with the appropriate module or file name


class QuizBrain:
    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def reset_quiz(self):
        # Fetch a new set of questions from the API
        parameters = {
            "amount": 10,
            "category": 17,  # Replace '17' with the category ID for primary class science
            "type": "boolean",
        }
        
        questions_requests = requests.get(url="https://opentdb.com/api.php", params=parameters)
        questions_requests.raise_for_status()
        question_data = questions_requests.json()["results"]
        questions_requests.close()

        # Convert fetched data into Question objects
        self.question_list = []
        for question in question_data:
            question_text = html.unescape(question["question"])
            question_answer = question["correct_answer"]
            new_question = Question(question_text, question_answer)
            self.question_list.append(new_question)

        self.question_number = 0
        self.score = 0

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        question_text = self.current_question.text  # Access the 'text' attribute of the Question object
        return f"{self.question_number}: {html.unescape(question_text)}"

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False
