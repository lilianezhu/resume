import pygame


def check_collision(a, b):
    return a.colliderect(b)


def resolve_collisions(player, enemies, player_bullets, enemy_bullets):
    score_gain = 0
    player_hit = False

    for enemy in list(enemies):
        for bullet in list(player_bullets):
            if check_collision(enemy.rect, bullet.rect):
                score_gain += enemy.score_value
                enemies.remove(enemy)
                player_bullets.remove(bullet)
                break

    for bullet in list(enemy_bullets):
        if check_collision(player.rect, bullet.rect):
            player.health -= 10
            enemy_bullets.remove(bullet)
            player_hit = True
            if player.health <= 0:
                player.lives -= 1
                player.health = 100

    return score_gain, enemies, player_bullets, enemy_bullets, player_hit
