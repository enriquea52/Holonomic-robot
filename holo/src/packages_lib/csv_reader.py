import csv
def map_getter(map):
    obstacles=[]
    with open(map) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
                obstacles.append([int(row[0]),int(row[1]),int(row[2]),int(row[3])])
                line_count += 1
    return obstacles



