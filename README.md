# Tower Defense

## Descrizione

Il progetto consiste nella realizzazione di un videogioco Tower Defense in cui il giocatore deve utilizzare torri difensive per contrastare l'avanzata dei nemici lungo un percorso prestabilito.

Lo sviluppo è stato un'occasione per applicare concetti di programmazione orientata agli oggetti, gestione degli eventi e logica di gioco, organizzando il codice in classi e moduli distinti.

## Funzionalità

- Movimento dei nemici lungo un percorso definito tramite waypoint.
- Gestione di diverse tipologie di nemici.
- Torri difensive con sistema di individuazione automatica dei bersagli.
- Gestione dei proiettili e delle interazioni con i nemici.
- Posizionamento delle torri tramite una griglia.
- Gestione delle ondate e delle principali risorse di gioco.

## Tecnologie utilizzate

- **Python** – linguaggio di programmazione.
- **Pygame** – libreria per lo sviluppo del videogioco.
- **Git** – sistema di versionamento del codice.
- **GitHub** – hosting del repository.

## Struttura del progetto

| File | Descrizione |
|---|---|
| `main.py` | Gestione principale del gioco e del ciclo di esecuzione. |
| `enemy.py` | Definizione e comportamento dei nemici. |
| `tower.py` | Logica delle torri difensive. |
| `bullet.py` | Gestione dei proiettili. |
| `config.py` | Parametri e configurazioni del gioco. |

## Installazione ed esecuzione

È necessario avere Python installato sul proprio computer.

1. Clonare il repository:

   ```bash
   git clone https://github.com/GPINI98/Tesi-Tower-Defense.git
   ```

2. Entrare nella cartella del progetto:

   ```bash
   cd Tesi-Tower-Defense
   ```

3. Installare Pygame:

   ```bash
   python -m pip install pygame
   ```

4. Avviare il gioco:

   ```bash
   python main.py
   ```
   
## Obiettivi del progetto

Il progetto ha permesso di approfondire la programmazione orientata agli oggetti, la gestione del movimento tramite vettori, l'interazione tra diversi componenti del gioco e l'organizzazione del codice in moduli distinti.

## Contesto

Progetto di Tesi realizzato nell'ambito del percorso di studi in Ingegneria Informatica.
