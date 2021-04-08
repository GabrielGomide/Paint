import pygame
import os
from tkinter import *
from tkinter import filedialog
import time

width, height = 700, 600
menuHeight = height - 150

canvas_size = width * (height - menuHeight)

surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('MS Paint')
pygame.display.set_icon(pygame.image.load(os.path.join('Assets', 'icon.png')))
pygame.font.init()
myFont = pygame.font.SysFont('comic', 30)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 0, 230)
ORANGE = (255, 150, 0)
CYAN = (0, 255, 255)

FPS = 60

rect_width = width / 35
rect_height = menuHeight / 25

current_color = BLACK
colors = [RED, GREEN, BLUE, YELLOW, PINK, BLACK, ORANGE, WHITE, CYAN]

pixels = []
filled = []

buttons = ['DRAW', "ERASE", "FILL", "CLEAR"]
file_buttons = ['SAVE', 'OPEN']

current_opt = 'd'

for y in range(25):
	pixels.append([])
	for pixel in pixels:
		for x in range(35):
			pixel.append([WHITE])

def clicked_in(pos, x, y, width, height):
	if pos[0] >= x and pos[0] <= x + width:
		if pos[1] >= y and pos[1] <= y + height:
			return True
	return False

def mouse_down():
	pos = pygame.mouse.get_pos()
	if clicked_in(pos, 0, menuHeight, width, height):
		if clicked_in(pos, 10, menuHeight + 10, 40 * 3, 40 * 3):
			clicked_pallet(pos)
		elif clicked_in(pos, 450, 480, 204, 84):
			clicked_tool(pos)
		elif clicked_in(pos, 200, 500, 205, 40):
			if clicked_in(pos, 200, 500, 100, 40):
				save_file()
			elif clicked_in(pos, 305, 500, 100, 40):
				open_file()
	elif clicked_in(pos, 0, 0, width, menuHeight):
		clicked_canvas(pos)

def clicked_pallet(pos):
	for color in colors:
		x = 10 + 42 * (colors.index(color) % 3)
		y = (menuHeight + (10 + (43 * (colors.index(color) // 3))))
		if clicked_in(pos, x, y, 40, 40):
			global current_color
			current_color = color

def clicked_tool(pos):
	for button in buttons:
		i = buttons.index(button)
		x = 450 + 102 * (i % 2)
		y = (menuHeight + (30 + (42 * (i // 2))))

		if clicked_in(pos, x, y, 102, 42):
			global current_opt
			current_opt = button[0].lower()

	if current_opt == 'c':
		clear_canvas()
		current_opt = 'd'


def clicked_canvas(pos):
	for y in pixels:
		i = 0
		for x in y:
			if clicked_in(pos, i * rect_width, pixels.index(y) * rect_height, rect_width, rect_height):
				if current_opt == 'd':
						x[0] = current_color
				elif current_opt == 'e':
						x[0] = WHITE
				elif current_opt == 'f':
					fill_canvas(i, pixels.index(y), pixels[pixels.index(y)][i][0])
			i += 1

def clear_canvas():
	global pixels
	for y in range(25):
		for x in range(35):
			pixels[y][x][0] = WHITE

def fill_canvas(x, y, color_clicked):
	global pixels

	if (pixels[y][x][0] != color_clicked or color_clicked == current_color):
		pass	
	else:
		pixels[y][x][0] = current_color

		if (y > 0):
			fill_canvas(x, y - 1, color_clicked)

		if (x > 0):
			fill_canvas(x - 1, y, color_clicked)

		if (x < width / rect_width - 1):
			fill_canvas(x + 1, y, color_clicked)

		if (y < menuHeight / rect_height - 1):
			fill_canvas(x, y + 1, color_clicked)


def open_file():
	global pixels

	window =  Tk()
	window.withdraw()
	filename = filedialog.askopenfile(title='Open file', filetypes=[('Windows text file', '*.txt')])

	file = open(filename.name, 'r')

	lines = file.readlines()

	for y in range(25):
		for x in range(35):
			line = lines[y * 35 + x]
			textRgb = line[:-1].split(',')
			color_tuple  = (int(textRgb[0]), int(textRgb[1]), int(textRgb[2]))
			pixels[y][x][0] = color_tuple


def save_file():
	window = Tk()
	window.withdraw()
	filename = filedialog.asksaveasfilename(title='Save file', filetypes=[('Windows text file', '*.txt')])

	try:
		file = open(filename, 'w+')
			
		for y in range(25):
			for x in range(35):
				file.write(f'{pixels[y][x][0][0]},{pixels[y][x][0][1]},{pixels[y][x][0][2]}\n')

		file.close()
	except:
		pass


def draw_window():
	surface.fill(WHITE)
	pygame.draw.line(surface, BLACK, (0, menuHeight), (width, menuHeight), 2)

	global current_color

	for y in pixels:
		i = 0
		for x in y:
			xPos = i * rect_width
			yPos = pixels.index(y) * rect_height

			pos = (xPos, yPos, rect_width, rect_height)

			pygame.draw.rect(surface, x[0], pos, 0)
			i += 1

	for color in colors:
		i = colors.index(color)
		x = 10 + 42 * (i % 3)
		y = (menuHeight + (10 + (42 * (i // 3))))

		out_rect_color = BLACK
		if current_color == color:
			out_rect_color = ORANGE

		pygame.draw.rect(surface, out_rect_color, (x - 1, y - 1, 42, 42), 0)
		pygame.draw.rect(surface, color, (x, y, 40, 40), 0)

	for file_button in file_buttons:
		i = file_buttons.index(file_button)
		x = 200 + 105 * i
		y = (menuHeight + 50)

		text = myFont.render(file_button, False, BLACK)
		pygame.draw.rect(surface, BLACK, (x, y, 100, 40), 2)
		textXPos = x + 105 / 2 - text.get_width() / 2
		textYPos = y + 42 / 2 - text.get_height() / 2
		surface.blit(text, (textXPos, textYPos))

	for button in buttons:
		i = buttons.index(button)
		x = 450 + 102 * (i % 2)
		y = (menuHeight + (30 + (42 * (i // 2))))

		out_rect_color = BLACK
		if current_opt == button[0].lower():
			out_rect_color = ORANGE

		pygame.draw.rect(surface, out_rect_color, (x - 1, y - 1, 102, 42), 2)
		text = myFont.render(button, False, BLACK)
		textXPos = x + 102 / 2 - text.get_width() / 2
		textYPos = y + 42 / 2 - text.get_height() / 2
		surface.blit(text, (textXPos, textYPos))


def main():
	gameOver = False
	clock = pygame.time.Clock()

	while not gameOver:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOver = True

			if pygame.mouse.get_pressed()[0]:
				mouse_down()

		draw_window()
		pygame.display.update()		

if __name__ == '__main__':
	main()
