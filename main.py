# main.py
import pygame
import config
from enemy import Enemy  # NUOVO: Importiamo la classe appena creata

# 1. Inizializzazione del motore
pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Tesi Tower Defense - Motore di Gioco")
clock = pygame.time.Clock()
running = True

# NUOVO: Creazione di una singola "istanza" del nemico
test_enemy = Enemy()

# 2. Game Loop (Il cuore pulsante)
while running:
    # A. Input Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # B. Update (Logica del gioco)
    test_enemy.update()  # NUOVO: Aggiorna la posizione del nemico

    # C. Rendering (Disegno a schermo)
    screen.fill(config.BLACK)
    
    test_enemy.draw(screen)  # NUOVO: Disegna il nemico sopra lo sfondo
    
    pygame.display.flip()

    # D. Sincronizzazione (Clock)
    clock.tick(config.FPS)

pygame.quit()