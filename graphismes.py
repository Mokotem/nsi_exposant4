import pygame
import os


PATH = "Content/"

# Couleurs principales
COLOR_GRADIENT_TOP = (0, 255, 227)   # #00FFE3
COLOR_GRADIENT_BOTTOM = (255, 4, 253)  # #FF04FD
COLOR_MENU_BG = (32, 23, 140)  # #20178C
COLOR_LIGHT_TEXT = (255, 255, 255)
COLOR_BLUE_BUTTON = (80, 134, 252)  # #5086FC
COLOR_BLUE_SHADOW = (36, 57, 149)   # #243995
COLOR_HIGHLIGHT = (255, 4, 253)  # #ff04fd

screen = None

def draw_gradient_text(text, font, x, y, top_color, bottom_color):
    global screen
    text_surface = font.render(text, True, (255, 255, 255))
    width, height = text_surface.get_size()
    gradient = pygame.Surface((width, height), pygame.SRCALPHA)

    for i in range(height):
        ratio = i / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(gradient, (r, g, b, 255), (0, i), (width, i))

    text_mask = pygame.mask.from_surface(text_surface)
    mask_surface = text_mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0))
    mask_surface.set_colorkey((0, 0, 0))
    gradient.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(gradient, (x, y))


ICON_SIZE_JOUER = (300, 300)
ICON_SIZE_PARAM = (170, 120)
ICON_SIZE_DISCORD = (64, 45)
ICON_SIZE_SETTINGS_BG = (1024, 800)
ICON_SIZE_BOT = (220, 180)
ICON_SIZE_ONLINE = (220, 180)


OnLocalSelected = lambda x: 0
OnOnlineSelected = lambda x: 0

def StartMenu():

    global screen

    # Écran
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Puissance 4")

    # Chargement des images
    settings_bg = pygame.image.load(PATH + "background_settings_1.png").convert_alpha()


    icons = {
        "jouer": pygame.image.load(PATH + "button_1.png").convert_alpha(),
        "local": pygame.image.load(PATH + "play_w_ia-11.png").convert_alpha(),
        "reseaux": pygame.image.load(PATH + "play_w_friend.png").convert_alpha(),
        "parametres": pygame.image.load(PATH + "settings.png").convert_alpha(),
        "discord": pygame.image.load(PATH + "discord.png").convert_alpha(),
        "son": pygame.image.load(PATH + "sound-on.png").convert_alpha(),
    }

    font_big = pygame.font.SysFont(None, 124)
    font_medium = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)
    font_new_game = pygame.font.SysFont(None,40 )  # Новый размер для кнопки "New game"

    running = True
    on_main_menu = True
    on_settings = False

    settings_y = -ICON_SIZE_SETTINGS_BG[1]
    settings_velocity = 0
    settings_acceleration = 0.2
    settings_bounce = True
    settings_animation_done = False

    icon_bot_rect = pygame.Rect(465, 300, *ICON_SIZE_BOT)
    icon_online_rect = pygame.Rect(700, 300, *ICON_SIZE_ONLINE)

    dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dark_overlay.fill((0, 0, 0))
    dark_overlay.set_alpha(150)

    while running:
        screen.fill(COLOR_MENU_BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    on_main_menu = True
                    on_settings = False
                    settings_y = -ICON_SIZE_SETTINGS_BG[1]
                    settings_velocity = 0
                    settings_animation_done = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if on_main_menu:
                    jouer_rect = pygame.Rect(SCREEN_WIDTH // 2 - ICON_SIZE_JOUER[0] // 2, 220, *ICON_SIZE_JOUER)
                    if jouer_rect.collidepoint(mx, my):
                        on_main_menu = False
                        on_settings = True
                        settings_y = -ICON_SIZE_SETTINGS_BG[1]
                        settings_velocity = 0
                        settings_animation_done = False
                elif on_settings:
                    if icon_bot_rect.collidepoint(mx, my):
                        pygame.quit()
                        OnLocalSelected()
                        return
                    elif icon_online_rect.collidepoint(mx, my):
                        pygame.quit()
                        OnOnlineSelected()
                        return

        if on_main_menu:
            screen.fill(COLOR_MENU_BG)
            draw_gradient_text("PUISSANCE 4", font_big, 320, 150, COLOR_GRADIENT_TOP, COLOR_GRADIENT_BOTTOM)
            icons_resized = {
                "jouer": pygame.transform.scale(icons["jouer"], ICON_SIZE_JOUER),
                "parametres": pygame.transform.scale(icons["parametres"], ICON_SIZE_PARAM),
                "discord": pygame.transform.scale(icons["discord"], ICON_SIZE_DISCORD),
            }
            # Рисуем кнопку "jouer" с текстом "New game" и эффектом затемнения
            jouer_rect = pygame.Rect(SCREEN_WIDTH // 2 - ICON_SIZE_JOUER[0] // 2, 220, *ICON_SIZE_JOUER)
            jouer_img = icons_resized["jouer"]

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]

            jouer_img_effect = jouer_img.copy()

            if jouer_rect.collidepoint(mouse_pos):
                if mouse_pressed:
                    # Более темное при нажатии
                    jouer_img_effect.fill((0, 0, 0, 150), special_flags=pygame.BLEND_RGBA_MULT)
                else:
                    # Немного темнее при наведении
                    jouer_img_effect.fill((50, 50, 50, 100), special_flags=pygame.BLEND_RGBA_MULT)

            screen.blit(jouer_img_effect, jouer_rect)

            # Текст "New game"
            text_new_game = font_new_game.render("New game", True, (215,215,215))
            text_rect = text_new_game.get_rect(center=jouer_rect.center)
            text_rect.centery -= 35
            screen.blit(text_new_game, text_rect)

            # Остальные иконки главного меню
            screen.blit(icons_resized["parametres"], (SCREEN_WIDTH - 150, 15))
            screen.blit(icons_resized["discord"], (60, 50))

        elif on_settings:
            screen.blit(dark_overlay, (0, 0))

            if not settings_animation_done:
                settings_velocity += settings_acceleration
                settings_y += settings_velocity
                if settings_y > (SCREEN_HEIGHT - ICON_SIZE_SETTINGS_BG[1]) // 2:
                    if settings_bounce:
                        settings_velocity = -settings_velocity * 0.4
                        settings_bounce = False
                    else:
                        settings_y = (SCREEN_HEIGHT - ICON_SIZE_SETTINGS_BG[1]) // 2
                        settings_animation_done = True

            bg_scaled = pygame.transform.scale(settings_bg, ICON_SIZE_SETTINGS_BG)
            bg_rect = bg_scaled.get_rect(center=(SCREEN_WIDTH // 2+70, int(settings_y + ICON_SIZE_SETTINGS_BG[1] // 2)))
            screen.blit(bg_scaled, bg_rect)

            # Texte "REGLAGE"
            COLOR_REGLAGE = (61, 64, 102)
            COLOR_SHADOW = (20, 20, 40)
            shadow_text = font_medium.render("REGLAGE", True, COLOR_SHADOW)
            shadow_rect = shadow_text.get_rect(center=(bg_rect.centerx + 3, bg_rect.top + 180 + 3))
            screen.blit(shadow_text, shadow_rect)
            reglage_text = font_medium.render("REGLAGE", True, COLOR_REGLAGE)
            reglage_rect = reglage_text.get_rect(center=(bg_rect.centerx, bg_rect.top + 180))
            screen.blit(reglage_text, reglage_rect)

            subtitle_text = font_small.render("VOUS VOULEZ JOUER CONTRE ...", True, COLOR_HIGHLIGHT)
            screen.blit(subtitle_text, (bg_rect.centerx - subtitle_text.get_width() // 2, bg_rect.top + 250))


            icon_bot_rect.topleft = (bg_rect.left + 270, bg_rect.top + 300)
            icon_online_rect.topleft = (bg_rect.left + 500, bg_rect.top + 300)


            # icons
            mouse_pos = pygame.mouse.get_pos()
            for name, rect in [("local", icon_bot_rect), ("reseaux", icon_online_rect)]:
                icon_img = pygame.transform.scale(icons[name], (rect.width, rect.height))

                # Effet de survol / clic
                if rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    temp_img = icon_img.copy()
                    temp_img.fill((50, 50, 50, 100), special_flags=pygame.BLEND_RGBA_MULT)
                    screen.blit(temp_img, rect)
                elif rect.collidepoint(mouse_pos):
                    temp_img = icon_img.copy()
                    temp_img.fill((80, 80, 80, 80), special_flags=pygame.BLEND_RGBA_MULT)
                    screen.blit(temp_img, rect)
                else:
                    screen.blit(icon_img, rect)

                # --- Текст под иконками ---
                label_text = font_small.render(name.upper(), True, (20,20,40))
                label_rect = label_text.get_rect(center=(rect.centerx, rect.bottom + 10))
                screen.blit(label_text, label_rect)


        pygame.display.flip()

    pygame.quit()
