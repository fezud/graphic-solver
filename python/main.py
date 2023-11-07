import pygame
from os.path import join
from constants import Colors


WIDTH, HEIGHT = 2000, 1200
BACKGROUND_COLOR = Colors.CHAMPAGNE_PINK
ACCENT_COLOR = Colors.LIGHT_SKY_BLUE
FPS = 60
POINT_SIZE = 15
LINE_THICKNESS = 10
TEXT_COLOR = Colors.JET

AXIS_THICKNESS = 3
AXIS_COLOR = Colors.DIM_GREY

pygame.init()
pygame.font.init()
MODE_FONT = pygame.font.SysFont('Consolas', 40)
INFO_FONT = pygame.font.SysFont('Consolas', 20)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Graphic Solver')


class Point:
    def __init__(self, x, y):
        self.x_abs = x
        self.y_abs = y

        self.x_draw = int((WIDTH/2.0) + x)
        self.y_draw = int((HEIGHT/2.0) - y)

    @classmethod
    def from_abs(cls, x, y):
        return cls(x, y)
    
    @classmethod
    def from_draw(cls, x, y):
        x_abs = -((WIDTH/2.0) - x)
        y_abs = (HEIGHT/2.0) - y
        return cls(x_abs, y_abs)
    
    @property
    def abs_coord(self):
        return (self.x_abs, self.y_abs)
    
    @property
    def draw_coord(self):
        return (self.x_draw, self.y_draw)
    
    def draw(self, screen):
        pygame.draw.circle(screen, ACCENT_COLOR, self.draw_coord, POINT_SIZE)

    def draw_info(self, pos, screen):
        (x, y) = pos
        if x > self.x_draw + POINT_SIZE or x < self.x_draw - POINT_SIZE:
            return
        if y > self.y_draw + POINT_SIZE or y < self.y_draw - POINT_SIZE:
            return
        
        txt_string_abs = f" Abs x: {self.x_abs}, y: {self.y_abs}"
        txt_string_draw = f"Draw x: {self.x_draw}, y: {self.y_draw}"

        text_abs = INFO_FONT.render(txt_string_abs, True, TEXT_COLOR)
        text_draw = INFO_FONT.render(txt_string_draw, True, TEXT_COLOR)

        text_place_abs = text_abs.get_rect(center=(self.x_draw, self.y_draw - 3*POINT_SIZE))
        text_place_draw = text_draw.get_rect(center=(self.x_draw, self.y_draw - 1.5*POINT_SIZE))

        screen.blit(text_abs, text_place_abs)
        screen.blit(text_draw, text_place_draw)


class Line:
    def __init__(self, points: tuple):
        for point in points:
            if not isinstance(point, Point): raise TypeError
        self.points = points

    
    def draw(self, window):
        (point1, point2) = self.points
        point1.draw(window)
        point2.draw(window)
        pygame.draw.line(window, ACCENT_COLOR, point1.draw_coord, point2.draw_coord, LINE_THICKNESS)


def draw_text(point_addition_mode: bool):
    txt_string = "Point Addition Mode" if point_addition_mode else "Line Addition Mode"
    text = MODE_FONT.render(txt_string, True, TEXT_COLOR)
    text_place = text.get_rect(center=(WIDTH - 250, HEIGHT - 50))
    window.blit(text, text_place)


def draw_axis():
    pygame.draw.line(window, AXIS_COLOR, (WIDTH/2, 0), (WIDTH/2, HEIGHT), AXIS_THICKNESS)
    pygame.draw.line(window, AXIS_COLOR, (0, HEIGHT/2), (WIDTH, HEIGHT/2), AXIS_THICKNESS)


def draw_follow_mouse_line(prev_point, pos):
    if not prev_point: return
    pygame.draw.line(window, ACCENT_COLOR, prev_point.draw_coord, pos, AXIS_THICKNESS)


def main():
    prev_point = None
    points = []
    lines = []
    run = True
    point_addition_mode = True  # True - adding points, False - adding lines

    clock = pygame.time.Clock()
    while run:
        window.fill(BACKGROUND_COLOR)  # filling background with color
        draw_axis()
        clock.tick(FPS)  # 60 fps limit
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # handling quitting the game (red cross in the top right)
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # handling mouse button presses
                left, _middle, right = pygame.mouse.get_pressed()  # getting which button was pressed
                if right:
                    point_addition_mode = not point_addition_mode  # right is for changing mode
                if left:
                    point = Point.from_draw(*pos)

                    if point_addition_mode:
                        points.append(point)
                        prev_point = None
                        break

                    if prev_point:
                        line = Line((prev_point, point))
                        lines.append(line)
                        prev_point = None
                        break

                    prev_point = point

        draw_follow_mouse_line(prev_point, pos)

        for point in points:  # drawing added elements
            point.draw(window)
            point.draw_info(pos, window)
        
        for line in lines:  # drawing added elements
            line.draw(window)
            for point in line.points:
                point.draw_info(pos, window)

        draw_text(point_addition_mode)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
