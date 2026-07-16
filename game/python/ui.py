import pygame
from .settings import BLACK, BLUE, GREEN, RED, WHITE, WIDTH, HEIGHT, FONT_SIZE, SMALL_FONT_SIZE


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.small_font = pygame.font.SysFont(None, SMALL_FONT_SIZE)

    def draw_hud(self, player, state, score):
        score_text = self.font.render(f"Score: {score}", True, WHITE)
        health_text = self.font.render(f"Health: {player.health}", True, GREEN)
        lives_text = self.font.render(f"Lives: {player.lives}", True, BLUE)
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(health_text, (20, 55))
        self.screen.blit(lives_text, (20, 90))

        if state == "paused":
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            title = self.font.render("Paused", True, WHITE)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))

    def draw_menu(self):
        self.screen.fill(BLACK)
        title = self.font.render("Space Shooter", True, WHITE)
        subtitle = self.small_font.render("Press Enter to start", True, BLUE)
        controls = self.small_font.render("Move: WASD/Arrows  Shoot: Space  Pause: P", True, WHITE)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 120))
        self.screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2 - 40))
        self.screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT // 2 + 20))

    def draw_game_over(self, score):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        self.screen.blit(overlay, (0, 0))
        title = self.font.render("Game Over", True, RED)
        score_text = self.font.render(f"Final Score: {score}", True, WHITE)
        restart_text = self.small_font.render("Press Enter or R to restart", True, BLUE)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 30))
