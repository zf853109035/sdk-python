# -*- coding: UTF-8 -*-
import time
from utils import *


def predict(filename_train, flavor_list):
    """
    :param filename_train: training data filename
    :param flavor_list:    flavor types need to predict
    :return:
    """
    """ Load train data """
    request_mat_train = analy_data(read_file(filename_train))       # 在此加入flavor类型约束???

    _, mu_whole, sigma_whole = feature_normalize2(request_mat_train)

    """ Split data """
    train_len = 4
    label_len = 7
    train_set, label_set = split_data(request_mat_train, train_len, label_len)

    """ Train """
    goal = 1e-4
    alpha = 0.05    # learning rate
    num_iters = 300    # max iterations

    theta_list = {}
    J_history_list = {}
    for flavor_type in flavor_list:
        theta, J_history = \
            train_one_flavor2(train_set[flavor_type], label_set[flavor_type], goal=goal, alpha=alpha, num_iters=num_iters)
        theta_list[flavor_type] = theta
        J_history_list[flavor_type] = J_history

    # # show curve convergence
    # plt.figure('Curve convergence')
    # for i, flavor_type in enumerate(flavor_list):
    #     plt.subplot(3, 5, i+1), plt.title(flavor_type)
    #     J_history = J_history_list[flavor_type]
    #     plt.plot([j for j in range(len(J_history))], J_history)
    # plt.show()

    """ Test """
    predict_list = {}
    for flavor_type in flavor_list:
        theta = theta_list[flavor_type]
        flavor_id = int(flavor_type.split('flavor')[-1]) - 1
        sample = request_mat_train[flavor_id][-train_len:]
        mu = 1.0 * sum(sample) / len(sample)
        sigma = math.sqrt(sum([(e - mu) ** 2 for e in sample]) / (len(sample) - 1))
        sample = [1, mu]
        predict = mat_multiply([sample], theta)
        predict_list[flavor_type] = int(round(predict[0][0] * label_len))

    return predict_list

def  linePre(filename_train,flavor_list):
    ans = predict(filename_train , flavor_list)
    return ans

# if __name__ == '__main__':
#     flavor_list = ['flavor1', 'flavor2', 'flavor3', 'flavor4', 'flavor5',
#                    'flavor6', 'flavor7', 'flavor8', 'flavor9', 'flavor10',
#                    'flavor11', 'flavor12', 'flavor13', 'flavor14', 'flavor15']
#
#     filename_train = '.\\data\\TrainData.txt'
#
#     ans = predict(filename_train, flavor_list)
#     print(ans)