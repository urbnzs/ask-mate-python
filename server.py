import os
from flask import Flask, render_template, request, redirect, send_from_directory, session, url_for, flash
from werkzeug.utils import escape

import connection
import data_manager
from datetime import datetime

app = Flask(__name__, static_url_path='/static')

DATA_HEADER_question = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
DATA_HEADER_answer = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
UPLOAD_folder = './static/'
ALLOWED_extensions = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_folder

app.secret_key = '_5#y2L"F4Q8zuin98xec]/'


@app.route('/index')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if data_manager.user_checker(username) != True:
            real_pass = data_manager.password_getter(username)
            if connection.verify_password(password, real_pass):
                session['username'] = username
                session['password'] = password
                session['logged_in'] = True
                return redirect('/list')
            else:
                return render_template('login.html', alerted=1)
        else:
            return render_template('login.html', alerted=1)
    return render_template('login.html', alerted=0)


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('index'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_extensions


@app.route('/', methods=['GET', 'POST'])
def list_latest_five():
    if request.method == 'POST':
        word = request.form['search']
        return redirect('/search?q={}'.format(word))

    questions = data_manager.get_last_five()
    return render_template('list_latest_five.html', list_of_data=questions)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        if data_manager.user_checker(username):
            password = connection.hash_password(request.form['password'])
            submission_time = datetime.now()
            reputation = 0
            new_user_id = data_manager.register_user(username, password, reputation, submission_time)
            session['user_id'] = new_user_id
            session['username'] = username
            session['password'] = password
            session['logged_in'] = True
            return redirect('/')
        else:
            return render_template('registration_form.html', alert=1)
    return render_template('registration_form.html', alert=0)


@app.route('/search')
def search():
    word = request.args['q']
    questions = data_manager.search(word)
    answers = data_manager.search_in_answers(word)
    return_questions = []

    question_ids = [str(answer['question_id']) for answer in answers]

    questions.append(dict(data_manager.get_questions_for_multiple_answers(question_ids)[0]))

    for item in questions:
        item['message'] = item['message'].split(" ")
        item['title'] = item['title'].split(" ")

    for i in questions:
        if i not in return_questions:
            return_questions.append(i)

    for item in answers:
        item['message'] = item['message'].split(" ")

    print("Questionok: " + str(questions))
    print("Answerek: " + str(answers))

    return render_template('search_list.html', list_of_questions=return_questions, word=word, list_of_answers=answers)


# DONE
@app.route('/list', methods=['GET', 'POST'])
def list_questions():
    questions = data_manager.list_questions()

    return render_template('list.html', list_of_data=questions)


# DONE
@app.route('/question/<id>')
def display_question(id):
    question = connection.get_question_by_id(id)
    answers = connection.answers_by_id(id)
    answer_ids = [str(answer['id']) for answer in answers]
    answer_comments = data_manager.get_comments_for_multiple_answers(answer_ids)
    answer_ids_for_answer_comments = [comment['answer_id'] for comment in answer_comments]
    question_id = id
    comments = data_manager.get_comment_by_question_id(id)
    connection.view_number(id)
    tags = data_manager.get_tag_name_by_question_id(id)
    return render_template('display_question_2.html', question=question, answers=answers, question_id=question_id,
                           comments=comments, answer_comments=answer_comments,
                           answer_ids=answer_ids_for_answer_comments,
                           tags=tags)


# DONE
@app.route('/add-question', methods=['GET', 'POST'])
def add_question():
    submission_time = datetime.now()
    view_num = 0
    vote_num = 0
    new_question = {'submission_time': submission_time, 'view_number': view_num, 'vote_number': vote_num,
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


# DONE
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
    return render_template('edit_question.html', question=question, id=id)


# DONE
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
    return render_template('edit_answer.html', question=answer, id=id)


# DONE
@app.route('/question/<id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(id):
    submission_time = datetime.now()
    vote_num = 0
    question_id = id
    question = data_manager.get_question_by_id(question_id)
    new_answer = {'submission_time': submission_time, 'vote_number': vote_num, 'question_id': question_id,
                  'message': None, 'image': None}
    if request.method == 'POST':
        new_answer['message'] = request.form['message']
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            new_answer['image'] = ('/static/' + file.filename)
        id_ = data_manager.add_new_answer(new_answer)
        return redirect('/question/' + str(question_id))
    return render_template('add_answer.html', question=question, id=id)


# DONE
@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_question(question_id):
    submission_time = datetime.now()
    new_comment = {'question_id': question_id, 'message': None, 'submission_time': submission_time, 'edited_count': 0}
    if request.method == 'POST':
        new_comment['message'] = request.form['message']
        data_manager.add_comment_to_question(new_comment)
        return redirect('/question/' + str(question_id))
    return render_template('add_comment.html', id=question_id)


# DONE
@app.route('/answer/<comment_id>/new-comment', methods=['GET', 'POST'])
def add_new_comment_to_answer(comment_id):
    submission_time = datetime.now()
    new_comment = {'answer_id': comment_id, 'message': None, 'submission_time': submission_time, 'edited_count': 0}
    answer = connection.answers_by_id(comment_id, False)
    question_id = answer[0]['question_id']
    if request.method == 'POST':
        new_comment['message'] = request.form['message']
        data_manager.add_comment_to_answer(new_comment)
        return redirect('/question/' + str(question_id))
    return render_template('add_comment_to_answer.html', id=comment_id)


# DONE
@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_question_comment(comment_id):
    submission_time = datetime.now()
    original_comment = data_manager.get_comment_by_id(comment_id)
    if original_comment[0]['edited_count'] != None:
        edited_count = int(original_comment[0]['edited_count']) + 1
    else:
        edited_count = 1
    edited_comment = {'submission_time': submission_time, 'edited_count': edited_count}
    if original_comment[0]['question_id'] != None:
        question_id = original_comment[0]['question_id']
    else:
        answer = data_manager.get_answer_by_id(original_comment[0]['answer_id'])
        question_id = answer[0]['question_id']
    if request.method == 'POST':
        edited_comment['message'] = request.form['message']
        data_manager.edit_comments(comment_id, edited_comment)
        return redirect('/question/' + str(question_id))
    return render_template('edit_comment.html', comment=original_comment, question_id=question_id)


# DONE
@app.route('/comment/<comment_id>/delete')
def delete_comment(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    print(comment)
    if comment[0]['question_id'] != None:
        question_id = comment[0]['question_id']
    else:
        answer = data_manager.get_answer_by_id(comment[0]['answer_id'])
        question_id = answer[0]['question_id']
    data_manager.delete_comments(comment_id)
    print(question_id)
    return redirect('/question/' + str(question_id))


# DONE
@app.route('/question/<id>/delete')
def question_delete(id):
    tag_ids = data_manager.get_tags_by_question(id)
    if tag_ids != []:
        for tag in tag_ids:
            data_manager.delete_tags_by_question(id, tag['tag_id'])
    data_manager.delete_comment_by_question_id(id)
    answers = connection.answers_by_id(id)
    for answer in answers:
        data_manager.delete_comment_by_answer_id(answer['id'])
    connection.delete_answer(id, True)
    connection.delete_question(id)
    return redirect('/list')


# DONE
@app.route('/answer/<id>/delete')
def answer_delete(id):
    answer_to_delete = connection.answers_by_id(id, False)
    data_manager.delete_comment_by_answer_id(id)
    question_id = answer_to_delete[0]['question_id']
    connection.delete_answer(id)
    return redirect('/question/' + str(question_id))


# DONE
@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_new_tag(question_id):
    tags = data_manager.get_all_tags()
    if request.method == 'POST':
        existing_tag = request.form['existing_tag']
        if existing_tag == "add_new_tag":
            new_tag = request.form["new_tag"]
            new_tag_id = data_manager.add_new_tag(new_tag)
            data_manager.add_new_tag_to_question(new_tag_id, question_id)
        else:
            existing_tag_id = data_manager.get_tag_id_by_name(existing_tag)
            data_manager.add_new_tag_to_question(existing_tag_id, question_id)
        return redirect('/question/' + str(question_id))
    return render_template('new_tag.html', question_id=question_id, tags=tags)


# DONE
@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    data_manager.delete_tags_by_question(question_id, tag_id)
    return redirect('/question/' + str(question_id))


# DONE
@app.route('/list/ordered/<order>/<direct>')
def list_ordered(order, direct):
    list_of_data = connection.sorting_questions(order, direct)
    return render_template('list.html', list_of_data=list_of_data)


# DONE
@app.route('/question/<question_id>/vote-up')
def vote_up_question(question_id):
    connection.voting_question(question_id, True)
    return redirect('/list')


# DONE
@app.route('/question/<question_id>/vote-down')
def vote_down_question(question_id):
    connection.voting_question(question_id, False)
    return redirect('/list')


# DONE
@app.route('/answer/<answer_id>/vote-up')
def vote_up_answer(answer_id):
    connection.voting_answers(answer_id, True)
    voted_answer = connection.answers_by_id(answer_id, False)
    question_id = voted_answer[0]['question_id']
    return redirect('/question/' + str(question_id))


# DONE
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


@app.route('/tags')
def list_all_tags():
    tags = data_manager.get_all_tags()
    return render_template('all_tags.html', tags=tags)


@app.route('/all-users')
def list_all_users():
    users = data_manager.get_all_users()
    return render_template('all_users.html', users=users)


@app.route('/<answer_id>/accept-answer')
def accepted_answer(answer_id):
    question_id = connection.accept_answer(answer_id)
    return redirect('/question/' + str(question_id))


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000)
