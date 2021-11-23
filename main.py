import pygame
import time
import json


f=open("ez.txt","r",encoding='UTF-8')
txt = f.read()
js = json.loads(txt)
time_list = []
column_list = []
column_li = []
try:
    for i in js['note']:
        column_list.append(i['column'])
        time0 = int((i['beat'][0]*60/180+(i['beat'][1]/i['beat'][2])/3)*1000)
        time_list.append(time0)

except Exception as e:
    print(e)
    pass
print(time_list)




background_image = 'images/1.jpg'
mouse_image = 'images/2.png'
start_0 = 'images/3.png'
start_1 = 'images/4.png'
hit_1 = 'images/hit.png'
hit_2 = 'images/hit2.png'
hit_3 = 'images/hit3.png'


# 初始化pygame，为使用硬件做准备
pygame.init()
pygame.mixer.init()

# 创建了一个窗口
screen = pygame.display.set_mode((1280, 800), 0, 32)
# 设置窗口标题
pygame.display.set_caption("hello world")
SCREEN_SIZE = (1280, 800)
# 加载并转换图像
background = pygame.image.load(background_image).convert()
mouse_cursor = pygame.image.load(mouse_image).convert_alpha()
start_0 = pygame.image.load(start_0).convert()
start_1 = pygame.image.load(start_1).convert()
hit_1 = pygame.image.load(hit_1).convert()
hit_2 = pygame.image.load(hit_2).convert()
hit_3 = pygame.image.load(hit_3).convert()



# 隐藏鼠标
pygame.mouse.set_visible(False)

# 字体设置
font = pygame.font.SysFont("MicrosoftYaHei", 32)
font_height = font.get_linesize()  # 字体行高
event_text = []


class Button(object):
    def __init__(self, text, color, x, y, select):
        self.surface = font.render(text, True, color)
        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()
        self.x = x
        self.y = y
        self.box = (x, y)
        self.select = select

    def display(self):
        if self.select == 0:
            screen.blit(start_0, (self.x-45, self.y-10))  # 画上背景图
        else:
            screen.blit(start_1, (self.x - 45, self.y - 10))
        screen.blit(self.surface, (self.x, self.y))

    def check_click(self, position):
        x_match = position[0] > self.x-30 and position[0] < self.x + self.WIDTH+50
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT+50
        if x_match and y_match:
            return True
        else:
            return False

class keyboard(object):
    def __init__(self,text,color,x,y,select):
        self.surface = font.render(text, True, color)
        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()
        self.x = x
        self.y = y
        self.box = (x, y)
        self.select = select
        self.text = text
        self.color = color

    def hit(self):
        if self.select == 1:
            screen.blit(hit_2, (self.x+3, self.y+2))  # 画上背景图
            screen.blit(font.render(self.text, True, self.color), (self.x+65, self.y+15))

        else:
            screen.blit(hit_1, (self.x+3, self.y+2))  # 画上背景图
            screen.blit(font.render(self.text, True, self.color), (self.x+65, self.y+15))

class note(object):
    def __init__(self, x, time_check, time_now):
        self.x = x
        self.time_check = time_check
        self.time_now = time_now


    def move(self):
        if (-(self.time_check-self.time_now) >= 0) and (-(self.time_check-self.time_now) <= 750) :
            screen.blit(hit_3, (self.x, -(self.time_check-self.time_now)))  # 画上背景图



def play_music():
    bgm = pygame.mixer.Sound("images/1.ogg")
    bgm.play()

def plat_hit():
    hit_fx= pygame.mixer.Sound("images/2.wav")
    hit_fx.play()




standardtime = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 接收到退出事件后退出程序
            exit()

    screen.blit(background, (0, 0))  # 画上背景图
    play_button = Button('start', (0, 0, 0), 600, 610, 1)
    play_button.display()



    x, y = pygame.mouse.get_pos()  # 获得鼠标位置

    if play_button.check_click((x, y)):
        play_button = Button('start', (255, 255, 255), 598, 608, 0)
        play_button.display()

        if event.type == pygame.MOUSEBUTTONUP:

            screen.fill((255, 255, 255))
            pygame.display.update()
            screen.blit(font.render("3", True, (0, 0, 255)), (10, 10))
            pygame.display.update()
            time.sleep(1)
            screen.fill((255,255,255))
            screen.blit(font.render("2", True, (0, 0, 255)), (10, 10))
            pygame.display.update()
            time.sleep(1)
            screen.fill((255,255,255))
            screen.blit(font.render("1", True, (0, 0, 255)), (10, 10))
            pygame.display.update()
            time.sleep(0.2)

            for i in range(len(time_list)):
                if column_list[i] == 0:
                    g = 350
                if column_list[i] == 1:
                    g = 500
                if column_list[i] == 2:
                    g = 650
                if column_list[i] == 3:
                    g = 800
                column_li.append(g)
            screen.fill((255,255,255))
            standardtime = pygame.time.get_ticks()
            play_music()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # 接收到退出事件后退出程序
                        exit()

                screen.fill((255, 255, 255))
                time_n = pygame.time.get_ticks()-standardtime
                note_list = [note(column_li[i],time_list[i],time_n) for i in range(len(time_list))]


                pygame.draw.line(screen,(0,0,0),(350,50),(350,780),5)
                pygame.draw.line(screen,(0,0,0),(500,50),(500,780),5)
                pygame.draw.line(screen,(0,0,0),(650,50),(650,780),5)
                pygame.draw.line(screen,(0,0,0),(800,50),(800,780),5)
                pygame.draw.line(screen,(0,0,0),(950,50),(950,780),5)
                pygame.draw.line(screen,(0,0,0),(350,700),(950,700),5)
                pygame.draw.line(screen,(0,0,0),(350,780),(950,780),5)

                for i in note_list:
                    i.move()

                #反馈部分
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        key_s = keyboard("S", (0, 0, 0), 350, 700, 1)
                        key_s.hit()
                        key_d = keyboard("D", (0, 0, 0), 500, 700, 0)
                        key_d.hit()
                        key_j = keyboard("J", (0, 0, 0), 650, 700, 0)
                        key_j.hit()
                        key_k = keyboard("K", (0, 0, 0), 800, 700, 0)
                        key_k.hit()
                    if event.key == pygame.K_d:
                        key_s = keyboard("S", (0, 0, 0), 350, 700, 0)
                        key_s.hit()
                        key_d = keyboard("D", (0, 0, 0), 500, 700, 1)
                        key_d.hit()
                        key_j = keyboard("J", (0, 0, 0), 650, 700, 0)
                        key_j.hit()
                        key_k = keyboard("K", (0, 0, 0), 800, 700, 0)
                        key_k.hit()
                    if event.key == pygame.K_j:
                        key_s = keyboard("S", (0, 0, 0), 350, 700, 0)
                        key_s.hit()
                        key_d = keyboard("D", (0, 0, 0), 500, 700, 0)
                        key_d.hit()
                        key_j = keyboard("J", (0, 0, 0), 650, 700, 1)
                        key_j.hit()
                        key_k = keyboard("K", (0, 0, 0), 800, 700, 0)
                        key_k.hit()
                    if event.key == pygame.K_k:
                        key_s = keyboard("S", (0, 0, 0), 350, 700, 0)
                        key_s.hit()
                        key_d = keyboard("D", (0, 0, 0), 500, 700, 0)
                        key_d.hit()
                        key_j = keyboard("J", (0, 0, 0), 650, 700, 0)
                        key_j.hit()
                        key_k = keyboard("K", (0, 0, 0), 800, 700, 1)
                        key_k.hit()



                else:
                    key_s = keyboard("S", (0, 0, 0), 350, 700, 0)
                    key_s.hit()
                    key_d = keyboard("D", (0, 0, 0), 500, 700, 0)
                    key_d.hit()
                    key_j = keyboard("J", (0, 0, 0), 650, 700, 0)
                    key_j.hit()
                    key_k = keyboard("K", (0, 0, 0), 800, 700, 0)
                    key_k.hit()




                x, y = pygame.mouse.get_pos()  # 获得鼠标位置
                # 计算光标左上角位置
                x -= mouse_cursor.get_width() / 2
                y -= mouse_cursor.get_height() / 2
                # 画上光标
                screen.blit(mouse_cursor, (x, y))
                # screen.blit(font.render(event_text, True, (255, 255, 255)), (0, 1))
                time = pygame.time.get_ticks()

                fclock = pygame.time.Clock()
                fps = 90
                fclock.tick(fps)

                # 刷新画面
                pygame.display.update()







    else:
        play_button = Button('start', (0, 0, 0), 600, 610, 1)
        play_button.display()

    # 计算光标左上角位置
    x -= mouse_cursor.get_width() / 2
    y -= mouse_cursor.get_height() / 2
    # 画上光标
    screen.blit(mouse_cursor, (x, y))

    #screen.blit(font.render(event_text, True, (255, 255, 255)), (0, 1))


    # 刷新画面
    pygame.display.update()
