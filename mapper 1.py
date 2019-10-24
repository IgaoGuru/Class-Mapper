import numpy as np

names = {
    0 : "João",
    1 : "Alice",
    2 : "Felipe",
    3 : "Maya"
}

num_classes = 2
num_students = len(names.keys())

classrooms = np.zeros((num_students, num_classes))

preferences = np.zeros((num_students, num_students))

preferences[0, 2] = 1
preferences[0, 3] = 1
preferences[1, 2] = 1
preferences[2, 1] = 1
preferences[3, 1] = 1

print(preferences)

populars = np.apply_along_axis(np.count_nonzero, 0, preferences)

demanders = np.apply_along_axis(np.count_nonzero, 1, preferences)