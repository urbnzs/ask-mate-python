import csv
import database_common

def get_all_data(filename):
    data = []
    reader = csv.DictReader(open(filename))
    for line in reader:
        data.append(line)
    return data


def write_data(filename, updated_data):
    f = open(filename, "w")
    if filename == 'sample_data/question.csv':
        field_names=["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
    else:
        field_names=["id", "submission_time", "vote_number", "question_id", "message", "image"]

    writer = csv.DictWriter(
        f, fieldnames= field_names)
    writer.writeheader()
    for line in updated_data:
        writer.writerow(line)
    f.close()

@database_common.connection_handler
def add_new_question(cursor, question):
    values = "(question['submission_time'], question['view_number'], question['vote_number'], question['title'], question['message'], question['images'])"

    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES %(values)s;
                     """, {'values': values})

    id = cursor.lastrowid
    return id