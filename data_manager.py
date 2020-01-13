import csv
import database_common



@database_common.connection_handler
def add_new_question(cursor, question):
    values = ', '.join("'" + str(x) + "'" for x in question.values())
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%s);
                     """ % (values))
    cursor.execute("""
                    SELECT id FROM question 
                    WHERE submission_time = %(submission_time)s;""", {'submission_time': question['submission_time']})

    id = cursor.fetchall()
    print(id[0]['id'])
    return id[0]['id']

@database_common.connection_handler
def add_new_answer(cursor, answer):
    values = ', '.join("'" + str(x) + "'" for x in answer.values())
    cursor.execute("""
                        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                        VALUES (%s);
                         """ % (values))
    cursor.execute("""
                        SELECT id FROM answer 
                        WHERE submission_time = %(submission_time)s;""",
                   {'submission_time': answer['submission_time']})

    id = cursor.fetchall()
    return id[0]['id']
@database_common.connection_handler
def get_question_by_id(cursor,id):
    cursor.execute("""
                    SELECT * FROM question
                    where id = %(id)s;
    
                    """, {'id' : id})

    question = cursor.fetchall()
    return question

@database_common.connection_handler
def list_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    """)

    questions = cursor.fetchall()

    return questions