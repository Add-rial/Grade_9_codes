import pygame

pygame.init()

infoObject = pygame.display.Info()
screen_width, screen_height = (500, 500)
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


class rectLineCollision:
    def __init__(self, rect, line_start, lineEnd):
        self.rect = rect
        self.line_start = line_start
        self.line_end = lineEnd

    def check(self):
        if self.rect.x < self.line_start[0] < self.rect.x + self.rect.width:
            if self.rect.y < self.line_start[1] < self.rect.y + self.rect.height:
                if self.rect.x < self.line_end[0] < self.rect.x + self.rect.width:
                    if self.rect.y < self.line_end[1] < self.rect.y + self.rect.height:
                        return True
        return False


black = (0, 0, 0)

runner = True

Myrect = pygame.Rect(20, 20, 10, 10)
line1 = ((400, 400), (50, 50))
line2 = ((300, 400), (400, 450))

check = rectLineCollision(Myrect, line1[0], line1[1])

while runner:
    screen.fill(black)

    pygame.draw.line(screen, (255, 255, 255), line1[0], line1[1])
    pygame.draw.line(screen, (255, 255, 255), line2[0], line2[1])
    pygame.draw.rect(screen, (255, 255, 255), Myrect)

    Myrect.x, Myrect.y = pygame.mouse.get_pos()

    blah = check.check()
    print(str(blah))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False

    clock.tick(60)
    pygame.display.update()
