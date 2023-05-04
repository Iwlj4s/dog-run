import pygame

clock = pygame.time.Clock()

pygame.init()

display_width = 1700                                                                              # <== Display settings
display_height = 793
screen = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Dog Run!")                                                                   # <== IMG Stuff
icon = pygame.image.load('img/icon.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('img/bg/Preview/Background2.png').convert_alpha()

slime = pygame.image.load('img/slime/idle/slime2.png').convert_alpha()                                       # <== slime

slime_list_in_game = []

slime_x = 750
slime_y = 700

player = pygame.image.load('img/dog/idle/idle1.png').convert_alpha()                               # <== Player Settings
player_speed = 3

player_x = 150
player_y = 700
player_x_upd = 10

is_jump = False
jump_count = 7

player_idle = [                                                                             # <== Player animation files
    pygame.image.load('img/dog/idle/idle1.png').convert_alpha(),
    pygame.image.load('img/dog/idle/idle2.png').convert_alpha(),
    pygame.image.load('img/dog/idle/idle3.png').convert_alpha(),
    pygame.image.load('img/dog/idle/idle4.png').convert_alpha(),
    pygame.image.load('img/dog/idle/idle5.png').convert_alpha(),
]

player_right = [
    pygame.image.load('img/dog/walk/walk1.png').convert_alpha(),
    pygame.image.load('img/dog/walk/walk2.png').convert_alpha(),
    pygame.image.load('img/dog/walk/walk3.png').convert_alpha(),
    pygame.image.load('img/dog/walk/walk4.png').convert_alpha(),
    pygame.image.load('img/dog/walk/walk5.png').convert_alpha(),
]

player_anim_count = 3
bg_x = 0

player_attack = pygame.image.load('img/dog/att/Attack.png').convert_alpha()                             # Player attack
player_attacks =[]
attacks_left = 5
attacks_rest = 5

bg_music = pygame.mixer.Sound('music/music 1.mp3')                                                       # <== bg music
bg_music.play()

slime_timer = pygame.USEREVENT + 1                                                              # <== Slime timer stuff
pygame.time.set_timer(slime_timer, 2600)


title = pygame.font.Font('fonts/Elfboyclassic.ttf', 100)                                    # <== screen lose text stuff
subtitle = pygame.font.Font('fonts/Elfboyclassic.ttf', 60)
y_btn = pygame.font.Font('fonts/Elfboyclassic.ttf', 45)
n_btn = pygame.font.Font('fonts/Elfboyclassic.ttf', 45)
lose_title = title.render('You Lose!', False, (163, 109, 62))
restart_subtitle = subtitle.render('Play again?', False, (163, 109, 62))
yes_btn = y_btn.render('Yes', False, (255, 246, 174))
yes_btn_rect = yes_btn.get_rect(topleft=(600, 430))
no_btn = n_btn.render('No', False, (255, 246, 174))
no_btn_rect = no_btn.get_rect(topleft=(1070, 430))

title_attack = pygame.font.Font('fonts/Elfboyclassic.ttf', 30)                             # <== info about attacks left
check_attack = title_attack.render('You have only 5 attacks!', False, (255, 246, 174))


gameplay = True                                                                        # <== Checking if player is alive


running = True
while running:

    screen.blit(bg, (bg_x, 0))                                                                      # <== Object Display
    screen.blit(bg, (bg_x + 928, 0))
    screen.blit(check_attack, (20, 30))

    if gameplay:

        player_rect = player_right[1].get_rect(topleft=(player_x, player_y))                         # <== Player hitbox

        if slime_list_in_game:
            for (i, el) in enumerate(slime_list_in_game):
                screen.blit(slime, el)
                el.x -= 10

                if el.x < -10:
                    slime_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        if player_x > display_width:                                                                       # <== bg upd
            player_x = player_x_upd
            slime_list_in_game.clear()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:                                                                            # <== Move stuff
            screen.blit(player_right[player_anim_count], (player_x, player_y))
            bg_x -= 2

            if bg_x == -918:
                bg_x = 0

        else:
            screen.blit(player_idle[player_anim_count], (player_x, player_y))
            bg_x -= 0

        if keys[pygame.K_d] and player_speed < 200:
            player_x += player_speed

        elif keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -7:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2

                jump_count -= 1
            else:
                is_jump = False
                jump_count = 7

        if player_anim_count == 4:                                                      # <== Animation of player object
            player_anim_count = 0
        else:
            player_anim_count += 1

        if player_attacks:
            for (i, el) in enumerate(player_attacks):
                screen.blit(player_attack, (el.x, el.y))
                el.x += 4

                if el.x > display_width:
                    player_attacks.pop(i)

                if slime_list_in_game:
                    for (index, slime_el) in enumerate(slime_list_in_game):
                        if el.colliderect(slime_el):
                            slime_list_in_game.pop(index)
                            player_attacks.pop(i)

    else:                                                                                           # <== If player died
        screen.fill((244, 176, 60))
        screen.blit(lose_title, (650, 300))
        screen.blit(restart_subtitle, (705, 370))
        screen.blit(yes_btn, yes_btn_rect)
        screen.blit(no_btn, no_btn_rect)

        mouse = pygame.mouse.get_pos()

        if yes_btn_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            slime_list_in_game.clear()
            player_attacks.clear()
            attacks_left = attacks_rest

        elif no_btn_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            pygame.quit()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == slime_timer:
            slime_list_in_game.append(slime.get_rect(topleft=(1800, 700)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_e and attacks_left > 0:
            player_attacks.append(player_attack.get_rect(topleft=(player_x + 50, player_y)))
            attacks_left -= 1

    clock.tick(13)