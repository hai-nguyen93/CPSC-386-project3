import sys
import pygame
from pygame.locals import *
from bullet import Bullet
from alien import Alien
from time import sleep
from squid import Squid
from virus import Virus
from boss import Boss
from bunker import Bunker

RIGHT_KEYS = [K_d, K_RIGHT]
LEFT_KEYS = [K_a, K_LEFT]


def change_fleet_direction(game_settings, aliens):
    """ Drop the fleet and change direction"""
    for a in aliens.sprites():
        if a.score < 200:
            a.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1


def check_fleet_edges(game_settings, aliens):
    for a in aliens.sprites():
        if a.check_edges() and a.score < 200:
            change_fleet_direction(game_settings, aliens)
            break


def check_events(game_settings, screen, stats, scoreboard, buttons, ship, aliens, bullets, enemy_bullets, bunkers):
    """Respong to keypresses and mouse events."""
    for e in pygame.event.get():
        if e.type == QUIT:
            terminate(stats)
        elif e.type == KEYDOWN:
            check_keydown_events(e, game_settings, screen, stats, ship, bullets)
        elif e.type == KEYUP:
            check_keyup_events(e, stats, ship)
        elif e.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, screen, stats, scoreboard, buttons[0],
                              ship, aliens, bullets, enemy_bullets, bunkers, mouse_x, mouse_y)
            check_high_score_button(stats=stats, button=buttons[1], mouse_x=mouse_x, mouse_y=mouse_y)


def check_high_score_button(stats, button, mouse_x, mouse_y):
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.game_status == 0:
        stats.score_data.prep_score_table()
        stats.game_status = 1


def check_play_button(game_settings, screen, stats, scoreboard, play_button, ship, aliens, bullets, enemy_bullets,
                      bunkers, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and stats.game_status != 2:
        # Reset game settings
        game_settings.initialize_dynamic_settings()

        # Hide mouse cursor
        pygame.mouse.set_visible(False)

        # Reset game stats
        stats.reset_stats()
        stats.game_status = 2

        # Reset scoreboard
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()

        # Clear aliens, bullets lists
        aliens.empty()
        game_settings.boss_number = 0
        bullets.empty()
        enemy_bullets.empty()

        # Create aliens fleet and center the ship
        create_fleet(game_settings, screen, aliens)

        # Create bunkers
        bunkers.clear()
        bunkers.append(Bunker(screen, 150, 480))
        bunkers.append(Bunker(screen, 400, 480))
        bunkers.append(Bunker(screen, 650, 480))
        ship.reset()


def check_keydown_events(event, game_settings, screen, stats, ship, bullets):
    """Respond to key presses"""
    if event.key in RIGHT_KEYS:
        ship.move_right = True
    elif event.key in LEFT_KEYS:
        ship.move_left = True
    elif event.key == K_SPACE:
        if stats.game_status == 2 and not ship.dead:
            fire_bullet(game_settings, screen, ship, bullets)


def check_keyup_events(event, stats, ship):
    """Respond to key releases"""
    if event.key == K_ESCAPE:
        terminate(stats)
    elif event.key in RIGHT_KEYS:
        ship.move_right = False
    elif event.key in LEFT_KEYS:
        ship.move_left = False


def check_aliens_bottom(game_settings, screen, ship, aliens):
    screen_rect = screen.get_rect()
    for a in aliens.sprites():
        if a.rect.bottom >= screen_rect.height:
            ship_hit(game_settings, ship)
            break


def check_bullet_alien_collision(game_settings, screen, stats, scoreboard, aliens, bullets, enemy_bullets):
    # Check for collision with aliens
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    if collisions:
        for aliens in collisions.values():
            for a in aliens:
                if not a.dead:
                    stats.score += int(a.score * game_settings.score_scale)
                    game_settings.explode_sound.play()
                    a.die()
        scoreboard.prep_score()
        check_high_score(stats, scoreboard)

    if len(aliens) == 0:
        aliens.empty()
        bullets.empty()
        enemy_bullets.empty()
        game_settings.increase_speed()
        stats.level += 1
        scoreboard.prep_level()
        game_settings.boss_number = 0
        create_fleet(game_settings, screen, aliens)
        sleep(0.75)


def update_records(stats):
    stats.score_data.data.append(int(stats.score))
    stats.score_data.data.sort(reverse=True)
    n = 10 if len(stats.score_data.data) > 10 else len(stats.score_data.data)
    stats.score_data.data = stats.score_data.data[:n]


def check_high_score(stats, scoreboard):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
    scoreboard.prep_high_score()


def create_alien(game_settings, screen, aliens, alien_number, row_number, enemy_type=1):
    alien = Alien(game_settings, screen)
    if enemy_type == 2:
        alien = Squid(game_settings, screen)
    elif enemy_type == 3:
        alien = Virus(game_settings, screen)

    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.1 * alien.rect.height * row_number
    aliens.add(alien)


def create_boss(game_settings, screen, aliens):
    boss = Boss(game_settings, screen)  # boss row
    game_settings.boss_number += 1
    aliens.add(boss)


def create_fleet(game_settings, screen, aliens):
    """Create a fleet of aliens"""
    # Create an alien and find the number of aliens on a row
    # Spacing between each alien is equal to 1 alien width
    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)

    for alien_number in range(number_aliens_x):  # 1st row
        create_alien(game_settings, screen, aliens, alien_number, 1, 3)
    for alien_number in range(number_aliens_x):  # 2nd row
        create_alien(game_settings, screen, aliens, alien_number, 2, 1)
    for alien_number in range(number_aliens_x):  # 3rd row
        create_alien(game_settings, screen, aliens, alien_number, 3, 2)
    for alien_number in range(number_aliens_x):  # 4th row
        create_alien(game_settings, screen, aliens, alien_number, 4, 1)


def fire_bullet(game_settings, screen, ship, bullets):
    # Create a bullet and add to bullets group
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(game_settings, alien_width):
    available_space_x = game_settings.scr_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))


def get_number_rows(game_settings, ship_height, alien_height):
    available_space_y = (game_settings.scr_height - (3 * alien_height) - ship_height)
    return int(available_space_y / (2 * alien_height))


def ship_hit(game_settings, ship):
    if not ship.dead:
        game_settings.explode_sound.play()
    ship.dead = True


def update_ship(game_settings, screen, stats, scoreboard, ship, aliens, bullets, enemy_bullets):
    if ship.dead and ship.die_anim.finished:
        if stats.ships_left > 0:
            stats.ships_left -= 1
            scoreboard.prep_ships()
            aliens.empty()
            game_settings.boss_number = 0
            bullets.empty()
            enemy_bullets.empty()
            create_fleet(game_settings, screen, aliens)
            ship.reset()
            sleep(0.75)
        else:
            update_records(stats)
            aliens.empty()
            game_settings.boss_number = 0
            bullets.empty()
            enemy_bullets.empty()
            stats.game_status = 0
            pygame.mouse.set_visible(True)


def terminate(stats):
    stats.score_data.save()
    pygame.quit()
    sys.exit()


def update_bullets(game_settings, screen, stats, scoreboard, aliens, bullets, enemy_bullets):
    bullets.update()
    check_bullet_alien_collision(game_settings, screen, stats, scoreboard, aliens, bullets, enemy_bullets)

    # Delete out of screen bullets
    for b in bullets.copy():
        if b.rect.bottom <= 0:
            bullets.remove(b)
    # print(len(bullets))


def update_aliens(game_settings, screen, ship, aliens):
    check_fleet_edges(game_settings, aliens)
    aliens.update()
    check_aliens_bottom(game_settings, screen, ship, aliens)

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, ship)


def update_enemy_bullets(game_settings, ship, bullets, enemy_bullets):
    enemy_bullets.update()

    # check collision with player's bullets
    pygame.sprite.groupcollide(enemy_bullets, bullets, True, True)

    # check collision with ship
    hit_bullet = pygame.sprite.spritecollideany(ship, enemy_bullets)
    if hit_bullet is not None:
        hit_bullet.kill()
        ship_hit(game_settings, ship)


def update_screen(game_settings, screen, stats, scoreboard, ship, aliens, bullets, enemy_bullets, bunkers,
                  buttons, startscreen):
    """Redraw the screen"""
    screen.fill(game_settings.bg_color)
    for b in bullets.sprites():
        b.draw()
    for a in aliens.sprites():
        a.draw()
    for eb in enemy_bullets.sprites():
        eb.draw()
    for b in bunkers:
        b.draw()
    ship.draw()

    # Draw score
    scoreboard.draw()

    # Draw Play button
    if stats.game_status != 2:
        if stats.game_status == 0:
            startscreen.draw()
        else:
            stats.score_data.draw()

        for b in buttons:
            b.draw()

    pygame.display.update()
