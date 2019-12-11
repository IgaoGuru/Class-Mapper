import numpy as np

names = {
    0 : "João",
    1 : "Alice",
    2 : "Felipe",
    3 : "Maya",
    4 : "Chuck Norris"
}

np.random.seed(0)
num_classes = 2
num_students = len(names.keys())
num_students_per_classroom = int(np.ceil(num_students/num_classes))

classrooms = (np.zeros((num_students_per_classroom, num_classes)) - 1).astype(int)
class_y = classrooms.shape[1]
class_x = classrooms.shape[0]

def choose_students(chooser, num_students):
    chosen = np.random.randint(0, num_students - 1, 2)

    #keep chosing until chooser not in choser and chosen has 2 different students :)
    while chooser in chosen or chosen[0] == chosen[1]:
        chosen = np.random.randint(0, num_students - 1, 2)
    return chosen

def nothing(classroom):
    pass

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
    print(stud_prefs, same_class, not_same_class)

    #if number of preferences in my classroom is greater than the ones outside; bring the ones outside in :)
    if len(same_class) >= (len(stud_prefs) - len(same_class)):
        #chooses students that will be swapped and lists them in array
        chosen_classroom = classrooms[:, stud_coord[1]]
        chosen_classroom = chosen_classroom.reshape((chosen_classroom.shape[0],))

        to_be_swapped = np.random.choice(chosen_classroom, len(not_same_class), replace=False)
        to_be_swapped = to_be_swapped.reshape((to_be_swapped.shape[0],))

        for student_idx ,student in enumerate(to_be_swapped):
            swapper(student, stud_prefs[student_idx], classrooms)
        print(classrooms)

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
        print(classrooms)


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
        chosen = choose_students(i, num_students)
        preferences[i, chosen] = 1
    #ensures diagonal is all zeros
    assert(np.all(np.diagonal(preferences) == np.zeros((num_students, ))))
    print(preferences)
    return preferences

shuffled_students = np.random.choice(np.array(range(0, num_students)), (num_students, ), False)
print(shuffled_students)
str = 0
#inserts each student in one slot in classrooms
for student in shuffled_students:
    #sets current column
    y_axis = int(np.floor((str / class_x)))
    #sets current row
    x_axis = int(np.floor(str - (y_axis * class_x)))
    str += 1
    classrooms[x_axis, y_axis] = student

print(classrooms)

#preferences = get_random_preferences(num_students)

preferences = np.zeros((num_students, num_students)).astype(int)
preferences[0, 1] = 1
preferences[0, 2] = 1
preferences[1, 0] = 1
preferences[1, 2] = 1
preferences[2, 0] = 1
preferences[2, 1] = 1
preferences[3, 4] = 1
preferences[3, 1] = 1
preferences[4, 3] = 1

for id in names.keys():
    student_satisfier_1(id, classrooms, preferences)

print(classrooms)