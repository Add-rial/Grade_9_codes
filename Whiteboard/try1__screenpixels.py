import pygame
import os

pygame.init()

x_loc = 0
y_loc = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x_loc, y_loc)

infoObject = pygame.display.Info()
screen_width, screen_height = (infoObject.current_w, infoObject.current_h - 60)
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


class ButtonText:
    def __init__(self, x, y, width, height, text="", active=False, colorActive=(0, 255, 255), colorPassive=(0, 0, 0),
                 outline=6,
                 outlineColor=(255, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active = active
        self.colorActive = colorActive
        self.colorPassive = colorPassive
        self.outline = outline
        self.outlineColor = outlineColor

        self.rect = pygame.Rect(x, y, width, height)

        self.font = pygame.font.SysFont('comicsansms', 32)

    def isOver(self):
        pos = pygame.mouse.get_pos()
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                self.active = True
            else:
                self.active = False
        else:
            self.active = False

    def isButtonClicked(self, event):
        if self.active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return True

        return False

    def blitter(self, window):
        if self.active:
            pygame.draw.rect(window, self.colorActive, self.rect)
        else:
            pygame.draw.rect(window, self.colorPassive, self.rect)
        pygame.draw.rect(window, self.outlineColor, self.rect, self.outline)

        text = self.font.render(self.text, True, (255, 255, 255))
        window.blit(self.text, (self.x + (self.width - text.get_width()) / 2,
                                self.y + (self.height - text.get_height()) / 2))


class ButtonImages:
    def __init__(self, x, y, path, active=False, colorActive=(0, 255, 255), colorPassive=(0, 0, 0), outline=2,
                 outlineColor=(255, 0, 0)):
        self.xGap = 15
        self.yGap = 10

        self.x = x - self.xGap
        self.y = y - self.yGap
        self.path = path
        self.active = active
        self.colorActive = colorActive
        self.colorPassive = colorPassive
        self.outline = outline
        self.outlineColor = outlineColor

        self.image = pygame.image.load(path)
        self.width = self.image.get_width() + 2 * self.xGap
        self.height = self.image.get_height() + 2 * self.yGap

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def isOver(self):
        pos = pygame.mouse.get_pos()
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                self.active = True
            else:
                self.active = False
        else:
            self.active = False

    def isButtonClicked(self, event):
        if self.active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return True

        return False

    def blitter(self, window):
        if self.active:
            pygame.draw.rect(window, self.colorActive, self.rect)
        else:
            pygame.draw.rect(window, self.colorPassive, self.rect)
        pygame.draw.rect(window, self.outlineColor, self.rect, self.outline)

        window.blit(self.image, (self.x + self.xGap,
                                 self.y + self.yGap))


def main_game():
    black = (0, 0, 0)

    runner = True

    paintBrush = ButtonImages(screen_width - 150, screen_height - 70, "paint-brush.png")
    eraser = ButtonImages(screen_width - 70, screen_height - 70, "eraser.png")

    imageButtons = [paintBrush, eraser]

    drawPanel = [screen_width - 160, screen_height]

    drawPanelRects = []
    rectsClicked = []
    x_rect = 0
    y_rect = 0
    for rect in range(drawPanel[0]*drawPanel[1]):
        rect = pygame.Rect(x_rect, y_rect, 1, 1)
        drawPanelRects.append(rect)
        x_rect += 1
        y_rect += 1
        rectsClicked.append(False)

    for rect in range(drawPanel[0] * drawPanel[1]):
        pygame.draw.rect(screen, (0, 0, 0), drawPanelRects[rect])

    while runner:
        screen.fill(black)

        for event in pygame.event.get():
            for i in range(len(imageButtons)):
                imageButtons[i].isButtonClicked(event)
            if event.type == pygame.QUIT:
                runner = False

        for i in range(len(imageButtons)):
            imageButtons[i].isOver()
            imageButtons[i].blitter(screen)

        for rect in range(drawPanel[0] * drawPanel[1]):
            if drawPanelRects[rect].collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, (255, 255, 255), drawPanelRects[rect])
            else:
                pygame.draw.rect(screen, (255, 255, 255), drawPanelRects[rect])

        clock.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    main_game()
