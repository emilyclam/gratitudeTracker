"""
GRATITUDE LOG

home page
X header text: "GRATITUDE"
X "add gratitude" button which leads to the gratitude page
X "cheer me up" button which leads to the cheer up page
X draw the blocks at the top
    X open the text file
    X format: date text color
    X use for loop to go through all the lines and create the blocks
    - make this a function so i can easily repeat this -

block class
X date, text, color, x, y
X when you click on it, it takes you to a new "page" (function?)

add gratitude page
X text at the top + bg color
X a blinking text line (cursor)
X use key input to make a text thing...
    X typing forward
    X can delete
    - keep it simple and don't worry about moving the cursor
X use enter to continue on to next step


color choosing page
X header text
X use a for loop to draw out all the squares
- check for clicks --> create a Block (array) and write the data in the text file
X move back to the home screen

saving the data
X when you start, read from the file and convert everything to Blocks
X when you exit the program, rewrite everything in the file with everything that's currently
in Blocks

back button class
X current page, page it leads to (x,y is automatically in top right corner?)


cheer me up button
X when clicked it chooses a random block and opens the page
X what happens if the btn gets clicked before any blocks are added?


TODO (BACK-BURNER)
X buttons shouldn't be clickable when you're on a different page
X add more colors
- figure out how to make text fit to width
- if there are too many rows of Blocks on the home page, only show that last 3? (2?) lines and make the rest
scrollable..... (scroll bar? arrows?)
X the BackButtons and Block are on the spot so it clicks both at the same time and won't let you
return to the home page
X make the blinking cursor for the add_grat page
X blocks get doubled when they're saved??
- make buttons interactive
- be able to delete Blocks
    - delete button
    - confirmation page


"""

import pygame
import sys
import datetime
import random

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gratitude")

# GAME VARIABLES
bg_color = (210, 210, 210)
colors = [(247, 241, 171), (203, 247, 171), (171, 247, 219), (171, 206, 247), (182, 171, 247), (247, 171, 214),
          (148, 142, 86), (114, 150, 87), (86, 148, 125), (86, 115, 148), (95, 86, 148), (148, 86, 121)]

SIZE = 60
page = "home"

# TEXT
title_font = pygame.font.SysFont("century gothic", 40, bold=True)
header_font = pygame.font.SysFont("century gothic", 35, bold=True)
body_font = pygame.font.SysFont("century gothic", 25)


# CLASSES


class Button:
    buttons = []

    def __init__(self, screen_name, screen, x, y, width, height, color, text, size, goto):
        self.screen_name = screen_name
        self.screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.center = (x, y)
        self.color = color
        self.goto = goto
        self.font = pygame.font.SysFont("century gothic", size)
        self.text = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(x, y))
        Button.buttons += [self]

    def clicked(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.rect.left <= mouseX <= self.rect.right:
            if self.rect.top <= mouseY <= self.rect.bottom:
                if page == self.screen_name:
                    return True
        return False

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.text, self.text_rect)


class BackButton(Button):
    def __init__(self, screen_name, screen, goto):
        super().__init__(screen_name, screen, 40, SCREEN_HEIGHT-30, 40, 20, bg_color, "<", 20, goto)
        # i can also change the color of the arrow


class ColorSquare:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, SIZE, SIZE)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def hover(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.rect.left <= mouseX <= self.rect.right:
            if self.rect.top <= mouseY <= self.rect.bottom:
                if type(self) == ColorSquare and page == "choose color":
                    return True
                if type(self) == Block and page == "home":
                    return True
        return False

    def clicked(self):
        date = str(datetime.date.today())
        date = date[5:7] + "/" + date[8:10] + "/" + date[:4]
        Block.blocks += [Block(self.color, text, date)]

        # add the *new* Block to the data file
        data = open("data.txt", "a")
        data.write(date + "|" + text + "|" + str(self.color) + "\n")
        data.close()


class Block(ColorSquare):
    blocks = []

    def __init__(self, color, text, date):
        super().__init__(0, 0, color)
        self.text = text
        self.date = date

    def clicked(self):
        # go to a new page that displays a gratitude page
        pass


# FUNCTIONS
def goto(new_page):
    global page
    page = new_page


def read_data():
    data = open("data.txt")
    for line in data.readlines():
        date, text, color = line.strip().split("|")
        color = color[1:-1]
        color = tuple(map(int, color.split(', ')))
        Block.blocks += [Block(color, text, date)]
    data.close()

# HOME PAGE ("home")
home_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
title = title_font.render("G R A T I T U D E", True, (0, 0, 0))
title_rect = title.get_rect(center=(SCREEN_WIDTH / 2, 240))
add_grat_btn = Button("home", home_screen, SCREEN_WIDTH / 2, 290, 300, 40, (194, 101, 113), "A D D  G R A T I T U D E", 15,
                      "add gratitude")
cheer_up_btn = Button("home", home_screen, SCREEN_WIDTH / 2, 330, 300, 25, (220, 220, 220), "c h e e r  m e  u p", 12,
                      "cheer up")
cheer_up_text = header_font.render(":)", True, (0, 0, 0))
cheer_up_rect = cheer_up_text.get_rect(center=(480, 236))
smiley = False

# read in all the data and make the Blocks
read_data()

# hold the new data/blocks (which will be written into the

# ADD GRATITUDE PAGE ("add gratitude")
add_grat_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
add_grat_header = header_font.render("what are you grateful for today?", True, (0, 0, 0))
add_grat_header_rect = add_grat_header.get_rect(center=(SCREEN_WIDTH / 2, 80))
add_grat_continue = body_font.render("press enter to continue", True, (255, 255, 255))
add_grat_continue_rect = add_grat_continue.get_rect(center=(SCREEN_WIDTH / 2, 350))
add_grat_back_btn = BackButton("add gratitude", add_grat_screen, "home")
add_grat_cursor = body_font.render("|", True, (0, 0, 0))
text = ""

# CHOOSE COLOR PAGE ("choose color")
color_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
color_header = header_font.render("nice. how would you describe today?", True, (0, 0, 0))
color_header_rect = color_header.get_rect(center=(SCREEN_WIDTH / 2, 80))
color_back_btn = BackButton("choose color", color_screen, "add gratitude")
color_squares = []
# for loop to create all the color squares (NOT blocks)
for i, color in enumerate(colors):
    color_squares += [ColorSquare(70 + (i % 6) * (SIZE + 20), 200 + (i // 6 * (SIZE + 20)), color)]


# GRATITUDE PAGE ("gratitude")
grat_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
grat_back_btn = BackButton("gratitude", grat_screen, "home")
this_block = None


# GAME LOOP

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            for btn in Button.buttons:
                if btn.clicked():
                    page = btn.goto
            for color_square in color_squares:
                if color_square.hover():
                    color_square.clicked()
                    text = ""
                    page = "home"
            for block in Block.blocks:
                if block.hover():
                    page = "gratitude"
                    this_block = block
        if event.type == pygame.KEYDOWN:
            if page == "add gratitude":
                if event.key == pygame.K_RETURN:
                    page = "choose color"
                    # print(text)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    text = text[:-1]
                else:
                    text += event.unicode

    if page == "home":
        screen.blit(home_screen, (0, 0))
        home_screen.fill(bg_color)
        home_screen.blit(title, title_rect)
        add_grat_btn.draw()
        cheer_up_btn.draw()

        if smiley:
            home_screen.blit(cheer_up_text, cheer_up_rect)

        # draw the Blocks at the top
        for i, block in enumerate(Block.blocks):
            # change the x and y
            block.rect.x = (i % 10) * SIZE
            block.rect.y = (i//10) * SIZE
            block.draw()

    if page == "add gratitude":
        smiley = False

        screen.blit(add_grat_screen, (0, 0))
        add_grat_screen.fill(bg_color)
        add_grat_screen.blit(add_grat_header, add_grat_header_rect)
        add_grat_screen.blit(add_grat_continue, add_grat_continue_rect)
        add_grat_back_btn.draw()

        # user input
        user_in = body_font.render(text, True, (0, 0, 0))
        user_in_rect = user_in.get_rect(center=(SCREEN_WIDTH / 2, 200))
        add_grat_screen.blit(user_in, user_in_rect)

        # cursor
        if pygame.time.get_ticks() % 1000 <= 500:
            add_grat_screen.blit(add_grat_cursor, (SCREEN_WIDTH / 2 + user_in_rect.width / 2 - 3, 185, 10, 10))

    if page == "choose color":
        screen.blit(color_screen, (0, 0))
        color_screen.fill(bg_color)
        color_screen.blit(color_header, color_header_rect)
        for color_square in color_squares:
            color_square.draw()

        color_back_btn.draw()

    if page == "gratitude":
        screen.blit(grat_screen, (0, 0))
        grat_screen.fill(this_block.color)
        grat_back_btn.draw()

        # make the text
        grat_header = header_font.render("on " + this_block.date + " you were grateful for: ", True, (0, 0 ,0))
        grat_header_rect = grat_header.get_rect(center=(SCREEN_WIDTH/2, 80))
        grat_body = body_font.render(this_block.text, True, (0, 0, 0))
        grat_body_rect = grat_body.get_rect(center=(SCREEN_WIDTH/2, 200))

        grat_screen.blit(grat_header, grat_header_rect)
        grat_screen.blit(grat_body, grat_body_rect)

    if page == "cheer up":
        if len(Block.blocks) <= 0:
            print(":)")
            smiley = True
            page = "home"
        else:
            this_block = random.choice(Block.blocks)
            page = "gratitude"

    pygame.display.update()
