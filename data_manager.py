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
def get_question_by_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM question
                    where id = %(id)s;
    
                    """, {'id': id})

    question = cursor.fetchall()
    return question


@database_common.connection_handler
def get_answer_by_id(cursor, id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(id)s
                    ORDER BY id;
                    """, {'id': id})

    answer = cursor.fetchall()
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
    title = question[0]['title']
    message = question[0]['message']
    image = question[0]['image']
    cursor.execute("""
                    
                    UPDATE question 
                    SET title = %(title)s,
                        message = %(message)s,
                        image = %(image)s
                    WHERE id = %(id)s;
                    """, {'id': id, 'title': title, 'message': message, 'image': image})


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
                    WHERE title  LIKE '{}'
                    OR message LIKE '{}';
                        """.format(word, word))

    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def search_in_answers(cursor, word):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE message  LIKE '%{}%';
                        """.format(word))

    answers = cursor.fetchall()
    return answers


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
def delete_comment_by_answer_id(cursor, answer_id):
    cursor.execute(""" 
                    DELETE FROM comment
                    WHERE answer_id = %s;
                    """ % (answer_id))


@database_common.connection_handler
def delete_comment_by_question_id(cursor, question_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE question_id = %s;
                    """ % (question_id))


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


@database_common.connection_handler
def get_comments_for_multiple_answers(cursor, answer_ids):
    if answer_ids != []:
        answer_id = ', '.join(answer_ids)
        cursor.execute("""
                        SELECT * FROM comment
                        WHERE answer_id IN (%s);
                        """ % (answer_id))
        comments = cursor.fetchall()
        return comments
    else:
        return []


@database_common.connection_handler
def delete_comments(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %s;
                    """ % (comment_id))


@database_common.connection_handler
def get_all_tags(cursor):
    cursor.execute("""
                    SELECT * FROM tag;
                    """)
    tags = cursor.fetchall()
    return tags


@database_common.connection_handler
def get_tags_by_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question_tag
                    WHERE question_id = %s;
                    """ % question_id)
    tags = cursor.fetchall()
    return tags


@database_common.connection_handler
def add_new_tag(cursor, new_tag):
    cursor.execute("""
                    SELECT * FROM tag
                    WHERE name = %(new_tag)s;
                    """, {'new_tag': new_tag})
    existing_tag = cursor.fetchall()
    if not existing_tag:
        cursor.execute("""
                        INSERT INTO tag (name)
                        VALUES (%(new_tag)s);
                        """, {'new_tag': new_tag})
    cursor.execute("""
                    SELECT * FROM tag
                    WHERE name = %(new_tag)s;
                    """, {'new_tag': new_tag})
    tag_ = cursor.fetchall()
    tag_id = tag_[0]['id']
    return tag_id


@database_common.connection_handler
def add_new_tag_to_question(cursor, tag_id, question_id):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id=%(question_id)s 
                    AND tag_id=%(tag_id)s;
                    """, {'question_id': question_id, 'tag_id': tag_id})
    cursor.execute("""
                    INSERT INTO question_tag (question_id, tag_id)
                    VALUES (%(question_id)s, %(tag_id)s);
                    """, {'question_id': question_id, 'tag_id': tag_id})


@database_common.connection_handler
def get_tag_id_by_name(cursor, tag_name):
    cursor.execute("""
                    SELECT id FROM tag
                    WHERE name=%(tag_name)s;
                    """, {'tag_name': tag_name})
    tag_id = cursor.fetchall()
    return tag_id[0]['id']


@database_common.connection_handler
def get_tag_names_by_tag_ids(cursor, tag_ids):
    if tag_ids != []:
        tag_id = ', '.join(tag_ids)
        cursor.execute("""
                        SELECT * FROM tag
                        WHERE id IN (%s);
                        """ % (tag_id))
        tags = cursor.fetchall()
        return tags
    else:
        return []


@database_common.connection_handler
def get_tag_name_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT tag_id FROM question_tag
                    WHERE question_id=%(question_id)s;
                    """, {'question_id': question_id})
    tag_ids_dict = cursor.fetchall()
    tag_ids = [str(tag['tag_id']) for tag in tag_ids_dict]
    tags = get_tag_names_by_tag_ids(tag_ids)
    return tags


@database_common.connection_handler
def delete_tags_by_question(cursor, question_id, tag_id):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE tag_id = %(tag_id)s 
                    AND question_id = %(question_id)s; 
                    """, {'tag_id': tag_id, 'question_id': question_id})


@database_common.connection_handler
def get_questions_for_multiple_answers(cursor, answer_ids):
    if answer_ids != []:
        answer_id = ', '.join(answer_ids)
        cursor.execute("""
                        SELECT * FROM question
                        WHERE id IN (%s);
                        """ % (answer_id))
        questions = cursor.fetchall()
        return questions
    else:
        return []

@database_common.connection_handler
def get_all_tags(cursor):
    cursor.execute("""
                    SELECT tag.name, COUNT(question_tag.question_id) AS count FROM tag
                    LEFT JOIN question_tag ON question_tag.tag_id = tag.id
                    GROUP BY tag.name;
                    """)
    tags = cursor.fetchall()
    return tags