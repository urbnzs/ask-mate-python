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
def get_answer_by_id(cursor, id):
    print(id)
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(id)s
                    ORDER BY id;
                    """, {'id': id})

    answer = cursor.fetchall()
    print(answer)
    return answer


@database_common.connection_handler
def list_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY id;
                    """)

    questions = cursor.fetchall()

    return questions

@database_common.connection_handler
def edit_question(cursor, id, question):
    print(question)
    title = question[0]['title']
    message = question[0]['message']
    image = question[0]['image']
    cursor.execute("""
                    
                    UPDATE question 
                    SET title = %(title)s,
                        message = %(message)s,
                        image = %(image)s
                    WHERE id = %(id)s;
                    """, {'id': id, 'title' : title, 'message': message, 'image': image})


@database_common.connection_handler
def edit_answer(cursor, id, answer):


    message = answer[0]['message']
    image = answer[0]['image']
    cursor.execute("""

                    UPDATE answer
                    SET message = %(message)s,
                        image = %(image)s
                    WHERE id = %(id)s;
                    """, {'id': id, 'message': message, 'image': image})

@database_common.connection_handler
def get_last_five(cursor):
    cursor.execute("""
                    SELECT * FROM question order by submission_time desc LIMIT 5;
                    """)

    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def search(cursor, word):
    cursor.execute(""" 
                    SELECT * FROM question
                    WHERE title  LIKE '%{}%'
                    OR message LIKE '%{}%';
                        """.format(word,word))

    questions = cursor.fetchall()
    print(questions)
    return questions

@database_common.connection_handler
def add_comment_to_question(cursor, comment):
    values = ', '.join("'" + str(x) + "'" for x in comment.values())
    cursor.execute("""
                          INSERT INTO comment (question_id, message, submission_time, edited_count)
                          VALUES (%s);
                           """ % (values))

@database_common.connection_handler
def get_comment_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id = %s;
                    """ % (question_id))
    comments = cursor.fetchall()
    return comments

@database_common.connection_handler
def add_comment_to_answer(cursor, comment):
    values = ', '.join("'" + str(x) + "'" for x in comment.values())
    cursor.execute("""
                          INSERT INTO comment (answer_id, message, submission_time, edited_count)
                          VALUES (%s);
                           """ % (values))

@database_common.connection_handler
def edit_comments(cursor, comment_id, comment):
    cursor.execute("""
                    UPDATE comment
                    SET message=%(message)s, submission_time=%(submission_time)s, edited_count=%(edited_count)s
                    WHERE id = %(comment_id)s; 
                    """, {'message': comment['message'], 'submission_time': comment['submission_time'],
                          'edited_count': comment['edited_count'], 'comment_id': comment_id})

@database_common.connection_handler
def get_comment_by_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE id = %s;
                    """ % (id))
    comments = cursor.fetchall()
    return comments