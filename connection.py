def sort_questions(data):
    data.sort(key=lambda x: x[1], reverse= True)

    return data
