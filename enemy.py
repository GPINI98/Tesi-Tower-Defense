# enemy.py
import pygame
import config

class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_pos, waypoints):
        super().__init__()
        
        # --- Attributi Grafici ---
        self.width = 30
        self.height = 30
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(config.RED) 
        self.rect = self.image.get_rect()
        
        # --- Attributi di default ---
        self.color = config.WHITE
        self.max_health = 100
        self.health = self.max_health
        self.speed = config.ENEMY_SPEED
        self.reward = 20 # Premio in monete alla morte
        
        # --- Attributi Spaziali ---
        self.pos = pygame.math.Vector2(start_pos)
       # self.rect.center = self.pos
        self.rect = self.image.get_rect(center=self.pos)
        self.waypoints = waypoints
        self.current_waypoint_index = 0  # Parte dal primo punto d'angolo

    def update(self):
        # Se abbiamo raggiunto la fine del percorso, non facciamo nulla
        if self.current_waypoint_index >= len(self.waypoints):
            return

        #  waypoint corrente
        target = pygame.math.Vector2(self.waypoints[self.current_waypoint_index])
        
        # Calcola distanza e vettore verso il target
        direzione = target - self.pos
        distanza = direzione.length()

        # Controllo di collisione con il Waypoint (SISTEMA WAYPOINT)
        # Se siamo abbastanza vicini al waypoint (meno dei pixel che copriamo in un frame)
        if distanza <= self.speed:
            self.pos = target  # Posiziona esattamente sul punto per evitare oscillazioni
            self.current_waypoint_index += 1  # Passa al waypoint successivo
        else:
            # Movimento vettoriale (CINEMATICA - Paragrafo 2.3)
            # Normalizziamo il vettore direzione (lo rendiamo di lunghezza 1)
            direzione_normalizzata = direzione.normalize()
            # Spostiamo la posizione float in base alla direzione e alla velocità
            self.pos += direzione_normalizzata * self.speed
            
        # Aggiorna il rect grafico (troncando a valori interi per lo schermo)
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        if self.health > 0:
            pygame.draw.rect(screen, config.RED, (self.rect.left, self.rect.top - 10, self.width, 5))
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, config.GREEN, (self.rect.left, self.rect.top - 10, self.width * health_ratio, 5))

            # --- CLASSI FIGLIE (I 3 tipi di nemici) ---

class StandardEnemy(Enemy):
    def __init__(self, start_pos, waypoints):
        super().__init__(start_pos, waypoints)
        self.color = config.RED
        self.image.fill(self.color)
        # Usa le statistiche base (100 HP, 2 Speed, 20 Oro)

class FastEnemy(Enemy):
    def __init__(self, start_pos, waypoints):
        super().__init__(start_pos, waypoints)
        self.max_health = 50      # Metà vita
        self.health = self.max_health
        self.speed = 4            # Velocità doppia
        self.reward = 15          # Dà meno oro
        self.color = config.YELLOW
        self.image.fill(self.color)

class TankEnemy(Enemy):
    def __init__(self, start_pos, waypoints):
        super().__init__(start_pos, waypoints)
        self.max_health = 250     # Tantissima vita
        self.health = self.max_health
        self.speed = 1            # Lento
        self.reward = 50          # Dà molto oro
        self.color = config.GRAY
        self.image.fill(self.color)