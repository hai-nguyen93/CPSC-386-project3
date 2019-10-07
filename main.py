import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from random import randint
from enemy_bullet import EnemyBullet
from start_screen import StartScreen
from bunker import Bunker


FPS = 60


def play():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.scr_width, settings.scr_height))
    pygame.display.set_caption('Alien Invasion')
    main_clock = pygame.time.Clock()

    stats = GameStats(settings, screen)
    sb = Scoreboard(settings, screen, stats)
    sscreen = StartScreen(settings, screen)

    # Make a ship
    ship = Ship(settings, screen)

    # Make bunkers
    bunkers = [Bunker(screen, 400, 480)]

    # Make bullets and aliens group
    bullets = Group()
    aliens = Group()
    enemy_bullets = Group()
    # gf.create_fleet(settings, screen, ship, aliens)

    # Make buttons
    play_button = Button(screen, 'PLAY', screen.get_rect().centerx, 400)
    score_button = Button(screen, 'HIGH SCORE', screen.get_rect().centerx, 480)
    buttons = [play_button, score_button]

    # Set up music
    bg_music1 = pygame.mixer.Sound('audio/background_1.wav')
    bg_music2 = pygame.mixer.Sound('audio/background_2.wav')
    is_playing_music = False
    is_playing_music2 = False
    game_over_sound = pygame.mixer.Sound('audio/gameover.wav')

    # Boss timer
    boss_respawn_time = randint(10, 18) * 1000  # 10-18s at level 1
    boss_timer = boss_respawn_time
    delta_time = 0

    # Enemy fire timer
    enemy_fire_time = randint(2, 6) * 1000  # 2-6s at level 1
    fire_timer = enemy_fire_time

    # Main game loop
    game_over = False
    while not game_over:
        gf.check_events(settings, screen, stats, sb, buttons, ship, aliens, bullets, enemy_bullets, bunkers)
        if stats.game_status == 2:
            # update bg music
            if not is_playing_music:
                bg_music1.play(-1)
                is_playing_music = True
                is_playing_music2 = False
            if len(aliens) - settings.boss_number <= 10 and not is_playing_music2:
                bg_music1.stop()
                bg_music2.play(-1)
                is_playing_music2 = True
            if is_playing_music2 and len(aliens) - settings.boss_number > 10:
                bg_music2.stop()
                bg_music1.play(-1)
                is_playing_music = True
                is_playing_music2 = False
            if ship.dead and ship.die_anim.finished and stats.ships_left > 0:
                pygame.mixer.stop()
                is_playing_music, is_playing_music2 = False, False
                # reset boss and fire timer when ship explodes
                boss_respawn_time = randint(10, 18) * 1000
                boss_timer = int(boss_respawn_time / settings.enemy_timer_scale)
                enemy_fire_time = randint(2, 6) * 1000
                fire_timer = int(enemy_fire_time / settings.enemy_timer_scale)

            for b in bunkers:
                b.update(bullets, enemy_bullets)
            ship.update()
            gf.update_ship(settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets)
            gf.update_bullets(settings, screen, stats, sb, aliens, bullets, enemy_bullets)

            # Spawn boss
            if settings.boss_number < settings.boss_number_limit:
                if boss_timer <= 0:
                    gf.create_boss(settings, screen, aliens)
                    boss_respawn_time = randint(10, 18) * 1000
                    boss_timer = int(boss_respawn_time / settings.enemy_timer_scale)
                else:
                    boss_timer -= delta_time

            gf.update_aliens(settings, screen, ship, aliens)

            # Enemy fire
            if fire_timer <= 0 and len(enemy_bullets) < settings.bullets_allowed:
                new_bullet = EnemyBullet(settings, screen, aliens)
                enemy_bullets.add(new_bullet)
                enemy_fire_time = randint(2, 6) * 1000
                fire_timer = int(enemy_fire_time / settings.enemy_timer_scale)
            elif fire_timer > 0:
                fire_timer -= delta_time
            gf.update_enemy_bullets(settings, ship, bullets, enemy_bullets)

        else:
            # update music
            if is_playing_music or is_playing_music2:
                pygame.mixer.stop()
                is_playing_music, is_playing_music2 = False, False
                if stats.ships_left == 0:
                    game_over_sound.play()
                    # reset boss and fire timer to level 1
                    boss_respawn_time = randint(10, 18) * 1000
                    boss_timer = boss_respawn_time
                    enemy_fire_time = randint(2, 6) * 1000
                    fire_timer = enemy_fire_time

        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, enemy_bullets, bunkers, buttons, sscreen)
        delta_time = main_clock.tick(FPS)


play()
