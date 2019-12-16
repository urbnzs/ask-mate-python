from flask import Flask, render_template, redirect, request
import connection
import data_manager

app = Flask(__name__)



@app.route('/list')
def list_questions():
    titles = ["id","submission_time","view_number","vote_number","title","message","image"]
    list_of_data = connection.sort_questions(data_manager.get_all_data("sample_data/question.csv", titles))
    return render_template('list.html', list_of_data = list_of_data)

@app.route('/question/<question_id>')
def display_question(question_id):
    return render_template('display_question.html', question_answer = question_answer)



























if __name__ == "__main__":
        app.run(
            debug=True,
            port=5000)