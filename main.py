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

# --- GESTIONE ONDATE (WAVES) ---
onda_corrente = 1
nemici_totali_onda = 5      # Quanti nemici compongono la prima ondata
nemici_spawnati_onda = 0    # Contatore dei nemici già generati nell'ondata corrente
pausa_tra_ondate = False
timer_pausa = 0

# Liste delle entità di gioco
enemies = []
towers = []
bullets = []

# Timer per generare un nemico a intervalli regolari (ogni 1.5 secondi)
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1500)

while running:
    current_time = pygame.time.get_ticks()

    # FASE 1: INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Generazione nemici controllata dal sistema a ondate
        elif event.type == SPAWN_EVENT and not game_over and not pausa_tra_ondate:
            # Inizia a generare nemici solo dopo che sono trascorsi 5 secondi dall'avvio
            if current_time >= 5000:
                if nemici_spawnati_onda < nemici_totali_onda:
                    TipoNemico = random.choice([StandardEnemy, FastEnemy, TankEnemy])
                    percorso_scelto = random.choice(percorsi)
                    enemies.append(TipoNemico(start_pos=percorso_scelto[0], waypoints=percorso_scelto))
                    nemici_spawnati_onda += 1

        # Generazione nemici controllata dal sistema a ondate
       # elif event.type == SPAWN_EVENT and not game_over and not pausa_tra_ondate:
            # Se ci sono ancora nemici da spawnare in questa ondata
           # if nemici_spawnati_onda < nemici_totali_onda:
               # TipoNemico = random.choice([StandardEnemy, FastEnemy, TankEnemy])
               # percorso_scelto = random.choice(percorsi)
               # enemies.append(TipoNemico(start_pos=percorso_scelto[0], waypoints=percorso_scelto))
               # nemici_spawnati_onda += 1
            
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
                
                # 2. Se abbiamo cliccato sul vuoto, prova a comprare una nuova torre (SISTEMA A GRIGLIA)
                if not torre_cliccata:
                    CELL_SIZE = 40 # Dimensione fissa della cella (la torre è 40x40)
                    
                    # Discretizzazione: converte la posizione del mouse nel centro della cella di griglia
                    grid_x = (mouse_pos[0] // CELL_SIZE) * CELL_SIZE + (CELL_SIZE // 2)
                    grid_y = (mouse_pos[1] // CELL_SIZE) * CELL_SIZE + (CELL_SIZE // 2)
                    
                    # Crea un rect provvisorio per verificare le collisioni prima di piazzare
                    new_rect = pygame.Rect(grid_x - CELL_SIZE//2, grid_y - CELL_SIZE//2, CELL_SIZE, CELL_SIZE)
                    
                    # Verifica che la cella non sia già occupata da un'altra torre
                    cella_occupata = False
                    for tower in towers:
                        if tower.rect.colliderect(new_rect):
                            cella_occupata = True
                            break
                    
                    # Se la cella è libera e ci sono i soldi, piazza la torre allineata alla griglia
                    if not cella_occupata and oro_giocatore >= config.TOWER_COST:
                        oro_giocatore -= config.TOWER_COST
                        towers.append(Tower(grid_x, grid_y))

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

        # Aggiornamento torri
        for tower in towers:
            tower.update(enemies, bullets)

        # Aggiornamento proiettili
        for bullet in bullets[:]:
            if bullet.update(enemies):
                bullets.remove(bullet)

        # --- LOGICA DI TRANSIZIONE ONDATE ---
        # Condizione di fine ondata: abbiamo spawnato tutti i nemici dell'onda E non ce ne sono più attivi a schermo
        if nemici_spawnati_onda >= nemici_totali_onda and len(enemies) == 0:
            if not pausa_tra_ondate:
                pausa_tra_ondate = True
                timer_pausa = current_time # Registra l'inizio della pausa
                oro_giocatore += 50 * onda_corrente # Bonus in oro per aver completato l'ondata
            
            # Aspetta 3 secondi (3000 ms) prima di far partire l'ondata successiva
            elif current_time - timer_pausa >= 3000:
                onda_corrente += 1
                nemici_totali_onda += 4  # Aumenta la difficoltà aggiungendo 4 nemici in più per la prossima onda
                nemici_spawnati_onda = 0 # Resetta il contatore di spawn
                pausa_tra_ondate = False

    # FASE 3: RENDERING 
    screen.fill(config.BLACK)
 ########################################################################à   
# --- CODICE TEMPORANEO PER SCREENSHOT GRIGLIA ---
    CELL_SIZE = 40
    COLORE_GRIGLIA = (50, 50, 50)

    # Linee verticali
    for x in range(0, config.SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, COLORE_GRIGLIA, (x, 0), (x, config.SCREEN_HEIGHT), 1)

    # Linee orizzontali
    for y in range(0, config.SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, COLORE_GRIGLIA, (0, y), (config.SCREEN_WIDTH, y), 1)
    # ------------------------------------------------
##############################################################################

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

    # 5. Interfaccia Utente (UI) con indicazione dell'Onda
    ui_testo = font.render(
        f"Onda: {onda_corrente} | Oro: {oro_giocatore} | Vite: {vite_giocatore} | Costo Torre: {config.TOWER_COST}", 
        True, 
        config.WHITE
    )
    screen.blit(ui_testo, (10, 10))

# Messaggio visivo dinamico con conto alla rovescia durante la pausa tra le ondate
    if pausa_tra_ondate and not game_over:
        # Calcoliamo i millisecondi trascorsi dall'inizio della pausa
        tempo_trascorso = current_time - timer_pausa
        tempo_rimanente_ms = max(0, 3000 - tempo_trascorso)  # 3000 ms = 3 secondi di pausa
        secondi_rimanenti = int(tempo_rimanente_ms / 1000) + 1  # Arrotonda per eccesso per mostrare da 3 a 1

        testo_pausa = font.render(
            f"Onda {onda_corrente - 1} completata! Prossima onda tra: {secondi_rimanenti}s", 
            True, 
            config.YELLOW
        )
        rect_pausa = testo_pausa.get_rect(center=(config.SCREEN_WIDTH // 2, 60))
        screen.blit(testo_pausa, rect_pausa)

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