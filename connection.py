import bcrypt

import data_manager
import database_common


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



@database_common.connection_handler
def sorting_questions(cursor, order_by, direction):
    if direction == "asc":
        cursor.execute("""
                        SELECT * FROM question
                        ORDER BY %s ASC;
                        """ % order_by)
    else:
        cursor.execute("""
                        SELECT * FROM question
                        ORDER BY %s DESC;
                        """ % order_by)
    questions = cursor.fetchall()

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


def hash_password(plain_text_password):

    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')