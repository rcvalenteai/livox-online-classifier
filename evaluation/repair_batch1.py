import helpers.io


def get_batch_objects(filename, user_number, output_filename=None):
    raw_responses = helpers.io.load_csv(filename)[1:]
    question_responses = raw_responses[user_number::8]
    question_categories = [[question_response[2]] for question_response in question_responses]
    helpers.io.write_list_csv("scratch", output_filename, question_categories)


for i in range(8):
    get_batch_objects("./data/labeled_mturk_b1.csv", i, "question_categories_" + str(i+1) + ".csv")
