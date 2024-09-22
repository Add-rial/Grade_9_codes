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
