
import pygame
import rgbcolors
from score import TimerScore

class Scene:
    def __init__(self, scene_id, screen, background_color=rgbcolors.springgreen1):
        self._id = scene_id
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._is_valid = True
        self._frame_rate = 60

    def draw(self):
        if self._screen:
            self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        if event.type == pygame.QUIT:
            print('Good bye!')
            self.set_not_valid()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_not_valid()

    def is_valid(self):
        return self._is_valid

    def set_not_valid(self):
        self._is_valid = False

    def update(self):
        pass

    def start_scene(self):
        print('starting {}'.format(self))

    def end_scene(self):
        print('ending {}'.format(self))

    def frame_rate(self):
        return self._frame_rate

    def __str__(self):
        return 'Scene {}'.format(self._id)

class TitleScene(Scene):
    def __init__(self, scene_id, screen, background_color, title, title_color, title_size):
        super().__init__(scene_id, screen, background_color)
        title_font = pygame.font.Font(pygame.font.get_default_font(), title_size)
        self._title = title_font.render(title, True, title_color)
        press_any_key_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self._press_any_key = press_any_key_font.render('Press any key.', True, rgbcolors.black)
        (w, h) = self._screen.get_size()
        self._title_pos = self._title.get_rect(center=(w/2, h/2))
        self._press_any_key_pos = self._press_any_key.get_rect(center=(w/2, h - 50))

    def draw(self):
        super().draw()
        self._screen.blit(self._title, self._title_pos)
        self._screen.blit(self._press_any_key, self._press_any_key_pos)

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self.set_not_valid()

class BlinkingTitle(TitleScene):
    def __init__(self, scene_id, screen, background_color, title, title_color, title_size):
        super().__init__(scene_id, screen, background_color, title, title_color, title_size)
        self._title_text = title
        self._title_size = title_size
        self._title_color = title_color
        self._title_color_complement = (255 - title_color[0], 255 - title_color[1], 255 - title_color[2])
        self._t = 0.0
        self._delta_t = 0.1

    def _interpolate(self):
        self._t += self._delta_t
        if self._t > 1.0 or self._t < 0.0:
            self._delta_t *= -1.0
        a = rgbcolors.mult_color((1.0 - self._t), self._title_color_complement)
        b = rgbcolors.mult_color((self._t), self._title_color)
        c = rgbcolors.sum_color(a, b)
        return c

    def draw(self):
        super().draw()
        title_font = pygame.font.Font(pygame.font.get_default_font(), self._title_size)
        title_color = self._interpolate()
        self._title = title_font.render(self._title_text, True, title_color)

        self._screen.blit(self._title, self._title_pos)


class LevelScene(Scene):
    def __init__(self, scene_id, screen, background_color=rgbcolors.springgreen1, player):
        super().__init__(scene_id, screen, background_color)
        self._player = player
        self._score = TimerScore()
    def draw(self):
        super().draw()
        self._player.draw()
        print('The score is {}'.format(self._score))

    def process_event(self, event):
        if event.type == pygame.QUIT:
            print('Good bye!')
            self.set_not_valid()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.set_not_valid()

    def update(self):
        self._player.update()
        if self._player.is_self_intersecting()
            print("You collided with yourself!")
        self._score.click()