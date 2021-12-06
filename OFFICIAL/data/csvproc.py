import csv
list = []


with open('game7.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    quarter = 1

    for row in csv_reader:
        if line_count == 0:
            list.append(["time_remaining", "Harvard", "Yale"])
            # print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:

            bool1 = False

            try:
                bool1 = (int(row[0]) > quarter)
            except:
                pass

            if(bool1):
                quarter = int(row[0])
            
            time = str(row[1])
            a = time.split(":")
            # print(a)
            # print(quarter)
            print(f'\t{((4-quarter)*15 + (float(a[0]) + float(a[1])/60))} seconds left when score is {row[4]} vs {row[5]}.')
            line_count += 1
            list.append([((4-quarter)*15 + (float(a[0]) + float(a[1])/60)), int(row[4]), int(row[5])])


    with open("cleangame7.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(list)


    # print(f'Processed {line_count} lines.')
    # print(list)