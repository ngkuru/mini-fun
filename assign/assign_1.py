import numpy as np
import scipy.optimize

people = np.array([[3, 4, 8, 6, 6], #1
                   [1, 1, 7, 8, 0], #2
                   [2, 7, 0, 2, 3], #3
                   [0, 1, 8, 4, 6], #4
                   [0, 0, 0, 0, 0], #5
                   [7, 9, 5, 9, 1], #6
                   [4, 9, 8, 9, 3], #7
                   [2, 0, 1, 8, 3], #8
                   [3, 6, 7, 3, 3], #9
                   [6, 6, 0, 0, 3], #10
                   [1, 5, 8, 1, 5], #11
                   [9, 5, 9, 6, 5], #12
                   [1, 9, 1, 0, 6], #13
                   [5, 0, 0, 4, 7], #14
                   [3, 6, 7, 9, 5], #15
                   [7, 3, 9, 8, 5], #16
                   [8, 7, 1, 7, 7], #17
                   [1, 3, 6, 6, 4], #18
                   [4, 3, 2, 9, 8], #19
                   [5, 2, 8, 7, 8]]) #20

assignment = np.array([people.T[0],
                       people.T[0] * 2,
                       people.T[0] * 3,
                       people.T[1],
                       people.T[1] * 2,
                       people.T[1] * 3,
                       people.T[2],
                       people.T[2] * 2,
                       people.T[2] * 3,
                       people.T[3],
                       people.T[3] * 2,
                       people.T[3] * 3,
                       people.T[4],
                       people.T[4] * 2,
                       people.T[4] * 3])

soln = scipy.optimize.linear_sum_assignment(assignment, True)
print(soln[1] + 1)
print(assignment[soln])
print(sum(assignment[soln]))

# def new():
#     for i in range(5):
#         new = np.array([people.T[i],
#                         people.T[i] * 2,
#                         people.T[i] * 3])
#         new_asn = np.concatenate([assignment, new])
#         soln = scipy.optimize.linear_sum_assignment(new_asn, True)
#         print(f"{i} sum {sum(new_asn[soln])}")
#
# new()
