import data_manager


def sort_questions(data):
    data.sort(key=lambda x: x['submission_time'], reverse=True)

    return data


def get_question_by_id(id):
    questions = data_manager.get_all_data('sample_data/question.csv')
    for question in questions:
        if question['id'] == id:
            return question


def answers_by_id(id, by_question=True):
    return_list = []
    answers = data_manager.get_all_data('sample_data/answer.csv')
    if by_question:
        for answer in answers:
            if answer['question_id'] == id:
                return_list.append(answer)
    else:
        for answer in answers:
            if answer['id'] == id:
                return_list.append(answer)

    return return_list


def delete_question(id):
    questions = data_manager.get_all_data("sample_data/question.csv")
    return_list = []
    for question in questions:
        if question['id'] != id:
            return_list.append(question)

    data_manager.write_data("sample_data/question.csv", return_list)


def delete_answer(id, by_question=False):
    return_list = []
    answers = data_manager.get_all_data('sample_data/answer.csv')
    if by_question:
        for answer in answers:
            if answer['question_id'] != id:
                return_list.append(answer)
    else:
        for answer in answers:
            if answer['id'] != id:
                return_list.append(answer)

    data_manager.write_data('sample_data/answer.csv', return_list)



def sorting_questions(order_by, direction):
    questions = data_manager.get_all_data('sample_data/question.csv')
    if direction == "asc":
        if questions[0][order_by].isdigit():
            questions.sort(key=lambda x: int(x[order_by]), reverse=False)
        else:
            questions.sort(key=lambda x: x[order_by].title(), reverse=False)
    else:
        if questions[0][order_by].isdigit():
            questions.sort(key=lambda x: int(x[order_by]), reverse=True)
        else:
            questions.sort(key=lambda x: x[order_by].title(), reverse=True)

    return questions


def voting_question(id, up):
    questions = data_manager.get_all_data('sample_data/question.csv')

    for question in questions:
        if question['id'] == id:
            if not up:
                question['vote_number'] = str(int(question['vote_number']) - 1)
            else:
                question['vote_number'] = str(int(question['vote_number']) + 1)

    data_manager.write_data('sample_data/question.csv', questions)


def voting_answers(id, up):
    answers = data_manager.get_all_data('sample_data/answer.csv')

    for answer in answers:
        if answer['id'] == id:
            if up is False:
                answer['vote_number'] = str(int(answer['vote_number']) - 1)
            else:
                answer['vote_number'] = str(int(answer['vote_number']) + 1)

    data_manager.write_data('sample_data/answer.csv', answers)


def view_number(id):
    questions = data_manager.get_all_data('sample_data/question.csv')

    for question in questions:
        if question['id'] == id:
            question['view_number'] = str(int(question['view_number']) + 1)

    data_manager.write_data('sample_data/question.csv', questions)
