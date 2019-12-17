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


def answers_by_id(id):
    return_list = []
    titles = ["id","submission_time","vote_number","question_id","message","image"]
    answers = data_manager.get_all_data('sample_data/answer.csv', titles)
    print(answers)
    id_index = 3
    for answer in answers:
        if answer[id_index] == id:
            return_list.append(answer)
    print(return_list)

    return return_list

