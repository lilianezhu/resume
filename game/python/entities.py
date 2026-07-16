import random
import pygame

try:
    from .settings import (
        BLUE,
        GREEN,
        PLAYER_BULLET_SPEED,
        PLAYER_HEALTH,
        PLAYER_SPEED,
        RED,
        WHITE,
        YELLOW,
    )
except ImportError:
    from settings import (
        BLUE,
        GREEN,
        PLAYER_BULLET_SPEED,
        PLAYER_HEALTH,
        PLAYER_SPEED,
        RED,
        WHITE,
        YELLOW,
    )


class Entity:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40)
        self.speed = PLAYER_SPEED
        self.health = PLAYER_HEALTH
        self.cooldown = 0
        self.lives = 3
        self.score = 0
        self.weapon_level = 1

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def shoot(self):
        if self.cooldown > 0:
            return []
        self.cooldown = 220
        bullets = []
        center_x = self.rect.centerx
        y = self.rect.top
        if self.weapon_level == 1:
            bullets.append(Bullet(center_x, y, 0, -PLAYER_BULLET_SPEED, "player"))
        else:
            bullets.append(Bullet(center_x - 8, y, 0, -PLAYER_BULLET_SPEED, "player"))
            bullets.append(Bullet(center_x + 8, y, 0, -PLAYER_BULLET_SPEED, "player"))
        return bullets

    def update(self):
        self.cooldown = max(0, self.cooldown - 1)

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)
        pygame.draw.rect(surface, GREEN, pygame.Rect(self.rect.x + 8, self.rect.y + 10, 24, 8))
        pygame.draw.rect(surface, WHITE, pygame.Rect(self.rect.x + 14, self.rect.y + 2, 8, 18))


class Enemy(Entity):
    def __init__(self, x, y, level=1):
        super().__init__(x, y, 32, 32)
        self.level = level
        self.health = max(1, level)
        self.speed = 2 + level * 0.2
        self.fire_cooldown = random.randint(0, 80)
        self.score_value = 100 * level

    def update(self):
        self.rect.y += self.speed

    def shoot(self):
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
            return None
        self.fire_cooldown = 80
        return Bullet(self.rect.centerx, self.rect.bottom, 0, 4, "enemy")

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)
        pygame.draw.rect(surface, YELLOW, pygame.Rect(self.rect.x + 6, self.rect.y + 6, 20, 8))


class Bullet(Entity):
    def __init__(self, x, y, dx, dy, owner):
        super().__init__(x, y, 4, 10)
        self.dx = dx
        self.dy = dy
        self.owner = owner

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, surface):
        color = BLUE if self.owner == "player" else RED
        pygame.draw.rect(surface, color, self.rect)


class PowerUp(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 16, 16)
        self.kind = random.choice(["weapon", "health"])

    def update(self):
        self.rect.y += 2

    def draw(self, surface):
        color = YELLOW if self.kind == "weapon" else GREEN
        pygame.draw.rect(surface, color, self.rect)
