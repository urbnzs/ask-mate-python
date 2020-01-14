import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import connection
import data_manager
from datetime import datetime

app = Flask(__name__, static_url_path='/static')

DATA_HEADER_question = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_answer = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
UPLOAD_folder = './static/'
ALLOWED_extensions = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_folder


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_extensions


@app.route('/', methods=['GET', 'POST'])
def loading_page():
    if request.method == "POST":
        return redirect('/list')
    return render_template('loading.html')

#DONE
@app.route('/list', methods=['GET', 'POST'])
def list_questions():
    questions = data_manager.list_questions()

    return render_template('list.html', list_of_data=questions)

#DONE
@app.route('/question/<id>')
def display_question(id):
    question = connection.get_question_by_id(id)
    answers = connection.answers_by_id(id)
    question_id = id
    connection.view_number(id)
    return render_template('display_question.html', question=question, answers=answers, question_id=question_id)

#DONE
@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    submission_time = datetime.now()
    view_num = 0
    vote_num = 0
    new_question = {'submission_time' : submission_time,'view_number' : view_num, 'vote_number' :vote_num,
                    'title': None, 'message': None, 'image': None}
    if request.method == 'POST':
        new_question['title'] = request.form['title']
        new_question['message'] = request.form['message']
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            new_question['image'] = "/static/{}".format(file.filename)
        id_ = data_manager.add_new_question(new_question)
        return redirect('/question/' + str(id_))
    return render_template('add_q.html')

#DONE
@app.route('/question/<id>/edit', methods=['GET', 'POST'])
def edit_question(id):
    question = data_manager.get_question_by_id(id)
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        file = request.files['file']
        if file and allowed_file(file.filename):

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            question['image'] = "/static/{}".format(file.filename)

        question[0]['title'] = title
        question[0]['message'] = message

        data_manager.edit_question(id, question)
        return redirect('/question/' + str(id))
    return render_template('edit_question.html', question=question, id = id)
#DONE
@app.route('/answer/<id>/edit', methods=['GET', 'POST'])
def edit_answer(id):
    answer = data_manager.get_answer_by_id(id)
    question_id = answer[0]['question_id']
    if request.method == 'POST':
        message = request.form['message']
        file = request.files['file']
        submission_time = datetime.now()
        if file and allowed_file(file.filename):

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            answer[0]['image'] = "/static/{}".format(file.filename)

        answer[0]['message'] = message

        data_manager.edit_answer(id, answer)
        return redirect('/question/' + str(question_id))
    return render_template('edit_answer.html', question=answer, id = id)
#TODO: Valami nem okés neki a question_id "foreign key"-el
@app.route('/question/<id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(id):
    submission_time = datetime.now()
    vote_num = 0
    question_id = id
    question = data_manager.get_question_by_id(question_id)
    new_answer = {'submission_time' : submission_time, 'vote_number' : vote_num, 'question_id' : question_id,'message' : None, 'image' : None}
    if request.method == 'POST':
        new_answer['message'] = request.form['message']
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            new_answer['image'] = ('/static/' + file.filename)
        id_ = data_manager.add_new_answer(new_answer)
        return redirect('/question/' + str(question_id))
    return render_template('add_answer.html', question=question, id=id)

#TODO:Valami baja van ezt se értem
@app.route('/question/<id>/delete')
def question_delete(id):
    connection.delete_question(id)
    connection.delete_answer(id, True)
    return redirect('/list')

#TODO: Valami baja van, nem értem
@app.route('/answer/<id>/delete')
def answer_delete(id):
    answer_to_delete = connection.answers_by_id(id, False)
    question_id = answer_to_delete[0]['question_id']
    connection.delete_answer(id)
    return redirect('/question/' + str(question_id))

#TODO: ordered list
@app.route('/list/ordered/<order>/<direct>')
def list_ordered(order, direct):
    list_of_data = connection.sorting_questions(order, direct)
    return render_template('list.html', list_of_data=list_of_data)

#DONE
@app.route('/question/<question_id>/vote-up')
def vote_up_question(question_id):
    connection.voting_question(question_id, True)
    return redirect('/list')

#DONE
@app.route('/question/<question_id>/vote-down')
def vote_down_question(question_id):
    connection.voting_question(question_id, False)
    return redirect('/list')

#DONE
@app.route('/answer/<answer_id>/vote-up')
def vote_up_answer(answer_id):
    connection.voting_answers(answer_id, True)
    voted_answer = connection.answers_by_id(answer_id, False)
    question_id = voted_answer[0]['question_id']
    return redirect('/question/' + str(question_id))

#DONE
@app.route('/answer/<answer_id>/vote-down')
def vote_down_answer(answer_id):
    connection.voting_answers(answer_id, False)
    voted_answer = connection.answers_by_id(answer_id, False)
    question_id = voted_answer[0]['question_id']
    return redirect('/question/' + str(question_id))


@app.route('/uploaded-image/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000)
