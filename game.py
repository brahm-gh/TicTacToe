import pygame
import numpy as np


#screen
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
BG_COLOR = (62, 88, 112)
LINE_COLOR = (42, 176, 228)
WIN.fill(BG_COLOR)
CIRCLE_COLOR = (239, 231, 240)
CROSS_COLOR = (147, 54, 119)



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
    board[row][col] = int(player)

def is_available(row, col):
    return board[row][col] == 0

def is_full():
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                return False
    return True

def check_win(player):
    # vertical check
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

        # horizontal check
        for row in range(3):
            if board[row][0] == player and board[row][1] == player and board[row][2] == player:
                draw_horizontal_winning_line(row, player)
                return True

        # asc diagonal check
        if board[2][0] == player and board[1][1] == player and board[0][2] == player:
            draw_asc_diagonal(player)
            return True

        # desc diagonal check
        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            draw_desc_diagonal(player)
            return True

        return False

def draw_vertical_winning_line(col, player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(WIN, color, (col*200 + 100, 15), (col*200 + 100, 585), 18)

def draw_horizontal_winning_line(row, player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(WIN, color, (15, row * 200 + 100), (585, row * 200 + 100), 18)

def draw_asc_diagonal(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(WIN, color, (15, 585), (585, 15), 18)

def draw_desc_diagonal(player):
    if player == 1:
        color = CIRCLE_COLOR
    elif player == 2:
        color = CROSS_COLOR

    pygame.draw.line(WIN, color, (15, 15), (585, 585), 18)

def restart():
    WIN.fill(BG_COLOR)
    draw_line()
    player = 1
    for row in range(3):
        for col in range(3):
            board[row][col] = 0



def main():
    clock = pygame.time.Clock()
    run = True
    player = 1
    game_over = False
    draw_line()
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

                mouseX = event.pos[0]  #x
                mouseY = event.pos[1]  #y

                clicked_row = int(mouseY // 200)
                clicked_col = int(mouseX // 200)

                if is_available(clicked_row, clicked_col):
                    if player == 1:
                        mark_square(clicked_row, clicked_col, 1)
                        check_win(player)
                        if check_win(player):
                            game_over = True
                        player = 2
                    elif player == 2:
                        mark_square(clicked_row, clicked_col, 2)
                        check_win(player)
                        if check_win(player):
                            game_over = True
                        player = 1

                    draw_figures()


                    print(board[:][:])



            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    game_over = False


        pygame.display.update()



if __name__ == "__main__":
    main()