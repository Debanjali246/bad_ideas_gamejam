import pygame
from sys import exit
from player import Player
from backgd import Background
from stuff import Stuff
from enemy import Enemy
from buttons import Button
import os

BASE_DIR = os.path.dirname(__file__)

HEIGHT = 608
LENGTH = 1024
FPS = 24
PLAYER_FAT = 20
PLAYER_HEIGHT = 30
PLAYER_X = 150
PLAYER_Y = 150
PLAYER_SPEED = 20
BLOCKSIZE = 32
GRAVITY = 0.5
PLAYER_VEL = -10

class Level3:
    
    def __init__(self):
        self.gameloop=True
    def play(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()

        screen = pygame.display.set_mode((LENGTH, HEIGHT))
        pygame.display.set_caption("Level 3 - We are on the box")

        ICON = pygame.image.load(os.path.join(BASE_DIR, "enemies", "CatBasket.png"))
        pygame.display.set_icon(ICON)

        clock = pygame.time.Clock()

        # ---- music helper ----
        def music_file(*parts):
            primary = os.path.join(BASE_DIR, "Music", *parts)
            if os.path.exists(primary):
                return primary
            alternate = os.path.join(BASE_DIR, "Music", "Music", *parts)
            if os.path.exists(alternate):
                return alternate
            raise FileNotFoundError(f"Missing music file: {parts[0]}")

        # background music loops forever underneath everything
        pygame.mixer.music.load(music_file("Backgroundsound.wav"))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        # cat sounds play on top of background music using Sound objects
        cute_cat_sound = pygame.mixer.Sound(music_file("cat_crying.mp3"))
        cat_crying_sound = pygame.mixer.Sound(music_file("scary_cat.mp3"))
        cute_cat_sound.set_volume(0.6)
        cat_crying_sound.set_volume(0.6)
        cute_cat_sound.play(-1)

        # ---- sound effects ----
        dead_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Music", "Deadsound.wav"))
        down_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Music", "Downsound.wav"))
        up_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Music", "Upsound.wav"))

        CAT_PROXIMITY = 150
        current_track = "normal"

        # ---- world ----
        world = Background(screen, (69, 69, 69), os.path.join(BASE_DIR, "background", "realbg.jpeg"))

        self.gameloop = True
        goal_box = pygame.Rect(300, 400, 32, 32)
        cat = Enemy(
            screen,
            LENGTH - ((BLOCKSIZE) * 6),
            HEIGHT - (BLOCKSIZE + BLOCKSIZE + 25),
            BLOCKSIZE,
            BLOCKSIZE,
            2,
            None
        )

        # ---- game state ----
        hit_cooldown = 0
        game_over = False
        sound_on = True
        menu_state = "game"   # "game" | "pause" | "settings" | "audio" | "end"

        # ---- floor ----
        floor = []
        for i in range(0, LENGTH, BLOCKSIZE):
            jerry = Stuff(
                screen,
                i,
                HEIGHT - BLOCKSIZE,
                32,
                32,
                os.path.join(BASE_DIR, "lands", "forestland.jpeg"),
                1,
                None
            )
            floor.append(jerry)

        # ---- platforms ----
        platform_layout = [
            (6, 10, 14),
            (13, 17, 11),
            (20, 25, 13),
            (28, 31, 9),
            (3, 6, 10),
        ]

        platforms = []
        for (start_col, end_col, row) in platform_layout:
            for col in range(start_col, end_col):
                block = Stuff(
                    screen,
                    col * BLOCKSIZE,
                    row * BLOCKSIZE,
                    BLOCKSIZE, BLOCKSIZE,
                    os.path.join(BASE_DIR, "lands", "forestland.jpeg"),
                    1, None
                )
                platforms.append(block)

        all_blocks = floor + platforms

        tom = Player(screen, PLAYER_X, PLAYER_Y, PLAYER_FAT, PLAYER_HEIGHT, all_blocks)

        # ---- fonts ----
        warn_font = pygame.font.SysFont("arialblack", 36)
        hud_font = pygame.font.Font(None, 32)
        font = pygame.font.Font(None, 32)
        big_font = pygame.font.SysFont("arialblack", 30)
        small_font = pygame.font.Font(None, 28)

        # ---- buttons ----
        resume_btn = Button(screen, "Resume", LENGTH // 2, HEIGHT // 2 - 60)
        settings_btn = Button(screen, "Settings", LENGTH // 2, HEIGHT // 2)
        quit_btn = Button(screen, "Quit", LENGTH // 2, HEIGHT // 2 + 60)
        audio_btn = Button(screen, "Audio", LENGTH // 2, HEIGHT // 2 - 30)
        sback_btn = Button(screen, "Back", LENGTH // 2, HEIGHT // 2 + 40)
        toggle_btn = Button(screen, "Toggle Sound", LENGTH // 2, HEIGHT // 2 - 30)
        aback_btn = Button(screen, "Back", LENGTH // 2, HEIGHT // 2 + 40)
        restart_btn = Button(screen, "Restart", LENGTH // 2, HEIGHT // 2 - 25)
        mainmenu_btn = Button(screen, "Main Menu", LENGTH // 2, HEIGHT // 2 + 25)


        # -------------------- LEVEL 3 PUZZLE ---------------------


        # ---- treasure box / chest ----
        box_rect = pygame.Rect(820, 420, 50, 50)
        box_opened = False

        # ---- only ONE fake object ----
        mystery_stone_rect = pygame.Rect(860, 500, 25, 25)

        fake_message = ""
        fake_message_timer = 0

        # ---- code typing system ----
        typed_code = ""
        level_cleared = False
        clear_message = ""
        clear_message_timer = 0

        # ---- backup hint ----
        box_open_timer = 0
        show_backup_hint = False

        # ---- extra troll signs ----
        sign1_rect = pygame.Rect(520, HEIGHT - BLOCKSIZE - 40, 40, 40)
        sign2_rect = pygame.Rect(760, HEIGHT - BLOCKSIZE - 40, 40, 40)

        # ---- spike class ----
        class Spike:
            def __init__(self, x, y, w, h, screen, spawn_x, spawn_y):
                self.rect = pygame.Rect(x, y, w, h)
                self.screen = screen
                self.warn_distance = 100
                self.spawn_x = spawn_x
                self.spawn_y = spawn_y
                self.near_spike_jumped = False
                self.cleared_spike = False

            def draw(self):
                tip = (self.rect.centerx, self.rect.top)
                left = (self.rect.left, self.rect.bottom)
                right = (self.rect.right, self.rect.bottom)
                pygame.draw.polygon(self.screen, (34, 54, 28), [tip, left, right])
                pygame.draw.polygon(self.screen, (22, 38, 18), [tip, left, right], 2)

            

            def update(self, player):
                near_spike = abs(player.x - self.rect.x) < self.warn_distance

                if near_spike:
                    if player.vel_y < 0:
                        self.near_spike_jumped = True

                    if (self.near_spike_jumped and
                        player.x <= self.rect.x + self.rect.width and
                        player.vel_y >= 0):
                        self.cleared_spike = True

                if player.colliderect(self.rect) and player.vel_y >= 0:
                    player.x = self.spawn_x
                    player.y = self.spawn_y
                    self.near_spike_jumped = False
                    self.cleared_spike = False

            def teleport(self, player, teleport_x, teleport_y):
                if self.cleared_spike and player.vel_y == 0:
                    player.x = teleport_x
                    player.y = teleport_y
                    self.cleared_spike = False
                    self.near_spike_jumped = False

        # ---- original spike ----
        spike = Spike(-300, HEIGHT - BLOCKSIZE - 16, 16, 16, screen, PLAYER_X, PLAYER_Y)

        # ---- level 3 spikes ----
        spikes_level3 = [
            Spike(420, HEIGHT - BLOCKSIZE - 16, 16, 16, screen, PLAYER_X, PLAYER_Y),
            Spike(620, HEIGHT - BLOCKSIZE - 16, 16, 16, screen, PLAYER_X, PLAYER_Y),
            Spike(700, HEIGHT - BLOCKSIZE - 16, 16, 16, screen, PLAYER_X, PLAYER_Y),
        ]

        TELEPORT_X = cat.x + cat.width + 20
        TELEPORT_Y = cat.y


        # ---------------- HELPER DRAW FUNCTIONS ------------------

        def draw_box():
            if not box_opened:
                pygame.draw.rect(screen, (139, 69, 19), box_rect)
                pygame.draw.rect(screen, (90, 40, 10), box_rect, 3)
                pygame.draw.line(screen, (255, 215, 0),
                                (box_rect.x, box_rect.y + 25),
                                (box_rect.x + 50, box_rect.y + 25), 3)
            else:
                pygame.draw.rect(screen, (139, 69, 19), (box_rect.x, box_rect.y + 15, 50, 35))
                pygame.draw.rect(screen, (90, 40, 10), (box_rect.x, box_rect.y + 15, 50, 35), 3)

                lid_points = [
                    (box_rect.x, box_rect.y + 15),
                    (box_rect.x + 50, box_rect.y + 15),
                    (box_rect.x + 40, box_rect.y - 10),
                    (box_rect.x - 10, box_rect.y - 10)
                ]
                pygame.draw.polygon(screen, (160, 82, 45), lid_points)
                pygame.draw.polygon(screen, (90, 40, 10), lid_points, 3)

        def draw_fake_object():
            # only one fake object: mysterious glowing stone
            pygame.draw.circle(screen, (0, 255, 255), mystery_stone_rect.center, 15)
            pygame.draw.circle(screen, (255, 255, 255), mystery_stone_rect.center, 15, 2)

        def draw_box_clue():
            clue1 = big_font.render("The path is not walked. The answer is not found.", True, (255, 255, 0))
            clue2 = big_font.render("Manifest WIN", True, (255, 255, 255))
            screen.blit(clue1, clue1.get_rect(center=(LENGTH // 2, 240)))
            screen.blit(clue2, clue2.get_rect(center=(LENGTH // 2, 160)))

        def draw_fake_message():
            if fake_message_timer > 0:
                msg = small_font.render(fake_message, True, (255, 255, 255))
                screen.blit(msg, msg.get_rect(center=(LENGTH // 2, 160)))

        def draw_backup_hint():
            if show_backup_hint:
                hint = small_font.render("Maybe the answer should be... entered.", True, (255, 200, 0))
                screen.blit(hint, hint.get_rect(center=(LENGTH // 2, 600)))

        def draw_clear_message():
            if clear_message_timer > 0:
                msg = big_font.render(clear_message, True, (0, 255, 100))
                screen.blit(msg, msg.get_rect(center=(LENGTH // 2, HEIGHT // 2 - 100)))

        def draw_typed_code():
            if box_opened and not level_cleared:
                code_text = small_font.render(f":{typed_code}", True, (255, 255, 255))
                screen.blit(code_text, (20, 50))

        def draw_signs():
            pygame.draw.rect(screen, (139, 69, 19), sign1_rect)
            s1 = small_font.render("...", True, (255, 255, 255))
            screen.blit(s1, s1.get_rect(center=sign1_rect.center))

            pygame.draw.rect(screen, (139, 69, 19), sign2_rect)
            s2 = small_font.render("?!", True, (255, 255, 255))
            screen.blit(s2, s2.get_rect(center=sign2_rect.center))

        def draw_box_prompt():
            if tom.colliderect(box_rect.inflate(60, 60)) and not box_opened and not level_cleared:
                prompt = small_font.render("Press E to open the box", True, (255, 255, 255))
                screen.blit(prompt, prompt.get_rect(center=(LENGTH // 2, HEIGHT - 100)))

        def draw_object_prompt():
            if box_opened and tom.colliderect(mystery_stone_rect.inflate(40, 40)) and not level_cleared:
                prompt = small_font.render("Press F to inspect", True, (255, 255, 255))
                screen.blit(prompt, prompt.get_rect(center=(LENGTH // 2, HEIGHT - 70)))


        #  MAIN LOOP 

        while self.gameloop == True:

            world.draw()

            lives_text = hud_font.render(f"Lives: {tom.health}", True, (255, 255, 255))
            screen.blit(lives_text, (10, 10))

            if not game_over and menu_state == "game":
                tom.movement(PLAYER_SPEED)
                tom.move()
                tom.draw()

                cat.draw()
                cat.update(tom)
                cat.show_door(tom)

                for i in all_blocks:
                    i.draw()

                draw_signs()

                spike.draw()
                #spike.show_warning(tom, warn_font, LENGTH, HEIGHT)

                for sp in spikes_level3:
                    sp.draw()
                    #sp.show_warning(tom, warn_font, LENGTH, HEIGHT)

                if hit_cooldown > 0:
                    hit_cooldown -= 1

                if tom.colliderect(cat) and hit_cooldown <= 0:
                    tom.health -= 1
                    hit_cooldown = int(FPS * 2.5)

                    if tom.health <= 0:
                        game_over = True
                        menu_state = "end"
                        dead_sound.play()

                spike.update(tom)
                spike.teleport(tom, TELEPORT_X, TELEPORT_Y)

                for sp in spikes_level3:
                    sp.update(tom)

                dist = ((tom.x - cat.x) ** 2 + (tom.y - cat.y) ** 2) ** 0.5
                if dist < CAT_PROXIMITY and current_track != "crying":
                    cute_cat_sound.stop()
                    cat_crying_sound.play(-1)
                    current_track = "crying"
                elif dist >= CAT_PROXIMITY and current_track != "normal":
                    cat_crying_sound.stop()
                    cute_cat_sound.play(-1)
                    current_track = "normal"

                # ---- LEVEL 3 DRAW ----
                if not level_cleared:
                    draw_box()

                    if box_opened:
                        draw_fake_object()
                        draw_box_clue()
                        draw_backup_hint()

                    draw_fake_message()
                    draw_typed_code()
                    draw_box_prompt()
                    draw_object_prompt()

                # only final win message remains visible
                draw_clear_message()

                # ---- timers ----
                if fake_message_timer > 0:
                    fake_message_timer -= 1

                if clear_message_timer > 0:
                    clear_message_timer -= 1

                if box_opened and not level_cleared:
                    box_open_timer += 1

                if box_open_timer > FPS * 8 and not level_cleared:
                    show_backup_hint = True

                if level_cleared and clear_message_timer <= 0:
                    menu_state = "end"

            elif menu_state in ["pause", "settings", "audio", "end"]:
                for i in all_blocks:
                    i.draw()

                cat.draw()
                draw_signs()

                spike.draw()
                for sp in spikes_level3:
                    sp.draw()

                if not level_cleared:
                    draw_box()
                    if box_opened:
                        draw_fake_object()
                        draw_box_clue()
                        draw_backup_hint()

                    draw_fake_message()
                    draw_typed_code()

                draw_clear_message()

            
            # MENUS
            
            if menu_state == "pause":
                paused_text = font.render("PAUSED", True, (255, 255, 0))
                screen.blit(paused_text, paused_text.get_rect(center=(LENGTH // 2, HEIGHT // 2 - 120)))
                resume_btn.draw()
                settings_btn.draw()
                quit_btn.draw()

            elif menu_state == "settings":
                stitle = font.render("SETTINGS", True, (255, 255, 0))
                screen.blit(stitle, stitle.get_rect(center=(LENGTH // 2, HEIGHT // 2 - 100)))
                audio_btn.draw()
                sback_btn.draw()

            elif menu_state == "audio":
                atitle = font.render("AUDIO", True, (255, 255, 0))
                screen.blit(atitle, atitle.get_rect(center=(LENGTH // 2, HEIGHT // 2 - 100)))
                status = font.render(f"Sound: {'ON' if sound_on else 'OFF'}", True, (255, 255, 255))
                screen.blit(status, status.get_rect(center=(LENGTH // 2, HEIGHT // 2 - 60)))
                toggle_btn.draw()
                aback_btn.draw()

            elif menu_state == "end":
                if level_cleared:
                    self.gameloop=False
                    etitle = font.render("YOU WIN. CLEARLY.", True, (0, 255, 100))#this wont be used now
                    
                else:
                    etitle = font.render("LoL FAILED", True, (255, 0, 0))

                screen.blit(etitle, etitle.get_rect(center=(LENGTH // 2, HEIGHT // 2 - 80)))
                restart_btn.draw()
                mainmenu_btn.draw()

            
            # EVENTS
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    if menu_state == "game":
                        menu_state = "pause"
                    elif menu_state == "pause":
                        menu_state = "game"

                # ---- open box with E ----
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    if menu_state == "game":
                        if tom.colliderect(box_rect.inflate(40, 40)) and not box_opened:
                            box_opened = True
                            box_open_timer = 0
                            show_backup_hint = False

                # ---- inspect ONLY ONE fake object with F ----
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f and box_opened and menu_state == "game":
                    if tom.colliderect(mystery_stone_rect.inflate(30, 30)):
                        fake_message = "It glows with absolutely no purpose."
                        fake_message_timer = FPS * 2

                    elif tom.colliderect(sign1_rect.inflate(20, 20)):
                        fake_message = "Almost there..."
                        fake_message_timer = FPS * 2

                    elif tom.colliderect(sign2_rect.inflate(20, 20)):
                        fake_message = "Definitely not a keyboard puzzle."
                        fake_message_timer = FPS * 2

                # ---- type WIN after box opens ----
                if event.type == pygame.KEYDOWN and box_opened and not level_cleared and menu_state == "game":
                    if event.key == pygame.K_w:
                        typed_code += "W"
                    elif event.key == pygame.K_i:
                        typed_code += "I"
                    elif event.key == pygame.K_n:
                        typed_code += "N"
                    elif event.key == pygame.K_BACKSPACE:
                        typed_code = typed_code[:-1]

                    if len(typed_code) > 3:
                        typed_code = typed_code[-3:]

                    if typed_code == "WIN":
                        level_cleared = True
                        clear_message = "WRONG CODE, AS EXPECTED FROM YOU.... JUST KIDDING "
                        clear_message_timer = FPS * 3

                        # clear old UI immediately
                        fake_message = ""
                        fake_message_timer = 0
                        typed_code = ""
                        show_backup_hint = False

                # ---- mouse buttons for menu ----
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if menu_state == "pause":
                        if resume_btn.is_clicked(mouse_pos):
                            menu_state = "game"

                        elif settings_btn.is_clicked(mouse_pos):
                            menu_state = "settings"

                        elif quit_btn.is_clicked(mouse_pos):
                            pygame.quit()
                            exit()

                    elif menu_state == "settings":
                        if audio_btn.is_clicked(mouse_pos):
                            menu_state = "audio"

                        elif sback_btn.is_clicked(mouse_pos):
                            menu_state = "pause"

                    elif menu_state == "audio":
                        if toggle_btn.is_clicked(mouse_pos):
                            sound_on = not sound_on
                            if sound_on:
                                pygame.mixer.unpause()
                            else:
                                pygame.mixer.pause()

                        elif aback_btn.is_clicked(mouse_pos):
                            menu_state = "settings"

                    elif menu_state == "end":
                        if restart_btn.is_clicked(mouse_pos):
                            tom = Player(screen, PLAYER_X, PLAYER_Y, PLAYER_FAT, PLAYER_HEIGHT, all_blocks)

                            game_over = False
                            hit_cooldown = 0
                            menu_state = "game"

                            current_track = "normal"
                            cute_cat_sound.stop()
                            cute_cat_sound.play(-1)

                            box_opened = False
                            typed_code = ""
                            level_cleared = False
                            clear_message = ""
                            clear_message_timer = 0
                            fake_message = ""
                            fake_message_timer = 0
                            box_open_timer = 0
                            show_backup_hint = False

                            spike.near_spike_jumped = False
                            spike.cleared_spike = False

                            for sp in spikes_level3:
                                sp.near_spike_jumped = False
                                sp.cleared_spike = False

                        elif mainmenu_btn.is_clicked(mouse_pos):
                            pygame.quit()
                            exit()

            pygame.draw.rect(screen, (0, 250, 250), goal_box, 0, 1, 100, -50, 90, 1110)

            pygame.display.update()
            clock.tick(FPS)
