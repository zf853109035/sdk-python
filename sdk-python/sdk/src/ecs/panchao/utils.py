# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta
# import matplotlib.pyplot as plt
import math
from ops import *

LAMBDA = 1e-3


# 从文件中读取record_list
def read_file(filename):
    """
    :param filename: txt文件路径
    :return: 列表, [flavor型号, 申请日期]
    """
    record_list = []
    with open(filename) as lines:
        for line in lines:
            items = line.strip().split('\t')
            flavor = int(items[1].split('flavor')[-1])
            date = datetime.strptime(items[2].split(' ')[0], '%Y-%m-%d')
            record_list.append([flavor, date])

    return record_list


# 从data_list中抽取flavor申请频率
def analy_data(record_list):
    """
    :param record_list: 记录列表, [flavor, date]
    :return: 二维列表 [flavor][date] = 请求次数
    """
    first_day = record_list[0][1]   # 开始日期
    last_day = record_list[-1][1]   # 结束日期
    time_span = (last_day - first_day).days + 1
    date_list = [first_day + timedelta(i) for i in range(time_span)]

    # 只关心flavor1 ~ flavor15
    request_mat = [[0 for i in range(len(date_list))] for j in range(15)]    # mat[flavor][date] = 请求次数
    for flavor, day in record_list:
        if 1 <= flavor <= 15:
            request_mat[flavor - 1][date_list.index(day)] += 1

    return request_mat


# # 可视化数据(各个flavor的申请变化)
# def visulize_data(request_mat, win_name, mu=None, sigma=None):
#     """
#     :param request_mat:
#     :param win_name: 窗口标题
#     :return: None
#     """
#     plt.figure(win_name)
#     for i in range(15):
#         plt.subplot(5, 3, i + 1)
#         plt.title('sample{0}'.format(i + 1))
#         plt.plot([d for d in range(len(request_mat[0]))], request_mat[i])
#         if mu is not None and sigma is not None:
#             plt.hlines(mu[i][0], 0, len(request_mat[0]), 'g', '--')
#             plt.hlines(mu[i][0] + 2 * sigma[i][0], 0, len(request_mat[0]), 'r', '--')
#     plt.show()


# 代价函数
def compute_cost(X, y, theta):
    m = len(y)      # 训练样本数
    J = mat_add(mat_multiply(X, theta), mat_mul(y, -1))
    J = mat_sum(mat_pow(J, 2))
    J = 1.0 / (2 * m) * J
    return J


# 梯度下降
def gradient_descent(X, y, goal, alpha, num_iters):
    m = len(y)      # 训练样本数
    theta = [[0] for i in range(len(X[0]))]
    J_history = []

    for iter in range(num_iters):
        temp = mat_add(mat_multiply(X, theta), mat_mul(y, -1))
        temp = mat_mul(mat_transpose(mat_sum(mat_dot(temp, X), axis=2)), alpha / m)
        theta = mat_add(theta, mat_mul(temp, -1))

        cost = compute_cost(X, y, theta)
        J_history.append(cost)
        if cost <= goal:
            break

    return theta, J_history


# 特征归一化(按天)
def feature_normalize(X):
    mu = mat_mul(mat_sum(X, axis=2), 1.0 / len(X))
    sigma = mat_std(X, mu)
    X_norm = [mat_add([x], mat_mul(mu, -1))[0] for x in X]
    X_norm = [[a / (b + LAMBDA) for a, b in zip(x, sigma[0])] for x in X_norm]    # 防止σ为0, 分母加上1e-3

    return X_norm, mu, sigma


# 特征归一化(按flavor)
def feature_normalize2(X):
    mu = mat_mul(mat_sum(X, axis=1), 1.0 / len(X[0]))
    sigma = mat_std(X, mu, axis=2)
    X_norm = [[e - u[0] for e in x] for x, u in zip(X, mu)]
    X_norm = [[e / (s[0] + LAMBDA) for e in x] for x, s in zip(X_norm, sigma)]    # 防止σ为0, 分母加上1e-3

    return X_norm, mu, sigma


# 范围修剪
def feature_clip(X, mu, sigma, axis=1):
    threshold = mat_add(mu, mat_mul(sigma, 2))  # μ ± 2σ
    if axis == 1:
        return [[t if e > t else e for e, t, u in zip(x, threshold[0], mu[0])] for x in X]
    elif axis == 2:
        return [[t[0] if e > t[0] else e for e in x] for x, t, u in zip(X, threshold, mu)]


# 分割数据集
def split_data(X, train_len, label_len):
    train_set = {}
    label_set = {}
    day_nums = len(X[0])
    for vm_type, flavor in enumerate(X):
        one_train = []
        one_label = []
        key = 'flavor' + str(vm_type + 1)
        for i in range(day_nums - train_len - label_len + 1):
            one_train.append(flavor[i: i+train_len])
            one_label.append(flavor[i+train_len: i+train_len+label_len])

        train_set[key] = one_train
        label_set[key] = one_label

    return train_set, label_set


# 训练一种flavor
def train_one_flavor(train_set, label_set, goal=1e-3, alpha=0.1, num_iters=1000):
    # normalize train set
    X = train_set
    X, mu, sigma = feature_normalize(X)
    X = feature_clip(X, mu, sigma)
    Y = label_set

    # S_t = theta_0 + theta_1 * x_1 + theta_2 * x_2 + ... + theta_n * x_n
    for x in X:
        x.insert(0, 1)

    theta, J_history = gradient_descent(X, Y, goal, alpha, num_iters)

    return theta, J_history, mu, sigma


# 训练一种flavor
def train_one_flavor2(train_set, label_set, goal=1e-3, alpha=0.1, num_iters=1000):
    # normalize train set
    _, X, sigma = feature_normalize2(train_set)
    _, Y, _ = feature_normalize2(label_set)

    # S_t = theta_0 + theta_1 * x_1 + theta_2 * x_2 + ... + theta_n * x_n
    for x, s in zip(X, sigma):
        x.insert(0, 1)
        # x.insert(-1, s[0])

    theta, J_history = gradient_descent(X, Y, goal, alpha, num_iters)

    return theta, J_history


# 预测一种flavor的序列
def predict_one_flavor(X, theta, days, train_len, mu=None, sigma=None):
    predict_seq = []

    for i in range(days):
        seq = X[-train_len:]
        if mu is not None and sigma is not None:
            if type(mu) == list:
                threshold = mat_add(mu, mat_mul(sigma, 2))
                seq = [x - u for x, u in zip(seq, mu[0])]
                seq = [x / (s + LAMBDA) for x, s in zip(seq, sigma[0])]
                seq = [t if e > t else e for e, t, u in zip(seq, threshold[0], mu[0])]
            elif type(mu) == float:
                seq = [(x - mu) / sigma for x in seq]
        seq.insert(0, 1)
        pred = mat_multiply([seq], theta)[0][0]
        predict_seq.append(pred)
        X.append(pred)

    return predict_seq


# 计算预测得分
def compute_predict_score(res):
    N = len(res)
    sum1 = 0
    sum2 = 0
    sum3 = 0
    for y, y_ in res:
        y, y_ = round(y), round(y_)
        sum1 += (y - y_) ** 2
        sum2 += y ** 2
        sum3 += y_ ** 2

    return 1 - math.sqrt(1.0 / N * sum1) / (math.sqrt(1.0 / N * sum2) + math.sqrt(1.0 / N * sum3))
