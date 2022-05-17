import pygame
import numpy as np


#screen
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
WIN.fill(BG_COLOR)

#board
board = np.zeros((3, 3))

def draw_line():
    pygame.draw.line(WIN, LINE_COLOR, (0, 200), (600, 200), 10)
    pygame.draw.line(WIN, LINE_COLOR, (0, 400), (600, 400), 10)
    pygame.draw.line(WIN, LINE_COLOR, (200, 0), (200, 600), 10)
    pygame.draw.line(WIN, LINE_COLOR, (400, 0), (400, 600), 10)

def mark_square(row, col, player):
    board[row][col] = player

def is_available(row, col):
    return board[row][col] == 0

def is_full():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                return False
    return True

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_line()

        pygame.display.update()



if __name__ == "__main__":
    main()