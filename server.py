from flask import Flask, render_template, redirect, request
import connection
import data_manager
import time

app = Flask(__name__)



@app.route('/list')
def list_questions():
    titles = ["id","submission_time","view_number","vote_number","title","message","image"]
    list_of_data = connection.sort_questions(data_manager.get_all_data("sample_data/question.csv", titles))
    return render_template('list.html', list_of_data = list_of_data)

@app.route('/question/<question_id>')
def display_question(question_id):
    return render_template('display_question.html', question_answer = question_answer)

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
        new_question.append(request.form['image'])
        list_of_data.append(new_question)
        print(new_question)
        data_manager.write_data("sample_data/question.csv", list_of_data, titles)
        print(list_of_data)
        return redirect('/question/id_')
    return render_template('add_q.html')


























if __name__ == "__main__":
        app.run(
            debug=True,
            port=5000)