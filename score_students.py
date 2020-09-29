from pprint import pprint
from config import CAPE_SCORING

def calculate_student_scores(students):
    for i in range(len(students)):
        #calculate general csec based score
        students[i] = calculate_general_score(students[i])

        #calculate first_choice score
        students[i] = calculate_cape_score(students[i], 'first_choices')    
        students[i] = calculate_cape_score(students[i], 'second_choices')    
        #calculate second_choice scores
        # students['second_choice_scores'] = {}
        pprint(students[i])
        # return

    
def calculate_general_score(student):
    score = 0
    for csec_subj in student['grades']:
        score += student['grades'][csec_subj]['score']
    student['grades']['GENERAL_SCORE'] = {'score':score}
    return student

def calculate_cape_score(student, choices_key):
    cape_choices_key = '%s_grades'%(choices_key)
    student[cape_choices_key] = {}
    cape_subjects = student[choices_key]
    i, L, cape_subject_score_total = 0, len(cape_subjects), 0 # in case they selected 4...
    while(i<L and i<3):
        cape_subj = cape_subjects[i]
        cape_subject_score = 0
        
        for csec_subj in CAPE_SCORING[cape_subj]:
            if csec_subj in student['grades']:
                # print(CAPE_SCORING[cape_subj])
                # print(student['grades'])
                # print(cape_subj)
                csec_subj_score = CAPE_SCORING[cape_subj][csec_subj] * student['grades'][csec_subj]['score']
                cape_subject_score += csec_subj_score

        student[cape_choices_key][cape_subj] = {'score':cape_subject_score}
        cape_subject_score_total += cape_subject_score
        i+=1
    student['%s_total'%cape_choices_key] = cape_subject_score_total
    return student
    

