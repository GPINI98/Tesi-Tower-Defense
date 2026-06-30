# enemy.py
import pygame
import config

class Enemy:
    def __init__(self):
        # Stato iniziale del nemico
        self.width = 30
        self.height = 30
        self.x = -self.width  # Parte appena fuori dallo schermo a sinistra
        self.y = config.SCREEN_HEIGHT // 2  # A metà altezza dello schermo
        self.speed = config.ENEMY_SPEED
        self.color = config.RED

    def update(self):
        # Logica di movimento: si sposta verso destra
        self.x += self.speed

    def draw(self, screen):
        # Disegna il nemico a schermo (un semplice rettangolo per ora)
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)