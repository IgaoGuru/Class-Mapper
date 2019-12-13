import numpy as np

#this is the oracle for the class mapper algorithms.
#this algorithms determines the happiness and sadness of a given classroom map.
#happiness is defined as the sum of all satisfied preferences.
#sadness is defined as the sum of all unsatisfied preferences.

def get_happiness(classroom_map, preferences):

    happiness = 0
    sadness = 0

    num_students = preferences.shape[0]

    for student in range(num_students):
        stud_coord = np.where(classroom_map == student)

        #defines list of student preferences
        stud_prefs = np.where(preferences[student, :] == 1)[0]

        print(student, stud_prefs)

        for preference in stud_prefs:
            if preference in classroom_map[:, stud_coord[1]]:
                happiness += 1
            else:
                sadness += 1
    return happiness, sadness