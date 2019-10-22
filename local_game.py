import pygame
import tkinter
import socket
import json,types,string
import threading
from sys import exit
import time
from ai import Ai



'''
初始化棋盘
'''

def chessboard_init(screen):
    global red_chess_location
    screen.blit(background, (0, 0))
    screen.blit(score_board, (0, 0))
    screen.blit(status_board,(cb_width-300,-10))
    pygame.draw.polygon(screen, PeachPuff, [chesses[5][12], chesses[11][12], chesses[8][15]])
    pygame.draw.polygon(screen, CornflowerBlue, [chesses[8][1], chesses[5][4], chesses[11][4]])
    for x in range(16):
        for i in range(15):
            if i + 1 in helpful_chess[x]:
                pygame.draw.circle(screen, white, chesses[x][i + 1], circle_radius)

    for x in range(8):
        pygame.draw.aaline(screen, white, chesses[8 + x][1 + x], chesses[1 + x][8 + x])
        pygame.draw.aaline(screen, white, chesses[1 + x][8 - x], chesses[8 + x][15 - x])
    for x in range(7):
        pygame.draw.aaline(screen, white, chesses[7 - x][2 + x], chesses[9 + x][2 + x])
        pygame.draw.aaline(screen, white, chesses[7 - x][14 - x], chesses[9 + x][14 - x])
    for x in range(10):

        screen.blit(back_chess[x],(red_chess_location_init[x][0] - circle_radius, red_chess_location_init[x][1] - circle_radius))
        screen.blit(back_chess[x],(blue_chess_loaction_init[x][0] - circle_radius, blue_chess_loaction_init[x][1] - circle_radius))
    '''
    描绘棋子
    '''
    for x in range(10):
        screen.blit(red_chess[x], (red_chess_location[x][0] - circle_radius, red_chess_location[x][1] - circle_radius))
        screen.blit(blue_chess[x],
                    (blue_chess_loaction[x][0] - circle_radius, blue_chess_loaction[x][1] - circle_radius))

    pygame.draw.line(screen, white, (0, cb_height), (width, cb_height))


'''
描绘选中框
'''
def draw_select_box(
        screen,pos,color,length):
    if pos == (0,0) or pos == None:
        return
    pygame.draw.lines(screen, color, 0,[(pos[0]-circle_radius, pos[1]-length), (pos[0]-circle_radius, pos[1]-circle_radius),(pos[0]-length, pos[1]-circle_radius)],1)
    pygame.draw.lines(screen, color, 0,[(pos[0]+circle_radius, pos[1]-length), (pos[0]+circle_radius, pos[1]-circle_radius),(pos[0]+length, pos[1]-circle_radius)],1)
    pygame.draw.lines(screen, color, 0,[(pos[0]-circle_radius, pos[1]+length), (pos[0]-circle_radius, pos[1]+circle_radius),(pos[0]-length, pos[1]+circle_radius)],1)
    pygame.draw.lines(screen, color, 0,[(pos[0]+circle_radius, pos[1]+length), (pos[0]+circle_radius, pos[1]+circle_radius),(pos[0]+length, pos[1]+circle_radius)],1)

'''
棋子数值转换
'''
def value_trans(x):
    if x in range(-9,0):
        return -x
    elif x == 10:
        return 0
    return x

'''
坐标转换
'''
def get_pos(pos):
    for x in range(15):
        for i in helpful_chess[x+1]:
            if (chesses[x+1][i][0]-pos[0])**2+(chesses[x+1][i][1]-pos[1])**2 <= circle_radius**2:
                return chesses[x+1][i],x+1,i


def is_near_empty(pos_one,pos_two):
    global news
    if (abs(pos_one[0]-pos_two[0]) == 1 and abs(pos_one[1]-pos_two[1]) == 1) or ((abs(pos_one[0]-pos_two[0])==2 ) and (pos_one[1]-pos_two[1]==0)):
        if map[pos_two[0]][pos_two[1]] == 9999:
            return True
    news = '不可行棋'
    return False

def is_far_empty(pos_one,pos_two):
    global news,is_busy
    if (abs(pos_one[0]-pos_two[0]) == 2 and abs(pos_one[1]-pos_two[1]) == 2) or ((abs(pos_one[0]-pos_two[0])==4 ) and (pos_one[1]-pos_two[1]==0)):
        if map[int((pos_one[0]+pos_two[0])/2)][int((pos_one[1]+pos_two[1])/2)] != 9999:
            return True
    news = '不可行棋'
    return False

def is_line_empty(pos_one, pos_two):
    global news
    sub_x = pos_one[0] - pos_two[0]
    sub_y = pos_one[1] - pos_two[1]
    sub = abs(sub_x)
    if (abs(sub_x) == abs(sub_y)) or sub_y == 0:
        if map[pos_two[0]][pos_two[1]] == 9999:
            if sub_x > 0 and sub_y > 0:
                if map[pos_two[0]+1][pos_two[1]+1] == 9999:
                    return False
                for x in range(1,sub):
                    if map[pos_one[0] - x][pos_one[1] - x] != 9999:
                        path_chess.append((pos_one[0] - x, pos_one[1] - x))
                        value = map[pos_one[0] - x][pos_one[1] - x]
                        value = value_trans(value)
                        path_chess_value[value] +=1
            elif sub_x > 0 and sub_y < 0:
                if map[pos_two[0]+1][pos_two[1]-1] == 9999:
                    return False
                for x in range(1,sub):
                    if map[pos_one[0] - x][pos_one[1] + x] != 9999:
                        path_chess.append((pos_one[0] - x, pos_one[1] + x))
                        value = map[pos_one[0] - x][pos_one[1] + x]
                        value = value_trans(value)
                        path_chess_value[value] +=1
            elif sub_x < 0 and sub_y > 0:
                if map[pos_two[0]-1][pos_two[1]+1] == 9999:
                    return False
                for x in range(1,sub):
                    if map[pos_one[0] + x][pos_one[1] - x] != 9999:
                        path_chess.append((pos_one[0] + x, pos_one[1] - x))
                        value = map[pos_one[0] + x][pos_one[1] - x]
                        value = value_trans(value)
                        path_chess_value[value] +=1
            elif sub_x < 0 and sub_y < 0:
                if map[pos_two[0]-1][pos_two[1]-1] == 9999:
                    return False
                for x in range(1,sub):
                    if map[pos_one[0] + x][pos_one[1] + x] != 9999:
                        path_chess.append((pos_one[0] + x, pos_one[1] + x))
                        value = map[pos_one[0] + x][pos_one[1] + x]
                        value = value_trans(value)
                        path_chess_value[value] +=1
            elif sub_x < 0 and sub_y == 0:
                if map[pos_two[0]-2][pos_two[1]] == 9999:
                    return False
                for x in range(1,sub):
                    if map[pos_one[0] + x][pos_one[1]] != 9999:
                        path_chess.append((pos_one[0] + x, pos_one[1]))
                        value = map[pos_one[0] + x][pos_one[1]]
                        value = value_trans(value)
                        path_chess_value[value] +=1
            elif sub_x > 0 and sub_y ==0:
                if map[pos_two[0]+2][pos_two[1]] == 9999:

                    return False
                for x in range(1, sub):
                    if map[pos_one[0] - x][pos_one[1]] != 9999:
                        path_chess.append((pos_one[0] - x, pos_one[1]))
                        value = map[pos_one[0] - x][pos_one[1]]
                        value = value_trans(value)
                        path_chess_value[value] +=1
            if path_chess == []:
                news = '不可行棋'
                return False
            else:
                get_formula()
                if is__formula_right(formula):
                    value = value_trans(map[move_chess[0][0]][move_chess[0][1]])
                    try:
                        if value == eval(formula):
                             return True
                        else:
                            news = '表达式值与棋子不符！'
                            return False
                    except:
                        news = '表达式错误'
                        return False

#0~9 48~57
#+ 43
#- 45
#* 42
#/ 47
#() 40 41
def is__formula_right(formula):
    global news,path_chess_value
    if formula == None:
        path_chess_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        return False
    formula_value = [0,0,0,0,0,0,0,0,0,0]
    for x in (formula):
        x = ord(x)
        if x not in range(40,58) or x == 44 or x == 46:
            news = '内容有误'
            path_chess_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            return False
    for x in formula:
        a = ord(x)
        if a in range(48,58):
            formula_value[int(chr(a))] += 1
    for x in range(0,10):
        if formula_value != path_chess_value:
            print(formula_value)
            print(path_chess_value)
            news = '数字与棋子不符'
            path_chess_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            return False
    for i,x in enumerate(formula):
        a = ord(x)
        if a in [42,43,45,47]:
            if ord(formula[i+1]) in [42,43,45,47]:
                news = '符号有误'
                path_chess_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                return  False
    try:
        result = eval(formula)
    except:
        news = '表达式错误'
        return False
    if result != int(result):
        news = '不可整除'
        path_chess_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        return False
    return True

'''
行棋功能
'''
def go_chess(pos,x,y):
    global news,path_chess,path_chess_value,cur_chess_value,select_pos,cur_player,move_chess,cur_chess_value,regret_chess,path_chess_value
    if cur_player == -1:
        return
    elif cur_player == 0:
        if (side == 0 and model ==1) or model == 0:
            if  map[x][y] >=0 and map[x][y] <=9:
                select_pos = pos
                move_chess[0] = (x,y)
                cur_chess_value = map[x][y]
                path_chess = []
                path_chess_value = [0,0,0,0,0,0,0,0,0,0]
                news = '红方选择棋子'+str(map[x][y])
            elif map[x][y] == 9999:
                if move_chess[0] != (0,0):
                    move_chess[1] = (x,y)
                    if is_near_empty(move_chess[0], move_chess[1]) or is_far_empty(move_chess[0], move_chess[1]) or is_line_empty(move_chess[0], move_chess[1]):
                        red_chess_location[cur_chess_value] = chesses[x][y]
                        map[x][y] = cur_chess_value
                        map[move_chess[0][0]][move_chess[0][1]] = 9999
                        regret_chess = [cur_player,cur_chess_value,move_chess[0],move_chess[1]]
                        cur_player = 1 -cur_player
                        news = '红棋('+str(cur_chess_value)+')移动前坐标:'+str(move_chess[0])+'移动后坐标:'+str(move_chess[1])
                        cal_score(move_chess[0],move_chess[1])
                        move_chess = [(0, 0), (0, 0)]
                        path_chess = []
                        path_chess_value = [0,0,0,0,0,0,0,0,0,0]
                        if model != 1:
                            return
                        num = regret_chess[1]
                        msg = {
                            "type": 1, "msg": {"game_id": game_id, "side": side, "num": num,
                                               "src": {"x":regret_chess[2][1]-1 , "y": regret_chess[2][0]-1},
                                               "dst": {"x":regret_chess[3][1]-1 , "y":regret_chess[3][0]-1 }, "exp": ""}
                        }
                        msg = json.dumps(msg)
                        s.send(msg.encode('utf-8'))
    elif cur_player == 1:
        if (side == 1 and model ==1) or model == 0:
            if map[x][y] in range(-9,0) or map[x][y] == 10:
                select_pos = pos
                move_chess[0] = (x, y)
                cur_chess_value = map[x][y]
                path_chess = []
                path_chess_value = [0,0,0,0,0,0,0,0,0,0]
                news = '蓝方选择棋子'+str(value_trans(map[x][y]))
            elif map[x][y] == 9999:
                if move_chess[0] != (0,0):
                    move_chess[1] = (x,y)
                    if is_near_empty(move_chess[0], move_chess[1]) or is_far_empty(move_chess[0], move_chess[1]) or is_line_empty(move_chess[0], move_chess[1]):
                        temp = -cur_chess_value if cur_chess_value in range(-9,0) else 0
                        blue_chess_loaction[temp] = chesses[x][y]
                        map[x][y] = cur_chess_value
                        map[move_chess[0][0]][move_chess[0][1]] = 9999
                        regret_chess = [cur_player, cur_chess_value, move_chess[0], move_chess[1]]
                        news = '蓝棋('+str(value_trans(cur_chess_value))+')移动前坐标:'+str(move_chess[0])+'移动后坐标:'+str(move_chess[1])
                        cal_score(move_chess[0], move_chess[1])
                        path_chess = []
                        path_chess_value = [0,0,0,0,0,0,0,0,0,0]
                        move_chess = [(0, 0), (0, 0)]
                        cur_player = 1 -cur_player
                        if model != 1:
                            return
                        num = value_trans(regret_chess[1])
                        msg = {
                            "type": 1, "msg": {"game_id": game_id, "side": side, "num": num,
                                               "src": {"x":regret_chess[2][1]-1 , "y": regret_chess[2][0]-1},
                                               "dst": {"x":regret_chess[3][1]-1 , "y": regret_chess[3][0]-1}, "exp": ""}
                        }
                        msg = json.dumps(msg)
                        s.send(msg.encode('utf-8'))


def auto_go_chess():
    global red_chess_location,blue_chess_loaction,map,num,news,cur_player
    while True:
        if num != '' and num != -1:
            if event_side == 0:
                red_chess_location[num] = chesses[dst[1]][dst[0]]
                map[dst[1]][dst[0]] = num
                map[src[1]][src[0]] = 9999
                news = '红棋移动前坐标:'+str(src)+'移动后坐标:'+str(dst)
                cur_player = 1 - cur_player
                num = ''
                pos_one = (src[1],src[0])
                pos_two = (dst[1], dst[0])
                cal_score(pos_one,pos_two)
            elif event_side == 1:
                print("----------------------蓝方",num)
                blue_chess_loaction[num] = chesses[dst[1]][dst[0]]
                map[dst[1]][dst[0]] = -num if num > 0 else 10
                print("---------------------蓝方map",map[dst[1]][dst[0]])
                map[src[1]][src[0]] = 9999
                news = '蓝棋移动前坐标:' + str(src) + '移动后坐标:' + str(dst)
                cur_player = 1 - cur_player
                num = ''
                pos_one = (src[1], src[0])
                pos_two = (dst[1], dst[0])
                cal_score(pos_one, pos_two)
        elif num == -1 :
            break



'''
悔棋功能
'''
def regret():
    global regret_chess,cur_player,red_chess_location,blue_chess_loaction,map,news
    if regret_chess == None:
        return False
    if regret_chess[0] == 0:
        if (side == 0 and model == 1) or model == 0:
            map[regret_chess[2][0]][regret_chess[2][1]] = regret_chess[1]
            map[regret_chess[3][0]][regret_chess[3][1]] = 9999
            red_chess_location[regret_chess[1]] = chesses[regret_chess[2][0]][regret_chess[2][1]]
            cal_score(regret_chess[3],regret_chess[2])
            cur_player = 1 - cur_player
            news = '红方悔棋，由坐标' + str(regret_chess[3]) + '回到坐标' + str(regret_chess[2])
            regret_chess = None

    elif regret_chess[0] ==1:
        if (side == 1 and model == 1) or model == 0:
            map[regret_chess[2][0]][regret_chess[2][1]] = regret_chess[1]
            map[regret_chess[3][0]][regret_chess[3][1]] = 9999
            regret_chess[1] = -regret_chess[1] if regret_chess[1]<0 else 0
            blue_chess_loaction[regret_chess[1]] = chesses[regret_chess[2][0]][regret_chess[2][1]]
            cal_score(regret_chess[3], regret_chess[2])
            cur_player = 1 - cur_player
            news = '蓝方悔棋，由坐标' + str(regret_chess[3]) + '回到坐标' + str(regret_chess[2])
            regret_chess = None

'''
弹窗功能
'''
def get_formula():
    global is_busy
    def showinfo():
        global formula
        formula = entry.get()
        print('表达式：',formula)

        win.destroy()
    win = tkinter.Tk()
    win.wm_attributes('-topmost', 1)
    win.title('输入表达式')
    win.geometry("250x80+50+50")
    entry = tkinter.Entry(win)
    entry.pack(pady=20)
    button = tkinter.Button(win, text="确认",command=showinfo)
    button.pack()
    win.mainloop()
'''
计分功能
'''
def cal_score(pos_one,pos_two):
    global red_score,blue_score
    x1 = pos_one[0]
    y1 = pos_one[1]
    x2 = pos_two[0]
    y2 = pos_two[1]
    if  map[x2][y2] in range(0,10):
        red_score = 0
        for x in blue_position:
            if map[x[0]][x[1]] in range(0,10):
                red_score = red_score + map[x[0]][x[1]] * blue_position.index(x)
    elif map[x2][y2] in range(-9,0) or map[x2][y2] == 10 :
        blue_score = 0
        for x in red_position:
            if map[x[0]][x[1]] in range(-9,0) or map[x[0]][x[1]] == 10:
                pos = - map[x[0]][x[1]] if map[x[0]][x[1]] in range(-9,0) else 0
                blue_score = blue_score + pos * red_position.index(x)

'''
叫停功能
'''
def pause(x):
    global news,cur_player,model,start_mark,num
    if x == 0:
        if cur_player == 0:
            for x in blue_position:
                if map[x[0]][x[1]] not in range(0,10):
                    print(map[x[0]][x[1]])
                    news = '未达到叫停条件'
                    return False
            if red_score > blue_score:
                news = '红胜'
            elif red_score < blue_score:
                news = '蓝胜'
            else:
                news = '平局'
            if model == 1:
                msg = {"type": 2, "msg": {"request": "stop", "game_id": game_id, "side": side}}
                msg = json.dumps(msg)
                s.send(msg.encode('utf-8'))
                s.close()
                num = -1
            cur_player = -1
            model = -1
            start_mark = 0

    elif x == 1:
        if cur_player == 1:
            for x in red_position:
                if map[x[0]][x[1]] not in range(-9,0):
                    if map[x[0]][x[1]] == 10:
                        continue
                    print(map[x[0]][x[1]])
                    news = '未达到叫停条件'
                    return False
            if red_score > blue_score:
                news = '红胜'
            elif red_score < blue_score:
                news = '蓝胜'
            else:
                news = '平局'
            if model == 1:
                msg = {"type": 2, "msg": {"request": "stop", "game_id": game_id, "side": side}}
                msg = json.dumps(msg)
                s.send(msg.encode('utf-8'))
                s.close()
                num = -1
            cur_player = -1
            model = -1
            start_mark = 0

'''
棋盘坐标值初始化
'''
def map_init():
    global map
    for x in range(16):
        for i in range(16):
            map[x][i] = 9999
    # 红方为正  蓝方为负 零为10
    map[8][15] = 0
    map[5][12] = 1
    map[7][12] = 3
    map[9][12] = 2
    map[11][12] = 4
    map[10][13] = 5
    map[8][13] = 6
    map[6][13] = 7
    map[7][14] = 8
    map[9][14] = 9
    map[8][1] = 10
    map[11][4] = -1
    map[9][4] = -3
    map[7][4] = -2
    map[5][4] = -4
    map[6][3] = -5
    map[8][3] = -6
    map[10][3] = -7
    map[9][2] = -8
    map[7][2] = -9

'''
开始游戏
'''
def local_start():
    global model
    model =0
    threading.Thread(target=aiGoChess,args=(1,)).start()

def net_start():
    red_chess_location = [chesses[8][15], chesses[5][12], chesses[7][12], chesses[9][12], chesses[11][12],
                          chesses[10][13],
                          chesses[8][13], chesses[6][13], chesses[7][14], chesses[9][14]]
    blue_chess_loaction = [chesses[8][1], chesses[11][4], chesses[9][4], chesses[7][4], chesses[5][4], chesses[6][3],
                           chesses[8][3], chesses[10][3], chesses[9][2], chesses[7][2]]
    global  news
    t1 = threading.Thread(target=recv_msg,args=()).start()


def start():

    global cur_player,red_chess_location,blue_chess_loaction,map,red_score,blue_score,select_pos,news
    select_pos = (0,0)
    red_score = blue_score = 0
    cur_player = 0
    # red_chess_location = [chesses[8][15], chesses[5][12], chesses[7][12], chesses[9][12], chesses[11][12],
    #                       chesses[10][13],
    #                       chesses[8][13], chesses[6][13], chesses[7][14], chesses[9][14]]
    # blue_chess_loaction = [chesses[8][1], chesses[11][4], chesses[9][4], chesses[7][4], chesses[5][4], chesses[6][3],
    #                        chesses[8][3], chesses[10][3], chesses[9][2], chesses[7][2]]
    # map_init()
    news = '开始游戏'
def game_quit():
    global cur_player,model,start_mark,news,num
    num = -1
    cur_player = -1
    model = -1
    start_mark = 0
    news = '我方认输'
    msg = {"type": 2, "msg": {"request": "quit", "game_id": game_id, "side": side}}
    msg = json.dumps(msg)
    s.send(msg.encode('utf-8'))
    s.close()
class Button:
    def __init__(self,x,y,width,height,image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def create_image(self):
        image = pygame.image.load(self.image).convert_alpha()
        self.image = pygame.transform.scale(image, (self.width, self.height))

    def blit(self,screen):
        screen.blit(self.image,(self.x,self.y))

    def is_click(self):
        pos = pygame.mouse.get_pos()
        if pos[0]>self.x and pos[0]<self.x+self.width:
            if pos[1]>self.y and pos[1]<self.y+self.height:
                return True

        return False

def mAiGoChess():
    global side
    while True:
        if side != '':
            print(side)
            print("启动")
            threading.Thread(target=aiGoChess,args=(side,)).start()
            break

def aiGoChess(player):
    global cur_player,chesses,map,red_chess_location,blue_chess_loaction,s,game_id,side
    ai  = Ai(chesses,player,red_position,blue_position,map)
    while(True):
        time.sleep(1)
        if cur_player == player and player == 0:
            print("走红旗")
            pause(0)
            t = ""
            if ai.getHasGoNum() >= 45:
                t = ai.moveOut(map,red_chess_location)
                if not t:
                    t = ai.goChess(map,red_chess_location)
            else:
                print("正常")
                t = ai.goChess(map, red_chess_location)
            print(t)
            cal_score(t[0],t[1])
            msg = {
                "type": 1, "msg": {"game_id": game_id, "side": side, "num": t[2],
                                   "src": {"x": t[0][1] - 1, "y": t[0][0] - 1},
                                   "dst": {"x": t[1][1] - 1, "y": t[1][0] - 1}, "exp": ai.formula}
            }
            msg = json.dumps(msg)
            s.send(msg.encode('utf-8'))
            cur_player = 1 - cur_player
        elif cur_player == player and player == 1:
            print("走蓝旗")
            pause(1)
            t = ""
            if ai.getHasGoNum() >= 45:
                t = ai.moveOut(map, blue_chess_loaction)
                if not t:
                    t = ai.goChess(map, blue_chess_loaction)
            else:
                print("正常")
                t = ai.goChess(map, blue_chess_loaction)
            print(t)
            cal_score(t[0], t[1])
            msg = {
                "type": 1, "msg": {"game_id": game_id, "side": side, "num": t[2],
                                   "src": {"x": t[0][1] - 1, "y": t[0][0] - 1},
                                   "dst": {"x": t[1][1] - 1, "y": t[1][0] - 1}, "exp": ai.formula}
            }
            try:
                msg = json.dumps(msg)
                s.send(msg.encode('utf-8'))
                cur_player = 1 - cur_player
            except:
                cur_player = 1 - cur_player

def button_click():
    global cur_player,news
    if button_start.is_click():
        local_start()
        print('local_start')
    elif button_regret.is_click():
        regret()
        print('regret')
    elif button_pause.is_click():
        net_start()
        print('net_start')
    elif button_blue_pause.is_click():
        pause(1)
        print('blue_pause')
    elif button_red_pause.is_click():
        pause(0)
        print('red_pause')
    elif button_quit.is_click():
        game_quit()

def draw_score(a,b):
    score_text = textfont.render(str(a)+':'+str(b), True, white)
    screen.blit(score_text, (40, 50))
def draw_status(status):
    if cur_player == 1:
        status = '蓝方回合'
        if side == cur_player:
            status = '蓝方回合(我)'
    elif cur_player == 0:
        status = '红方回合'
        if side == cur_player:
            status = '红方回合(我)'
    else:
        status = '请开始游戏'
    status_text = statusfont.render(status,True,white)
    screen.blit(status_text,(cb_width-225,33))
def draw_news(news):
    news_text = newsfont.render(news,True,white)
    screen.blit(news_text,(cb_width-450,cb_height+15))

def connection():
    global news
    ip = '192.168.43.211'

    port = 50005
    s = socket.socket()
    s.connect((ip, port))
    return s

def recv_msg():
    global status,player_name, side, game_id,num,src,dst,exp,request,event_side,model,news,start_mark,cur_player,s,news
    STATUS = True
    news = '正在连接'
    try:
        s = connection()
        news = '正在匹配'
        threading.Thread(target=auto_go_chess).start()
        threading.Thread(target=mAiGoChess).start()
        send_msg = {"type": 0, "msg": {"name": "客户端1号-李天奇"}}
        send_msg = json.dumps(send_msg)
        s.send(send_msg.encode('utf-8'))
    except:
        STATUS = False
        news = '连接主机失败'

    while STATUS:
        print('recv_msg')
        try:
            msg = json.loads(s.recv(1024).decode('utf-8'))
        except:
            STATUS = False
        print(msg)
        if not 'status' in msg and 'num' in msg:#走棋数据
            num = msg['num']
            dst = (msg['dst']['x']+1,msg['dst']['y']+1)
            src = (msg['src']['x']+1,msg['src']['y']+1)
            exp = msg['exp']
            event_side = msg['side']
            continue
        if msg['status'] == 1: #是否连接
            status = msg['status']
            player_name = msg['counterpart_name']
            side = msg['side']
            game_id = msg['game_id']
            model = 1
            continue
        elif msg['status'] == 2:    #叫停 or 退出
            status  = msg['status']
            request = msg['request']
            event_side = msg['side']
            if request == 'quit':
                news = '对方认输'
            elif request == 'stop':
                if red_score > blue_score:
                    news = '红胜'
                elif red_score < blue_score:
                    news = '蓝胜'
                else:
                    news = '平局'
            num = -1
            model = -1
            start_mark = 0
            cur_player = -1
            msg = {"type": 3, "side": side}
            msg = json.dumps(msg)
            s.send(msg.encode('utf-8'))
            s.close()
            break
        elif msg['status'] == 3:    #超时
            event_side = msg['side']
            if side == event_side:
                news = '我方超时，自动认输'
            else:
                news='敌方超时，自动认输'
            num = -1
            model = -1
            start_mark = 0
            cur_player = -1
            msg = {"type": 3, "side": side}
            msg = json.dumps(msg)
            s.send(msg.encode('utf-8'))
            s.close()
            break
        if s == None:
            STATUS = False
#-----------------------------------------------------------------------------------------------------------------

'''
颜色参数
'''
white = (255,255,255)
PeachPuff = (255,218,185)
CornflowerBlue = (100,149,237)
Red = (255,0,0)
'''
系统参数
'''
background_image_filename = 'b.jpg'
score_board_image_filename = 'images/heiban.png'
status_image_filename = 'images/heiban2.png'
size = width , height = 960,640
clock = pygame.time.Clock()
FPS = 30
running = True
start_mark = 0
model = -1
s = None
player_name = ''
game_id = ''
side = ''
event_side = ''
status = ''
num = ''
src = ''
dst = ''
exp = ''
cur_think_time = 0
cur_total_time = 0
think_time = 30
total_time = 600
'''
棋盘参数
'''
cb_width = width
cb_height = height - 100

rectangle_width = 60
rectangle_height =  35

circle_radius = 20

first_chess_x = 50
first_chess_y = 30

chesses = [[] for i in range (16)] #棋盘坐标
for x in range(15):
    chesses[x+1].append((0,0))
for x in range(15):
    for i in range(15):
        chesses[x + 1].append((first_chess_x + i * rectangle_width, first_chess_y + x * rectangle_height))

helpful_chess = [(9999,),(8,),(7,9),(6,8,10),(5,7,9,11),(4,6,8,10,12),(3,5,7,9,11,13),(2,4,6,8,10,12,14),(1,3,5,7,9,11,13,15),
                 (2,4,6,8,10,12,14),(3,5,7,9,11,13),(4,6,8,10,12),(5,7,9,11),(6,8,10),(7,9),(8,)]

screen = pygame.display.set_mode(size,0,32)
pygame.display.set_caption('国际数棋-李天奇')
background = pygame.image.load(background_image_filename).convert()
score_board = pygame.image.load(score_board_image_filename).convert_alpha()
score_board = pygame.transform.scale(score_board,(250,190))
status_board = pygame.image.load(status_image_filename).convert_alpha()
status_board = pygame.transform.scale(status_board,(250,100))

'''
棋子参数
'''
red_chess = [] #图片对象
blue_chess = []
back_chess = []
red_chess_location = [chesses[8][15],chesses[5][12],chesses[9][12],chesses[7][12],chesses[11][12],chesses[10][13],
                      chesses[8][13],chesses[6][13],chesses[7][14],chesses[9][14]]
blue_chess_loaction = [chesses[8][1],chesses[11][4],chesses[7][4],chesses[9][4],chesses[5][4],chesses[6][3],
                       chesses[8][3],chesses[10][3],chesses[9][2],chesses[7][2]]
red_chess_location_init = [chesses[8][15], chesses[5][12],chesses[9][12], chesses[7][12],  chesses[11][12],
                          chesses[10][13],
                          chesses[8][13], chesses[6][13], chesses[7][14], chesses[9][14]]
blue_chess_loaction_init = [chesses[8][1], chesses[11][4],chesses[7][4], chesses[9][4],  chesses[5][4], chesses[6][3],
                           chesses[8][3], chesses[10][3], chesses[9][2], chesses[7][2]]

for i in range(10):
    url = 'images/red_1_'+str(i)+'.png'
    image = pygame.image.load(url).convert_alpha()
    image = pygame.transform.scale(image,(2*circle_radius,2*circle_radius))
    red_chess.append(image)
for i in range(10):
    url = 'images/blue_1_' + str(i) + '.png'
    image = pygame.image.load(url).convert_alpha()
    image = pygame.transform.scale(image, (2*circle_radius, 2*circle_radius))
    blue_chess.append(image)
for i in range(0,10):
    filename = 'images/' + str(i)+'.png'
    image = pygame.image.load(filename).convert_alpha()
    image = pygame.transform.scale(image, (2 * circle_radius, 2 * circle_radius))
    back_chess.append(image)




'''
红正 蓝负
'''
map = [[] for i in range (16)]
for x in range(16):
    for i in range(16):
        map[x].append(9999)
map[8][15]=0;map[5][12]=1;map[7][12]=3;map[9][12]=2;map[11][12]=4;map[10][13]=5;map[8][13]=6;map[6][13]=7;
map[7][14]=8;map[9][14]=9
map[8][1]=10;map[11][4]=-1;map[9][4]=-3;map[7][4]=-2;map[5][4]=-4;map[6][3]=-5;map[8][3]=-6;map[10][3]=-7;
map[9][2]=-8;map[7][2]=-9

'''
计分数据
'''
score = [[] for i in range (16)]
for x in range(16):
    for i in range(16):
        score[x].append(9999)

score[8][1]=score[8][15]=0
score[11][4]=score[5][12]=1
score[9][4]=score[7][12]=2
score[7][4]=score[9][12]=3
score[5][4]=score[11][12]=4
score[6][3]=score[10][13]=5
score[8][3]=score[8][13]=6
score[10][3]=score[6][13]=7
score[9][2]=score[7][14]=8
score[7][2]=score[9][14]=9

red_position = [(8,15),(5,12),(7,12),(9,12),(11,12),(10,13),(8,13),(6,13),(7,14),(9,14)]
blue_position = [(8,1),(11,4),(9,4),(7,4),(5,4),(6,3),(8,3),(10,3),(9,2),(7,2)]

red_score = 0
blue_score = 0
'''
按钮
'''
button_start = Button(20,cb_height+10,140,40,'button/danji.png')
button_regret = Button(340,cb_height+10,140,40,'button/huiqi.png')
button_pause = Button(180,cb_height+10,140,40,'button/wangluo.png')
button_blue_pause = Button(20,cb_height-60,140,42,'button/lanting.png')
button_red_pause = Button(cb_width-160,cb_height-60,140,42,'button/hongting.png')
button_quit = Button(340,cb_height+60,140,40,'button/quit.png')
button_ai = Button(170,cb_height+30,60,80,'button/ai.png')
button_start.create_image()
button_regret.create_image()
button_pause.create_image()
button_blue_pause.create_image()
button_red_pause.create_image()
button_quit.create_image()
button_ai.create_image()
'''
音效
'''
pygame.mixer.init()
sound_chess = pygame.mixer.Sound('mp3/mutou.wav')

'''
动作参数
'''
select_pos = (0,0)
move_chess = [(0,0),(0,0)]
cur_chess_value = None
cur_player = -1
formula = None
path_chess = []
path_chess_value = [0,0,0,0,0,0,0,0,0,0]
regret_chess = None
cur_status = '请开始游戏'
news = '消息提示'

pygame.init()
textfont = pygame.font.Font('font/font.ttf',60)
statusfont = pygame.font.Font('font/status.ttf',25)
newsfont = pygame.font.Font('font/font.ttf',20)

'''
入口
'''
def main():
    global news,model,start_mark,side
    while running:
        clock.tick(FPS)
        chessboard_init(screen)#初始化棋盘
        button_start.blit(screen)
        button_regret.blit(screen)
        button_pause.blit(screen)
        button_ai.blit(screen)
        if side == 0 or model == 0:
            button_red_pause.blit(screen)
        if side == 1 or model == 0:
            button_blue_pause.blit(screen)
        if model == 1:
            button_quit.blit(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                exit()
            # 鼠标点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 判断按钮是否被点击
                button_click()
                # 获得坐标
                pos = event.pos
                #根据坐标获取
                temp = get_pos(pos)
                if temp != None:
                    sound_chess.play()
                    go_chess(temp[0],temp[1],temp[2])
        draw_select_box(screen,select_pos,Red,circle_radius/2)
        draw_score(blue_score, red_score)
        draw_status(cur_status)

        draw_news(news)

        if model != -1 and start_mark == 0:
            start()
            start_mark = 1

        pygame.display.update()
if __name__ == '__main__':
    main()