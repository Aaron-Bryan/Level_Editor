import pygame
import button
import csv
import pickle

pygame.init()


#Game Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_WINDOW = 100
SIDE_WINDOW = 300

#Screen
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_WINDOW, SCREEN_HEIGHT + LOWER_WINDOW))
pygame.display.set_caption("Level Editor")


#Game Variables
clock = pygame.time.Clock()
FPS = 60

ROWS = 16
MAX_COLUMNS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
current_tile = 0

level = 0

GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

font = pygame.font.SysFont("Futura", 30)

scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

#Background Image Files
pine1_img = pygame.image.load("img/Background/pine1.png").convert_alpha()
pine2_img = pygame.image.load("img/Background/pine2.png").convert_alpha()
mountain_img = pygame.image.load("img/Background/mountain.png").convert_alpha()
sky_img = pygame.image.load("img/Background/sky_cloud.png").convert_alpha()

save_img = pygame.image.load("img/save_btn.png").convert_alpha()
load_img = pygame.image.load("img/load_btn.png").convert_alpha()

tile_list = []
for file in range(TILE_TYPES):
    img = pygame.image.load(f"img/tile/{file}.png")
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

    tile_list.append(img)


WORLD_DATA = []
for row in range(ROWS):
    world_row = [-1] * MAX_COLUMNS
    WORLD_DATA.append(world_row)

for tile in range(0, MAX_COLUMNS):
    WORLD_DATA[ROWS - 1][tile] = 0


def draw_text(text, font, text_color, x, y):
    text_img = font.render(text, True, text_color)
    screen.blit(text_img, (x, y))


#Create Function for Drawing background
def draw_bg():
    screen.fill(GREEN)
    width = mountain_img.get_width()
    for ctr in range(4):
        screen.blit(sky_img, ((ctr * width) - scroll * 0.3, 0))
        screen.blit(mountain_img, ((ctr * width) - scroll * 0.5, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((ctr * width) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((ctr * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

#Function to Create the Grid
def draw_grid():
    #Columns
    for col in range(MAX_COLUMNS + 1):
        pygame.draw.line(screen, WHITE, (col * TILE_SIZE - scroll, 0), (col * TILE_SIZE - scroll, SCREEN_HEIGHT))

    #Rows
    for row in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, row * TILE_SIZE ), (SCREEN_WIDTH, row * TILE_SIZE))


#Draw the tiles onto WORLD_DATA
def draw_world():

    for row_num, row in enumerate(WORLD_DATA):
        for col_num, tile in enumerate(row):
            if tile >= 0:
                screen.blit(tile_list[tile], (col_num * TILE_SIZE - scroll, row_num * TILE_SIZE))


#Buttons
save_button = button.create_button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_WINDOW - 50, save_img, 1)
load_button = button.create_button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_WINDOW - 50, load_img, 1)

button_list = []
button_col = 0
button_row = 0

for ctr in range(len(tile_list)):
    tile_button = button.create_button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, tile_list[ctr], 1)
    button_list.append(tile_button)
    #Postition the next set of buttons after the previous one
    button_col = button_col + 1
    #Position the button on a lower row when the col variable reaches 3
    if button_col == 3:
        button_row = button_row + 1
        button_col = 0


run = True
while run == True:

    clock.tick(FPS)
    draw_bg()
    draw_grid()
    draw_world()


    draw_text(f"Level: {level}", font, WHITE, 10, SCREEN_HEIGHT + LOWER_WINDOW - 90)
    draw_text("Press UP or DOWN to change the level", font, WHITE, 10, SCREEN_HEIGHT + LOWER_WINDOW - 65)

    #Saving Level Data
    if save_button.draw(screen):
        with open(f"level{level}_data.csv", "w", newline="") as file:
            writer =  csv.writer(file, delimiter = ",")

            for row in WORLD_DATA:
                writer.writerow(row)

        #Using pickle removes te need of converting it to a csv file
        """pickle_out = open(f'level{level}_data', 'wb')
        pickle.dump(WORLD_DATA, pickle_out)
        pickle_out.close()"""

    #Loading Level Data
    if load_button.draw(screen):
        #Put scroll position back to original position
        scroll = 0

        with open(f"level{level}_data.csv", newline="") as file:
            reader =  csv.reader(file, delimiter = ",")

            for row_num, row in enumerate(reader):
                for col_num, tile in enumerate(row):
                    WORLD_DATA[row_num][col_num] = int(tile)

        #Using pickle removes te need of converting it to a csv file
        """world_data = []
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)"""

    # Draw side panel for the tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    #Tile selection
    button_count = 0
    for button_count, button in enumerate(button_list):
        if button.draw(screen):
            current_tile = button_count

    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    #Scrolling through the Map
    if scroll_left == True and scroll > 0:
        scroll = scroll - 5 * scroll_speed
    elif scroll_right == True and scroll < (MAX_COLUMNS * TILE_SIZE) - SCREEN_WIDTH:
        scroll = scroll + 5 * scroll_speed

    #Adding new tiles to the world
    #Get mouse position
    pos = pygame.mouse.get_pos()
    mouse_x = (pos[0] + scroll) // TILE_SIZE
    mouse_y = pos[1] // TILE_SIZE

    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        #Update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if WORLD_DATA[mouse_y][mouse_x] != current_tile:
                WORLD_DATA[mouse_y][mouse_x] = current_tile

        if pygame.mouse.get_pressed()[2] == 1:
            WORLD_DATA[mouse_y][mouse_x] = -1


    for event in pygame.event.get():
        #Quit Function
        if event.type == pygame.QUIT:
            run = False

        #On Key Press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level = level + 1
            if event.key == pygame.K_DOWN and level > 0:
                level = level - 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 5

        #On Key Release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1

    pygame.display.update()


pygame.quit()