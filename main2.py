import pygame
import sys
import os
import json

import logic_2048 as logic
import logic_20482

SIZE = logic.SIZE
TILE_SIZE = 100
MARGIN = 10
TOP_MARGIN = 100

WINDOW_WIDTH = SIZE * TILE_SIZE + (SIZE + 1) * MARGIN
WINDOW_HEIGHT = SIZE * TILE_SIZE + (SIZE + 1) * MARGIN + TOP_MARGIN

BG_COLOR = (187, 173, 160)
TEXT_COLOR = (119, 110, 101)
SCORE_COLOR = (249, 246, 242)
BUTTON_BG = (119, 110, 101)
BUTTON_TEXT = (255, 255, 255)

TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

STATS_FILE = "stats.json"
WIN_TILE = 2048

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {"games": []}


def add_stat(score, moves, max_tile, won):
    stats = load_stats()
    stats["games"].append({
        "score": score,
        "moves": moves,
        "max_tile": max_tile,
        "won": won
    })
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)


def print_stats():
    stats = load_stats()
    games = stats.get("games", [])
    print("\n===== STATISTIKY TESTU =====")
    print(f"Počet her: {len(games)}")
    if games:
        scores = [g["score"] for g in games]
        tiles = [g["max_tile"] for g in games]
        wins = sum(1 for g in games if g.get("won"))
        print(f"Průměrné skóre: {sum(scores)/len(scores):.1f}")
        print(f"Průměrná max hodnota: {sum(tiles)/len(tiles):.1f}")
        print(f"Dosaženo 2048+: {wins}x ({wins/len(games)*100:.1f}%)")
        print("--- TOP 3 SKÓRE ---")
        for i, sc in enumerate(sorted(scores, reverse=True)[:3], 1):
            print(f"{i}. {sc}")
        print("--- TOP 3 DLAŽDICE ---")
        for i, t in enumerate(sorted(tiles, reverse=True)[:3], 1):
            print(f"{i}. {t}")
    print("===== KONEC STATISTIK =====\n")

def draw_board(screen, board, score, font, game_number=None, games_total=None):
    screen.fill(BG_COLOR)
    title_font = pygame.font.SysFont(None, 60)
    title = "2048 - Monte Carlo AI2"
    if game_number and games_total:
        title += f"  Hra {game_number}/{games_total}"
    screen.blit(title_font.render(title, True, TEXT_COLOR), (MARGIN, MARGIN))
    screen.blit(font.render(f"Skóre: {score}", True, SCORE_COLOR), (MARGIN, 60))

    for r in range(SIZE):
        for c in range(SIZE):
            val = board[r][c]
            color = TILE_COLORS.get(val, TILE_COLORS[2048])
            x = c * TILE_SIZE + (c + 1) * MARGIN
            y = r * TILE_SIZE + (r + 1) * MARGIN + TOP_MARGIN
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect, border_radius=5)
            if val:
                txt = font.render(str(val), True, TEXT_COLOR)
                screen.blit(txt, txt.get_rect(center=rect.center))

def run_automatic_test(total_games=30, ai_speed=0):
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2048 - Automatický test AI2")
    font = pygame.font.SysFont(None, 40)

    # Reset statistics
    if os.path.exists(STATS_FILE):
        os.remove(STATS_FILE)
    else:
        with open(STATS_FILE, "w") as f:
            json.dump({"games": []}, f)

    print(f"SPOUŠTÍM AUTOMATICKÝ TEST - {total_games} HER")
    print("----------------------------------")

    for game_number in range(1, total_games + 1):
        print(f"\nZačíná hra {game_number}/{total_games}")
        board = logic.init_board()
        score = 0
        moves = 0
        running = True

        while running:
            new_board, changed, new_score = logic_20482.ai2_move(board, score)
            if changed:
                board, score = new_board, new_score
                moves += 1
                logic.spawn_new_tile(board)
                if not logic.can_move(board):
                    max_tile = max(max(row) for row in board)
                    won = max_tile >= WIN_TILE
                    add_stat(score, moves, max_tile, won)
                    print(f"Konec hry {game_number}! Skóre: {score}, Max hodnota: {max_tile}, Tahy: {moves}")
                    running = False
            pygame.time.wait(ai_speed)
            draw_board(screen, board, score, font, game_number, total_games)
            pygame.display.flip()

    print(f"\n===== SOUHRN AUTOMATICKÉHO TESTU ({total_games} HER) =====")
    print_stats()
    pygame.quit()
    sys.exit()

def main():
    run_automatic_test(total_games=30, ai_speed=0)

if __name__ == "__main__":
    main()