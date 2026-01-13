import pygame
import pygame_menu    # module to make menus in the video game
from pygame.locals import *
import random                   # module to import random numbers for
import math

pygame.init()                           #initializes the game window
pygame.mixer.init()                 # mixer is a pygame module used for music
fps = 120                                            #frames per second
cell_size = 30
top_panel_height = 30                       #top panel is the menu bar where time and flag count appears
left_mouse_click = 1                          # a constant used for the right mouse click
right_mouse_click = 3                       # constant used for right mouse click
font = pygame.font.Font(pygame.font.get_default_font(), 18)         # sets the default font for the
clue_colors = ['blue', 'green', 'red', 'purple', 'maroon', 'turquoise', 'black', 'dimgray']


class Game:
    def __init__(self):
        self.set_difficulty('beginner')
        self.setup_window()
        self.new_game_menu = None
        self.gameover_menu = None
        self.display_new_game_menu()


    def set_difficulty(self, difficulty):
        if difficulty == 'beginner':
            self.size = {'rows': 8, 'cols': 8}
            self.num_mines = 10
        elif difficulty == 'intermediate':
            self.size = {'rows': 16, 'cols': 16}
            self.num_mines = 40
        elif difficulty == 'expert':
            self.size = {'rows': 16, 'cols': 30}
            self.num_mines = 99

    def setup_window(self):
        width = cell_size * self.size['cols']
        height = cell_size * self.size['rows'] + top_panel_height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Minesweeper')

    def new_game(self, difficulty):
        self.gameover = False
        self.set_difficulty(difficulty)
        self.setup_window()
        self.cells = dict()
        self.create_cells()
        self.revealed_count = 0
        self.flag_count = 0
        self.time = 0
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)
        self.new_game_menu.disable()
        if self.gameover_menu is not None:
            self.gameover_menu.disable()
            pygame.mixer.music.stop()

    def display_new_game_menu(self):
        my_theme = pygame_menu.themes.THEME_GREEN
        my_theme.title_font_size = 18
        my_theme.widget_font_size = 15
        self.new_game_menu = pygame_menu.Menu('New Game', 240, 270, theme=my_theme)
        self.new_game_menu.add.button('Beginner', self.new_game_beginner)
        self.new_game_menu.add.button('Intermediate', self.new_game_intermediate)
        self.new_game_menu.add.button('Expert', self.new_game_expert)
        self.new_game_menu.mainloop(self.window, fps_limit=fps)

    def new_game_beginner(self):
        self.new_game('beginner')

    def new_game_intermediate(self):
        self.new_game('intermediate')

    def new_game_expert(self):
        self.new_game('expert')

    def display_gameover_menu(self, heading):
        my_theme = pygame_menu.themes.THEME_SOLARIZED
        my_theme.title_font_size = 18
        my_theme.widget_font_size = 12
        self.gameover_menu = pygame_menu.Menu(heading, 240, 270, theme=my_theme)
        if heading == 'Game Over':
            pygame.mixer.music.load("lose game.mp3")
            pygame.mixer.music.play()
            self.gameover_menu.add.label('You clicked on a mine!')
        elif heading == 'Game Cleared':
            pygame.mixer.music.load("win.mp3")
            pygame.mixer.music.play()
            self.gameover_menu.add.label(f'You won \n Clear Time: {self.time} seconds')
        self.gameover_menu.add.vertical_margin(30)
        self.gameover_menu.add.button('Play Again', self.display_new_game_menu)
        self.gameover_menu.mainloop(self.window, fps_limit=fps)


    def create_cells(self):
        for row in range(self.size['rows']):
            for col in range(self.size['cols']):
                cell = Cell(row, col)
                self.cells[(row, col)] = cell

    def draw_cells(self):
        for (row, col) in self.cells:
            cell = self.cells[(row, col)]
            cell.draw(self.window)

    def draw_top_panel(self):
        top_panel = Rect(0, 0, self.window.get_width(), top_panel_height)
        dark_green = (1,50,32)
        pygame.draw.rect(self.window, dark_green, top_panel)
        time_text = font.render(f'Time: {str(self.time)}', True, (255, 255, 255))
        time_rect = time_text.get_rect()
        time_rect.center = (40, top_panel_height // 2)
        self.window.blit(time_text, time_rect)
        flag_count_text = font.render(f'Flags: {str(self.flag_count)}', True, (255, 255, 255))
        flag_count_rect = flag_count_text.get_rect()
        flag_count_rect.center = (self.window.get_width() - 40, top_panel_height // 2)
        self.window.blit(flag_count_text, flag_count_rect)

    def place_mines(self, clicked_cell):
        mine_count = 0
        while mine_count < self.num_mines:
            row = random.randint(0, self.size['rows'] - 1)
            col = random.randint(0, self.size['cols'] - 1)
            mine_cell = self.cells[(row, col)]
            distance = math.sqrt((row - clicked_cell.row) ** 2 + (col - clicked_cell.col) ** 2)
            if distance > 2 and not mine_cell.has_mine:
                mine_cell.has_mine = True
                mine_count += 1

    def update_clues(self):
        for (row, col) in self.cells:
            cell = self.cells[(row, col)]
            for adjacent_row in range(row - 1, row + 2):
                for adjacent_col in range(col - 1, col + 2):
                    if cell.row == adjacent_row and cell.col == adjacent_col:
                        continue
                    if (adjacent_row, adjacent_col) in self.cells:
                        adjacent_cell = self.cells[(adjacent_row, adjacent_col)]
                        if adjacent_cell.has_mine:
                            cell.clue += 1

    def reveal_all_cells(self):
        for (row, col) in self.cells:
            cell = self.cells[(row, col)]
            self.revealed_count += cell.reveal(self.cells)
    def get_clicked_cell(self, click_location):
        for (row, col) in self.cells:
            cell = self.cells[(row, col)]
            if cell.collidepoint(click_location):
                if cell.has_mine:
                    pygame.mixer.music.load("wrong mine.wav")
                    pygame.mixer.music.play()
                else:
                    pygame.mixer.music.load("click cells.wav")
                    pygame.mixer.music.play()
                return cell
        return None

    def left_click(self, click_location):
        if self.gameover:
            return
        clicked_cell = self.get_clicked_cell(click_location)
        if clicked_cell is not None:
            if self.revealed_count == 0:
                self.place_mines(clicked_cell)
                self.update_clues()
            self.revealed_count += clicked_cell.reveal(self.cells)
            if clicked_cell.has_mine:
                self.gameover = True
            if self.revealed_count == self.size['rows'] * self.size['cols'] - self.num_mines:
                self.gameover = True
                self.display_gameover_menu('Game Cleared')

    def right_click(self, click_location):
        if self.gameover:
            return
        clicked_cell = self.get_clicked_cell(click_location)
        if clicked_cell is not None and clicked_cell.state != 'revealed':
            if clicked_cell.state == 'flagged':
                clicked_cell.state = 'hidden'
                pygame.mixer.music.load("flagged.wav")
                pygame.mixer.music.play()
                self.flag_count -= 1
            else:
                clicked_cell.state = 'flagged'
                self.flag_count += 1
                pygame.mixer.music.load("flagged.wav")
                pygame.mixer.music.play()

    def cheat_reveal_mine_positions(self):
        with open("mine_cheats.txt", "w") as file:
            for (row, col) in self.cells:
                cell = self.cells[(row, col)]
                if cell.has_mine:
                    file.write(f'Mine at position: ({row}, {col})\n')

class Cell(pygame.Rect):     # class nahi hain , ik variable specify kia tha usko call krha
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.left = col * cell_size
        self.top = row * cell_size + top_panel_height
        self.width = cell_size
        self.height = cell_size
        self.state = 'hidden'
        self.has_mine = False
        self.clue = 0

    def draw(self, window):
        if (self.row + self.col) % 2 == 0:
            bg_color = (80, 200, 120)
        else:
            bg_color = (144, 238, 144)
        pygame.draw.rect(window, bg_color, self)
        if self.state == 'revealed':
            if self.has_mine:
                pygame.draw.rect(window, 'crimson', self)
                center_x = self.left + cell_size // 2
                center_y = self.top + cell_size // 2
                pygame.draw.circle(window, 'black', (center_x, center_y), cell_size / 4)
            else:
                if (self.row + self.col) % 2 == 0:
                    pygame.draw.rect(window, 'azure1', self)
                else:
                    pygame.draw.rect(window, 'azure3', self)
                if self.clue > 0:
                    text = font.render(str(self.clue), True, clue_colors[self.clue])
                    text_rect = text.get_rect()
                    center_x = self.left + cell_size // 2
                    center_y = self.top + cell_size // 2
                    text_rect.center = (center_x, center_y)
                    window.blit(text, text_rect)
        if self.state == 'flagged':
            point1 = (self.left + cell_size // 3, self.top + cell_size // 5)
            point2 = (self.left + cell_size // 3, self.top + cell_size // 2)
            point3 = (self.left + cell_size // 3 * 2, self.top + cell_size // 3)
            pygame.draw.polygon(window, 'red', (point1, point2, point3))
            start = (self.left + cell_size // 3, self.top + cell_size // 5)
            end = (self.left + cell_size // 3, self.top + cell_size * 4 // 5)
            pygame.draw.line(window, 'red', start, end)
        start = (self.left, self.top)
        end = (self.left + cell_size, self.top)
        pygame.draw.line(window, 'yellow', start, end)
        start = (self.left + cell_size, self.top)
        end = (self.left + cell_size, self.top + cell_size)
        pygame.draw.line(window, 'yellow', start, end)
        start = (self.left + cell_size, self.top + cell_size)
        end = (self.left, self.top + cell_size)
        pygame.draw.line(window, 'yellow', start, end)
        start = (self.left, self.top + cell_size)
        end = (self.left, self.top)
        pygame.draw.line(window, 'yellow', start, end)


    def reveal(self, cells):
        if self.state == 'revealed' or self.state == 'flagged':
            return 0
        self.state = 'revealed'
        revealed_count = 1
        if self.clue == 0:
            for adjacent_row in range(self.row - 1, self.row + 2):
                for adjacent_col in range(self.col - 1, self.col + 2):
                    if (adjacent_row, adjacent_col) in cells:
                        adjacent_cell = cells[(adjacent_row, adjacent_col)]
                        revealed_count += adjacent_cell.reveal(cells)
        return revealed_count


def main():
    game = Game()                                 #instance of the game class
    clock = pygame.time.Clock()            # pygame clock to control frame rate
    running = True
    cheat_code = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == game.timer_event and not game.gameover:
                game.time += 1
            if event.type == MOUSEBUTTONDOWN:
                if event.button == left_mouse_click:
                    game.left_click(event.pos)
                elif event.button == right_mouse_click:
                    game.right_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.cheat_reveal_mine_positions()
                    cheat_code = False

        game.draw_top_panel()
        game.draw_cells()
        pygame.display.update()
        if game.gameover:
            game.reveal_all_cells()
            game.draw_cells()
            pygame.display.update()
            pygame.time.wait(2000)
            game.display_gameover_menu('Game Over')
    pygame.quit()
main()