from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2


engine = create_engine('postgresql+psycopg2://admin:admin@quiz_db:5432/quiz_db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Questions(Base):
    """Модель для хранения вопросов и ответов для викторины."""
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, unique=True, nullable=True)
    question_text = Column(String(500), nullable=True)
    answer = Column(String(500), nullable=True)
    created_at = Column(Date, nullable=True)

    def __repr__(self):
        return f'id: {self.id}, ' \
               f'question_id: {self.question_id}, ' \
               f'question_text: {self.question_text},' \
               f'answer: {self.answer},' \
               f'created_at: {self.created_at}'

    def to_json(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
