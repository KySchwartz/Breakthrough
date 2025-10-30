# breakthrough_board.py
import pygame
import sys

# window and square size
WIDTH, HEIGHT = 640, 640           
ROWS, COLS = 8, 8
SQ = WIDTH // COLS                 

# Colors
LIGHT = (210, 180, 140)  # tan
DARK  = (139, 69, 19)    # brown
WHITE = (245, 245, 245)  # white
BLACK = (30, 30, 30)     # black
HILITE= (255, 215, 0)    # yellow

# Board representation:
# None = empty, 'W' = white pawn, 'B' = black pawn
def new_start_board():
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    # Black pawns on rows 0 and 1 (move +1 down)
    for r in (0, 1):
        for c in range(COLS):
            board[r][c] = 'B'
    # White pawns on rows 6 and 7 (move -1 up)
    for r in (6, 7):
        for c in range(COLS):
            board[r][c] = 'W'
    return board

def draw_board(surface):
    surface.fill(DARK)
    for r in range(ROWS):
        for c in range(COLS):
            color = LIGHT if (r + c) % 2 == 0 else DARK
            pygame.draw.rect(surface, color, (c*SQ, r*SQ, SQ, SQ))

def draw_pieces(surface, board, selected=None):
    for r in range(ROWS):
        for c in range(COLS):
            piece = board[r][c]
            if piece is None:
                continue
            cx = c * SQ + SQ // 2
            cy = r * SQ + SQ // 2
            radius = int(SQ * 0.36)
            col = WHITE if piece == 'W' else BLACK
            pygame.draw.circle(surface, col, (cx, cy), radius)
            pygame.draw.circle(surface, (0,0,0), (cx, cy), radius, 2)

    # highlight
    if selected is not None:
        r, c = selected
        pygame.draw.rect(
            surface, HILITE, (c*SQ+3, r*SQ+3, SQ-6, SQ-6), 3
        )

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Breakthrough game")
    clock = pygame.time.Clock()

    board = new_start_board()
    selected = None  # (row, col) if you want to click-select later
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # click to highlight a square/piece
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                c, r = mx // SQ, my // SQ
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if selected == (r, c):
                        selected = None
                    else:
                        selected = (r, c)

        draw_board(screen)
        draw_pieces(screen, board, selected)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
