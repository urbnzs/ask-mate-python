import csv

answers_titles = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

def get_all_data(filename, titles):
    with open(filename) as file:
        file_reader = csv.DictReader(file, delimiter=',')
        datalist = []
        for row in file_reader:
            data = []
            for title in titles:
                data.append(row[title])
            datalist.append(data)
    return datalist

def write_data(filename, updated_data, titles):
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(titles)

        for line in updated_data:
            writer.writerow(line)

