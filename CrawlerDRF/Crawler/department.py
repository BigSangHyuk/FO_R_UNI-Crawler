import csv

def get_department():
    
    csv_path = 'department.csv'
    department = []

    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        for row in csv_reader:
            code = row[1].strip()
            number = row[2].strip()
            department.append([code, number])
            
    return department