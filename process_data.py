from config import CSEC_MAPPING, DETAILS_MAPPING, GRADE_SCORE
from pprint import pprint

def handle_process_csv(file_path):
    f =  open(file_path, 'r')

    headers = f.readline()
    line = f.readline()
    students = []
    while(line):
        students.append(create_student(line))
        line = f.readline()
        # return
    pprint(students)

def create_student(data_str):
    data_arr = data_str.split(',')
    student = {'grades':{}}

    for i in range(len(data_arr)): # i => col index
        if i in DETAILS_MAPPING:
            student[DETAILS_MAPPING[i]] = data_arr[i]
        elif (i in CSEC_MAPPING and data_arr[i]!=''):
            score = GRADE_SCORE[data_arr[i]] if data_arr[i] in GRADE_SCORE else 0
            student['grades'][CSEC_MAPPING[i]] = {'grade_string':data_arr[i], 'score': score}
    return student

if __name__ == "__main__":
    handle_process_csv('sample.csv')

# 1 = 3
# 2 = 2
# 3 = 1


