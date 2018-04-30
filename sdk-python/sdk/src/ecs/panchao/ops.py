# -*- coding: UTF-8 -*-
import math


# 矩阵相乘
def mat_multiply(A, B):
    col_A = len(A[0])
    row_B = len(B)
    if col_A != row_B:
        print('Error: Inner matrix dimensions must agree.')
        exit(-1)
    else:
        return [[sum(x * y for x, y in zip(a, b)) for b in zip(*B)] for a in A]


# 矩阵点乘
def mat_dot(A, B):
    row_A = len(A)
    col_A = len(A[0])
    row_B = len(B)
    col_B = len(B[0])

    if col_B == 1:  # 列向量
        B = [[x[0] for i in range(len(A[0]))] for x in B]
        col_B = col_A
    elif col_A == 1:
        A = [[x[0] for i in range(len(B[0]))] for x in A]
        col_A = col_B

    if row_A != row_B or col_A != col_B:
        print('Error: Two matrix dimensions must same.')
        exit(-1)
    else:
        return [[x * y for x, y in zip(a, b)] for a, b in zip(A, B)]


# 矩阵幂
def mat_pow(A, n):
    return [[x ** n for x in a] for a in A]


# 矩阵数乘
def mat_mul(A, n):
    return [[x * n for x in a] for a in A]


# 矩阵求和
def mat_sum(A, axis=0):
    if axis == 0:   # 全部求和
        return sum([sum(a) for a in A])
    elif axis == 1:     # 按行求和
        return [[sum(a)] for a in A]
    elif axis == 2:     # 按列求和
        return [[sum(a) for a in zip(*A)]]


# 矩阵相加
def mat_add(A, B):
    row_A = len(A)
    col_A = len(A[0])
    row_B = len(B)
    col_B = len(B[0])
    if row_A != row_B or col_A != col_B:
        print('Add Error: Two matrix dimensions must same.')
        exit(-1)
    else:
        return [[x + y for x, y in zip(a, b)] for a, b in zip(A, B)]


# 矩阵转置
def mat_transpose(A):
    return map(list, zip(*A))


# 矩阵方差
def mat_std(A, mu, axis=1):
    if axis == 1:
        std = mat_pow([mat_add([a], mat_mul(mu, -1))[0] for a in A], 2)
        std = mat_mul(mat_sum(std, axis=2), 1.0 / (len(A) - 1))
        return [[math.sqrt(x) for x in std[0]]]
    elif axis == 2:
        std = mat_pow([[e - u[0] for e in a] for a, u in zip(A, mu)], 2)
        std = mat_mul(mat_sum(std, axis=1), 1.0 / (len(A) - 1))
        return [[math.sqrt(x[0])] for x in std]
