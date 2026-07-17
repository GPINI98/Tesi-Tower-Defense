# main.py
import pygame
import config
from enemy import Enemy
from tower import Tower  

pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Tesi Tower Defense - Motore di Gioco")
clock = pygame.time.Clock()
running = True

# Waypoints
# Definisce strada dei nemici
percorso_di_prova = [(0, 300), (400, 300), (400, 500)]
punto_di_partenza = percorso_di_prova[0]

# nemico di test
test_enemy = Enemy(start_pos=punto_di_partenza, waypoints=percorso_di_prova)

# Torre al centro dello schermo
test_tower = Tower(config.SCREEN_WIDTH // 2 - 20, config.SCREEN_HEIGHT // 2 - 20)

while running:
    # Fase 1: Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fase 2: Update
    test_enemy.update()
    
    # Controllo se il nemico è morto
    if test_enemy.health <= 0:
        test_enemy = Enemy(start_pos=punto_di_partenza, waypoints=percorso_di_prova)

    # Fase 3: Rendering 
    screen.fill(config.BLACK)
    
    test_tower.draw(screen, test_enemy)  # Disegna prima la torre +  il suo raggio
    test_enemy.draw(screen)  # Poi disegna il nemico
    
    pygame.display.flip()

    # Gestione FPS 
    clock.tick(config.FPS)

pygame.quit()


