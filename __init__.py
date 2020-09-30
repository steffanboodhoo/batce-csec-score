import config
import process_data, score_students, read_details
from pprint import pprint
import csv

def main():
    students = process_data.handle_process_csv(config.FILE_NAME)
    [application_code_index_dict, email_index_dict] = process_data.create_mapping_dict(students)
    students = score_students.calculate_student_scores(students)

    student_meta_records = read_details.handle_read_student_meta('student_details.csv')
    students = merge_student_meta_and_student(students, student_meta_records, application_code_index_dict, email_index_dict)
    for cape_subject in config.CAPE_SCORING:
        handle_generate_subject_file(students, cape_subject)
    create_general_score_file(students)


def merge_student_meta_and_student(students, student_meta_records, application_code_index_dict, email_index_dict):
    for student_meta in student_meta_records:
        # print(student_meta)
        index = -1
        if student_meta['EMAIL_ADDRESS']!='' and student_meta['EMAIL_ADDRESS'] in email_index_dict:
            index = email_index_dict[student_meta['EMAIL_ADDRESS']]
        elif student_meta['APPLICATION_CODE']!='' and student_meta['APPLICATION_CODE'] in application_code_index_dict:
            index = application_code_index_dict[student_meta['APPLICATION_CODE']]
        
        if index != -1:
            students[index]['SCHOOL'] = student_meta['SCHOOL']
        
    return students

def handle_generate_subject_file(students, cape_subject):
    filename = '%s_scores.csv'%(cape_subject)
    headers = ['EMAIL_ADDRESS','APPLICATION_CODE','FIRST_NAME', 'LAST_NAME', 'SCHOOL', 'SUBJECT', 'SCORE', 'CHOICE']
    with open(filename, 'w', newline='\n') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=headers)    
        writer.writeheader()
        for student in students:
            choice = -1
            if cape_subject in student['first_choices']:
                choice = 1
            elif cape_subject in student['second_choices']:
                choice = 2

            if choice != -1:
                data_obj = create_student_write_obj(student, choice, cape_subject)
                data_obj['CHOICE'] = choice
                writer.writerow(data_obj)
                # write to file
    out_file.close()


def create_student_write_obj(student, choice, cape_subject):
    choice_key = 'first_choices_grades' if choice == 1 else 'second_choices_grades'
    # pprint(student)
    # print(choice_key)
    data_obj = {
        'EMAIL_ADDRESS': student['EMAIL_ADDRESS'],
        'APPLICATION_CODE': student['APPLICATION_CODE'],
        'FIRST_NAME': student['FIRST_NAME'],
        'LAST_NAME': student['LAST_NAME'],
        'SCHOOL': student['SCHOOL'],
        'SUBJECT': cape_subject,
        'SCORE': student[choice_key][cape_subject]['score']
    }
    return data_obj

def create_general_score_file(students):
    headers = ['EMAIL_ADDRESS', 'APPLICATION_CODE', 'FIRST_NAME', 'LAST_NAME', 'SCHOOL', 'first_choices_grades_total', 'second_choices_grades_total', 'GENERAL_SCORE']
    filename = 'general_scores.csv'
    with open(filename, 'w', newline='\n') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=headers)    
        writer.writeheader()
        for student in students:
            data_obj = create_general_data_obj(student)
            writer.writerow(data_obj)
    out_file.close()


def create_general_data_obj(student):
    data_obj = {
        'EMAIL_ADDRESS': student['EMAIL_ADDRESS'],
        'APPLICATION_CODE': student['APPLICATION_CODE'],
        'FIRST_NAME': student['FIRST_NAME'],
        'LAST_NAME': student['LAST_NAME'],
        'SCHOOL': student['SCHOOL'],
        'first_choices_grades_total':student['first_choices_grades_total'],
        'second_choices_grades_total':student['second_choices_grades_total'],
        'GENERAL_SCORE': student['grades']['GENERAL_SCORE']['score']
    }
    return data_obj

if __name__ == "__main__":
    main()


# {'APPLICATION_CODE': 'e7e502b189',
#  'FIRST_NAME': 'Zahra',
#  'LAST_NAME': 'Gaskin',
#  'first_choices': ['ECONOMICS', 'PURE MATHEMATICS', 'APPLIED MATHEMATICS'],
#  'first_choices_grades': {'APPLIED MATHEMATICS': {'score': 43},
#                           'ECONOMICS': {'score': 31},
#                           'PURE MATHEMATICS': {'score': 40}},
#  'first_choices_grades_total': 114,
#  'grades': {'ADDITIONAL MATHEMATICS': {'grade_string': 'I', 'score': 3},
#             'ECONOMICS': {'grade_string': 'II', 'score': 2},
#             'ENGLISH A': {'grade_string': 'I', 'score': 3},
#             'ENGLISH B': {'grade_string': 'I', 'score': 3},
#             'FRENCH': {'grade_string': 'I', 'score': 3},
#             'GENERAL_SCORE': {'score': 25},
#             'MATHEMATICS': {'grade_string': 'I', 'score': 3},
#             'PHYSICAL EDUCATION AND SPORT': {'grade_string': 'II', 'score': 2},
#             'PRINCIPLES OF ACCOUNTS': {'grade_string': 'I', 'score': 3},
#             'SPANISH': {'grade_string': 'I', 'score': 3}},
#  'second_choices': ['PURE MATHEMATICS', 'ENTREPRENEURSHIP', 'SPANISH'],
#  'second_choices_grades': {'ENTREPRENEURSHIP': {'score': 25},
#                            'PURE MATHEMATICS': {'score': 40},
#                            'SPANISH': {'score': 34}},
#  'second_choices_grades_total': 99}
