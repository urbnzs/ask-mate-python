import csv

def get_all_data(filename, ):
    with open(filename) as file:
        file_reader = csv.DictReader(file, delimiter=',')
        datalist = []
        for row in file_reader:
            datalist.append([row['id'], row['title'], row['user_story'], row['acceptance_criteria'],
                                        row['business_value'], row['estimation'], row['status']])
    return datalist