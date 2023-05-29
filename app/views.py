import requests
import logging

from sqlalchemy import desc

from models import Questions, session
from datetime import datetime, date


logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel('INFO')


URL: str = 'https://jservice.io/api/random'


def add_questions(request_form):

    number_of_questions = request_form['questions_num']
    number = 0
    while number < number_of_questions:
        result = requests.get(URL).json()

        question_id: int = int(result[0]['id'])
        question: str = result[0]['question']
        answer: str = result[0]['answer']

        created_at: str = result[0]['created_at']
        created_at: date = datetime.strptime(created_at[:10], '%Y-%m-%d').date()

        question_in_db = session.query(Questions).filter(Questions.question_id == question_id).one_or_none()

        if question_in_db:
            logger.info(f'Вопрос id "{question_id}" уже есть в базе данных.')
            continue

        new_question = Questions(
            question_id=question_id,
            question_text=question,
            answer=answer,
            created_at=created_at
        )

        session.add(new_question)
        session.commit()
        logger.info(f'Вопрос id "{question_id}" добавлен в базу данных.')
        number += 1


def get_previous_questions():
    previous_questions = session.query(Questions).order_by(desc(Questions.id)).first()
    if previous_questions is not None:
        return previous_questions


def get_all_questions():
    data_db = session.query(Questions).all()
    data_list = []
    for row in data_db:
        data_list.append(row)
    return data_list


def delete_all_questions():
    session.query(Questions).delete()
    session.commit()
