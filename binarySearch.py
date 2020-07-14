import pygame
import sys
import random
import math

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon

pygame.init()

width, height = 500, 500

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("binary search")

rows, cols = 20, 20
maxNum = 400

delay = 500 #in milliseconds

myfont = pygame.font.SysFont('Arial', int(height / cols / 2))


arr = [random.randint(0, maxNum) for x in range(rows * cols)]


def partion(low, high):
    i = low - 1

    for j in range(low, high):
        # check if arr[j] is less than the arr[high]
        if arr[j] <= arr[high]:
            # increase index of pivot
            i += 1

            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort(low, high):
    if low < high:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pi = partion(low, high)

        quicksort(low, pi - 1)
        quicksort(pi + 1, high)


quicksort(0, len(arr) - 1)


def drawArray():
    for i in range(len(arr)):
        x = i % rows
        y = math.floor(i / rows)

        text = myfont.render(str(arr[i]), False, (0, 0, 0))
        text_rect = text.get_rect(center=(int(x / rows * width + (width / rows) / 2),
                                          int(y / cols * height + (height / cols) / 2)))
        screen.blit(text, text_rect)
    pygame.display.update()


def drawRectAtIndex(i, color):
    x = i % rows
    y = math.floor(i / rows)

    pygame.draw.rect(screen, color,
                     (int(x / rows * width), int(y / cols * height), int(width / rows), int(height / cols)))


def binarysearch(n):
    left = 0
    right = len(arr) - 1

    while left <= right:
        middle = int((right + left) / 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(pygame.Color(255, 255, 255))

        drawRectAtIndex(left, pygame.Color(255, 0, 0))
        drawRectAtIndex(right, pygame.Color(255, 0, 0))
        drawRectAtIndex(middle, pygame.Color(0, 0, 255))

        drawArray()

        pygame.display.update()

        pygame.time.delay(delay)

        if arr[middle] == n:
            return middle
        elif arr[middle] > n:
            right = middle - 1
        else:
            left = middle + 1

    return -1


def mainLoop(foundIndex):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(pygame.Color(255, 255, 255))
        if foundIndex != -1:
            x = foundIndex % rows
            y = math.floor(foundIndex / rows)

            pygame.draw.rect(screen, pygame.Color(0, 255, 0),
                             (int(x / rows * width), int(y / cols * height), int(width / rows), int(height / cols)))
        drawArray()
        pygame.display.update()

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Sodoku Solver'
        self.left = 100
        self.top = 100
        self.width = 300
        self.height = 100
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.input = QLineEdit(self)
        self.input.move(0, 0)
        self.input.resize(150, 100)
        f = self.input.font()
        f.setPointSize(27)  # sets the size to 27
        self.input.setFont(f)

        # Create a button in the window
        self.button = QPushButton('Find', self)
        self.button.move(150, 0)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
    	try:
    		mainLoop(binarysearch(int(self.input.text())))
    	except ValueError:
    		self.msg = QMessageBox(self)
    		self.msg.setWindowTitle('Error')
    		self.msg.setText("Input must be a number!")
    		self.msg.setIcon(QMessageBox.Critical)
    		x = self.msg.exec_()
    	

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen.fill(pygame.Color(255, 255, 255))
    drawArray()
    pygame.display.update()
    ex = App()
    sys.exit(app.exec_())
