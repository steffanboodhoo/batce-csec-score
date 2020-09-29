import config
import process_data, score_students
from pprint import pprint

def main():
    students = process_data.handle_process_csv(config.FILE_NAME)
    score_students.calculate_student_scores(students)

if __name__ == "__main__":
    main()