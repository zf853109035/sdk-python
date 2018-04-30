# coding=utf-8
import datetime


class prdict:
    input_txt = ''
    train_txt = ''
    abnormal = ['2016-02-07', '2016-02-08', '2016-02-22', '2016-04-02', '2016-04-03', '2016-04-04']

    def __init__(self, train_txt, input_txt):
        self.input_txt = input_txt
        self.train_txt = train_txt
        # 测试训练数据时间节点
        # for i in range(1,32):
        #     for j in range(1,3):
        #         if i<10:
        #             day = '0'+str(i)
        #         else:
        #             day = str(i)
        #         if j<10:
        #             month = '0'+str(j)
        #         else:
        #             month = str(j)
        #         self.abnormal.append('2016-'+month+'-'+day)
        # print self.abnormal

    def DelAbnormal(self, temp, sum):
        ave = float(sum) / len(temp)
        sum = 0
        length = 0
        for i in range(len(temp)):
            if temp[i] > ave - 3 and temp[i] < ave + 3:
                sum += temp[i]
                length += 1
        print ave, sum, length
        return float(sum) / length

    def pre1(self, input_txt, train_txt, time):
        res_vm = {}
        print 'input_txt:', input_txt
        print 'train_txt:', train_txt
        sum = 0

        lasttime = ''
        nowtime = ''
        Mincpu_flavor = ''
        Mincpu_flavor2 = ''
        Mincpu = 100000
        for flavor_input, cpu, mem in input_txt:
            res_vm.setdefault(flavor_input, 0)
            sum = 0
            temp = []
            s = 0
            for index, item in enumerate(train_txt):
                flavor_train = item[0]
                date = item[1]
                nowtime = date
                if flavor_input == flavor_train:
                    s += 1
                if index == len(train_txt) - 1:
                    if s != 0:
                        temp.append(s)
                        sum += s
                    break
                if lasttime != nowtime:
                    lasttime = nowtime
                    if s != 0:
                        temp.append(s)
                        sum += s
                        s = 0
                        if int(cpu) < Mincpu:
                            Mincpu_flavor = flavor_input
                            if Mincpu_flavor2 == '':
                                Mincpu_flavor2 = flavor_input
                            Mincpu = int(cpu)
                        if int(cpu) == Mincpu and Mincpu_flavor2 == Mincpu_flavor:
                            Mincpu_flavor2 = flavor_input
            ave = float(sum) / len(temp)
            #ave = self.DelAbnormal(temp,sum)
            # print flavor_input,sum,ave,len(temp)
            # print temp
            print 'flavor and ave:', flavor_input, ave
            res_vm.__setitem__(flavor_input, int(round(ave * time)))
            # print flavor_input,sum,length
        print Mincpu_flavor, Mincpu_flavor2
        # temp = int(res_vm.get(Mincpu_flavor))
        # temp += 15
        # res_vm.__setitem__(Mincpu_flavor,temp)
        # temp = int(res_vm.get(Mincpu_flavor2))
        # temp += 9
        # res_vm.__setitem__(Mincpu_flavor2 , temp)
        # print 'predict:' , res_vm
        return res_vm

    def pre2(self):
        print 'input_txt', self.input_txt
        print 'train_txt', self.train_txt
        return
