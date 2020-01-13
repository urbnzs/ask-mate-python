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
    values = ', '.join("'" + str(x) + "'" for x in question.values())
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%s);
                     """ % (values))
    cursor.execute("""
                    SELECT id FROM question 
                    WHERE submission_time = %(submission_time)s;""", {'submission_time': question['submission_time']})

    id = cursor.fetchall()
    print(id[0][1])
    return id[0][1]