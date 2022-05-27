import pygame
import numpy as np

pygame.init()

WIDTH = 600
HEIGHT = WIDTH
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH//BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE//3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE//4
BG_COLOR = (62, 88, 112)
LINE_COLOR = (42, 176, 228)
CIRCLE_COLOR = (239, 231, 240)
CROSS_COLOR = (147, 54, 119)
WINNER_FONT = pygame.font.SysFont('comicsans', WIDTH//6)


# SCREEN
WIN = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'TIC TAC TOE' )
WIN.fill( BG_COLOR )

# CONSOLE BOARD
board = np.zeros( (BOARD_ROWS, BOARD_COLS) )

# FUNCTIONS
def draw_lines():
	# 1 horizontal
	pygame.draw.line( WIN, LINE_COLOR, (15, SQUARE_SIZE), (WIDTH-15, SQUARE_SIZE), LINE_WIDTH )
	# 2 horizontal
	pygame.draw.line( WIN, LINE_COLOR, (15, 2 * SQUARE_SIZE), (WIDTH-15, 2 * SQUARE_SIZE), LINE_WIDTH )

	# 1 vertical
	pygame.draw.line( WIN, LINE_COLOR, (SQUARE_SIZE, 15), (SQUARE_SIZE, HEIGHT-15), LINE_WIDTH )
	# 2 vertical
	pygame.draw.line( WIN, LINE_COLOR, (2 * SQUARE_SIZE, 15), (2 * SQUARE_SIZE, HEIGHT-15), LINE_WIDTH )

def draw_figures():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 1:
				pygame.draw.circle( WIN, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
			elif board[row][col] == 2:
				pygame.draw.line( WIN, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )
				pygame.draw.line( WIN, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )

def mark_square(row, col, player):
	board[row][col] = player

def available_square(row, col):
	return board[row][col] == 0

def is_board_full():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 0:
				return False

	return True

def check_win(player):
	# vertical win check
	for col in range(BOARD_COLS):
		if board[0][col] == player and board[1][col] == player and board[2][col] == player:
			draw_vertical_winning_line(col, player)
			return True

	# horizontal win check
	for row in range(BOARD_ROWS):
		if board[row][0] == player and board[row][1] == player and board[row][2] == player:
			draw_horizontal_winning_line(row, player)
			return True

	# asc diagonal win check
	if board[2][0] == player and board[1][1] == player and board[0][2] == player:
		draw_asc_diagonal(player)
		return True

	# desc diagonal win chek
	if board[0][0] == player and board[1][1] == player and board[2][2] == player:
		draw_desc_diagonal(player)
		return True

	return False

def draw_vertical_winning_line(col, player):
	posX = col * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( WIN, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH )

def draw_horizontal_winning_line(row, player):
	posY = row * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( WIN, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH )

def draw_asc_diagonal(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( WIN, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

def draw_desc_diagonal(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == 2:
		color = CROSS_COLOR

	pygame.draw.line( WIN, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )



def draw_winner(text):
	draw_text = WINNER_FONT.render(text, 1, (144, 6, 22))
	WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()/2, HEIGHT//3 - draw_text.get_height()/2))
	pygame.display.update()


def restart():
	WIN.fill( BG_COLOR )
	draw_lines()
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = 0

draw_lines()


# MAINLOOP
def main():
	player = 1
	game_over = False
	run = True
	text = 'Game Over'
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

				mouseX = event.pos[0] # x
				mouseY = event.pos[1] # y

				clicked_row = int(mouseY // SQUARE_SIZE)
				clicked_col = int(mouseX // SQUARE_SIZE)

				if available_square( clicked_row, clicked_col ):

					mark_square( clicked_row, clicked_col, player )
					if check_win( player ):
						game_over = True
						draw_winner(text)
					player = player % 2 + 1

					draw_figures()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					restart()
					player = 1
					game_over = False

		pygame.display.update()
	pygame.quit()


if __name__ == '__main__':
	main()