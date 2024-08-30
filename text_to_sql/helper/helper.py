import sys
import json


def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_list_as_sql(sql_file_path, query_list):
    with open(sql_file_path, 'w') as file:
        for query in query_list:
            file.write(query + '\n')  # Write each query on a new line

def save_list_as_json(json_file_path, query_list):
    # Save the list as a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(query_list, json_file, indent=4)

def print_progress_bar(iteration, total, length=40):
    progress = iteration / total
    bar = '█' * int(length * progress) + '-' * (length - int(length * progress))
    sys.stdout.write(f'\rGenerating SQL queries for 30 random questions: {round(progress*100)}%|{bar}| {iteration}/{total}')
    sys.stdout.flush()