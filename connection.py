import data_manager
import database_common

#TODO: sort questions
def sort_questions(data):
    data.sort(key=lambda x: x['submission_time'], reverse=True)

    return data


@database_common.connection_handler
def get_question_by_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM question
                    where id = %(id)s;

                    """, {'id': id})

    question = cursor.fetchall()
    return question

@database_common.connection_handler
def answers_by_id(cursor, id, by_question=True):
    if by_question:
        cursor.execute("""
                        SELECT * FROM answer
                        WHERE question_id = %(id)s;
                        
                        """, {'id' : id})
    else:
        cursor.execute("""
                        SELECT * FROM answer
                        WHERE id = %(id)s
                        
                        """, {'id': id})

    answers = cursor.fetchall()
    return answers



@database_common.connection_handler
def delete_question(cursor,id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(id)s;
    
                    """,{'id': id})


@database_common.connection_handler
def delete_answer(cursor, id,by_question = False):
    if by_question:
        cursor.execute("""
                            DELETE FROM answer
                            WHERE question_id = %(id)s;
                            """,{'id' : id})
    else:
        cursor.execute("""
                            DELETE FROM answer
                            WHERE id = %(id)s;
                            """, {'id' : id})



#TODO: sorting questions by any order and direction
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

@database_common.connection_handler
def voting_question(cursor, id, up):

    if up:
        cursor.execute("""
                        UPDATE question
                        SET vote_number = vote_number +1 
                        WHERE id = %(id)s;
                        """, {'id' : id})
    else:
        cursor.execute("""
                                UPDATE question
                                SET vote_number = vote_number -1 
                                WHERE id = %(id)s;
                                """, {'id': id})


@database_common.connection_handler
def voting_answers(cursor, id, up):
    if up:
        cursor.execute("""
                        UPDATE answer
                        SET vote_number = vote_number +1 
                        WHERE id = %(id)s;
                        """, {'id': id})
    else:
        cursor.execute("""
                                UPDATE answer
                                SET vote_number = vote_number -1 
                                WHERE id = %(id)s;
                                """, {'id': id})

@database_common.connection_handler
def view_number(cursor, id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = %(id)s;
                     
                    """, {'id' : id})
