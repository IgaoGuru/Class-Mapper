import numpy as np

#this is the oracle for the class mapper algorithms.
#this algorithms determines the Happiness and Sadness of a given classroom map.
#Happiness is defined as the sum of all satisfied preferences.
#hh is abbreviated as "hh"
#Sadness is defined as the sum of all unsatisfied preferences.
#Sadness is abbreviated as "ss"

def get_hh_ss(classroom_map, preferences):

    hh = 0
    ss = 0

    num_students = preferences.shape[0]

    for student in range(num_students):
        stud_coord = np.where(classroom_map == student)

        #defines list of student preferences
        stud_prefs = np.where(preferences[student, :] == 1)[0]

        #print(student, stud_prefs)

        for preference in stud_prefs:
            if preference in classroom_map[:, stud_coord[1]]:
                hh += 1
            else:
                ss += 1
    return hh, ss

def per_student_hh_to_csv(classroom_map, preferences):

    num_students = preferences.shape[0]

    with open('hhhtocsv', 'w+') as csv:
        for student in range(num_students):
            hh = 0
            stud_coord = np.where(classroom_map == student)

            # defines list of student preferences
            stud_prefs = np.where(preferences[student, :] == 1)[0]

            for preference in stud_prefs:
                if preference in classroom_map[:, stud_coord[1]]:
                    hh += 1

            if student < (num_students - 1):
                csv.write('{}, '.format(hh))
            else:
                csv.write('{}'.format(hh))



