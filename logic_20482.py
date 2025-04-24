import random
from copy import deepcopy
import logic_2048 as logic

def random_playout(board, score, max_moves=1000):
    b = deepcopy(board)
    sc = score
    moves = 0
    while logic.can_move(b) and moves < max_moves:
        moves += 1
        # collect all valid next moves
        options = []
        for func in (logic.move_up, logic.move_down, logic.move_left, logic.move_right):
            nb, changed, ns = func(deepcopy(b), sc)
            if changed:
                options.append((nb, ns))
        if not options:
            break
        # pick one at random
        b, sc = random.choice(options)
        logic.spawn_new_tile(b)
    return sc


def ai2_move(board, score, simulations=30, playout_depth=200):

    best_avg = -float('inf')
    best_result = (board, False, score)

    for func in (logic.move_up, logic.move_down, logic.move_left, logic.move_right):
        new_b, changed, new_s = func(deepcopy(board), score)
        if not changed:
            continue
        total = 0
        for _ in range(simulations):
            total += random_playout(new_b, new_s, max_moves=playout_depth)
        avg = total / simulations
        if avg > best_avg:
            best_avg = avg
            best_result = (new_b, True, new_s)

    return best_result
