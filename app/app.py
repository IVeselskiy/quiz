import logging

from flask import Flask, request, Response, render_template
from sqlalchemy import inspect


from models import Base, engine
from views import add_questions, get_previous_questions, get_all_questions, delete_all_questions
from forms import RequestForm


logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel('INFO')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'DfFF3$657&*Tgiv*&vuvYVkuyy^&FytdrES^o8t^76857HBIG'


@app.before_request
def before_request() -> None:
    """Эндпойнт проверяет есть ли таблица "questions" в базе данных и если ее нет создает."""
    ins = inspect(engine)
    table_exist = ins.dialect.has_table(engine.connect(), 'questions')

    if not table_exist:
        Base.metadata.create_all(bind=engine)
        logger.info(f'Таблица "questions" успешно создана.')


@app.route('/quiz', methods=['GET', 'POST'])
def get_questions():
    """Эндпойнт делает запрос на ресурс jservice.io и добавляет в БД заданное количество вопросов."""
    form = RequestForm()

    if form.validate_on_submit():
        previous_questions = get_previous_questions()
        num_of_questions = form.number_of_questions.data
        request_form = {'questions_num': num_of_questions}
        add_questions(request_form)
        return render_template('index.html', form=form, questions=previous_questions)
    return render_template('index.html', form=form)


@app.route('/admin', methods=['GET', 'POST'])
def for_admin() -> Response or str:
    if request.method == 'GET':
        return render_template('admin.html', questions=get_all_questions())
    else:
        delete_all_questions()
        return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)
