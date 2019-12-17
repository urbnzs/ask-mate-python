import data_manager

def sort_questions(data):
    data.sort(key=lambda x: x[1], reverse= True)

    return data

def get_question_by_id(id):
    titles = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    questions = data_manager.get_all_data('sample_data/question.csv', titles)
    id_index = 0
    for question in questions:
        if question[id_index] == id:
            return question


def answers_by_id(id, by_question=True):
    return_list = []
    titles = ["id","submission_time","vote_number","question_id","message","image"]
    answers = data_manager.get_all_data('sample_data/answer.csv', titles)
    if by_question:
        id_index = 3
    else:
        id_index = 0
    for answer in answers:
        if answer[id_index] == id:
            return_list.append(answer)

    return return_list

def delete_question(id):
    titles = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    questions = data_manager.get_all_data("sample_data/question.csv", titles)
    return_list = []
    for question in questions:
        if question[0] != id:
            return_list.append(question)

    data_manager.write_data("sample_data/question.csv", return_list, titles)

def delete_answer(id, by_question=False):
    titles = ["id","submission_time","vote_number","question_id","message","image"]
    answers = data_manager.get_all_data('sample_data/answer.csv', titles)
    return_list = []
    if by_question:
        index = 3
    else:
        index = 0
    for answer in answers:
        if answer[index] != id:
            return_list.append(answer)

    data_manager.write_data("sample_data/answer.csv", return_list, titles)


def sorting_questions(order_by, direction):
    titles = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    questions = data_manager.get_all_data('sample_data/question.csv', titles)
    title_dict = {"id": 0, "submission-time": 1, "view-number": 2, "vote-number": 3, "title": 4}

    if direction == "asc":
        questions.sort(key=lambda x: x[title_dict[order_by]], reverse=False)
    else:
        questions.sort(key=lambda x: x[title_dict[order_by]], reverse=True)

    return questions

def voting_question(id, up):

    titles= ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    questions = data_manager.get_all_data('sample_data/question.csv', titles)

    for question in questions:
        if question[0] == id:
            if up == False:
                question[3] = str(int(question[3]) - 1)
            else:
                question[3] = str(int(question[3]) + 1)

    data_manager.write_data('sample_data/question.csv', questions, titles)

def voting_answers(id, up):
    titles = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
    answers = data_manager.get_all_data('sample_data/answer.csv', titles)

    for answer in answers:
        if answer[0] == id:
            if up == False:
                answer[2] = str(int(answer[2]) - 1)
                inta -= 1
            else:
                answer[2] = str(int(answer[2]) + 1)

    data_manager.write_data('sample_data/answer.csv')




