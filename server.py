from flask import Flask, render_template, redirect, request


app = Flask(__name__)



@app.route('/list')
def list_questions():
    return render_template('list.html', list_of_data = list_of_data)

@app.route('/question/<question_id>')
def display_question(question_id):
    return render_template('display_question.html', question_answer = question_answer)



























if __name__ == "__main__":
        app.run(
            debug=True,
            port=5000)