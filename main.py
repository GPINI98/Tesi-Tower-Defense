# main.py
import pygame
import config
from enemy import Enemy
from tower import Tower  # NUOVO: Importiamo la torre

pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Tesi Tower Defense - Motore di Gioco")
clock = pygame.time.Clock()
running = True

# Creazione delle istanze (Entità del gioco)
test_enemy = Enemy()
# NUOVO: Posizioniamo la torre al centro dello schermo
test_tower = Tower(config.SCREEN_WIDTH // 2 - 20, config.SCREEN_HEIGHT // 2 - 20)

while running:
    # A. Input Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # B. Update (Logica del gioco)
    test_enemy.update()

    # C. Rendering (Disegno a schermo)
    screen.fill(config.BLACK)
    
    # L'ordine di rendering è importante (chi viene disegnato per ultimo sta "sopra")
    test_tower.draw(screen, test_enemy)  # NUOVO: Disegna prima la torre (e il suo raggio)
    test_enemy.draw(screen)  # Poi disegna il nemico
    
    pygame.display.flip()

    # D. Sincronizzazione (Clock)
    clock.tick(config.FPS)

pygame.quit()