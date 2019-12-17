import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import connection
import data_manager
import time

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')


@app.route('/list', methods=['GET', 'POST'])
def list_questions():
    titles = ["id","submission_time","view_number","vote_number","title","message","image"]
    list_of_data = connection.sort_questions(data_manager.get_all_data("sample_data/question.csv", titles))
    if request.method == "POST":
        order = request.form['Order By']
        direction = request.form['Direction']
        return redirect('/list/order_by=' + order + '&order_direction=' + direction)

    return render_template('list.html', list_of_data = list_of_data)

@app.route('/question/<id>')
def display_question(id):
    question = connection.get_question_by_id(id)
    answers = connection.answers_by_id(id)
    question_id = id
    return render_template('display_question.html', question = question, answers = answers, question_id=question_id)

@app.route('/question/<id>/edit')
@app.route('/add-question', methods=['GET', 'POST'])
def add_new_question():
    titles = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    list_of_data = data_manager.get_all_data("sample_data/question.csv", titles)
    id_ = int(list_of_data[-1][0]) + 1
    submission_time = int(time.time())
    view_num = 0
    vote_num = 0
    new_question = [id_, submission_time, view_num, vote_num]
    if request.method == 'POST':
        new_question.append(request.form['title'])
        new_question.append(request.form['message'])
        profile = request.files['image']
        profile.save(os.path.join(uploads_dir, secure_filename(profile.filename)))
        list_of_data.append(new_question)
        data_manager.write_data("sample_data/question.csv", list_of_data, titles)
        return redirect('/question/' + str(id_))
    return render_template('add_q.html')

@app.route('/question/<id>/new-answer', methods=['GET','POST'])
def add_new_answer(id):
    question = connection.get_question_by_id(id)
    titles = ['id', 'submission_time', 'vote_number', 'question_id', 'message','image']
    all_answers = data_manager.get_all_data("sample_data/answer.csv", titles)
    answer_id = int(all_answers[-1][0]) + 1
    submission_time = int(time.time())
    vote_num = 0
    question_id = id
    new_answer = [answer_id, submission_time, vote_num, question_id]
    if request.method == 'POST':
        new_answer.append(request.form['message'])
        new_answer.append(request.form['image'])
        all_answers.append(new_answer)
        data_manager.write_data("sample_data/answer.csv", all_answers, titles)
        return redirect('/question/' + str(question_id))
    return render_template('add_answer.html', question=question, id=id)

@app.route('/question/<id>/delete')
def question_delete(id):
    connection.delete_question(id)
    connection.delete_answer(id, True)
    return redirect('/list')

@app.route('/answer/<id>/delete')
def answer_delete(id):
    answer_to_delete = connection.answers_by_id(id, False)
    question_id = answer_to_delete[0][3]
    connection.delete_answer(id)
    return redirect('/question/' + str(question_id))


@app.route('/list/order_by=<order>&order_direction=<direct>')
def list_ordered(order, direct):


    list_of_data = connection.sorting_questions(order, direct)
    return render_template('list.html', list_of_data = list_of_data)




















if __name__ == "__main__":
        app.run(
            debug=True,
            port=5000)