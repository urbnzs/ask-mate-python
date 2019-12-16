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
    with open(filename, mode='w') as file:
        file.writelines(titles.join(','))
        file.write('\n')
        for item in updated_data:
            file.writelines(item.join(','))
            file.write('\n')


l = get_all_data('sample_data/answer.csv', answers_titles)
l.append(['0', '1493398154', '4', '0', 'You need to use brackets: my_list = []', ''])
print(l)
write_data('sample_data/answer.csv', l, answers_titles)