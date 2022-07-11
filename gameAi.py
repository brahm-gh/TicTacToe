import copy
import sys
import pygame
import random
import numpy as np
import logging
import datetime

#Constants
WIDTH = 600
HEIGHT = WIDTH
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
LINE_WIDTH = 15
CIRC_WIDTH = 15
CROSS_WIDTH = 25
CIRCLE_RADIUS = SQUARE_SIZE // 3
OFFSET = 50
BG_COLOR = (62, 88, 112)
LINE_COLOR = (42, 176, 228)
CIRCLE_COLOR = (239, 231, 240)
CROSS_COLOR = (147, 54, 119)
TEXT = 'Game Over'

#Setup
pygame.init()
WINNER_FONT = pygame.font.SysFont('comicsans', WIDTH // 6)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)


# --- CLASSES ---

class Model:

    def __init__(self):
        self.squares = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.empty_sqrs = self.squares  # [squares]
        self.marked_sqrs = 0

    def final_state(self, show=False):
        # vertical wins
        for col in range(BOARD_COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    fPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(BOARD_ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    fPos = (WIDTH - 20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # no win yet
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_squares(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.empty_squares(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    def is_full(self):
        return self.marked_sqrs == 9

    def is_empty(self):
        return self.marked_sqrs == 0


class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player



    def random(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx]  # (row, col)



    def minimax(self, board, maximizing):

        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None  # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.is_full():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move


    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.random(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move  # row, col




class View:

    def __init__(self):
        self.board = Model()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'
        self.running = True
        self.show_lines()

    # --- DRAW METHODS ---

    def show_lines(self):
        screen.fill(BG_COLOR)

        # vertical
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUARE_SIZE, 0), (WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)

        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            # desc line
            start_desc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # asc line
            start_asc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            # draw circle
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRC_WIDTH)


    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def return_gamemode(self):
        return self.gamemode

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'
        logging.basicConfig(level = logging.INFO)
        if self.gamemode == 'ai':
            logging.info('You are in AI mode')
        else:
            logging.info('You are in pear vs pear mode')


    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()

    def reset(self):
        self.__init__()

    def draw_winner(self, text):
        draw_text = WINNER_FONT.render(text, 1, (144, 6, 22))
        screen.blit(draw_text, (WIDTH // 2 - draw_text.get_width() / 2, HEIGHT // 3 - draw_text.get_height() / 2))
        pygame.display.update()




class Controller:
    def main(self):

        game = View()
        board = game.board
        ai = game.ai

        # profiling
    def random_boards(self, n):
        self.view = View()
        empty_sqrs = self.board.get_empty_sqrs()

        for i in range(n):
            idx = random.randrange(0, len(empty_sqrs))
            self.board.mark_square(empty_sqrs[idx][0], empty_sqrs[idx][1], self.player)
        return self.board

    total = 0
    total1 = 0
    n = 9
    for j in range(9):
        for i in range(100):
            board = random_boards(n)
            start = datetime.now()
            main().ai.level = 0
            row, col = eval(board)
            main().game.make_move(row, col)
            end = datetime.now() - start
            total += end
            start1 = datetime.now()

            main().ai.level = 1
            row, col = eval(board)
            main().game.make_move(row, col)
            end1 = datetime.now() - start1
            total1 += end1

            n -= 1

        print('Random AI took: ', total // 100, f'for {n} remaining squares')
        print('Unbeatable AI took: ', total1 // 100, f'for {n} remaining squares')



        while True:


            for event in pygame.event.get():

                # quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # keydown event
                if event.type == pygame.KEYDOWN:

                    # g-gamemode
                    if event.key == pygame.K_g:
                        game.change_gamemode()

                    # r-restart
                    if event.key == pygame.K_r:
                        game.reset()
                        board = game.board
                        ai = game.ai

                    # 0-random ai
                    if event.key == pygame.K_0:
                        ai.level = 0

                    # 1-random ai
                    if event.key == pygame.K_1:
                        ai.level = 1

                # click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1] // SQUARE_SIZE
                    col = pos[0] // SQUARE_SIZE

                    # human mark sqr
                    if board.empty_squares(row, col) and game.running:
                        game.make_move(row, col)

                        if game.isover():
                            game.draw_winner(TEXT)
                            game.running = False

            # AI initial call
            if game.gamemode == 'ai' and game.player == ai.player and game.running:

                # update the screen
                pygame.display.update()

                # eval
                row, col = ai.eval(board)
                game.make_move(row, col)

                if game.isover():
                    game.draw_winner(TEXT)
                    game.running = False

            pygame.display.update()

controller = Controller()
controller.main()