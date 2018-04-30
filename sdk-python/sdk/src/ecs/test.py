import matplotlib.pyplot as plt
import datetime
from collections import Counter
array = []
TrainData = []
flavors = []
num = 0
lasttime = ''
nowtime = ''
with open('../../../TrainData.txt' , 'r') as lines:
    for line in lines:
        values = line.split("\t")
        flavor = values[1]
        nowtime = values[2].split(' ')[0]
        flavors.append(flavor)
        if  lasttime!=nowtime:
            num+=1
            lasttime=nowtime
        TrainData.append([flavor, num])
print(TrainData)
cnt = Counter(flavors)
temp = []
for k,v in cnt.items():
    x = []
    y = []
    num = 0
    for index in range(len(TrainData)):
        if TrainData[index][0]==k:
            num+=1
        if index==len(TrainData)-1:
            x.append(TrainData[index][1])
            y.append(num)
            break
        if TrainData[index][1]!=TrainData[index+1][1]:
            x.append(TrainData[index][1])
            y.append(num)
            num=0
    # Count = Counter(temp)
    # print(type(Count))
    # for kk,vv in Count.items():
    #     x.append(kk)
    #     y.append(vv)
    print(k)
    print(x)
    print(y)
    plt.plot(x,y)
    plt.show()

# EndTime = datetime.datetime.strptime(TrainData[-1][1] , '%Y-%m-%d')
# BeginTime = datetime.datetime.strptime(TrainData[0][1].split(' ')[0] , '%Y-%m-%d')
# length = (EndTime - BeginTime).days
# print(length)
# x = [1,2,3]
# y = [1,4,8]
# plt.plot(x,y)
# plt.show()