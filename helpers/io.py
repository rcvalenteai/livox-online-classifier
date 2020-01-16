import csv
import os


def write_list_csv(output_folder, filename, rows):
    output_path = "./" + output_folder + "/"
    filename = output_path + filename
    #print(filename)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(filename, 'w', newline='', encoding='utf-8') as out:
        csv_cout = csv.writer(out)
        for row in rows:
            csv_cout.writerow(row)


# load a csv into a list
def load_csv(filename):
    loaded_csv = list()
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            loaded_csv.append(row)
    return loaded_csv


def query(db, stmt, params=()):
    """
    this function pulls the stmt from the database and returns a list of rows
    :param db: database for query to be executed on
    :type db: MySQLDB
    :param stmt: SQL statement to be executed on database
    :type stmt: str
    :param params: parameters to be put into SQL statement
    :type params: tuple
    :return: returns the query results in a tuple with each row being an element in the overall tuple
    :rtype: tuple
    """
    cur = db.insert(stmt, params)
    results = cur.fetchall()
    return results
