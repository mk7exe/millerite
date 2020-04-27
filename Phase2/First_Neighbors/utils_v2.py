import csv


def read_csv(filename):
    with open(filename, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
        list_int = [list(map(int, x)) for x in list_of_rows]
    return list_int


def read_struct_type(filename):
    content = []
    with open(filename) as f:
        for line in f:
            temp = line.split()
            content.append(int(temp[1]))
    return content
