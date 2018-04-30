# coding=utf-8
import datetime
import os
import assign
import assign2
import assign3
import predict
from panchao.predict import linePre
Debug = False


def read_lines(file_path):
    if os.path.exists(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
    else:
        print 'file not exist: ' + file_path
        return None

def predict_vm(ecsDataPath, inputFilePath):
    # Do your work from here#
    ecs_lines = read_lines(ecsDataPath)
    input_lines = read_lines(inputFilePath)
    result = []
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result

    # 读取训练数据
    TrainData = []
    for item in ecs_lines:
        values = item.split("\t")
        # print values
        uuid = values[0]
        flavorName = values[1]
        createTime = values[2]
        TrainData.append([flavorName, createTime.split(' ')[0]])
        # print uuid,flavorName,createTime

    # 读取输入数据
    cpu = 0
    mem = 0
    ram = 0
    OptimizaType = ''
    VirtualComputer = []
    Allflavor = []
    BeginTime = datetime.datetime.strptime(input_lines[-2].split(' ')[0], '%Y-%m-%d')
    EndTime = datetime.datetime.strptime(input_lines[-1].split(' ')[0], '%Y-%m-%d')
    Time = (EndTime - BeginTime).days
    print Time

    for index, item in enumerate(input_lines):
        if index == 0:
            values = item.split(" ")
            cpu = values[0]
            mem = values[1]
            ram = values[2]
        elif index == 2:
            for i in range(index + 1, index + int(item[0]) + 1):
                flag = input_lines[i].split(' ')
                VirtualComputer.append([flag[0], flag[1], flag[2].replace('\n', '')])
                Allflavor.append(flag[0])
        if item.split('\n')[0] == "CPU" or item.split('\n')[0] == "MEM" \
                or item.split('\n')[0] == "mem" or item.split('\n')[0] == "cpu":
            OptimizaType = item.split('\n')[0]

    if Debug:
        print '预测时间间隔', Time
        print '虚拟主机类型', VirtualComputer
        print '优化类型', OptimizaType

    # 预测
    print 'VirtualComputer',VirtualComputer
    print 'TrainData',TrainData
    # pre = predict.prdict(VirtualComputer, TrainData)
    # pre = pre.pre1(VirtualComputer, TrainData, Time)
    # print 'pre1' , pre
    pre = linePre(ecsDataPath,Allflavor)
    print 'pre' , pre

    # #分配
    # ass = assign.assign(cpu, mem, OptimizaType)
    # result = ass.assign(VirtualComputer , pre)
    #
    # ass = assign2.assign2(cpu , mem , OptimizaType)
    # result = ass.assign(VirtualComputer , pre)
    #
    ass = assign3.assign3(cpu, mem, OptimizaType)
    result = ass.assign(VirtualComputer, pre)

    return result

