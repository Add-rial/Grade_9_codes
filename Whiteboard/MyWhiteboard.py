import pygame
import os
##from win32api import GetMonitorInfo, MonitorFromPoint
##
##monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
##monitor_area = monitor_info.get("Monitor")
##work_area = monitor_info.get("Work")

pygame.init()

x_loc = 0
y_loc = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x_loc, y_loc)

infoObject = pygame.display.Info()
screen_width, screen_height = (infoObject.current_w, infoObject.current_h - 40)
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


class Slider:
    def __init__(self, x, y, gap, divisions, radius, color_active=(255, 0, 0), color_passive=(255, 255, 0),
                 color_slider=(0, 255, 255)):
        self.x = x
        self.y = y
        self.width = 2 * radius * divisions + (divisions - 1) * gap
        self.divisions = divisions - 1
        self.gap = gap
        self.height = 2 * radius - 10
        self.color_active = color_active
        self.color_passive = color_passive
        self.color_slider = color_slider

        self.circle_r = radius
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.active = False
        self.value = 0

        self.circle_pos = [self.x + self.gap * self.value + 2 * self.circle_r * self.value,
                           self.y + self.circle_r - 5]

        self.dragging = False
        self.singlePixelPower = self.divisions / self.width

        self.bubble = pygame.transform.scale(pygame.image.load("Whiteboard\\bubble.png"), (40, 40))
        self.currentPower = 1

    def blitter(self, window):
        if self.active:
            pygame.draw.rect(window, self.color_active, self.rect)
        else:
            pygame.draw.rect(window, self.color_passive, self.rect)

        pygame.draw.rect(window, (0, 0, 0), self.rect, 2)

        pygame.draw.circle(window, self.color_slider, self.circle_pos, self.circle_r)

    def handleInput(self, e):
        pos = pygame.mouse.get_pos()
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                if self.rect.collidepoint(pos):
                    self.dragging = True
                    self.circle_pos[0] = pos[0]
                    self.active = True
                else:
                    self.active = False
        if e.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.active = True
                pos_new = pygame.mouse.get_pos()
                x_new = pos_new[0]
                if self.x < x_new < self.x + self.width:
                    self.circle_pos[0] = x_new
            else:
                self.active = False
        else:
            self.active = False

        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                self.dragging = False

    def valueChange(self):
        current_width = self.circle_pos[0] - self.x
        self.currentPower = round(current_width * self.singlePixelPower) + 1

        return self.currentPower

    def isOver(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) or self.active:
            return True
        return False

    def interactive(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) or self.active:
            active = True
            pygame.mouse.set_cursor(pygame.cursors.diamond)
        else:
            active = False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        myFont = pygame.font.SysFont('comicsansms', 16)
        if active:
            screen.blit(self.bubble, (self.circle_pos[0] - 20, self.circle_pos[1] - 40))
            text = myFont.render(str(self.currentPower), True, (0, 0, 0))
            screen.blit(text, (self.circle_pos[0] - 3, self.circle_pos[1] - 35))


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


currentx, currenty = 0, 0
myPoints = []


def locate_xy():
    global currentx, currenty
    currentx, currenty = pygame.mouse.get_pos()


def addLine(pos, pos_new):
    global currentx, currenty, myPoints
    theStoringTuple = pos, pos_new, paint_value, color
    myPoints.append(theStoringTuple)


paint_value = 1
color = (0, 0, 0)


class colorInput:
    def __init__(self, x, y, width, height, color1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color1

        self.rect = pygame.Rect(x, y, width, height)
        self.pos = pygame.mouse.get_pos()

    def blitter(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        self.pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(self.pos):
            pygame.draw.rect(window, (30, 40, 45), self.rect, 3)

    def eventHandler(self, event, currentColor):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(self.pos):
                    return self.color

        return currentColor


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


def main_game():
    global paint_value, color
    runner = True

    paintBrushButton = ButtonImages(screen_width - 150, screen_height - 70, "Whiteboard\paint-brush.png")
    eraserButton = ButtonImages(screen_width - 70, screen_height - 70, "Whiteboard\eraser.png")

    imageButtons = [paintBrushButton, eraserButton]
    clicked = [False, False]

    drawPanel = [screen_width - 206, screen_height]
    drwPanelRect = pygame.Rect(3, 0, 200, screen_height)

    paintBrushCur = pygame.image.load("Whiteboard\paint-brush.png")
    eraserCur = pygame.image.load("Whiteboard\eraser.png")

    cursors = [paintBrushCur, eraserCur]

    white = (255, 255, 255)

    dragging = False

    myFont = pygame.font.SysFont('comicsansms', 25)
    text = myFont.render("Brush Size:", True, (0, 0, 0))
    slider_paint_size = Slider(screen_width - 190, 70, 20, 5, 10)
    slider_eraser_size = Slider(screen_width - 190, 160, 20, 5, 10)

    colorPicker = pygame.image.load("Whiteboard\ColorPicker.png")
    colorPickerRect = colorPicker.get_rect(topleft=(screen_width - 185, 270))

    colorRect = pygame.Rect(screen_width - 185, 470, 175, 40)
    eraser_value = 10
    eraser_rect = pygame.Rect(0, 0, eraser_value*10, eraser_value*10)

    width_i = 30
    height_i = 30
    diff = 10
    black_i = colorInput(screen_width - 185 + 5, 520, width_i, height_i, (0, 0, 0))
    blue_i = colorInput(screen_width - 185 + 10 + width_i + diff, 520, width_i, height_i, (0, 70, 255))
    green_i = colorInput(screen_width - 185 + 15 + 2 * width_i + 2 * diff, 520, width_i, height_i, (0, 255, 26))
    red_i = colorInput(screen_width - 185 + 20 + 3 * width_i + 3 * diff, 520, width_i, height_i, (219, 45, 42))
    brown_i = colorInput(screen_width - 185 + 5, 520 + width_i + diff, width_i, height_i, (165, 42, 42))
    pink_i = colorInput(screen_width - 185 + 10 + width_i + diff, 520 + width_i + diff, width_i, height_i,
                        (255, 105, 180))
    yellow_i = colorInput(screen_width - 185 + 15 + 2 * width_i + 2 * diff, 520 + width_i + diff, width_i, height_i,
                          (223, 255, 0))
    orange_i = colorInput(screen_width - 185 + 20 + 3 * width_i + 3 * diff, 520 + width_i + diff, width_i, height_i,
                          (255, 69, 0))
    i_colors = [black_i, blue_i, green_i, red_i, brown_i, pink_i, yellow_i, orange_i]
    while runner:
        screen.fill(white)
        pos = pygame.mouse.get_pos()

        for i in range(len(myPoints)):
            if myPoints[i][0][0] < screen_width - 200 or myPoints[i][1][0] < screen_width - 200:
                pygame.draw.line(screen, myPoints[i][3], myPoints[i][0], myPoints[i][1], myPoints[i][2])

        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(0, 0, screen_width - 200, screen_height), 3)
        pygame.draw.rect(screen, (204, 222, 224), pygame.Rect(screen_width - 200, 0, 200, screen_height))
        pygame.draw.rect(screen, (204, 222, 224), pygame.Rect(3, screen_height - 40, drawPanel[0] , 20))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(screen_width - 200, 0, 200, screen_height), 3)

        screen.blit(text, (screen_width - 190, 20))
        text2 = myFont.render("Eraser Size:", True, (0, 0, 0))
        screen.blit(text2, (screen_width - 190, 110))
        text3 = myFont.render("Color: ", True, (0, 0, 0))
        screen.blit(text3, (screen_width - 190, 200))
        screen.blit(colorPicker, (screen_width - 185, 270))
        pygame.draw.rect(screen, color, colorRect)

        for event in pygame.event.get():
            slider_paint_size.handleInput(event)
            slider_eraser_size.handleInput(event)

            for h in range(len(i_colors)):
                color = i_colors[h].eventHandler(event, color)

            for i in range(len(imageButtons)):
                if imageButtons[0].isButtonClicked(event):
                    pygame.mouse.set_visible(False)
                    clicked[0] = True
                    clicked[1] = False
                if imageButtons[1].isButtonClicked(event):
                    pygame.mouse.set_visible(False)
                    clicked[1] = True
                    clicked[0] = False
            if event.type == pygame.QUIT:
                runner = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if clicked[0]:
                        locate_xy()
                        dragging = True


            if pygame.mouse.get_pressed(3)[0]:
                if colorPickerRect.collidepoint(pos):
                    color = pygame.Surface.get_at(screen, (currentx, currenty))
                if event.type == pygame.MOUSEMOTION:
                    pos_new = pygame.mouse.get_pos()
                    if colorPickerRect.collidepoint(pos):
                        color = pygame.Surface.get_at(screen, pos_new)

                if clicked[1]:
                    reduced = 0
                    for i in range(len(myPoints)):
                        myx, myy = pygame.mouse.get_pos()
                        eraser_rect.x, eraser_rect.y = myx, myy
                        check = rectLineCollision(eraser_rect, myPoints[i][0], myPoints[i][1])
                        checker = check.check()
                        #print("1")
                        if checker:
                            myPoints.pop(i)
                            #print("2")
                            reduced += 1
                        if i == i - reduced + 1:
                            #print("3")
                            break

            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    pos_new = pygame.mouse.get_pos()
                    if clicked[0]:
                        addLine(pos, pos_new)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

        for i in range(len(imageButtons)):
            imageButtons[i].isOver()
            imageButtons[i].blitter(screen)
            if clicked[i]:
                pos = pygame.mouse.get_pos()
                if pos[0] < screen_width - 200:
                    pygame.mouse.set_visible(False)
                    if i == 0:
                        screen.blit(cursors[i], (pos[0], pos[1] - 24))
                    elif i == 1:
                        myx = pos[0]
                        myy = pos[1]
                        eraser_rect.x = myx
                        eraser_rect.y = myy
                        pygame.draw.rect(screen, (0, 0, 0), eraser_rect, 2)
                else:
                    pygame.mouse.set_visible(True)

        slider_paint_size.blitter(screen)
        slider_eraser_size.blitter(screen)
        if slider_paint_size.isOver():
            slider_paint_size.interactive()
        else:
            if slider_eraser_size.isOver():
                slider_eraser_size.interactive()
            else:
                if colorPickerRect.collidepoint(pos):
                    pygame.mouse.set_cursor(pygame.cursors.broken_x)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        paint_value = slider_paint_size.valueChange()
        eraser_value = slider_eraser_size.valueChange()

        for h in range(len(i_colors)):
            i_colors[h].blitter(screen)

        clock.tick(120)
        pygame.display.flip()
        pygame.display.update()


if __name__ == '__main__':
    main_game()
