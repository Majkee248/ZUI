import random
import json
import os
from datetime import datetime

SIZE = 4
STATS_FILE = "stats.json"
WIN_TILE = 2048

def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, dict) and "games" in data:
                    return data
                print("Warning: Stats file has incorrect format. Creating new file.")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading stats file: {e}. Creating new file.")
    return {"games": [], "summary": {}}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

def add_stat(score, moves, max_tile, moves_by_direction, won=False):
    try:
        stats = load_stats()
        if not isinstance(stats, dict):
            stats = {"games": [], "summary": {}}
        if "games" not in stats:
            stats["games"] = []

        game_data = {
            "score": score,
            "moves": moves,
            "max_tile": max_tile,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "won": won,
            "moves_up": moves_by_direction.get("up", 0),
            "moves_down": moves_by_direction.get("down", 0),
            "moves_left": moves_by_direction.get("left", 0),
            "moves_right": moves_by_direction.get("right", 0)
        }

        stats["games"].append(game_data)

        all_games = stats["games"]
        if not all_games:
            return

        scores = [game["score"] for game in all_games]
        max_tiles = [game["max_tile"] for game in all_games]
        wins = sum(1 for game in all_games if game["won"])

        moves_up = sum(game.get("moves_up", 0) for game in all_games)
        moves_down = sum(game.get("moves_down", 0) for game in all_games)
        moves_left = sum(game.get("moves_left", 0) for game in all_games)
        moves_right = sum(game.get("moves_right", 0) for game in all_games)
        total_moves = sum(game["moves"] for game in all_games)

        stats["summary"] = {
            "games_played": len(all_games),
            "best_score": max(scores),
            "worst_score": min(scores),
            "avg_score": sum(scores) / len(scores),
            "wins": wins,
            "losses": len(all_games) - wins,
            "win_rate": (wins / len(all_games)) * 100,
            "avg_max_tile": sum(max_tiles) / len(max_tiles),
            "avg_moves_per_game": total_moves / len(all_games),
            "moves_up": moves_up,
            "moves_down": moves_down,
            "moves_left": moves_left,
            "moves_right": moves_right,
            "avg_moves_up": moves_up / len(all_games),
            "avg_moves_down": moves_down / len(all_games),
            "avg_moves_left": moves_left / len(all_games),
            "avg_moves_right": moves_right / len(all_games)
        }

        stats["games"].sort(key=lambda x: x["score"], reverse=True)

        save_stats(stats)
    except Exception as e:
        print(f"Error saving game statistics: {e}")

def print_stats():
    stats = load_stats()
    if not stats or "games" not in stats or not stats["games"]:
        print("Zatím žádné uložené statistiky.")
        return

    summary = stats.get("summary", {})
    sorted_games = sorted(stats["games"], key=lambda x: x["score"], reverse=True)

    print("\n=== STATISTIKY HRY 2048 ===")
    print(f"Počet odehraných her: {summary.get('games_played', 0)}")
    print(f"Nejlepší skóre: {summary.get('best_score', 0)}")
    print(f"Nejhorší skóre: {summary.get('worst_score', 0)}")
    print(f"Průměrné skóre: {summary.get('avg_score', 0):.2f}")
    print(f"Výhry: {summary.get('wins', 0)} ({summary.get('win_rate', 0):.1f}%)")
    print(f"Prohry: {summary.get('losses', 0)}")
    print(f"Průměrná max hodnota: {summary.get('avg_max_tile', 0):.1f}")
    print(f"Průměrný počet tahů na hru: {summary.get('avg_moves_per_game', 0):.1f}")

    print("\n--- Směry tahů ---")
    print(f"Nahoru: {summary.get('moves_up', 0)} (průměr: {summary.get('avg_moves_up', 0):.1f})")
    print(f"Dolů: {summary.get('moves_down', 0)} (průměr: {summary.get('avg_moves_down', 0):.1f})")
    print(f"Vlevo: {summary.get('moves_left', 0)} (průměr: {summary.get('avg_moves_left', 0):.1f})")
    print(f"Vpravo: {summary.get('moves_right', 0)} (průměr: {summary.get('avg_moves_right', 0):.1f})")

    reached_2048_count = sum(1 for game in stats["games"] if game["max_tile"] >= 2048)
    print(f"\nDosaženo 2048 nebo více: {reached_2048_count}x ({(reached_2048_count/len(stats['games'])*100):.1f}% her)")

    print("\n--- ŽEBŘÍČEK TOP 5 HER PODLE SKÓRE ---")
    for i, game in enumerate(sorted_games[:5]):
        print(f"{i+1}. Skóre: {game['score']} | Max hodnota: {game['max_tile']} | Tahy: {game['moves']} | Výhra: {'Ano' if game.get('won', False) else 'Ne'}")

    all_max_tiles = sorted([game["max_tile"] for game in stats["games"]], reverse=True)
    top_3_tiles = all_max_tiles[:3] if len(all_max_tiles) >= 3 else all_max_tiles
    print("\n--- TOP 3 NEJVĚTŠÍ DOSAŽENÉ HODNOTY ---")
    for i, tile in enumerate(top_3_tiles):
        print(f"{i+1}. {tile}")

    print("\n--- DETAIL VŠECH HER ---")
    for i, game in enumerate(stats["games"]):
        print(f"Hra #{i+1}:")
        print(f"  Skóre: {game['score']}")
        print(f"  Max hodnota: {game['max_tile']}")
        print(f"  Celkem tahů: {game['moves']}")
        print(f"  Tahy: nahoru={game.get('moves_up', 0)}, dolů={game.get('moves_down', 0)}, vlevo={game.get('moves_left', 0)}, vpravo={game.get('moves_right', 0)}")
        print(f"  Distribuce směrů: nahoru={game.get('moves_up', 0)/game['moves']*100:.1f}%, dolů={game.get('moves_down', 0)/game['moves']*100:.1f}%, do stran={(game.get('moves_left', 0)+game.get('moves_right', 0))/game['moves']*100:.1f}%")
        print(f"  Datum: {game.get('date', 'neznámé')}")
        print(f"  Dosažena výhra (2048+): {'Ano' if game.get('won', False) or game['max_tile'] >= 2048 else 'Ne'}")
        print()

    print("=== KONEC STATISTIK ===\n")

def init_board():
    board = [[0]*SIZE for _ in range(SIZE)]
    spawn_new_tile(board)
    spawn_new_tile(board)
    return board

def spawn_new_tile(board):
    empties = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if not empties:
        return
    r, c = random.choice(empties)
    board[r][c] = 4 if random.random()<0.1 else 2

def can_move(board):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return True
    for r in range(SIZE):
        for c in range(SIZE):
            if c<SIZE-1 and board[r][c]==board[r][c+1]:
                return True
            if r<SIZE-1 and board[r][c]==board[r+1][c]:
                return True
    return False

def copy_board(board):
    return [row[:] for row in board]

def compress(row):
    filtered = [x for x in row if x!=0]
    filtered += [0]*(SIZE-len(filtered))
    return filtered

def merge(row, score):
    for i in range(SIZE-1):
        if row[i]!=0 and row[i]==row[i+1]:
            row[i]*=2
            score+=row[i]
            row[i+1]=0
    return row, score

def move_left(board, score):
    new_board=[]
    changed=False
    for r in range(SIZE):
        row=board[r]
        row=compress(row)
        row,score=merge(row,score)
        row=compress(row)
        new_board.append(row)
        if row!=board[r]:
            changed=True
    return new_board,changed,score

def reverse_row(row):
    return row[::-1]

def transpose(board):
    return [list(x) for x in zip(*board)]

def move_right(board, score):
    reversed_b=[reverse_row(r) for r in board]
    temp_b,ch,score=move_left(reversed_b,score)
    final_b=[reverse_row(r) for r in temp_b]
    return final_b,ch,score

def move_up(board, score):
    trans=transpose(board)
    temp_b,ch,score=move_left(trans,score)
    final_b=transpose(temp_b)
    return final_b,ch,score

def move_down(board, score):
    trans=transpose(board)
    temp_b,ch,score=move_right(trans,score)
    final_b=transpose(temp_b)
    return final_b,ch,score

def merges_count(board):
    cnt=0
    for r in range(SIZE):
        for c in range(SIZE):
            if c<SIZE-1 and board[r][c]!=0 and board[r][c]==board[r][c+1]:
                cnt+=1
            if r<SIZE-1 and board[r][c]!=0 and board[r][c]==board[r+1][c]:
                cnt+=1
    return cnt

def top_row_monotonicity(board):
    row=board[0]
    mon=0
    for i in range(SIZE-1):
        if row[i]>=row[i+1]:
            mon+=1
    return mon

def row_fill_bonus(board):
    top_row=board[0]
    return sum(1 for x in top_row if x!=0)

def get_max_tile(board):
    return max(max(row) for row in board)

def evaluate_board(board):
    val = 0.0
    max_tile = get_max_tile(board)
    weights = [
        [16, 15, 14, 13],
        [9,  10, 11, 12],
        [8,  7,  6,  5],
        [1,  2,  3,  4]
    ]
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] > 0:
                val += board[r][c] * weights[r][c]
    if board[0][0] == max_tile:
        val += max_tile * 5
    for c in range(SIZE):
        if board[0][c] > 0:
            val += board[0][c] * 2
    h_mon = 0
    for r in range(SIZE):
        for c in range(SIZE-1):
            if board[r][c] >= board[r][c+1]:
                if r == 0:
                    h_mon += 20
                else:
                    h_mon += 5
    val += h_mon
    v_mon = 0
    for c in range(SIZE):
        for r in range(SIZE-1):
            if board[r][c] >= board[r+1][c]:
                if c == 0:
                    v_mon += 20
                else:
                    v_mon += 5
    val += v_mon
    merges = merges_count(board)
    val += merges * 25
    top_merges = merges_row0_row1(board)
    val += top_merges * 200
    empty_count = sum(row.count(0) for row in board)
    val += empty_count * 15
    blocked_tiles = 0
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] != 0:
                is_blocked = True
                for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < SIZE and 0 <= nc < SIZE:
                        if board[nr][nc] == 0 or board[nr][nc] == board[r][c]:
                            is_blocked = False
                            break
                if is_blocked:
                    blocked_tiles += 1
    val -= blocked_tiles * 10
    snake_bonus = 0
    snake_path = [
        (0,0), (0,1), (0,2), (0,3),
        (1,3), (1,2), (1,1), (1,0),
        (2,0), (2,1), (2,2), (2,3),
        (3,3), (3,2), (3,1), (3,0)
    ]
    for i in range(len(snake_path)-1):
        r1, c1 = snake_path[i]
        r2, c2 = snake_path[i+1]
        if board[r1][c1] >= board[r2][c2] and board[r1][c1] != 0:
            snake_bonus += 10
    val += snake_bonus
    return val

def merges_row0_row1(board):
    ccount=0
    for c in range(SIZE):
        if board[0][c]!=0 and board[0][c]==board[1][c]:
            ccount+=1
    return ccount

def get_preferred_moves(board, score):
    from copy import deepcopy
    possible_moves = []
    b_up, ch_up, sc_up = move_up(deepcopy(board), score)
    if ch_up:
        possible_moves.append(("UP", b_up, sc_up))
    b_left, ch_left, sc_left = move_left(deepcopy(board), score)
    if ch_left:
        possible_moves.append(("LEFT", b_left, sc_left))
    b_right, ch_right, sc_right = move_right(deepcopy(board), score)
    if ch_right:
        possible_moves.append(("RIGHT", b_right, sc_right))
    if not possible_moves:
        b_down, ch_down, sc_down = move_down(deepcopy(board), score)
        if ch_down:
            possible_moves.append(("DOWN", b_down, sc_down))
    return possible_moves

def get_all_new_tiles(board):
    empties=[(r,c) for r in range(SIZE) for c in range(SIZE) if board[r][c]==0]
    if not empties:
        return []
    if len(empties)>5:
        empties=random.sample(empties,5)
    variants=[]
    p_each=1.0/len(empties)
    for (r,c) in empties:
        b2=copy_board(board)
        b2[r][c]=2
        variants.append((b2,p_each))
    return variants

def choose_depth(board):
    empties=sum(row.count(0) for row in board)
    if empties<=3:
        return 4
    elif empties<=6:
        return 3
    else:
        return 2

def expectimax(board, score, depth):
    if depth==0 or not can_move(board):
        return evaluate_board(board), board
    moves=get_preferred_moves(board, score)
    if not moves:
        return evaluate_board(board), board
    best_eval=-1e9
    best_state=board
    for (mname, new_b, new_s) in moves:
        tile_vars=get_all_new_tiles(new_b)
        if not tile_vars:
            val=evaluate_board(new_b)
            if val>best_eval:
                best_eval=val
                best_state=new_b
        else:
            exp_val=0.0
            for (b_a, prob) in tile_vars:
                v,st=expectimax(b_a, new_s, depth-1)
                exp_val+=v*prob
            if exp_val>best_eval:
                best_eval=exp_val
                best_state=new_b
    return best_eval, best_state

def ai_move(board, score):
    depth=choose_depth(board)
    val,best_b=expectimax(board, score, depth)
    if best_b==board:
        return board,False,score
    from copy import deepcopy
    possible = [move_up, move_left, move_right]
    for func in possible:
        test_b,ch,new_score=func(deepcopy(board), score)
        if ch and test_b==best_b:
            return test_b,True,new_score
    for func in possible:
        test_b,ch,new_score=func(deepcopy(board), score)
        if ch and test_b==best_b:
            return test_b,True,new_score
    return best_b,True,score