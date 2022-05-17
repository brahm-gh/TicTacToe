import pygame
import numpy as np


#screen
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
WIN.fill(BG_COLOR)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)


#board
board = np.zeros((3, 3))

def draw_line():
    pygame.draw.line(WIN, LINE_COLOR, (0, 200), (600, 200), 10)
    pygame.draw.line(WIN, LINE_COLOR, (0, 400), (600, 400), 10)
    pygame.draw.line(WIN, LINE_COLOR, (200, 0), (200, 600), 10)
    pygame.draw.line(WIN, LINE_COLOR, (400, 0), (400, 600), 10)

def draw_figures():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:
                pygame.draw.circle(WIN, CIRCLE_COLOR, (int(col*200 + 100 ), int(row*200 + 100)), 60, 10)
            elif board[row][col] == 2:
                pygame.draw.line(WIN,CROSS_COLOR , (col*200 + 50, row*200 + 150), (col*200 + 150, row*200 + 50), 15)
                pygame.draw.line(WIN, CROSS_COLOR, (col * 200 + 50, row * 200 + 50),
                                   (col * 200 + 150, row * 200 + 150), 15)


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
    player = 1
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]  #x
                mouseY = event.pos[1]  #y

                clicked_row = int(mouseY // 200)
                clicked_col = int(mouseX // 200)

                if is_available(clicked_row, clicked_col):
                    if player == 1:
                        mark_square(clicked_row, clicked_col, 1)
                        player = 2
                    elif player == 2:
                        mark_square(clicked_row, clicked_col, 2)
                        player = 1

                    draw_figures()




        draw_line()

        pygame.display.update()



if __name__ == "__main__":
    main()