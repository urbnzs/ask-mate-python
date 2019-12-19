import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import connection
import data_manager
import time

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
    if request.method=="POST":
        return redirect('/list')
    return render_template('loading.html')
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
    connection.view_number(id)
    return render_template('display_question.html', question = question, answers = answers, question_id=question_id)

@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
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
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename_original = file.filename.split('.')
            filename = ".".join([str(id_), filename_original[-1]])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_question.append('/static/' + filename)
        list_of_data.append(new_question)
        data_manager.write_data("sample_data/question.csv", list_of_data, titles)
        return redirect('/question/' + str(id_))
    return render_template('add_q.html')

@app.route('/question/<id>/edit', methods=['GET', 'POST'])
def edit_question(id):
    question = []
    mentheto = False
    titles = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    questions = data_manager.get_all_data('sample_data/question.csv', titles)

    for item in questions:
        if item[0] == id:
            question = item
    generated_id = int(questions[-1][0]) + 1
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename_original = file.filename.split('.')
            filename = "20" + ".".join([id, filename_original[-1]])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            mentheto = True
        question[4] = title
        question[5] = message
        if mentheto == True:
            question[6] = "/static/" + filename
        #for item in questions:
            #if item[0] == question[0]:
                #question[0] = int(questions[-1][0]) + 1
                #item = question
        data_manager.write_data('sample_data/question.csv', questions, titles)
        return redirect('/question/' + str(id))
    return render_template('edit_question.html', question = question)



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
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename_original = file.filename.split('.')
            filename = '10' + ".".join([str(answer_id), filename_original[-1]])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_answer.append('/static/' + filename)
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


@app.route('/list/ordered/<order>/<direct>')
def list_ordered(order, direct):
    list_of_data = connection.sorting_questions(order, direct)
    return render_template('list.html', list_of_data = list_of_data)

@app.route('/question/<question_id>/vote-up')
def vote_up_question(question_id):
    connection.voting_question(question_id, True)
    return redirect('/list')

@app.route('/question/<question_id>/vote-down')
def vote_down_question(question_id):
    connection.voting_question(question_id, False)
    return redirect('/list')

@app.route('/answer/<answer_id>/vote-up')
def vote_up_answer(answer_id):
    connection.voting_answers(answer_id, True)
    voted_answer = connection.answers_by_id(answer_id, False)
    question_id = voted_answer[0][3]
    return redirect('/question/' + str(question_id))

@app.route('/answer/<answer_id>/vote-down')
def vote_down_answer(answer_id):
    connection.voting_answers(answer_id, False)
    voted_answer = connection.answers_by_id(answer_id, False)
    question_id = voted_answer[0][3]
    return redirect('/question/' + str(question_id))

@app.route('/uploaded-image/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)










if __name__ == "__main__":
        app.run(
            debug=True,
            port=5000)