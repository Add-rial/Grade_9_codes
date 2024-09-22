import pygame
import os
from win32api import GetMonitorInfo, MonitorFromPoint

monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
monitor_area = monitor_info.get("Monitor")
work_area = monitor_info.get("Work")

pygame.init()

x_loc = 0
y_loc = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x_loc, y_loc)

infoObject = pygame.display.Info()
screen_width, screen_height = (infoObject.current_w, infoObject.current_h - (monitor_area[3] - work_area[3]))
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()


def main_game():
    black = (0, 0, 0)

    runner = True

    while runner:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runner = False
        clock.tick(60)
        pygame.display.update()


if __name__ == '__main__':
    main_game()
