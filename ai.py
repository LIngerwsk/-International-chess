import math

class Formula:

    def init(self,list,value):
        self.formula = ""
        self.PRECISION = 1E-6
        self.expression = []
        self.NUMBER_TO_BE_CAL = value
        self.number = list
        self.COUNT_OF_NUMBER = len(list)
        for i in range(0, self.COUNT_OF_NUMBER):
            self.expression.append(str(self.number[i]))
    def solve(self,n):
        if (1 == n):
            if (math.fabs(self.NUMBER_TO_BE_CAL - self.number[0]) < self.PRECISION):
                self.formula = self.expression[0]
                return True
            else:
                return False
        else:
            for i in range(0, n):
                for j in range(i + 1, n):
                    a = self.number[i]
                    b = self.number[j]
                    # **********************************
                    #   将剩下的有效数字往前挪，
                    #   由于两数计算结果保存在number[i]中，
                    #   所以将数组末元素覆盖number[j]即可
                    # www.iplaypy.com
                    # **********************************
                    self.number[j] = self.number[n - 1]
                    expa = self.expression[i]
                    expb = self.expression[j]
                    self.expression[j] = self.expression[n - 1]
                    # 计算a+b
                    self.expression[i] = '(' + expa + '+' + expb + ')'
                    self.number[i] = a + b
                    if (self.solve(n - 1)):
                        return True;

                    # 计算a-b
                    self.expression[i] = '(' + expa + '-' + expb + ')'
                    self.number[i] = a - b
                    if (self.solve(n - 1)):
                        return True

                    # 计算b-a
                    self.expression[i] = '(' + expb + '-' + expa + ')'
                    self.number[i] = b - a
                    if (self.solve(n - 1)):
                        return True

                    # 计算(a*b)
                    self.expression[i] = '(' + expa + '*' + expb + ')'
                    self.number[i] = a * b
                    if (self.solve(n - 1)):
                        return True;

                    # 计算(a/b)
                    if (b != 0):
                        self.expression[i] = '(' + expa + '/' + expb + ')'
                        self.number[i] = a / b
                        if (self.solve(n - 1)):
                            return True

                        # 计算(b/a)
                        if (a != 0):
                            self.expression[i] = '(' + expb + '/' + expa + ')'
                            self.number[i] = b / a
                            if (self.solve(n - 1)):
                                return True

                    # 恢复现场
                    self.number[i] = a
                    self.number[j] = b
                    self.expression[i] = expa
                    self.expression[j] = expb
            return False



class Ai:
    def __init__(self,chess,player,redPosition,bluePosition,map):
        self.map = map
        self.formula = ""
        self.redPosition = redPosition
        self.bluePosition = bluePosition
        self.hasGoNum = 0
        self.player = player
        self.chess = chess
        self.f = Formula()
        self.helpfulChess = []
        self.leftTopBorder =     [(8,1),(7,2),(6,3),(5,4),(4,5),(3,6),(2,7),(1,8)]
        self.rightTopBorder =    [(1,8),(2,9),(3,10),(4,11),(5,12),(6,13),(7,14),(8,15)]
        self.rightBottomBorder = [(8,15),(9,14),(10,13),(11,12),(12,11),(13,10),(14,9),(15,8)]
        self.leftBottomBorder =  [(15,8),(14,7),(13,6),(12,5),(11,4),(10,3),(9,2),(8,1)]


    def getPath(self):
        pass
    def getPreLocation(self,pos):
        status = [0,0,0,0,0,0]
        stop = [1,1,1,1,1,1]
        preLocation = []
        leftTop,leftBottom,rightTop,rightBottom,top,bottom = pos,pos,pos,pos,pos,pos
        while True:
            if status == stop:
                break
            if status[0] != 1:
                leftTop = (leftTop[0] - 1, leftTop[1] - 1)
                if pos not in self.leftTopBorder:
                    if leftTop in self.leftTopBorder:
                        status[0] = 1
                    preLocation.append(leftTop)
                else:
                    status[0] = 1

            if status[1] != 1:
                rightTop = (rightTop[0] - 1, rightTop[1] + 1)
                if pos not in self.rightTopBorder:
                    if rightTop in self.rightTopBorder:
                        status[1] = 1
                    preLocation.append(rightTop)
                else:
                    status[1] = 1

            if status[2] != 1:
                leftBottom = (leftBottom[0] + 1, leftBottom[1] - 1)
                if pos not in self.leftBottomBorder:
                    if leftBottom in self.leftBottomBorder:
                        status[2] = 1
                    preLocation.append(leftBottom)
                else:
                    status[2] = 1

            if status[3] != 1:
                rightBottom = (rightBottom[0] + 1, rightBottom[1] + 1)
                if pos not in self.rightBottomBorder:
                    if rightBottom in self.rightBottomBorder:
                        status[3] = 1
                    preLocation.append(rightBottom)
                else:
                    status[3] = 1

            if status[4] != 1:
                bottom = (bottom[0] + 2, bottom[1])
                if pos not in self.rightBottomBorder and pos not in self.leftBottomBorder:
                    if bottom in self.rightBottomBorder or bottom in self.leftBottomBorder:
                        status[4] = 1
                    preLocation.append(bottom)
                else:
                    status[4] = 1


            if status[5] != 1:
                top = (top[0] - 2, top[1])
                if pos not in self.rightTopBorder and pos not in self.leftTopBorder:
                    if top in self.rightTopBorder or top in self.leftTopBorder:
                        status[5] = 1
                    preLocation.append(top)
                else:
                    status[5] = 1

        return preLocation


    def getMovePreLocation(self,map,num,pos):
        moveLocation = []
        preLocation = self.getPreLocation(pos)
        for location in preLocation:
            if self.is_near_empty(map,pos,location) or self.is_far_empty(map,pos,location) or self.is_line_empty(map,num,pos,location):
                moveLocation.append(location)
        return moveLocation


    def getSingleWeight(self,map,num,pos,where):
        weight = 0
        movePos = (0,0)
        moveLocation = self.getMovePreLocation(map,num,pos)
        for location in moveLocation:
            if self.player == 0:
                if pos in self.bluePosition:
                    if num * self.value_trans(self.map[pos[0]][pos[1]]) > num * self.value_trans(self.map[location[0]][location[1]]):
                        weight = 0
                        continue
            else:
                if pos in self.redPosition:
                    if num * self.map[pos[0]][pos[1]] > num * self.map[location[0]][location[1]]:
                        weight = 0
                        continue
            if self.player == 0:
                moveLength = pos[1]-location[1]
            else:moveLength = location[1]-pos[1]
            if moveLength == 0:
                moveLength = 0.1
            if num == 0:
                if 1*moveLength > weight:
                    weight = 1*moveLength
                    movePos = location
            if num*moveLength > weight:
                weight = num*moveLength
                movePos = location

        if where == 1 :
            if movePos == (0,0):
                for location in moveLocation:
                    if self.player == 0:
                        moveLength = location[1] - pos[1]
                    else:
                        moveLength = pos[1] - location[1]
                    if moveLength == 0:
                        moveLength = 0.1
                    if num == 0:
                        if 1 * moveLength > weight:
                            movePos = location
                    if num * moveLength > weight:
                        movePos = location
        return weight,num,pos,movePos

    def moveOut(self,map,location):
        weight = 0
        result = None
        position = []
        for pos in location:
            y = int((pos[0] - 50) / 60 + 1)
            x = int((pos[1] - 30) / 35 + 1)
            position.append((x, y))
        if self.player == 0:
            for num,pos in enumerate(position):
                if pos in self.redPosition:
                    temp = self.getSingleWeight(map,num,pos,0)
                    if temp[0] > weight:
                        result = temp
                        weight = result[0]
        else:
            for num,pos in enumerate(position):
                if pos in self.bluePosition:
                    temp = self.getSingleWeight(map,num,pos,0)
                    if temp[0] > weight:
                        result = temp
                        weight = result[0]
        if result == None or result[3] == (0,0):
            return False
        location[result[1]] = self.chess[result[3][0]][result[3][1]]
        map[result[2][0]][result[2][1]] = 9999
        if self.player == 0:
            num = result[1]
        else:
            num = self.pToN(result[1])
        map[result[3][0]][result[3][1]] = num

        if self.player == 0:
            print("红旗", num, "移动前坐标", result[2], "移动后坐标", result[3])
        else:
            print("蓝旗", num, "移动前坐标", result[2], "移动后坐标", result[3])
        self.hasGoNum = self.hasGoNum + 1
        if self.is_near_empty(map, result[2], result[3]) or self.is_far_empty(map, result[2], result[3]) or self.is_line_empty(map,self.value_trans(result[1]),result[2], result[3]):
            print(result)
        return result[2], result[3], self.value_trans(num)



    def getHasGoNum(self):
        return self.hasGoNum


    def getAllWeight(self,map,location):
        result = self.getSingleWeight(map,0,location[0],1)
        for num,pos in enumerate(location):
            temp = self.getSingleWeight(map,num,pos,1)
            if temp[0] > result[0]:
                result = temp
        return result

    def goChess(self,map,location):
        position = []
        for pos in location:
            y = int((pos[0] - 50) / 60 + 1)
            x = int((pos[1] - 30) / 35 + 1)
            position.append((x, y))
        result = self.getAllWeight(map,position)
        if self.is_near_empty(map, result[2], result[3]) or self.is_far_empty(map, result[2], result[3]) or self.is_line_empty(map,result[1],result[2], result[3]):
            print(result)
        location[result[1]] = self.chess[result[3][0]][result[3][1]]
        map[result[2][0]][result[2][1]] = 9999
        if self.player == 0:
            num = result[1]
        else:
            num = self.pToN(result[1])
        map[result[3][0]][result[3][1]] = num

        if self.player == 0:
            print("红旗",num,"移动前坐标",result[2],"移动后坐标",result[3])
        else:print("蓝旗",num,"移动前坐标",result[2],"移动后坐标",result[3])
        self.hasGoNum = self.hasGoNum + 1
        return result[2], result[3],self.value_trans(num)



    def is_near_empty(self,map,pos_one, pos_two):
        self.formula = ""
        if (abs(pos_one[0] - pos_two[0]) == 1 and abs(pos_one[1] - pos_two[1]) == 1) or (
                (abs(pos_one[0] - pos_two[0]) == 2) and (pos_one[1] - pos_two[1] == 0)):
            if map[pos_two[0]][pos_two[1]] == 9999:
                return True

        return False

    def is_far_empty(self,map,pos_one, pos_two):
        if (abs(pos_one[0] - pos_two[0]) == 2 and abs(pos_one[1] - pos_two[1]) == 2) or (
                (abs(pos_one[0] - pos_two[0]) == 4) and (pos_one[1] - pos_two[1] == 0)):
            if map[int((pos_one[0] + pos_two[0]) / 2)][int((pos_one[1] + pos_two[1]) / 2)] != 9999 and map[pos_two[0]][pos_two[1]] == 9999:
                return True

        return False

    def is_line_empty(self,map,num,pos_one, pos_two):
        path_chess = []
        path_chess_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        sub_x = pos_one[0] - pos_two[0]
        sub_y = pos_one[1] - pos_two[1]
        sub = abs(sub_x)
        if (abs(sub_x) == abs(sub_y)) or sub_y == 0:
            if map[pos_two[0]][pos_two[1]] == 9999:
                if sub_x > 0 and sub_y > 0:
                    if map[pos_two[0] + 1][pos_two[1] + 1] == 9999:
                        return False
                    for x in range(1, sub):
                        if map[pos_one[0] - x][pos_one[1] - x] != 9999:
                            path_chess.append((pos_one[0] - x, pos_one[1] - x))
                            value = map[pos_one[0] - x][pos_one[1] - x]
                            value = self.value_trans(value)
                            path_chess_value[value] += 1
                elif sub_x > 0 and sub_y < 0:
                    if map[pos_two[0] + 1][pos_two[1] - 1] == 9999:
                        return False
                    for x in range(1, sub):
                        if map[pos_one[0] - x][pos_one[1] + x] != 9999:
                            path_chess.append((pos_one[0] - x, pos_one[1] + x))
                            value = map[pos_one[0] - x][pos_one[1] + x]
                            value = self.value_trans(value)
                            path_chess_value[value] += 1
                elif sub_x < 0 and sub_y > 0:
                    if map[pos_two[0] - 1][pos_two[1] + 1] == 9999:
                        return False
                    for x in range(1, sub):
                        if map[pos_one[0] + x][pos_one[1] - x] != 9999:
                            path_chess.append((pos_one[0] + x, pos_one[1] - x))
                            value = map[pos_one[0] + x][pos_one[1] - x]
                            value = self.value_trans(value)
                            path_chess_value[value] += 1
                elif sub_x < 0 and sub_y < 0:
                    if map[pos_two[0] - 1][pos_two[1] - 1] == 9999:
                        return False
                    for x in range(1, sub):
                        if map[pos_one[0] + x][pos_one[1] + x] != 9999:
                            path_chess.append((pos_one[0] + x, pos_one[1] + x))
                            value = map[pos_one[0] + x][pos_one[1] + x]
                            value = self.value_trans(value)
                            path_chess_value[value] += 1
                elif sub_x < 0 and sub_y == 0:
                    if map[pos_two[0] - 2][pos_two[1]] == 9999:
                        return False
                    for x in range(1, sub):
                        if map[pos_one[0] + x][pos_one[1]] != 9999:
                            path_chess.append((pos_one[0] + x, pos_one[1]))
                            value = map[pos_one[0] + x][pos_one[1]]
                            value = self.value_trans(value)
                            path_chess_value[value] += 1
                elif sub_x > 0 and sub_y == 0:
                    if map[pos_two[0] + 2][pos_two[1]] == 9999:


                        return False
                    for x in range(1, sub):
                        if map[pos_one[0] - x][pos_one[1]] != 9999:
                            path_chess.append((pos_one[0] - x, pos_one[1]))
                            value = map[pos_one[0] - x][pos_one[1]]
                            value = self.value_trans(value)
                            path_chess_value[value] += 1
                if path_chess == []:
                    return False
                else:
                    path = []
                    for x,i in enumerate(path_chess_value):
                        if i != 0:
                            for n in range(0,i):
                                path.append(x)
                    self.f.init(path,num)
                    if self.f.solve(len(path)):
                        self.formula = self.f.formula
                        return True
                    else:return False


    def value_trans(self,x):
        if x in range(-9, 0):
            return -x
        elif x == 10:
            return 0
        return x

    def pToN(self,x):
        if x in range(1,10):
            return -x
        elif x == 0:
            return 10
        return x






