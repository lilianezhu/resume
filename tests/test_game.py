import pygame

from game.python.collision import check_collision, resolve_collisions
from game.python.entities import Bullet, Enemy, Player


def test_check_collision_detects_overlap():
    a = pygame.Rect(0, 0, 10, 10)
    b = pygame.Rect(8, 8, 10, 10)
    assert check_collision(a, b) is True


def test_resolve_collisions_removes_hit_entities():
    player = Player(100, 100)
    enemy = Enemy(100, 100, 1)
    bullet = Bullet(player.rect.centerx, player.rect.centery, 0, -1, "player")

    player_bullets = [bullet]
    enemy_bullets = []
    enemies = [enemy]

    score_gain, remaining_enemies, remaining_player_bullets, remaining_enemy_bullets, player_hit = resolve_collisions(
        player,
        enemies,
        player_bullets,
        enemy_bullets,
    )

    assert score_gain == 100
    assert remaining_enemies == []
    assert remaining_player_bullets == []
    assert remaining_enemy_bullets == []
    assert player_hit is False
