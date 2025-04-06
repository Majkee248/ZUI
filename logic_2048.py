import random
import json
import os
from datetime import datetime

SIZE = 4
STATS_FILE = "stats.json"
WIN_TILE = 2048  # Tile value that counts as a "win"

def load_stats():
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r") as f:
                data = json.load(f)
                # Verify the loaded data has the correct structure
                if isinstance(data, dict) and "games" in data:
                    return data
                print("Warning: Stats file has incorrect format. Creating new file.")
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading stats file: {e}. Creating new file.")
    
    # Return a fresh stats dictionary with the proper structure
    return {"games": [], "summary": {}}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

def add_stat(score, moves, max_tile, moves_by_direction, won=False):
    try:
        stats = load_stats()
        
        # Ensure stats is properly structured
        if not isinstance(stats, dict):
            stats = {"games": [], "summary": {}}
        if "games" not in stats:
            stats["games"] = []
        
        # Add individual game data
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
        
        # Update summary statistics
        all_games = stats["games"]
        if not all_games:
            return
        
        # Calculate summary
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
        
        # Sort by score for the top games list
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
    top_games = stats["games"][:5]  # Top 5 games by score
    
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
    
    print("\n--- TOP 5 HER ---")
    for i, game in enumerate(top_games):
        print(f"{i+1}. Skóre: {game['score']} | Max hodnota: {game['max_tile']} | Tahy: {game['moves']} | Výhra: {'Ano' if game.get('won', False) else 'Ne'}")
    print("=== KONEC STATISTIK ===\n")

# Keep all the other functions the same...
# -------------------------------------------------------------------------
# Inicializace a kontrola boardu
# -------------------------------------------------------------------------
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

# -------------------------------------------------------------------------
# Pohyby a slučování se skóre
# -------------------------------------------------------------------------
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
    # Dolů v AI nepoužíváme.
    trans=transpose(board)
    temp_b,ch,score=move_right(trans,score)
    final_b=transpose(temp_b)
    return final_b,ch,score

# -------------------------------------------------------------------------
# Heuristika
# -------------------------------------------------------------------------
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
    val=0.0
    max_tile=get_max_tile(board)
    if board[0][0]==max_tile:
        val+=max_tile*3

    merges=merges_count(board)
    val+=merges*15

    fill=row_fill_bonus(board)
    val+=fill*5

    mon=top_row_monotonicity(board)
    val+=mon*20

    return val

# -------------------------------------------------------------------------
# if row=1 and row=0 -> forced up?
# We'll keep that, but also consider left or right with the same priority
# -------------------------------------------------------------------------
def can_merge_row0_row1(board):
    """
    Pokud row=1 a row=0 lze sloučit v nějakém sloupci, up je extra zajímavé.
    """
    for c in range(SIZE):
        if board[0][c]!=0 and board[0][c]==board[1][c]:
            return True
    return False

def get_preferred_moves(board, score):
    """
    VRÁTÍ VŠECHNY MOŽNÉ TAHY z [UP, LEFT, RIGHT],
    abychom left a right NEpreferovali, ale nechali Expectimaxu.
    Navíc, pokud row=1 a row=0 je co sloučit, PŘIDÁME UP ZNOVU
    (což je menší hack) => up se objeví dvakrát => Expectimax mu
    dá vyšší šanci?
    Ovšem dvojnásobné up by jen dublovalo stejný stav => raději
    ho přidáme jen jednou s info "FORCED_UP"?
    Ale to by Expectimax nepoznal rozdíl.

    Jednodušší:
    1) up, left, right => vyzkoušet,
    2) pokud can_merge_row0_row1 => up má speciální "tag" =>
       ohodnotíme ho plus?

    Můžeme to udělat tak,
      - vyrobíme list moves,
      - up, left, right => pokud changed => moves.append
    3) Pokud can_merge_row0_row1 =>
         dáme up do moves znovu s drobným "forced" bonusem v heuristice?

    Ale to by znepřehlednilo logiku.
    Lepší bude v heuristice =>
        pokud row=1 a row=0 je sloučit => scoreboard + extra
        => up se stane nejlepší volbou.
    => realizujeme v evaluate_board ->
       jestli "row1" a "row0" je stejná nenul => + bonus.

    Tím Expectimax rozhodne pro up.

    Zkusíme snadný přístup:
    Vratime up, left, right.
    down = None
    Expectimax vybere.
    """
    from copy import deepcopy

    possible_moves = []
    # up
    b_up, ch_up, sc_up = move_up(deepcopy(board), score)
    if ch_up:
        possible_moves.append(("UP", b_up, sc_up))

    # left
    b_left, ch_left, sc_left = move_left(deepcopy(board), score)
    if ch_left:
        possible_moves.append(("LEFT", b_left, sc_left))

    # right
    b_right, ch_right, sc_right = move_right(deepcopy(board), score)
    if ch_right:
        possible_moves.append(("RIGHT", b_right, sc_right))

    return possible_moves

# Pro "row=1 a row=0" merges => dodelame mini-bonus v evaluate
def merges_row0_row1(board):
    """
    Vrátí, kolik sloupců v row=0 a row=1 je stejná nenulová hodnota.
    """
    ccount=0
    for c in range(SIZE):
        if board[0][c]!=0 and board[0][c]==board[1][c]:
            ccount+=1
    return ccount

# Uprava evaluate - specialni bonus
old_eval = evaluate_board
def evaluate_board_plus(board):
    base = old_eval(board)
    # Pokud row=0 a row=1 se můžou sloučit, +100 bodů za každý takový sloupec
    # Tím se "up" stane pro AI výrazně atraktivní
    c = merges_row0_row1(board)
    return base + c*100

# nahradime evaluate ve zbytku
evaluate_board = evaluate_board_plus

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
    # re-check moves up, left, right
    possible = [move_up, move_left, move_right]
    for func in possible:
        test_b,ch,new_score=func(deepcopy(board), score)
        if ch and test_b==best_b:
            return test_b,True,new_score
    
    # If we couldn't determine which move led to best_b, recalculate the score
    # (This shouldn't happen but is a fallback)
    # Try all possible moves to find which one creates this board state
    for func in possible:
        test_b,ch,new_score=func(deepcopy(board), score)
        if ch and test_b==best_b:
            return test_b,True,new_score
    
    return best_b,True,score  # Fallback if we can't determine the correct score