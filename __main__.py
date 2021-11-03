import pygame, sys, os, random 
from pygame.locals import *  

colors = [
    (37, 235, 11), 
    (160, 154, 143), 
    (139, 176, 186), 
    (57, 217, 227), 
    (82, 30, 24),
    (13, 216, 46),
    (198, 39, 57)
]

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

level = 1
lines_to_clear = 1

class Figure:
    '''
    Figure class is used to create the blocks that will fall down from the top of the screen 
    |0 |1 |2 |3 |
    |4 |5 |6 |7 |
    |8 |9 |10|11|
    |12|13|14|15|
    This is a visual of the 4x4 grid system used 
    to rotation the various shapes in Tetris game.

    Tetromino: is a geometric shape composed of 4 squares 
    '''
    figures = [
        [[4, 5, 6, 7], [1, 5, 9, 13]], # for straight line
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], # for pyramid tetromino
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 8, 9], [4, 5, 6, 10]], # for left side L-shaped tetromino 
        [[1, 2, 6, 10], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]], # for right side L-shaped tetromino 
        [[5, 6, 9, 10]], # for square shape 
        [[1, 2, 4, 5], [0, 4, 5, 9], [5, 6, 8, 9], [1, 5, 6, 10]], # for left side zig-zag shaped tetromino 
        [[1, 2, 6, 7], [3, 6, 7, 10], [5, 6, 10, 11], [2, 5, 6, 9]] # for right side zig-zag shaped tetromino 
    ]

    def __init__(self, x, y):
        self.x = x 
        self.y = y 
        self.type = random.randint(0, (len(self.figures) - 1))
        self.color = random.randint(1, (len(colors) - 1))
        self.rotation = 0 

    # gets the specific shape and color of currently falling object 
    def get_image(self):
        return self.figures[self.type][self.rotation]

    # increments to the next rotation of any type of figure
    def rotate(self):
        self.rotation = (self.rotation + 1) % (len(self.figures[self.type])) 

class Tetris:
    lines_cleared = 0
    score = 0 
    state = "start"
    field = [] 
    HEIGHT = 0
    WIDTH = 0 
    startX = 100 
    startY = 50
    zoom = 20 
    figure = None 

    def __init__(self, height, width):
        self.field = []  
        self.figure = None 
        self.height = height 
        self.width = width
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)   

    def create_figure(self):
        self.figure = Figure(3, 0)
 
    def intersects(self):
        intersects = False 
        for i in range(4):
            for j in range(4):
                if (i * 4) + j in self.figure.get_image():
                    if (i + self.figure.y) > (self.height - 1) or \
                        (j + self.figure.x) > (self.width - 1) or \
                        (j + self.figure.x) < 0 or \
                        self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersects = True 
        return intersects 

    def freeze_figure(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.get_image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color        
        self.break_lines()
        self.create_figure()
        if self.intersects():
            self.state = "gameover"      

    def break_lines(self):
        lines = 0 
        for i in range(1, self.height):
            zeros = 0 
            for j in range(0, self.width):
                if self.field[i][j] == 0:
                    zeros += 1
                
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]        
        self.score += lines ** 2
        self.lines_cleared += lines 
        self.check_level_up() 
    
    def check_level_up(self):
        global level 
        global lines_to_clear 
        if self.lines_cleared >= level:
            level += 1
            lines_to_clear = level 
            self.lines_cleared = 0 
            return True 
        else:
            lines_to_clear = level - self.lines_cleared 
            return False 

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1 
        self.freeze_figure()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze_figure()

    def go_sideways(self, dx):
        previous_x = self.figure.x 
        self.figure.x += dx  
        if self.intersects():
            self.figure.x = previous_x  

    def rotate(self):
        previous_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = previous_rotation   
