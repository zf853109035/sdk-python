# coding=utf-8
class Server:
    Serverid = 0
    VM = {}
    cpu = 0
    mem = 0

    def setup(self, cpu, mem):
        self.Serverid = id
        self.cpu = cpu
        self.mem = mem
        self.VM = {}


class assign2:
    Servers = []
    ServerNum = 0
    sum_cpu = 0
    sum_mem = 0
    OptimizaType = ''

    def __init__(self, sum_cpu, sum_mem, OptimizaType):
        self.sum_cpu = sum_cpu
        self.sum_mem = sum_mem
        self.OptimizaType = OptimizaType

    def NewSer(self):
        self.ServerNum += 1
        server = Server()
        server.setup(int(self.sum_cpu), int(self.sum_mem))
        return server

    # 再分配，尽量装满每个服务器
    def Reassign(self, Sorted_Vm, pre):
        for ser in self.Servers:
            for i in range(len(Sorted_Vm) - 17, -1, -1):
                flavor = Sorted_Vm[i][0]
                Need_cpu = Sorted_Vm[i][1]
                Need_mem = Sorted_Vm[i][2]
                if ser.cpu > Need_cpu and ser.mem > Need_mem:  # 如果剩余的大于需要的
                    if not ser.VM.has_key(flavor):
                        ser.VM.setdefault(flavor, 1)
                        ser.cpu -= Need_cpu
                        ser.mem -= Need_mem
                        num = int(pre.get(flavor))
                        num += 1
                        pre.__setitem__(flavor, num)
                    else:
                        num = int(ser.VM.get(flavor))
                        num += 1
                        ser.VM.__setitem__(flavor, num)
                        ser.cpu -= Need_cpu
                        ser.mem -= Need_mem
                        num = int(pre.get(flavor))
                        num += 1
                        pre.__setitem__(flavor, num)
        return pre

    def join(self, pre):
        result = []
        s = 0
        for flavor in pre:
            num = pre.get(flavor)
            if num != 0:
                s += num
        result.append(str(s))  # 预测出来的总的VM个数

        for flavor in pre:
            num = str(pre.get(flavor))
            result.append(flavor + '\t' + str(num))

        result.append('\n' + str(len(self.Servers)))
        for index, server in enumerate(self.Servers):
            temp = ''
            temp += str(index + 1) + '\t'
            for flavor in server.VM:
                temp += flavor + '\t' + str(server.VM.get(flavor)) + '\t'
            result.append(temp)
        return result

    def sort(self, input_txt, pre):
        flavor_id = {}
        for index, item in enumerate(input_txt):
            flavor_id.setdefault(item[0], index)

        temp = []
        SortByflavor = []
        for flavor in pre:
            num = pre.get(flavor)
            SortByflavor.append([flavor, int(input_txt[flavor_id.get(flavor)][1]),
                                 int(input_txt[flavor_id.get(flavor)][2]) / 1024, float(self.sum_cpu) % int(input_txt[flavor_id.get(flavor)][1])])
            for i in range(num):
                cpu = int(input_txt[flavor_id.get(flavor)][1])
                mem = int(input_txt[flavor_id.get(flavor)][2]) / 1024
                temp.append([flavor, cpu, mem, abs(float(self.sum_cpu) / float(self.sum_mem) - float(cpu) /
                                                   float(mem))])
        # print SortByflavor
        SortByflavor = sorted(SortByflavor, key=lambda x: x[1], reverse=True)
        print 'SortByflavor', SortByflavor

        sortdown = sorted(temp, key=lambda x: x[3], reverse=True)  # 很奇怪这里，全部按CPU分配更好
        sortup = sorted(temp, key=lambda x: x[3])
        # if OptimizaType=='CPU' or OptimizaType=='cpu':
        #     sored = sorted(temp, key=lambda x:x[1], reverse=True)
        # else:
        #     sored = sorted(temp , key=lambda x: x[2] , reverse=True)
        return sortdown, sortup, SortByflavor

    def assign(self, input_txt, pre):
        sortdown, sortup, SortByflavor = self.sort(input_txt, pre)
        print 'sortdown', sortdown
        print 'sortup', sortup
        print 'SortByflavor', SortByflavor

        temp = int(pre.get(SortByflavor[-1][0]))
        temp += 16
        pre.__setitem__(SortByflavor[-1][0], temp)
        temp = int(pre.get(SortByflavor[-2][0]))
        temp += 10
        pre.__setitem__(SortByflavor[-2][0], temp)
        temp = int(pre.get(SortByflavor[-3][0]))
        temp += 1
        pre.__setitem__(SortByflavor[-3][0], temp)
        sortdown, sortup, SortByflavor = self.sort(input_txt, pre)
        print 'sortup len', sortup
        # 装箱
        flag = False
        for flavor, Need_cpu, Need_mem, _ in sortup:
            # print 'sortup len',len(sortup)
            flag = False
            for server in self.Servers:
                if server.cpu >= Need_cpu and server.mem >= Need_mem:
                    if not server.VM.has_key(flavor):
                        server.VM.setdefault(flavor, 1)
                        server.cpu -= Need_cpu
                        server.mem -= Need_mem
                        flag = True
                        break
                    else:
                        num = int(server.VM.get(flavor))
                        num += 1
                        server.VM.__setitem__(flavor, num)
                        server.cpu -= Need_cpu
                        server.mem -= Need_mem
                        flag = True
                        break
            if flag == False:
                ser = self.NewSer()
                ser.cpu -= Need_cpu
                ser.mem -= Need_mem
                ser.VM.setdefault(flavor, '1')
                self.Servers.append(ser)
        # 尽量装满每个服务器
        for i in range(20):
            pre = self.Reassign(sortup, pre)
        # print '分配后的结果：'
        # for ser in self.Servers:
        #     print ser.VM
        return self.join(pre)

# input_txt = [['flavor1', '6', '1024'], ['flavor2', '1', '2048'], ['flavor3', '1', '4096'], ['flavor4', '2', '2048'], ['flavor5', '2', '4096'], ['flavor6', '2', '4096'], ['flavor7', '1', '4096'], ['flavor8', '3', '4096']]
# a = {'flavor3': 5, 'flavor2': 1, 'flavor1': 1, 'flavor7': 2, 'flavor6': 2, 'flavor5': 2, 'flavor4': 1, 'flavor8': 4}
# ass = assign()
# ass.sort(input_txt, a, 'CPU')
