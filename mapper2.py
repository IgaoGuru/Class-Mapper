import numpy as np
from Oracle1 import get_hh_ss
from Oracle1 import per_student_hh_to_csv
import time

#names isnt being used right now because I dont have a list of 120 names,
#in a real life scenario, the names dictionary would be a 120 keys dic. with 120 names
names = {
    0 : "João",
    1 : "Alice",
    2 : "Felipe",
    3 : "Maya",
    4 : "Chuck Norris"
}

np.random.seed(3)
num_classes = 4
num_students = 120
num_students_per_classroom = int(np.ceil(num_students/num_classes))
num_random_preferences = 10
num_runs = 10



def choose_students(chooser, num_students, choice_per_student):
    chosen = np.random.randint(0, num_students - 1, choice_per_student)

    #keep chosing until chooser not in choser and chosen has 2 different students :)
    while chooser in chosen or chosen[0] == chosen[1]:
        chosen = np.random.randint(0, num_students - 1, choice_per_student)
    return chosen

def nothing(classroom):
    pass

def satisfier_deployer(satisfier_func, preferences):

    classrooms = random_deployer(preferences)

    for id in range(num_students):
        satisfier_func(id, classrooms, preferences)

    return classrooms

def random_deployer(preferences):

    num_students = preferences.shape[0]
    classrooms = (np.zeros((num_students_per_classroom, num_classes)) - 1).astype(int)

    randomly_allocate_students(classrooms, num_students)

    return classrooms

def student_satisfier_1(student, classrooms, preferences):
    prefs = preferences[student, :]
    stud_prefs = np.where(preferences[student, :] == 1)[0]
    stud_coord = np.where(classrooms == student)
    pref_coords = [np.where(classrooms == s) for s in stud_prefs]

    same_class = set([])
    not_same_class = set([])

    for preference in pref_coords:
        i, j = preference
        if j[0] == stud_coord[1]:
            same_class.add(classrooms[i, j][0])

    not_same_class = set(stud_prefs) - same_class
    #print(stud_prefs, same_class, not_same_class)

    #if number of preferences in my classroom is greater than the ones outside; bring the ones outside in :)
    if len(same_class) >= (len(stud_prefs) - len(same_class)):
        #chooses students that will be swapped and lists them in array
        chosen_classroom = classrooms[:, stud_coord[1]]
        chosen_classroom = chosen_classroom.reshape((chosen_classroom.shape[0],))

        to_be_swapped = np.random.choice(chosen_classroom, len(not_same_class), replace=False)
        to_be_swapped = to_be_swapped.reshape((to_be_swapped.shape[0],))

        for student_idx ,student in enumerate(to_be_swapped):
            swapper(student, stud_prefs[student_idx], classrooms)
        #print(classrooms)

    #if number of preferences in my classroom is smaller than the ones outside; put the student in the other classroom :)
    else:
        # counts number of preffered students in each classroom
        counted = np.apply_along_axis(count_pref, 0, classrooms, prefs)
        # chooses classroom with most preferences in them
        # TODO bias: will always choose leftmost classroom
        swap_classroom_idx = np.argmax(counted)
        # creates separate indices of non-preffered students

        # chooses random student from classroom to be swaped (cant be preference)
        to_be_swapped = np.random.choice(classrooms[:, swap_classroom_idx])
        while to_be_swapped in stud_prefs:
            to_be_swapped = np.random.choice(classrooms[:, swap_classroom_idx])
        # calls swapper() to swap the original student with the chosen one
        swapper(student, to_be_swapped, classrooms)
        #print(classrooms)


def count_pref(classroom, stud_pref):
    counter = 0
    for i in classroom:
        if i in stud_pref:
            counter += 1
    return counter

def swapper(student1, student2, classrooms):
    #finds students coordinates
    student1coord = np.where(classrooms == student1)
    student2coord = np.where(classrooms == student2)
    #interchanges students
    classrooms[student1coord] = student2
    classrooms[student2coord] = student1


def get_random_preferences(num_students):

    preferences = np.zeros((num_students, num_students)).astype(int)

    for i in range(num_students):
        chosen = choose_students(i, num_students, choice_per_student=4)
        preferences[i, chosen] = 1
    #ensures diagonal is all zeros
    assert(np.all(np.diagonal(preferences) == np.zeros((num_students, ))))
    #print(preferences)
    return preferences

def randomly_allocate_students(classrooms, num_students, verbose=False):
    shuffled_students = np.random.choice(np.array(range(0, num_students)), (num_students, ), False)
    str = 0
    #inserts each student in one slot in classrooms
    for student in shuffled_students:
        #sets current column
        y_axis = int(np.floor((str / classrooms.shape[0])))
        #sets current row
        x_axis = int(np.floor(str - (y_axis * classrooms.shape[0])))
        str += 1
        classrooms[x_axis, y_axis] = student
    if verbose:
        print(classrooms)



with open('hhhtocsv', 'w') as csv:

    for i in range(num_random_preferences):
        random_preferences = get_random_preferences(num_students)

        for j in range(num_runs):

            #runs my algorithm
            classroom = satisfier_deployer(student_satisfier_1, random_preferences)

            happiness, _ = get_hh_ss(classroom, random_preferences)

            csv.write(str(happiness) + ",")

            #runs random alg.
            classroom = random_deployer(random_preferences)

            happiness, _ = get_hh_ss(classroom, random_preferences)

            if j < (num_runs - 1):
                csv.write(str(happiness) + ",")
            else:
                csv.write(str(happiness))
            # print(f'{j / num_runs:.2f}%', end='\n')

        csv.write('\n')
        print(f'{100*(i+1)/num_random_preferences:.0f}%', end = '\n')