import pygame
from os.path import join
from constants import Colors

WIDTH, HEIGHT = 2000, 1200

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Graphic Solver')

BACKGROUND_COLOR = Colors.CHAMPAGNE_PINK
LINE_COLOR = Colors.LIGHT_SKY_BLUE

FPS = 60

DOT_WIDTH, DOT_HEIGHT = 20, 20
LINE_THICKNESS = 10
DOT_IMAGE = pygame.image.load(join('sprites', 'Dot1.png'))
DOT = pygame.transform.scale(DOT_IMAGE, (DOT_WIDTH, DOT_HEIGHT))

def draw_entities(dots = [], line_dots = []):
    window.fill(BACKGROUND_COLOR)

    number_of_lines = len(line_dots) // 2
    number_of_dots_connected = number_of_lines * 2
    line_dots_paired = line_dots[:number_of_dots_connected]
    for i in range(0, len(line_dots_paired), 2):
        first_dot = line_dots[i]
        second_dot = line_dots[i + 1]

        window.blit(DOT, first_dot.center)
        window.blit(DOT, second_dot.center)

        first_dot_pos = (first_dot.x + DOT_WIDTH, first_dot.y + DOT_HEIGHT)
        second_dot_pos = (second_dot.x + DOT_WIDTH, second_dot.y + DOT_HEIGHT)

        pygame.draw.line(window, LINE_COLOR, first_dot_pos, second_dot_pos, LINE_THICKNESS)
    
    for dot in line_dots[number_of_dots_connected:]:
        window.blit(DOT, dot.center)

    for dot in dots:
        window.blit(DOT, dot.center)

    pygame.display.update()


def main():
    dots = []
    lines = []
    clock = pygame.time.Clock()
    run = True
    dot_mode = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                left, _middle, right = pygame.mouse.get_pressed()
                if right:
                    dot_mode = not dot_mode
                if left:
                    x_click_pos, y_click_pos = pygame.mouse.get_pos()
                    rect_pos = (x_click_pos - DOT_WIDTH, y_click_pos - DOT_WIDTH)
                    new_dot = pygame.Rect(*rect_pos, DOT_WIDTH, DOT_HEIGHT)

                    if dot_mode:
                        dots.append(new_dot)
                        break
                    lines.append(new_dot)

        draw_entities(dots, lines)

    pygame.quit()

if __name__ == "__main__":
    main()
