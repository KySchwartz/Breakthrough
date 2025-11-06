# breakthrough_board.py
import pygame
import sys
import copy
import time
import random
import json
import csv
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any

# Window and board constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQ = WIDTH // COLS

# Colors
LIGHT = (210, 180, 140)  # tan
DARK  = (139, 69, 19)    # brown
WHITE = (245, 245, 245)  # white
BLACK = (30, 30, 30)     # black
HILITE= (255, 215, 0)    # yellow
MOVEH = (0, 170, 255)    # move target highlight

# Board representation utils
def new_start_board() -> List[List[Optional[str]]]:
    """None = empty, 'W' = white pawn, 'B' = black pawn"""
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    # Black on rows 0 and 1 (moves +1 down)
    for r in (0, 1):
        for c in range(COLS):
            board[r][c] = 'B'
    # White on rows 6 and 7 (moves -1 up)
    for r in (6, 7):
        for c in range(COLS):
            board[r][c] = 'W'
    return board


# Step 1: Game scaffold
Move = Tuple[int, int, int, int]  # (r0, c0, r1, c1)

@dataclass
class GameState:
    board: List[List[Optional[str]]]
    to_move: str = 'W'   # White moves first
    move_idx: int = 0

    def clone(self) -> "GameState":
        return GameState(copy.deepcopy(self.board), self.to_move, self.move_idx)

def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < ROWS and 0 <= c < COLS

def legal_moves(state: GameState) -> List[Move]:
    """Breakthrough rules: forward 1 if empty; diagonals capture only."""
    board, side = state.board, state.to_move
    dr = -1 if side == 'W' else 1
    enemy = 'B' if side == 'W' else 'W'
    moves: List[Move] = []
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != side:
                continue
            # forward
            r1, c1 = r + dr, c
            if in_bounds(r1, c1) and board[r1][c1] is None:
                moves.append((r, c, r1, c1))
            # diag-left capture
            r1, c1 = r + dr, c - 1
            if in_bounds(r1, c1) and board[r1][c1] == enemy:
                moves.append((r, c, r1, c1))
            # diag-right capture
            r1, c1 = r + dr, c + 1
            if in_bounds(r1, c1) and board[r1][c1] == enemy:
                moves.append((r, c, r1, c1))
    return moves

def moves_from(state: GameState, r0: int, c0: int) -> List[Move]:
    """All legal moves starting at (r0,c0)."""
    return [m for m in legal_moves(state) if m[0] == r0 and m[1] == c0]

def apply_move(state: GameState, move: Move) -> GameState:
    r0, c0, r1, c1 = move
    side = state.to_move
    nxt = state.clone()
    nxt.board[r1][c1] = side
    nxt.board[r0][c0] = None
    nxt.to_move = 'B' if side == 'W' else 'W'
    nxt.move_idx += 1
    return nxt

def has_won(board: List[List[Optional[str]]], side: str) -> bool:
    if side == 'W':
        return any(board[0][c] == 'W' for c in range(COLS))
    else:
        return any(board[ROWS-1][c] == 'B' for c in range(COLS))

def terminal_and_winner(state: GameState) -> Tuple[bool, Optional[str]]:
    if has_won(state.board, 'W'):
        return True, 'W'
    if has_won(state.board, 'B'):
        return True, 'B'
    # no pieces left
    w_exists = any(cell == 'W' for row in state.board for cell in row)
    b_exists = any(cell == 'B' for row in state.board for cell in row)
    if not w_exists:
        return True, 'B'
    if not b_exists:
        return True, 'W'
    # no legal moves (treat as loss for side to move)
    if not legal_moves(state):
        return True, 'B' if state.to_move == 'W' else 'W'
    return False, None


# Step 2: Instrumentation
class Timer:
    def __enter__(self):
        self.t0 = time.perf_counter()
        return self
    def __exit__(self, *exc):
        self.dt = time.perf_counter() - self.t0

@dataclass
class MoveStats:
    move_idx: int
    side: str
    nodes_expanded: int
    move_time_sec: float

class Agent:
    """Placeholder agent. Replace choose() with search later.
       Keep counters so instrumentation works transparently."""
    def __init__(self):
        self.nodes_expanded = 0
    def reset_counters(self):
        self.nodes_expanded = 0
    def choose(self, state: GameState) -> Move:
        # Random legal move (no search). Override later with minimax/alpha-beta.
        self.nodes_expanded = 1  # placeholder so logs aren't zero
        return random.choice(legal_moves(state))

def play_match_instrumented(agent_w: Agent, agent_b: Agent, seed: int = 0,
                            csv_path: Optional[str] = None,
                            json_path: Optional[str] = None) -> Dict[str, Any]:
    random.seed(seed)
    state = GameState(new_start_board(), 'W', 0)
    per_move: List[MoveStats] = []
    captured_total = 0

    csvf = csvw = None
    if csv_path:
        csvf = open(csv_path, "w", newline="")
        csvw = csv.writer(csvf)
        csvw.writerow(["move_idx", "side", "nodes_expanded", "move_time_sec"])

    while True:
        term, win = terminal_and_winner(state)
        if term:
            result = {
                "winner": win,
                "final_board": state.board,
                "total_moves": state.move_idx,
                "captured_total": captured_total,
                "per_move": [m.__dict__ for m in per_move],
            }
            if json_path:
                with open(json_path, "w") as jf:
                    json.dump(result, jf, indent=2)
            if csvf:
                csvf.close()
            return result

        agent = agent_w if state.to_move == 'W' else agent_b
        if hasattr(agent, "reset_counters"):
            agent.reset_counters()

        with Timer() as t:
            mv = agent.choose(state)

        # capture counting
        r0, c0, r1, c1 = mv
        if state.board[r1][c1] is not None:
            captured_total += 1

        nodes = getattr(agent, "nodes_expanded", 0)
        stats = MoveStats(state.move_idx + 1, state.to_move, nodes, t.dt)
        per_move.append(stats)
        if csvw:
            csvw.writerow([stats.move_idx, stats.side, stats.nodes_expanded, stats.move_time_sec])

        state = apply_move(state, mv)

# Drawing / GUI helpers
def draw_board(surface):
    surface.fill(DARK)
    for r in range(ROWS):
        for c in range(COLS):
            color = LIGHT if (r + c) % 2 == 0 else DARK
            pygame.draw.rect(surface, color, (c*SQ, r*SQ, SQ, SQ))

def draw_pieces(surface, board, selected=None, targets: Optional[List[Tuple[int,int]]] = None):
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

    # highlight selected and targets
    if selected is not None:
        r, c = selected
        pygame.draw.rect(surface, HILITE, (c*SQ+3, r*SQ+3, SQ-6, SQ-6), 3)
    if targets:
        for (tr, tc) in targets:
            pygame.draw.rect(surface, MOVEH, (tc*SQ+6, tr*SQ+6, SQ-12, SQ-12), 3)


# Pygame loop (manual play)
def run_gui():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Breakthrough (manual) - Step 1/2 scaffold")
    clock = pygame.time.Clock()

    state = GameState(new_start_board(), 'W', 0)
    selected = None
    target_cells: List[Tuple[int, int]] = []
    running = True
    winner_text = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if winner_text is None and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                c, r = mx // SQ, my // SQ
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if selected is None:
                        # select a piece of the side to move
                        if state.board[r][c] == state.to_move:
                            selected = (r, c)
                            target_cells = [(m[2], m[3]) for m in moves_from(state, r, c)]
                    else:
                        # check if clicked a target; if so, apply move
                        sr, sc = selected
                        chosen = None
                        for m in moves_from(state, sr, sc):
                            if (r, c) == (m[2], m[3]):
                                chosen = m
                                break
                        if chosen:
                            state = apply_move(state, chosen)
                            selected = None
                            target_cells = []
                            term, win = terminal_and_winner(state)
                            if term:
                                winner_text = f"Winner: {win}"
                                pygame.display.set_caption(f"Breakthrough - {winner_text}")
                        else:
                            # reselect or clear
                            if state.board[r][c] == state.to_move:
                                selected = (r, c)
                                target_cells = [(m[2], m[3]) for m in moves_from(state, r, c)]
                            else:
                                selected = None
                                target_cells = []

        draw_board(screen)
        draw_pieces(screen, state.board, selected, target_cells)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


# Headless demo of logging
def headless_demo():
    aW, aB = Agent(), Agent()
    summary = play_match_instrumented(
        aW, aB, seed=42,
        csv_path="match_log.csv",
        json_path="match_summary.json"
    )
    print("Winner:", summary["winner"])
    print("Total moves:", summary["total_moves"])
    print("Moves logged to match_log.csv; summary in match_summary.json")


# Entrypoint
if __name__ == "__main__":
    run_gui()

    

# Alpha-Beta Agent (depth=4)
class AlphaBetaAgent:
    def __init__(self, depth: int = 4):
        self.depth = depth
        self.nodes_expanded = 0

    def reset_counters(self):
        self.nodes_expanded = 0

    # Evaluation from the perspective of max_side ('W' or 'B')
    def evaluate(self, state: GameState, max_side: str) -> float:
        # Material
        w_cnt = sum(1 for row in state.board for x in row if x == 'W')
        b_cnt = sum(1 for row in state.board for x in row if x == 'B')
        material = w_cnt - b_cnt

        # Advancement (reward being closer to goal rank)
        adv_w = 0
        adv_b = 0
        for r in range(ROWS):
            for c in range(COLS):
                if state.board[r][c] == 'W':
                    # Closer to row 0 is better
                    adv_w += (ROWS - 1 - r)
                elif state.board[r][c] == 'B':
                    # Closer to row ROWS-1 is better
                    adv_b += r
        advancement = (adv_w - adv_b) / 10.0  # small weight

        score_white = material + advancement
        score = score_white if max_side == 'W' else -(score_white)
        return score

    # Move ordering: prefer captures first
    def ordered_moves(self, state: GameState) -> List[Move]:
        ms = legal_moves(state)
        # A move is a capture if destination currently has an enemy piece
        def is_capture(m: Move) -> int:
            r0, c0, r1, c1 = m
            return 1 if state.board[r1][c1] is not None else 0
        # Sort: captures first
        ms.sort(key=is_capture, reverse=True)
        return ms

    def alphabeta(self, state: GameState, depth: int, alpha: float, beta: float, max_side: str) -> float:
        self.nodes_expanded += 1

        terminal, winner = terminal_and_winner(state)
        if terminal:
            if winner == max_side:
                return 10_000.0  # big positive
            elif winner is None:
                return 0.0
            else:
                return -10_000.0  # big negative

        if depth == 0:
            return self.evaluate(state, max_side)

        # If it's max_side's turn then maximizing node; else minimizing node
        maximizing = (state.to_move == max_side)

        if maximizing:
            value = -float('inf')
            for mv in self.ordered_moves(state):
                child = apply_move(state, mv)
                value = max(value, self.alphabeta(child, depth - 1, alpha, beta, max_side))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # beta cut
            return value
        else:
            value = float('inf')
            for mv in self.ordered_moves(state):
                child = apply_move(state, mv)
                value = min(value, self.alphabeta(child, depth - 1, alpha, beta, max_side))
                beta = min(beta, value)
                if alpha >= beta:
                    break  # alpha cut
            return value

    def choose(self, state: GameState) -> Move:
        """Return best move for side-to-move using alpha-beta at fixed depth."""
        self.nodes_expanded = 0
        max_side = state.to_move
        best_mv: Optional[Move] = None
        best_val = -float('inf')

        # If no moves (should be terminal), just return any to avoid crash
        moves = self.ordered_moves(state)
        if not moves:
            return (0, 0, 0, 0)  # unreachable if terminal handled elsewhere

        alpha, beta = -float('inf'), float('inf')
        for mv in moves:
            child = apply_move(state, mv)
            val = self.alphabeta(child, self.depth - 1, alpha, beta, max_side)
            if val > best_val:
                best_val = val
                best_mv = mv
            alpha = max(alpha, best_val)

        return best_mv


