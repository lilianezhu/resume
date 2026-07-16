import random
import sys
from pathlib import Path

import pygame

if __package__ in {None, ""}:
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.append(str(current_dir))

    from collision import resolve_collisions
    from entities import Enemy, Player, PowerUp
    from settings import (
        ENEMY_SPAWN_INTERVAL,
        FPS,
        HEIGHT,
        POWERUP_SPAWN_CHANCE,
        WIDTH,
    )
    from ui import UI
else:
    from .collision import resolve_collisions
    from .entities import Enemy, Player, PowerUp
    from .settings import (
        ENEMY_SPAWN_INTERVAL,
        FPS,
        HEIGHT,
        POWERUP_SPAWN_CHANCE,
        WIDTH,
    )
    from .ui import UI


class SpaceShooterGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.ui = UI(self.screen)
        self.state = "menu"
        self.player = Player(WIDTH // 2 - 20, HEIGHT - 80)
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.powerups = []
        self.score = 0
        self.enemy_spawn_timer = 0
        self.level = 1
        self.running = True

    def reset_game(self):
        self.player = Player(WIDTH // 2 - 20, HEIGHT - 80)
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        self.powerups = []
        self.score = 0
        self.enemy_spawn_timer = 0
        self.level = 1
        self.state = "playing"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.state == "menu" or self.state == "game_over":
                        self.reset_game()
                elif event.key == pygame.K_r and self.state == "game_over":
                    self.reset_game()
                elif event.key == pygame.K_p:
                    if self.state == "playing":
                        self.state = "paused"
                    elif self.state == "paused":
                        self.state = "playing"

    def update(self):
        if self.state != "playing":
            return

        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        self.player.move(dx, dy)

        self.player.rect.x = max(0, min(WIDTH - self.player.rect.width, self.player.rect.x))
        self.player.rect.y = max(0, min(HEIGHT - self.player.rect.height, self.player.rect.y))

        if keys[pygame.K_SPACE]:
            new_bullets = self.player.shoot()
            self.player_bullets.extend(new_bullets)

        self.player.update()

        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= ENEMY_SPAWN_INTERVAL // max(1, self.level):
            self.spawn_enemy()
            self.enemy_spawn_timer = 0

        for enemy in self.enemies:
            enemy.update()
            if enemy.rect.y > HEIGHT:
                self.enemies.remove(enemy)
                self.player.health -= 10

        for bullet in self.player_bullets:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.player_bullets.remove(bullet)

        for bullet in self.enemy_bullets:
            bullet.update()
            if bullet.rect.top > HEIGHT:
                self.enemy_bullets.remove(bullet)

        for powerup in self.powerups:
            powerup.update()
            if powerup.rect.y > HEIGHT:
                self.powerups.remove(powerup)

        for enemy in self.enemies:
            if random.random() < 0.01:
                shot = enemy.shoot()
                if shot is not None:
                    self.enemy_bullets.append(shot)

        score_gain, self.enemies, self.player_bullets, self.enemy_bullets, player_hit = resolve_collisions(
            self.player,
            self.enemies,
            self.player_bullets,
            self.enemy_bullets,
        )
        self.score += score_gain

        if player_hit:
            if self.player.lives <= 0:
                self.state = "game_over"

        if self.score >= self.level * 1000:
            self.level += 1

        for powerup in self.powerups:
            if self.player.rect.colliderect(powerup.rect):
                if powerup.kind == "weapon":
                    self.player.weapon_level = min(2, self.player.weapon_level + 1)
                else:
                    self.player.health = min(100, self.player.health + 20)
                self.powerups.remove(powerup)

        if random.random() < POWERUP_SPAWN_CHANCE:
            self.powerups.append(PowerUp(random.randint(20, WIDTH - 20), -20))

    def spawn_enemy(self):
        lane = random.randint(0, WIDTH - 40)
        level = min(3, 1 + self.level // 2)
        enemy = Enemy(lane, -40, level)
        self.enemies.append(enemy)

    def draw(self):
        self.screen.fill((0, 0, 0))

        for i in range(0, WIDTH, 20):
            pygame.draw.line(self.screen, (20, 20, 40), (i, 0), (i, HEIGHT))

        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        self.player.draw(self.screen)

        self.ui.draw_hud(self.player, self.state, self.score)

        if self.state == "menu":
            self.ui.draw_menu()
        elif self.state == "game_over":
            self.ui.draw_game_over(self.score)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()


def main():
    game = SpaceShooterGame()
    game.run()


if __name__ == "__main__":
    main()
