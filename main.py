import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

DEBUG = not True

FPS = 120
is_fullscreen = False

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.font.init()
font_cs = pygame.font.SysFont('Comic Sans MS', 30)

spaceship = pygame.image.load('assets/spaceship.png')
spaceship = pygame.transform.scale(spaceship, (WIDTH, HEIGHT))

progress_image = pygame.image.load('assets/sp2.png')
progress_image = pygame.transform.scale(progress_image, (32, 32))
progress_image = pygame.transform.rotate(progress_image, 270)
pi_x = WIDTH // 4
pi_y = 5
pi_inc = 0
pi_done = False

background = pygame.image.load('assets/background-2.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

pygame.display.set_caption("D-Day 3135")

clock = pygame.time.Clock()

text_elements = []
asteroids_list = []

bg_x = 0
bg_y = 0

game_over_bd = pygame.image.load('assets/db.gif')
game_over_bd = pygame.transform.scale(game_over_bd, (WIDTH, HEIGHT))
game_over_banner = pygame.image.load('assets/gameovertext.png')
game_over_banner = pygame.transform.scale(game_over_banner, (WIDTH, HEIGHT))


def toggle_fullscreen():
    global is_fullscreen, screen, spaceship, WIDTH, HEIGHT
    if is_fullscreen:
        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Windowed mode
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Fullscreen mode
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()

    update_components()
    is_fullscreen = not is_fullscreen


def add_text_element(text, pos_x, pos_y, lev_as=None):
    global text_elements

    if type(pos_x) == int:
        pos_x = str(pos_x)

    if type(pos_y) == int:
        pos_y = str(pos_y)

    t1 = font_cs.render(text, True, (200, 200, 200))
    t1_rect = t1.get_rect(center=(eval(pos_x), eval(pos_y)))
    text_elements.append([t1, t1_rect, {
        u'width': pos_x,
        u'height': pos_y,
        u'associated_level': lev_as if lev_as is not None else LEVEL
    }])


def update_components(rec=False):
    global spaceship, background, text_elements, lv, game_over_bd, game_over_banner

    if not rec:
        if LEVEL == 1:
            # spaceship = pygame.transform.scale(spaceship, (WIDTH, HEIGHT))
            # background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            lv.update_components()

        elif LEVEL == 2:
            lv.loop()

        elif LEVEL == 3:
            lv.update_components()

        elif LEVEL == 4:
            lv.update_components()

        elif LEVEL == SHOW_MENU:
            lv.loop()

        elif LEVEL == SHOW_WINSCREEN:
            lv.update()

    for i in text_elements:
        if i[-1]['associated_level'] == LEVEL:
            i[1] = i[0].get_rect(center=(eval(i[-1]['width']), eval(i[-1]['height'])))

    game_over_bd = pygame.transform.scale(game_over_bd, (WIDTH, HEIGHT))
    game_over_banner = pygame.transform.scale(game_over_banner, (WIDTH, HEIGHT))


def draw_vertical_gradient(start_color, end_color, width, height):
    for y in range(height):
        # Interpolate the color for each line (y)
        ratio = y / height
        r = start_color[0] + (end_color[0] - start_color[0]) * ratio
        g = start_color[1] + (end_color[1] - start_color[1]) * ratio
        b = start_color[2] + (end_color[2] - start_color[2]) * ratio

        # Draw a horizontal line with the interpolated color
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (width, y))


og_spaceship_instance = spaceship


class HomePage:
    bg = None
    txts = None
    s_pressed = False
    i_pressed = False
    level = None
    i_state_fs = False

    def __init__(self):
        self.config()

    def config(self):
        self.bg = pygame.image.load('assets/gargantua.jpg')
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        self.txts = [{
            'content': 'Welcome to DD3135!',
            'px': '100',
            'py': 'HEIGHT // 4',
            'size': 60,
            'color': (232, 64, 64)
        }, {
            'content': 'Press S to start',
            'px': '100',
            'py': 'HEIGHT // 2.5',
            'size': 40,
            'color': (232, 64, 64)
        },
            {
                'content': 'Press I for instructions',
                'px': '100',
                'py': 'HEIGHT // 2',
                'size': 40,
                'color': (64, 64, 232)
            },
            {
                'content': 'Press F to toggle fullscreen',
                'px': '100',
                'py': 'HEIGHT // 1.1',
                'size': 40,
                'color': (64, 232, 64)
            }]

    def handle_events(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_s] and not self.s_pressed:
            self.txts.append({
                'content': 'Enter Level number (1-4)',
                'px': '100',
                'py': 'HEIGHT // 1.5',
                'size': 40,
                'color': (0, 255, 0)
            })
            self.s_pressed = True

        if keys[pygame.K_i] and not self.i_pressed:
            self.i_pressed = True
            self.i_state_fs = is_fullscreen

        if self.s_pressed:
            if keys[pygame.K_1]:
                self.level = 1
            elif keys[pygame.K_2]:
                self.level = 2
            elif keys[pygame.K_3]:
                self.level = 3
            elif keys[pygame.K_4]:
                self.level = 4

            elif keys[pygame.K_b]:
                self.level = None
                self.s_pressed = False

                try:
                    self.txts.remove({
                        'content': 'Enter Level number (1-3)',
                        'px': '100',
                        'py': 'HEIGHT // 1.5',
                        'size': 40,
                        'color': (0, 255, 0)
                    })
                except ValueError:
                    pass

        if self.i_pressed:
            self.i_pressed = False
            if not is_fullscreen:
                toggle_fullscreen()

            self.i_pressed = True
            self.txts.clear()

            msg = """
            The game is set in the year 3135, where astronaut and journalist Orion Drake 
            sets on the mission to uncover the secrets of Area 51k, also known as 'Area of the melts'. 
            A collection of dwarf planets that were once a home to many nuclear plants, 
            the facility was shut down in 3067, without adequate explanation for the same.
            Under a secret mission carried by scientists who once worked for the government, funded
            by OPHRA (Oil Pharmacy Housing Retail and Allies), Drake sets off into the mysterious wanderlust.
            Unfortunately he gets spotted by the government and is forced to make a run. Help him on his escape
            mission to uncover any and every detail captured by him on A51k, before he gets hunted down by the
            "Harbingers of Democracy".\n
            Press B to go back to menu.
            """
            msg = msg.split('\n')
            msg = [i.strip() for i in msg]
            msg = [i for i in msg if i]

            c = 50
            for i in msg:
                self.txts.append({
                    'content': i,
                    'px': '100',
                    'py': str(c),
                    'size': 20,
                    'color': (0, 255, 0)
                })
                c += 30

            if keys[pygame.K_b]:
                self.i_pressed = False
                self.config()

                if self.i_state_fs != is_fullscreen:
                    toggle_fullscreen()
                    self.i_pressed = is_fullscreen

    def loop(self):
        self.handle_events()
        self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))

        screen.blit(self.bg, (0, 0))

        if self.i_pressed:
            pygame.draw.rect(screen, (32, 32, 32), (0, 0, WIDTH, HEIGHT))

        self.add_text()
        pygame.display.update()

    def add_text(self):
        for i in self.txts:
            ft = pygame.font.SysFont('Consolas', i['size'])
            tel = ft.render(i['content'], True, i['color'])
            screen.blit(tel, (eval(i['px']), eval(i['py'])))


class Alien:
    frames = None
    frame_index = 0
    frame_delay = 240
    last_update_time = 0
    coord_x = 0
    coord_y = 0
    scale_x = 32
    scale_y = 32

    def __init__(self):
        self.coord_x = random.randint(WIDTH // 3, int(WIDTH / 1.7))
        self.coord_y = random.randint(HEIGHT // 3, HEIGHT // 2)
        self.frames = [pygame.image.load(f'assets/alien/Alien{x}.png') for x in range(1, 9)]
        self.last_update_time = pygame.time.get_ticks()

    def add(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_update_time = current_time

        ci = pygame.transform.scale(self.frames[self.frame_index], (self.scale_x, self.scale_y))

        screen.blit(ci, (self.coord_x, self.coord_y))

    def check_gunfire(self):
        if (self.coord_x < WIDTH // 1.8 < self.coord_x + self.scale_x) and \
                (self.coord_y < HEIGHT // 1.8 < self.coord_y + self.scale_y):
            return True

        return False

    def print(self):
        print(f"""{{
            frame_index: {self.frame_index},
            frame_delay: {self.frame_delay},
            last_update_time: {self.last_update_time}
            coord_x: {self.coord_x},
            coord_y: {self.coord_y},
            scale_x: {self.scale_x},
            scale_y: {self.scale_y},
            }}
        """)


class Alien2:
    img = None
    coord_x = 0
    coord_y = 0
    scale_x = 32
    scale_y = 32
    rn = 1

    health = 100

    coord_str_x = None
    coord_str_y = None

    def __init__(self):
        self.rn = random.randint(2, 5)
        self.config()

    def config(self):
        # self.img = pygame.image.load(f'assets/lev3assets/a{self.rn}.png')
        self.img = pygame.image.load(f'assets/lev3assets/a2.png')
        self.img = pygame.transform.scale(self.img, (self.scale_x, self.scale_y))

    def set_coords(self, x, y):
        self.coord_x = x
        self.coord_y = y
        self.coord_str_x = str(self.coord_x)
        self.coord_str_y = str(self.coord_y)

    def set_scale(self, x, y):
        self.scale_x = x
        self.scale_y = y

    def update(self):
        self.coord_x = eval(self.coord_str_x)
        self.coord_y = eval(self.coord_str_y)
        self.config()

    def reduce_health(self, n):
        self.health -= n

    def check_fire(self):
        # ignore y-coord check for optimization
        return (self.coord_x < WIDTH // 2 < self.coord_x + self.scale_x) or self.health <= 0

    def display(self):
        self.update()
        screen.blit(self.img, (self.coord_x, self.coord_y))

        clr = (0, 255, 0)

        if 30 < self.health < 70:
            clr = (255, 255, 0)
        elif self.health < 30:
            clr = (255, 0, 0)

        pygame.draw.rect(
            screen,
            clr,
            (
                WIDTH // 2 - 100,
                HEIGHT // 20,
                self.health * 2,
                50
            ), border_radius=10
        )


class Level1:
    spaceship = None
    og_spaceship_instance = None
    background = None
    progress_image = None

    pi_x = WIDTH // 4
    pi_y = 5
    pi_inc = 0
    pi_done = False

    bg_x = 0
    bg_y = 0

    asteroids_list = None
    show_levelinfo = True

    bgm = None
    bgm_is_playing = False

    def __init__(self):
        pygame.display.set_caption('Level 1')
        self.config()

    def config(self):
        self.spaceship = pygame.image.load('assets/spaceship.png')
        self.spaceship = pygame.transform.scale(self.spaceship, (WIDTH, HEIGHT))

        self.og_spaceship_instance = self.spaceship

        self.background = pygame.image.load('assets/background-2.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.progress_image = pygame.image.load('assets/sp2.png')
        self.progress_image = pygame.transform.scale(self.progress_image, (32, 32))
        self.progress_image = pygame.transform.rotate(self.progress_image, 270)
        self.asteroids_list = []

        self.bgm = pygame.mixer.Sound(f'assets/audio/Level_1.mp3')

        self.pi_x = WIDTH // 4
        self.pi_y = 5
        self.pi_inc = 0
        self.pi_done = False

        self.bg_x = 0
        self.bg_y = 0

    def handle_events(self):
        global running, LEVEL
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Toggle fullscreen with F key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                toggle_fullscreen()
                self.og_spaceship_instance = self.spaceship

            # Exit the game with Escape key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                LEVEL = SHOW_MENU
                break

            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                if self.pi_done:
                    LEVEL = 2
                if self.show_levelinfo:
                    self.show_levelinfo = False
                break

            if event.type == pygame.KEYUP:
                self.spaceship = self.og_spaceship_instance

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            for i in self.asteroids_list:
                i['pos_x'] = i['pos_x'] + i['size']

            if self.spaceship == self.og_spaceship_instance:
                self.spaceship = pygame.transform.rotate(self.spaceship, 1)

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            for i in self.asteroids_list:
                i['pos_x'] = i['pos_x'] - i['size']

            if self.spaceship == self.og_spaceship_instance:
                self.spaceship = pygame.transform.rotate(self.spaceship, -1)

        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            for i in self.asteroids_list:
                i['pos_y'] = i['pos_y'] + i['size']

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            for i in self.asteroids_list:
                i['pos_y'] = i['pos_y'] - i['size']

    def loop(self):
        global gameover
        self.handle_events()

        if self.show_levelinfo:
            font = pygame.font.SysFont('Consolas', 20)
            msg = """Escape the asteroid belt and reach planet 'Salvanos'\nto send out an SOS signal to OPHRA.\nUse WASD or arrow keys to steer your spaceship\naway from incoming asteroids.\nPress N to continue. """
            msg = msg.split('\n')

            screen.blit(self.background, (bg_x, bg_y))
            c = 50
            for i in msg:
                screen.blit(font.render(i, True, (255, 255, 255)), (100, 100 + c))
                c += 50
            pygame.display.flip()
            clock.tick(FPS)
            return

        screen.blit(self.background, (bg_x, bg_y))
        if not self.bgm_is_playing:
            self.bgm_is_playing = True
            self.bgm.play()

        if self.pi_done:
            font = pygame.font.SysFont('Consolas', 50)
            lc_text = font.render('Level Cleared!', True, (64, 64, 64))
            screen.blit(lc_text, (WIDTH // 4, 50))

            pn = font.render('Press N to proceed', True, (200, 200, 200))
            screen.blit(pn, (WIDTH // 4, HEIGHT // 1.1))

            pygame.display.flip()
            clock.tick(FPS)
            return

        for i in self.asteroids_list:
            at = pygame.image.load('assets/asteroid.png')
            at = pygame.transform.scale(at, (i['size'], i['size']))

            if i['pos_x'] > WIDTH // 2:
                screen.blit(at, (i['pos_x'] + 50 - i['size'], i['pos_y']))
            else:
                screen.blit(at, (i['pos_x'] - 50 + i['size'], i['pos_y']))

            at_w, at_h = at.get_size()
            if at_w * at_h > (WIDTH * HEIGHT) // 1.2 and i['pos_x'] in [WIDTH // 4, 0.75 * WIDTH] and i['pos_y'] in [
                HEIGHT // 4, 0.75 * HEIGHT]:
                gameover = True
                break

            i['size'] += 20

        screen.blit(self.spaceship, (0, 0))

        for i in text_elements:
            screen.blit(i[0], i[1])

        if self.pi_done:
            pygame.draw.rect(screen, (16, 16, 16), (WIDTH // 4, 5, WIDTH // 2 + 32, 32))
            screen.blit(self.progress_image, (WIDTH - WIDTH // 4, 5))
        else:
            pygame.draw.rect(screen, (16, 16, 16), (WIDTH // 4, 5, WIDTH // 2 + 32, 32))
            screen.blit(self.progress_image, (self.pi_x, self.pi_y))

        pygame.display.flip()

        if len(self.asteroids_list) < 5:
            self.asteroids_list.append({
                u'pos_x': random.randint(0, WIDTH),
                u'pos_y': random.randint(0, HEIGHT),
                u'size': 50,
            })

        for i in self.asteroids_list:
            # print (i)
            if i['size'] > HEIGHT:
                wh = WIDTH // 2
                wy = HEIGHT // 2
                if i['pos_x'] > wh:
                    if i['pos_x'] - i['size'] < wh:
                        if i['pos_y'] < wy:
                            if i['pos_y'] + i['size'] > wy:
                                gameover = True
                else:
                    if i['pos_x'] + i['size'] > wh:
                        if i['pos_y'] < wy:
                            if i['pos_y'] + i['size'] < wy:
                                gameover = True
                self.asteroids_list.remove(i)
            if i['pos_x'] < 0 or i['pos_x'] > WIDTH:
                self.asteroids_list.remove(i)
            elif i['pos_y'] < 0 or i['pos_y'] > HEIGHT:
                self.asteroids_list.remove(i)

        if self.pi_x < (WIDTH // 2 + WIDTH // 4):
            self.pi_inc += 0.002 * WIDTH
            # self.pi_inc += 0.05 * WIDTH
            self.pi_x = (WIDTH // 4) + self.pi_inc
        else:
            self.pi_done = True

        clock.tick(FPS)

    def update_components(self):
        self.spaceship = pygame.transform.scale(self.spaceship, (WIDTH, HEIGHT))
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def __del__(self):
        self.bgm.fadeout(1500)


class Level2:
    surface = None
    gun = None
    gunfired = None
    gd = 0
    gdp = 0
    surf_x = 0
    surf_y = 0
    aliens = []
    crosshair = None
    addgunfire = False
    progress_image = None
    pi_done = False
    pi_x = WIDTH // 4
    pi_y = 5
    pi_inc = 0
    dome = None
    dome_sx = 0.1
    dome_sy = 0.1
    dome_dh = 0
    dome_dw = 0
    show_levelinfo = True

    bgm = None
    gunshot = None

    def __init__(self):
        self.surface = pygame.image.load('assets/surface.jpeg')
        self.surface = pygame.transform.scale(self.surface, (WIDTH * 2, HEIGHT * 2))

        self.gun = pygame.image.load('assets/gunfpp.png')
        self.gun = pygame.transform.scale(self.gun, (WIDTH, HEIGHT))

        self.gunfired = pygame.image.load('assets/gunfired.png')
        self.gunfired = pygame.transform.scale(self.gunfired, (WIDTH, HEIGHT))

        self.crosshair = pygame.image.load('assets/crosshair.png')
        self.crosshair = pygame.transform.scale(self.crosshair, (32, 32))
        self.aliens.append(Alien())

        self.progress_image = pygame.image.load('assets/alien/Alien1.png')
        self.progress_image = pygame.transform.scale(self.progress_image, (32, 32))
        self.progress_image = pygame.transform.flip(self.progress_image, True, False)

        self.dome = pygame.image.load('assets/dome.png')
        self.dw, self.dh = self.dome.get_size()
        self.dome = pygame.transform.scale(self.dome, (0.25 * self.dw, 0.25 * self.dh))

        pygame.display.set_caption('Level 2')

        self.pi_done = False
        self.pi_x = WIDTH // 4
        self.pi_y = 5
        self.pi_inc = 0

        self.bgm = pygame.mixer.Sound('assets/audio/Level_2.mp3')
        self.bgm.play()

        self.gunshot = pygame.mixer.Sound('assets/audio/gunshots/pistol.mp3')
        self.gunshot.set_volume(1)

    def handle_events(self):
        global running, LEVEL

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Toggle fullscreen with F key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                toggle_fullscreen()

            # Exit the game with Escape key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                LEVEL = SHOW_MENU

            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                if self.pi_done:
                    LEVEL = 3
                if self.show_levelinfo:
                    self.show_levelinfo = False
                break

        if self.pi_done:
            return

        self.addgunfire = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                k = event.key
                if k == pygame.K_SPACE:
                    self.addgunfire = True
                    # self.gunshot.stop()
                    # self.gunshot.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.surf_x < 0:
                self.surf_x += 0.003 * WIDTH

                for i in self.aliens:
                    i.coord_x += 0.003 * WIDTH

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.surf_x > -HEIGHT:
                self.surf_x -= 0.003 * WIDTH

                for i in self.aliens:
                    i.coord_x -= 0.003 * WIDTH

        elif keys[pygame.K_SPACE]:
            self.addgunfire = True
            self.gunshot.stop()
            self.gunshot.play()

    def loop(self):
        global gameover

        self.handle_events()
        screen.blit(self.surface, (self.surf_x, self.surf_y))

        if self.show_levelinfo:
            font = pygame.font.SysFont('Consolas', 20)
            msg = """Congratulations on making it so Salvanos.\nHead over to the OPHRA Automated Research Facility\nto send an SOS signal.\nKill all aliens that come in your way.\nUse AD or arrow keys to move and space to shoot.\nPress N to proceed. """
            msg = msg.split('\n')

            c = 50
            for i in msg:
                screen.blit(font.render(i, True, (0, 0, 0)), (100, 200 + c))
                c += 50

            pygame.display.flip()
            clock.tick(FPS)
            return

        if self.pi_done:
            screen.blit(self.dome, (WIDTH // 3, HEIGHT // 3))

            font = pygame.font.SysFont('Consolas', 50)
            lc_text = font.render('Level Cleared!', True, (64, 64, 64))
            screen.blit(lc_text, (WIDTH // 4, 50))

            pn = font.render('Press N to proceed', True, (200, 200, 200))
            screen.blit(pn, (WIDTH // 4, HEIGHT // 1.1))

            pygame.display.flip()
            clock.tick(FPS)
            return

        if not self.aliens:
            self.aliens.append(Alien())

        for i in self.aliens:
            # i.print()
            i.add()
            i.scale_x += 0.003 * WIDTH
            i.scale_y += 0.003 * HEIGHT

            if i.coord_x + i.scale_x - WIDTH > 0.6 * WIDTH:
                self.aliens.remove(i)

            if i.coord_x + i.scale_x >= WIDTH and i.coord_y + i.scale_y >= HEIGHT:
                gameover = True
                break

        if self.addgunfire:
            screen.blit(self.gunfired, (0, self.gdp))
            for i in self.aliens:
                if i.check_gunfire():
                    self.aliens.remove(i)

                elif self.surf_x < -HEIGHT or self.surf_y > 0:
                    self.aliens.remove(i)
        else:
            screen.blit(self.gun, (0, self.gdp))
        # pygame.draw.circle(screen, (255, 0, 0), (WIDTH // 1.6, HEIGHT // 1.6), 32, 10)
        screen.blit(self.crosshair, (WIDTH // 2, HEIGHT // 2))

        if self.pi_done:
            pygame.draw.rect(screen, (16, 16, 16), (WIDTH // 4, 5, WIDTH // 2 + 32, 32), 3, border_radius=5)
            screen.blit(self.progress_image, (WIDTH - WIDTH // 4, 5))
        else:
            pygame.draw.rect(screen, (16, 16, 16), (WIDTH // 4, 5, WIDTH // 2 + 32, 32), 3, border_radius=5)
            screen.blit(self.progress_image, (self.pi_x, self.pi_y))

        if self.pi_x < (WIDTH // 2 + WIDTH // 4):
            self.pi_inc += 0.0002 * WIDTH
            # self.pi_inc += 0.01 * WIDTH
            self.pi_x = (WIDTH // 4) + self.pi_inc
        else:
            self.pi_done = True

        pygame.display.flip()
        clock.tick(FPS)
        self.update_components()

    def update_components(self):
        self.surface = pygame.transform.scale(self.surface, (WIDTH * 2, HEIGHT * 2))
        self.gun = pygame.transform.scale(self.gun, (WIDTH * 1.2, HEIGHT * 1.5))
        self.gunfired = pygame.transform.scale(self.gunfired, (WIDTH * 1.2, HEIGHT * 1.5))

        if self.gd:
            self.gdp -= 0.5
        else:
            self.gdp += 0.5

        if self.gdp > 0.02 * HEIGHT:
            self.gd = 1
            self.gdp = 0.019 * HEIGHT
        if self.gdp < 0:
            self.gd = 0
            self.gdp = 1

    def __del__(self):
        self.bgm.stop()


class Level4:
    surf = None
    gun = None
    firegun = None

    gx = 0
    gy = 0
    ginc = 0
    ginc_reset = 0
    shift_ginc = False
    gflipped = False

    alien_spawn_range_x = None
    alien_spawn_range_y = None
    aliens = None

    gunfired = None

    countdown = 45
    clt = None
    show_levelinfo = True

    bgm = None
    bgm_is_playing = False

    gunshot = None

    def __init__(self):
        pygame.display.set_caption('Level 4')
        self.bgm = pygame.mixer.Sound('assets/audio/Level_4.mp3')
        self.config()

    def config(self):
        self.surf = pygame.image.load('assets/mars_surface.jpg')
        self.surf = pygame.transform.scale(self.surf, (WIDTH, HEIGHT))
        self.gun = pygame.image.load('assets/gunlv3.png')
        self.gun = pygame.transform.scale(self.gun, (WIDTH // 2, HEIGHT // 2))
        self.firegun = pygame.image.load('assets/gl3fire.png')
        self.firegun = pygame.transform.scale(self.firegun, (WIDTH // 2, HEIGHT // 2))
        self.gx = WIDTH // 2
        self.gy = HEIGHT // 2
        self.ginc = 0.03 * HEIGHT
        self.ginc_reset = self.ginc

        self.alien_spawn_range_x = (self.gun.get_width(), WIDTH - self.gun.get_width())
        self.alien_spawn_range_y = (self.gun.get_height() - 40, self.gun.get_height())
        self.aliens = []

        self.gunshot = pygame.mixer.Sound('assets/audio/gunshots/m4.mp3')
        self.gunshot.set_volume(1)

    def handle_events(self):
        global running, LEVEL

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Toggle fullscreen with F key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                toggle_fullscreen()

            # Exit the game with Escape key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                LEVEL = SHOW_MENU

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.gunfired = True
                self.gunshot.stop()
                self.gunshot.play()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                if self.show_levelinfo:
                    self.show_levelinfo = False

                if self.countdown < 1:
                    LEVEL = SHOW_WINSCREEN

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.gx + self.gun.get_width() / 2 > 0:
                self.gx -= 10

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.gx + self.gun.get_width() / 2 < WIDTH:
                self.gx += 10

        # if keys[pygame.K_SPACE]:
        #     self.gunfired = True

    def update_components(self):
        self.gx, self.gy = WIDTH // 2, HEIGHT // 2
        self.surf = pygame.transform.scale(self.surf, (WIDTH, HEIGHT))
        self.gun = pygame.transform.scale(self.gun, (WIDTH // 2, HEIGHT // 2))
        self.firegun = pygame.transform.scale(self.firegun, (WIDTH // 2, HEIGHT // 2))
        self.alien_spawn_range_x = (self.gun.get_width(), WIDTH - self.gun.get_width())
        self.alien_spawn_range_y = (self.gy - 40, self.gy)

        for i in self.aliens:
            i.set_coords(
                random.randint(self.alien_spawn_range_x[0], self.alien_spawn_range_x[1]),
                random.randint(self.alien_spawn_range_y[0], self.alien_spawn_range_y[1])
            )

        if self.gx < WIDTH // 2 and not self.gflipped:
            self.gflipped = True
            self.gun = pygame.transform.flip(self.gun, True, False)
            self.firegun = pygame.transform.flip(self.firegun, True, False)

    def loop(self):
        global gameover
        self.handle_events()

        if self.show_levelinfo:
            font = pygame.font.SysFont('Consolas', 20)
            msg = """Your SOS has been transmitted. A rescue team is\non their way. Defend yourself till the\nteam gets to you.\nUse AD or arrow keys to move and space to shoot.\nPress N to proceed. """
            msg = msg.split('\n')

            screen.blit(self.surf, (0, 0))

            c = 50
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (90, 200, WIDTH // 1.2, 50 * (len(msg) + 1)),
                border_bottom_right_radius=30,
                border_top_left_radius=30
            )
            for i in msg:
                screen.blit(font.render(i, True, (0, 230, 25)), (100, 200 + c))
                c += 50

            pygame.display.flip()
            clock.tick(FPS)
            return

        if not self.bgm_is_playing:
            self.bgm_is_playing = True
            self.bgm.play()

        if self.clt is None:
            self.clt = pygame.time.get_ticks()

        cr = pygame.time.get_ticks()
        if cr - self.clt > 1000:
            self.countdown -= 1
            self.clt = cr

        self.handle_events()
        screen.blit(self.surf, (0, 0))

        if self.countdown < 1:
            font = pygame.font.SysFont('Consolas', 50)
            lc_text = font.render('Level Cleared!', True, (64, 64, 64))
            screen.blit(lc_text, (WIDTH // 4, 50))

            pn = font.render('Press N to proceed', True, (200, 200, 200))
            screen.blit(pn, (WIDTH // 4, HEIGHT // 1.1))

            pygame.display.flip()
            clock.tick(FPS)
            return

        font = pygame.font.SysFont('Arial', 40)
        ct = font.render(f'ETA: {self.countdown}', True, (0, 0, 0))
        screen.blit(ct, (0.75 * WIDTH, 0.05 * HEIGHT))

        if self.gx + self.gun.get_width() // 2 < WIDTH // 2 and not self.gflipped:
            self.gflipped = True
            self.gun = pygame.transform.flip(self.gun, True, False)
            self.firegun = pygame.transform.flip(self.firegun, True, False)

        if self.gx + self.gun.get_width() // 2 > WIDTH // 2 and self.gflipped:
            self.gflipped = False
            self.gun = pygame.transform.flip(self.gun, True, False)
            self.firegun = pygame.transform.flip(self.firegun, True, False)

        if not len(self.aliens):
            a2 = Alien2()

            a2.set_coords(
                abs(self.gx - WIDTH // 3),
                random.randint(self.alien_spawn_range_y[0] + 40, self.alien_spawn_range_y[1]))

            self.aliens.append(a2)

        for i in self.aliens:
            if self.gunfired:
                s1 = set(range(i.coord_x, i.coord_x + i.scale_x))
                s2 = set(range(self.gx, self.gx + self.gun.get_width())) if not self.gflipped else \
                    set(range(self.gx + self.gun.get_width() - 40, self.gx + self.gun.get_width() + 40))
                if s1 & s2:
                    i.reduce_health(20)

                    if i.health <= 0:
                        self.aliens.remove(i)
                    continue

            if abs((i.scale_x - i.coord_x) * (i.scale_y - i.coord_y)) > WIDTH * HEIGHT / 3:
                gameover = True
                break

            i.display()

            i.set_scale(i.scale_x + 1, i.scale_y + 1)

        if self.gunfired:
            screen.blit(self.firegun, (self.gx, self.gy + self.ginc))
        else:
            screen.blit(self.gun, (self.gx, self.gy + self.ginc))

        self.gunfired = False

        if self.ginc > 0 and not self.shift_ginc:
            self.ginc -= 1
        else:
            self.shift_ginc = True
            self.ginc += 1

            if self.ginc == self.ginc_reset:
                self.shift_ginc = False

        pygame.display.flip()
        clock.tick(FPS)

    def __del__(self):
        self.bgm.fadeout(1500)


class Enemy1:
    spr = None
    frm = 0
    frh = 128
    frw = 128
    last_clock = None
    mcref = None  # Main character reference
    flip_sprite = False
    health = 100

    IDLE_SPRITE = 'assets/sprites/enemycharacter/Soldier_1/Idle.png'
    HURT_SPRITE = 'assets/sprites/enemycharacter/Soldier_1/Hurt.png'
    SHOT1_SPRITE = 'assets/sprites/enemycharacter/Soldier_1/Shot_1.png'
    DEAD_SPRITE = 'assets/sprites/enemycharacter/Soldier_1/Dead.png'

    curr_sprite = IDLE_SPRITE
    last_hurt_clock = None
    got_hurt = False

    shot_clock_1 = None

    shot_fired = False
    shot_clock_2 = None

    dead_clock = None
    is_dead = False
    dcp1 = False

    pos_x = 0
    pos_y = 0

    px_str = ''
    py_str = ''

    def __init__(self, px = None, py = None):
        self.config()
        self.shot_clock_1 = pygame.time.get_ticks()

        if not px:
            self.px_str = 'WIDTH * 0.5 - self.frw'
        else:
            self.px_str = px

        if not py:
            self.py_str = 'HEIGHT * 0.6 - self.frh'
        else:
            self.py_str = py

        self.pos_x = eval(self.px_str)
        self.pos_y = eval(self.py_str)

    def update(self):
        p = pygame.time.get_ticks()

        if p - self.last_clock > 100:
            self.last_clock = p
            self.frm += 1

        # if self.mcref is None:
        self.spr = pygame.image.load(self.curr_sprite)
        if self.flip_sprite:
            self.spr = pygame.transform.flip(self.spr, True, False)

        self.pos_x = eval(self.px_str)
        self.pos_y = eval(self.py_str)

    def config(self):
        # if self.mcref is None:
        self.spr = pygame.image.load(self.curr_sprite)
        if self.flip_sprite:
            self.spr = pygame.transform.flip(self.spr, True, False)
        self.last_clock = pygame.time.get_ticks()

        self.pos_x = WIDTH * 0.5 - self.frw
        self.pos_y = HEIGHT * 0.6 - self.frh

    def loop(self):
        self.update()

        if self.is_dead:
            x = 0
            y = 0

            if not self.flip_sprite:
                x = 3 * self.frw
            cf = self.spr.subsurface(pygame.Rect(x, y, self.frw, self.frh))
            cf = pygame.transform.scale(cf, (WIDTH // 2, HEIGHT // 2))
            screen.blit(cf, (self.pos_x, self.pos_y))
            return

        x = (self.frm % 128) * self.frw
        y = (self.frm // 128) * self.frh

        try:
            current_frame = self.spr.subsurface(pygame.Rect(x, y, self.frw, self.frh))
        except:
            self.frm = 0

            if self.dead_clock is not None and not self.dcp1:
                if not self.flip_sprite:
                    self.frm = 2
                else:
                    self.frm = 1

                self.dcp1 = True

            x = (self.frm % 128) * self.frw
            y = (self.frm // 128) * self.frh

            current_frame = self.spr.subsurface(pygame.Rect(x, y, self.frw, self.frh))

        current_frame = pygame.transform.scale(current_frame, (WIDTH // 2, HEIGHT // 2))
        screen.blit(current_frame, (self.pos_x, self.pos_y))

        if DEBUG:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                pygame.Rect(self.pos_x, self.pos_y, current_frame.get_width(),
                            current_frame.get_height())
                , 2)

        if self.health <= 0 and not self.is_dead:
            self.curr_sprite = self.DEAD_SPRITE
            if self.dead_clock is None:
                self.dead_clock = pygame.time.get_ticks()

            if pygame.time.get_ticks() - self.dead_clock > 250:
                self.is_dead = True

        if self.mcref is not None:
            # Enemy
            c1x, c1y = self.pos_x, self.pos_y
            c2x, c2y = c1x + current_frame.get_width(), c1y + current_frame.get_height()

            # Main Character
            d1x, d1y = self.mcref.pos_x, self.mcref.pos_y
            d2x, d2y = d1x + self.mcref.spr_rect.get_width(), d1y + self.mcref.spr_rect.get_height()

            if self.mcref:
                if d2x < c1x or d1x > c2x:
                    # No collision
                    pass
                else:
                    if d1y != c1y:
                        # While jumping there is no need to check for collision
                        pass
                    else:
                        area_x1, area_x2 = None, None
                        if c1x <= d2x <= c2x:
                            # Main character is to the left of the enemy
                            self.flip_sprite = True
                            area_x1 = c1x
                            area_x2 = d2x
                        elif d1x <= c2x <= d2x:
                            # Main character is to the right of the enemy
                            self.flip_sprite = False
                            area_x1 = d1x
                            area_x2 = c2x

                        if not self.got_hurt and self.mcref.is_attacking:
                            assert (area_x1, area_x2) != (None, None)
                            area_common = d1y * (area_x2 - area_x1)  # area_x2 is always >= area_x1
                            area = d1y * (max(c1x, c2x, d1x, d2x) - min(c1x, c2x, d1x, d2x))

                            if area_common / area >= 0.6:
                                # Attack delivered
                                self.got_hurt = True
                                self.last_hurt_clock = pygame.time.get_ticks()
                                self.curr_sprite = self.HURT_SPRITE

            if self.got_hurt:
                p = pygame.time.get_ticks()

                if p - self.last_hurt_clock > 200:
                    self.got_hurt = False
                    self.curr_sprite = self.IDLE_SPRITE
                    self.health -= 10

        if not self.got_hurt:
            p = pygame.time.get_ticks()
            if not self.shot_fired:
                if p - self.shot_clock_1 > 1000:
                    self.shot_clock_1 = p
                    self.curr_sprite = self.SHOT1_SPRITE

                    self.shot_fired = True
                    self.shot_clock_2 = p

                    if not self.mcref.is_jumping:
                        self.mcref.reduce_health(20)
            else:
                if p - self.shot_clock_2 > 333:
                    self.shot_fired = False
                    self.curr_sprite = self.IDLE_SPRITE



class MainCharacter:
    spr = None
    frm = 0
    frh = 128
    frw = 128
    last_clock = None
    pos_x = None
    pos_y = None
    health = 100

    IDLE_SPRITE = 'assets/sprites/maincharacter/City_men_3/Idle.png'
    RUNNING_SPRITE = 'assets/sprites/maincharacter/City_men_3/Run.png'
    WALK_SPRITE = 'assets/sprites/maincharacter/City_men_3/Walk.png'
    ATTACK_SPRITE = 'assets/sprites/maincharacter/City_men_3/Attack.png'
    DEAD_SPRITE = 'assets/sprites/maincharacter/City_men_3/Dead.png'
    HURT_SPRITE = 'assets/sprites/maincharacter/City_men_3/Hurt.png'

    curr_sprite = IDLE_SPRITE
    flip_sprite = False

    px_str = None
    py_str = None

    vel_y = 0
    gravity = 0.5
    jump_power = -HEIGHT / 55
    is_jumping = False

    last_attack_clock = None
    is_attacking = False

    got_hurt = False
    last_hurt_clock = None

    spr_rect = None

    dead_clock = None
    is_dead = False
    dcp1 = False

    def __init__(self, px = None, py = None):
        if not px:
            self.px_str = '-self.frw'
        else:
            self.px_str = px

        if not py:
            self.py_str = 'HEIGHT * 0.6 - self.frh'
        else:
            self.py_str = py

        self.config()


    def update(self):
        p = pygame.time.get_ticks()

        if p - self.last_clock > 100:
            self.last_clock = p
            self.frm += 1

        self.spr = pygame.image.load(self.curr_sprite)
        self.jump_power = -HEIGHT / 55

    def config(self):
        self.spr = pygame.image.load(self.curr_sprite)
        self.last_clock = pygame.time.get_ticks()

        if self.pos_x is None:
            self.pos_x = eval(self.px_str)
            # self.pos_x = -self.frw

        if self.pos_y is None:
            self.pos_y = eval(self.py_str)
            # self.pos_y = HEIGHT * 0.6 - self.frh

    def handle_events(self):
        global running, LEVEL
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Toggle fullscreen with F key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                toggle_fullscreen()

            # Exit the game with Escape key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                LEVEL = SHOW_MENU

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.curr_sprite != self.ATTACK_SPRITE:
                    self.curr_sprite = self.ATTACK_SPRITE
                    self.last_attack_clock = pygame.time.get_ticks()
                    self.is_attacking = True

        keys = pygame.key.get_pressed()
        mods = pygame.key.get_mods()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if mods & pygame.KMOD_LSHIFT:
                self.curr_sprite = self.WALK_SPRITE
                self.pos_x += 1
            else:
                self.curr_sprite = self.RUNNING_SPRITE
                self.pos_x += 2

            if self.is_jumping:
                self.pos_x += 1

            self.flip_sprite = False

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if mods & pygame.KMOD_LSHIFT:
                self.curr_sprite = self.WALK_SPRITE
                self.pos_x -= 1
            else:
                self.curr_sprite = self.RUNNING_SPRITE
                self.pos_x -= 2

            if self.is_jumping:
                self.pos_x -= 1

            self.flip_sprite = True
            if self.pos_x < -self.frw:
                self.curr_sprite = self.IDLE_SPRITE
                self.pos_x = -self.frw

        elif keys[pygame.K_e]:
            if not self.is_jumping:
                self.curr_sprite = self.ATTACK_SPRITE
                self.last_attack_clock = pygame.time.get_ticks()
                self.is_attacking = True

        else:
            if not self.got_hurt:
                if self.is_attacking:
                    p = pygame.time.get_ticks()

                    if p - self.last_attack_clock > 100:
                        self.curr_sprite = self.IDLE_SPRITE
                        self.is_attacking = False
                else:
                    self.curr_sprite = self.IDLE_SPRITE

        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_SPACE]) and not self.is_jumping:
            self.is_jumping = True
            self.vel_y = self.jump_power

        self.vel_y += self.gravity
        self.pos_y += self.vel_y

        if self.pos_y >= eval(self.py_str):
            self.pos_y = eval(self.py_str)
            self.vel_y = 0
            self.is_jumping = False

    def reduce_health(self, a):
        self.health -= a
        self.got_hurt = True
        self.last_hurt_clock = pygame.time.get_ticks()
        self.curr_sprite = self.HURT_SPRITE

    def loop(self):
        if self.is_dead:
            cf = self.spr.subsurface(pygame.Rect(4 * self.frw, 0, self.frw, self.frh))

            if self.flip_sprite:
                cf = pygame.transform.flip(cf, True, False)

            cf = pygame.transform.scale(cf, (WIDTH // 2, HEIGHT // 2))
            self.spr_rect = cf

            screen.blit(cf, (self.pos_x, self.pos_y))
            return

        self.update()

        if not self.got_hurt:
            self.handle_events()

        x = (self.frm % 128) * self.frw
        y = (self.frm // 128) * self.frh

        try:
            current_frame = self.spr.subsurface(pygame.Rect(x, y, self.frw, self.frh))
        except:
            self.frm = 2
            x = (self.frm % 128) * self.frw
            y = (self.frm // 128) * self.frh
            current_frame = self.spr.subsurface(pygame.Rect(x, y, self.frw, self.frh))

        if self.flip_sprite:
            current_frame = pygame.transform.flip(current_frame, True, False)

        current_frame = pygame.transform.scale(current_frame, (WIDTH // 2, HEIGHT // 2))
        self.spr_rect = current_frame

        screen.blit(current_frame, (self.pos_x, self.pos_y))

        if DEBUG:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                pygame.Rect(self.pos_x, self.pos_y, current_frame.get_width(), current_frame.get_height())
                , 2)

        if self.health <= 0:
            self.curr_sprite = self.DEAD_SPRITE
            if self.dead_clock is None:
                self.dead_clock = pygame.time.get_ticks()

            if pygame.time.get_ticks() - self.dead_clock > 100:
                self.is_dead = True

        if self.got_hurt:
            p = pygame.time.get_ticks()
            if p - self.last_hurt_clock > 333:
                self.got_hurt = False
                self.curr_sprite = self.IDLE_SPRITE


class Level3:
    background = None
    current_panel = 1
    e = None
    mc = None
    show_levelinfo = True

    bgm = None
    bgm_is_playing = False

    def __init__(self):
        pygame.display.set_caption('Level 3')
        self.bgm = pygame.mixer.Sound('assets/audio/Level_3.mp3')
        self.config()

    def handle_events(self):
        global running, LEVEL

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Toggle fullscreen with F key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                toggle_fullscreen()

            # Exit the game with Escape key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                LEVEL = SHOW_MENU

            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                if self.show_levelinfo:
                    self.show_levelinfo = False
                else:
                    LEVEL = 4

    def update_components(self):
        self.config()

    def config(self):
        if self.current_panel == 1:
            self.background = pygame.image.load('assets/sprites/lab1.jpg')

        elif self.current_panel == 2:
            self.background = pygame.image.load('assets/sprites/lab2.jpg')

        elif self.current_panel == 3:
            self.background = pygame.image.load('assets/sprites/lab3.jpg')

        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def loop(self):
        global gameover
        self.handle_events()

        screen.blit(self.background, (0, 0))

        if self.show_levelinfo:
            font = pygame.font.SysFont('Consolas', 20)
            msg = """You have successfully breached inside\nthe Communications Building.\nKill all the guards and reach the Network Tower\nto send SOS.\nUse WAD or arrow keys to move/jump and E to attack.\nYou can also use space to jump and shift to walk.\nPress N to proceed. """
            msg = msg.split('\n')

            c = 50
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (90, 200, WIDTH // 1.2, 50 * (len(msg) + 1)),
                border_bottom_right_radius=30,
                border_top_left_radius=30
            )
            for i in msg:
                screen.blit(font.render(i, True, (0, 230, 25)), (100, 200 + c))
                c += 50

            pygame.display.flip()
            clock.tick(FPS)
            return

        if not self.bgm_is_playing:
            self.bgm.play()

        if type(self.e) != Enemy1:
            if self.current_panel == 3:
                self.e = Enemy1('WIDTH * 0.5 - self.frw', 'HEIGHT * 0.65 - self.frh')
            elif self.current_panel == 2:
                self.e = Enemy1('WIDTH * 0.4 - self.frw')
            elif self.current_panel == 1:
                self.e = Enemy1()
            else:
                self.e = None

        if self.e:
            self.e.loop()

        if type(self.mc) != MainCharacter:
            if self.current_panel == 3:
                self.mc = MainCharacter('-self.frw', 'HEIGHT * 0.65 - self.frh')
            elif self.current_panel == 2:
                self.mc = MainCharacter()
            elif self.current_panel == 1:
                self.mc = MainCharacter()
            else:
                self.mc = None

        if self.mc:
            self.mc.loop()

        if self.current_panel > 3:
            font = pygame.font.SysFont('Consolas', 50)
            lc_text = font.render('Level Cleared!', True, (255, 0, 0))

            pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 3, 50, lc_text.get_width(), lc_text.get_height()))
            screen.blit(lc_text, (WIDTH // 3, 50))

            pn = font.render('Press N to proceed', True, (0, 200, 0))

            pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 4, HEIGHT // 1.1, pn.get_width(), pn.get_height()))
            screen.blit(pn, (WIDTH // 4, HEIGHT // 1.1))

            pygame.display.flip()
            clock.tick(FPS)
            return

        if self.mc and self.mc.is_dead:
            gameover = True

        if self.mc and self.mc.pos_x + self.mc.spr_rect.get_width() >= WIDTH and not self.e.is_dead:
            self.mc.pos_x = WIDTH - self.mc.spr_rect.get_width()

        if self.mc and self.mc.pos_x > WIDTH:
            if self.e.is_dead:
                self.current_panel += 1
                self.mc = None
                self.e = None
                self.update_components()
            else:
                self.mc.pos_x = WIDTH - self.mc.spr_rect.get_width()

        if self.e and self.e.mcref is None:
            self.e.mcref = self.mc

        pygame.display.flip()
        clock.tick(FPS)

    def __del__(self):
        self.bgm.stop()


class WinScreen:
    background = None

    def __init__(self):
        self.config()

    def config(self):
        self.background = pygame.image.load('assets/winscreen.jpg')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def update(self):
        self.config()

    def handle_events(self):
        global running, LEVEL

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Toggle fullscreen with F key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                toggle_fullscreen()

            # Exit the game with Escape key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                LEVEL = SHOW_MENU

    def loop(self):
        self.handle_events()
        screen.blit(self.background, (0, 0))

        font = pygame.font.SysFont('Consolas', 50)
        heading = font.render('Mission Successful!', True, (255, 255, 255))
        screen.blit(heading, (100, 50))

        c = 120
        msg = """This game was created by Shrehan Raj Singh as\n
        a part of the Game Creation task for\n
        Computer Graphics Society, IIT Kharagpur.\n\n
        All images have been used from https://www.pngwing.com.\nPress ESC to go back to home screen."""

        msg = msg.split('\n')
        font = pygame.font.SysFont('Consolas', 20)

        for i in range(len(msg)):
            m = font.render(msg[i].strip(), True, (255, 255, 255))
            screen.blit(m, (100, c + 50))
            c += 30
        pygame.display.flip()
        clock.tick(FPS)


running = True
gameover = False
lv = None

SHOW_MENU = -1
SHOW_WINSCREEN = -2

LEVEL = SHOW_MENU
try:
    while running:
        if gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    toggle_fullscreen()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # running = False
                    gameover = False
                    LEVEL = SHOW_MENU

            if LEVEL == 1:
                screen.blit(background, (bg_x, bg_y))
                screen.blit(spaceship, (0, 0))
                for i in text_elements:
                    screen.blit(i[0], i[1])

            pygame.draw.rect(screen, (200, 200, 200), game_over_banner.get_rect())
            screen.blit(game_over_bd, (0, 0))
            screen.blit(game_over_banner, (0, 0))

            # add_text_element("Press <Esc> to quit", "WIDTH // 2", "HEIGHT // 1.5")

            pygame.display.flip()
            clock.tick(FPS)
        else:
            if LEVEL == SHOW_MENU:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    # Toggle fullscreen with F key
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                        toggle_fullscreen()

                    # Exit the game with Escape key
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False

                if type(lv) != HomePage:
                    lv = HomePage()

                if lv.level is not None:
                    LEVEL = lv.level
                    lv = None
                    continue

                lv.loop()
                pygame.display.flip()
                clock.tick(FPS)

            # elif LEVEL == 1:
            #     for event in pygame.event.get():
            #         if event.type == pygame.QUIT:
            #             running = False
            #
            #         # Toggle fullscreen with F key
            #         if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            #             toggle_fullscreen()
            #             og_spaceship_instance = spaceship
            #
            #         # Exit the game with Escape key
            #         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #             LEVEL = SHOW_MENU
            #             break
            #
            #         if event.type == pygame.KEYUP:
            #             spaceship = og_spaceship_instance
            #
            #     if LEVEL == SHOW_MENU:
            #         continue
            #
            #     keys = pygame.key.get_pressed()
            #     if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            #         for i in asteroids_list:
            #             i['pos_x'] = i['pos_x'] + i['size']
            #
            #         if spaceship == og_spaceship_instance:
            #             spaceship = pygame.transform.rotate(spaceship, 1)
            #
            #     elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            #         for i in asteroids_list:
            #             i['pos_x'] = i['pos_x'] - i['size']
            #
            #         if spaceship == og_spaceship_instance:
            #             spaceship = pygame.transform.rotate(spaceship, -1)
            #
            #     elif keys[pygame.K_UP] or keys[pygame.K_w]:
            #         for i in asteroids_list:
            #             i['pos_y'] = i['pos_y'] + i['size']
            #
            #     elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            #         for i in asteroids_list:
            #             i['pos_y'] = i['pos_y'] - i['size']
            #
            #     # screen.fill((16, 16, 16))
            #     # draw_vertical_gradient((0, 128, 255), (255, 255, 255), WIDTH, HEIGHT)
            #
            #     screen.blit(background, (bg_x, bg_y))
            #
            #     for i in asteroids_list:
            #         at = pygame.image.load('assets/asteroid.png')
            #         at = pygame.transform.scale(at, (i['size'], i['size']))
            #
            #         if i['pos_x'] > WIDTH // 2:
            #             screen.blit(at, (i['pos_x'] + 50 - i['size'], i['pos_y']))
            #         else:
            #             screen.blit(at, (i['pos_x'] - 50 + i['size'], i['pos_y']))
            #
            #         at_w, at_h = at.get_size()
            #         if at_w * at_h > (WIDTH * HEIGHT) // 1.2 and i['pos_x'] in [WIDTH // 4, 0.75 * WIDTH] and i['pos_y'] in [HEIGHT // 4, 0.75 * HEIGHT]:
            #             gameover = True
            #             break
            #
            #         i['size'] += 5
            #
            #     screen.blit(spaceship, (0, 0))
            #
            #     for i in text_elements:
            #         screen.blit(i[0], i[1])
            #
            #     if pi_done:
            #         pygame.draw.rect(screen, (16, 16, 16), (WIDTH // 4, 5, WIDTH // 2 + 32, 32))
            #         screen.blit(progress_image, (WIDTH - WIDTH // 4, 5))
            #     else:
            #         pygame.draw.rect(screen, (16, 16, 16), (WIDTH // 4, 5, WIDTH // 2 + 32, 32))
            #         screen.blit(progress_image, (pi_x, pi_y))
            #
            #     pygame.display.flip()
            #
            #     if len (asteroids_list) < 5:
            #         asteroids_list.append({
            #             u'pos_x': random.randint(0, WIDTH),
            #             u'pos_y': random.randint(0, HEIGHT),
            #             u'size': 50,
            #         })
            #
            #     for i in asteroids_list:
            #         # print (i)
            #         if i['size'] > HEIGHT:
            #             wh = WIDTH // 2
            #             wy = HEIGHT // 2
            #             if i['pos_x'] > wh:
            #                 if i['pos_x'] - i['size'] < wh:
            #                     if i['pos_y'] < wy:
            #                         if i['pos_y'] + i['size'] > wy:
            #                             gameover = True
            #             else:
            #                 if i['pos_x'] + i['size'] > wh:
            #                     if i['pos_y'] < wy:
            #                         if i['pos_y'] + i['size'] < wy:
            #                             gameover = True
            #             asteroids_list.remove(i)
            #         if i['pos_x'] < 0 or i['pos_x'] > WIDTH:
            #              asteroids_list.remove(i)
            #         elif i['pos_y'] < 0 or i['pos_y'] > HEIGHT:
            #             asteroids_list.remove(i)
            #
            #     if pi_x < (WIDTH // 2 + WIDTH // 4):
            #         pi_inc += 0.0005 * WIDTH
            #         pi_x = (WIDTH // 4) + pi_inc
            #     else:
            #         pi_done = True
            #     clock.tick(FPS)

            elif LEVEL == 1:
                if type(lv) != Level1:
                    lv = Level1()

                lv.loop()

            elif LEVEL == 2:
                if type(lv) != Level2:
                    lv = Level2()

                lv.loop()

            elif LEVEL == 3:
                if type(lv) != Level3:
                    lv = Level3()

                lv.loop()

            elif LEVEL == 4:
                if type(lv) != Level4:
                    lv = Level4()

                lv.loop()

            elif LEVEL == SHOW_WINSCREEN:
                if type(lv) != WinScreen:
                    lv = WinScreen()

                lv.loop()
except:
    pass

pygame.quit()
sys.exit()
