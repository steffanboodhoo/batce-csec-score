from config import OTHER_FILE_DETAILS_MAPPING

def handle_read_student_meta(file_path):
    f =  open(file_path, 'r')

    headers = f.readline()
    line = f.readline()
    student_meta_records = []
    while(line):
        student_meta_records.append(create_student_meta(line))
        line = f.readline()
        # return
    return student_meta_records

def create_student_meta(data_str):
    student_meta = {}
    data_arr = data_str.split(',')
    for i in range(len(data_arr)): # i => col index
        if i in OTHER_FILE_DETAILS_MAPPING:
            student_meta[OTHER_FILE_DETAILS_MAPPING[i]] = data_arr[i]
    # print(student_meta)
    student_meta['EMAIL_ADDRESS'] = student_meta['EMAIL_ADDRESS'].lower()

    return student_meta