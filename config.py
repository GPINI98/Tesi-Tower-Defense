# Modulo di configurazione per Tesi Tower Defense

# Dimensioni Schermo
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Parametri Gioco
FPS = 60

# Colori (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)       # Nemico Standard
YELLOW = (255, 255, 0)  # Nemico Veloce / Colore Proiettile
GRAY = (150, 150, 150)  # Nemico Corazzato
BLUE = (0, 0, 255)      # Torre
DARK_GRAY = (50, 50, 50) # Colore del sentiero
GREEN = (0, 255, 0)     # Barra della vita

# Game Balance 
ENEMY_SPEED = 2
TOWER_RANGE = 120
TOWER_COST = 50
UPGRADE_COST = 50

# Parametri Proiettile (Capitolo 3)
BULLET_SPEED = 6
BULLET_SIZE = 5

# Waypoints: Definiscono le strade dei nemici
percorsi = [
    [(0, 100), (400, 100), (400, 300), (200, 300), (200, 500), (800, 500)], # 1. Entra da sinistra
    [(400, 0), (400, 100), (600, 100), (600, 400), (800, 400)],             # 2. Entra dall'alto
    [(0, 450), (300, 450), (300, 200), (700, 200), (700, 600)]              # 3. Entra dal basso a sinistra
]