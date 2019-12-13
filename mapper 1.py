import numpy as np

names = {
    0 : "João",
    1 : "Alice",
    2 : "Felipe",
    3 : "Maya"
}

num_classes = 2
num_students = len(names.keys())
num_students_per_classroom = int(np.ceil(num_students/num_classes))

classrooms = np.zeros((num_students_per_classroom, num_classes)) - 1

preferences = np.zeros((num_students, num_students))

preferences[0, 2] = 1
preferences[0, 3] = 1
preferences[1, 2] = 1
preferences[2, 1] = 1
preferences[3, 1] = 1

#block: creates list of most chosen students
popularity = np.apply_along_axis(np.count_nonzero, 0, preferences)
popularity_sorted_idxs = np.argsort(popularity)[::-1]
populars = popularity_sorted_idxs[:num_classes]

#block: creates list of students who chose the least (out of the non-populars)
demand = np.apply_along_axis(np.count_nonzero, 1, preferences)
demand_sorted_idxs = np.argsort(demand)

#puts each popular into one classroom
classrooms[0, :] = populars
print(classrooms)

print("_______________________________")

on_hold = np.zeros((num_students, 3)) - 1

for student in demand_sorted_idxs:
    if student not in populars:
        demanded = np.nonzero(preferences[student,:])[0]
        print(student, demanded)

        if student in on_hold[:, 0]:
            
        for d in demanded:
            i, j = np.where(classrooms == d)
            if i.size == 0 or j.size == 0:
                print("não acho nao maluco")
                on_hold[student,:] = [d, i, j]

            print(i, j)





