# main.py
import pygame
import random
import config
from enemy import StandardEnemy, FastEnemy, TankEnemy
from tower import Tower
from config import percorsi

pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption("Tesi Tower Defense - Motore di Gioco")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36) # Font per i testi a schermo
font_gameover = pygame.font.SysFont(None, 100) # Font Game Over

# --- STATO DEL GIOCO ---
running = True
game_over = False
oro_giocatore = 150  # Soldi iniziali
vite_giocatore = 10

# Liste delle entità di gioco
enemies = []
towers = []
bullets = []  # Lista che gestisce i proiettili attivi (Capitolo 3)

# Timer per generare un nemico ogni 1.5 secondi
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1500)

while running:
    # FASE 1: INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Generazione casuale dei nemici
        elif event.type == SPAWN_EVENT and not game_over:
            TipoNemico = random.choice([StandardEnemy, FastEnemy, TankEnemy])
            percorso_scelto = random.choice(percorsi)
            enemies.append(TipoNemico(start_pos=percorso_scelto[0], waypoints=percorso_scelto))
            
        # Gestione Mouse (Piazzamento e Upgrade Torri)
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if event.button == 1: # Click sinistro
                mouse_pos = pygame.mouse.get_pos()
                torre_cliccata = False
                
                # 1. Controlla se abbiamo cliccato su una torre già esistente (Upgrade)
                for tower in towers:
                    if tower.rect.collidepoint(mouse_pos):
                        torre_cliccata = True
                        if oro_giocatore >= tower.upgrade_cost:
                            oro_giocatore -= tower.upgrade_cost
                            tower.upgrade()
                        break
                
                # 2. Se abbiamo cliccato sul vuoto, prova a comprare una nuova torre
                if not torre_cliccata:
                    if oro_giocatore >= config.TOWER_COST:
                        oro_giocatore -= config.TOWER_COST
                        towers.append(Tower(mouse_pos[0], mouse_pos[1]))

    # FASE 2: UPDATE (Logica di Gioco)
    if not game_over:
        # Aggiornamento nemici
        for enemy in enemies[:]:
            enemy.update()

            # Controllo se il nemico è morto
            if enemy.health <= 0:
                oro_giocatore += enemy.reward
                enemies.remove(enemy)
            # Il nemico ha raggiunto la fine del percorso?
            elif enemy.current_waypoint_index >= len(enemy.waypoints):
                vite_giocatore -= 1
                enemies.remove(enemy)

                if vite_giocatore <= 0:
                    game_over = True

        # Aggiornamento torri (passando nemici e lista proiettili)
        for tower in towers:
            tower.update(enemies, bullets)

        # Aggiornamento proiettili (ciclo con copia per rimozione sicura)
        for bullet in bullets[:]:
            if bullet.update(enemies):
                bullets.remove(bullet)

    # FASE 3: RENDERING 
    screen.fill(config.BLACK)
    
    # 1. Disegna i sentieri
    for p in percorsi:
        pygame.draw.lines(screen, config.DARK_GRAY, False, p, 40)

    # 2. Disegna i nemici
    for enemy in enemies:
        enemy.draw(screen)

    # 3. Disegna le torri
    for tower in towers:
        tower.draw(screen)

    # 4. Disegna i proiettili
    for bullet in bullets:
        bullet.draw(screen)

    # 5. Interfaccia Utente (UI) in alto a sinistra
    ui_testo = font.render(f"Oro: {oro_giocatore} | Vite: {vite_giocatore} | Costo Torre: {config.TOWER_COST}", True, config.WHITE)
    screen.blit(ui_testo, (10, 10))

    # 6. Gestione schermata Game Over
    if game_over:
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(config.BLACK)
        screen.blit(overlay, (0, 0))
        
        testo_go = font_gameover.render("GAME OVER", True, config.RED)
        rect_go = testo_go.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2))
        screen.blit(testo_go, rect_go)
    
    pygame.display.flip()

    # Gestione FPS 
    clock.tick(config.FPS)

pygame.quit()