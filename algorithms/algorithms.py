from typing import List
from . import register_algorithm
import random
import statistics

@register_algorithm("random")
def choose_move(available_moves: List[int], current_held: List[int], opponent_held: List[int], k: int) -> int:
    if not available_moves:
        return -1
    return random.choice(available_moves)

@register_algorithm("heuristic")
def choose_move(available_moves: List[int], current_held: List[int], opponent_held: List[int], k: int) -> int:
    if not available_moves:
        return -1
    median_val: float = statistics.median(available_moves)
    best_score: float = -float('inf')
    best_move: int = available_moves[0]
    for num in available_moves:
        score: float = -abs(num - median_val)
        if current_held:
            score -= min(abs(num - x) for x in current_held)
        if score > best_score:
            best_score = score
            best_move = num
    return best_move

@register_algorithm("min")
def choose_move(available_moves: List[int], current_held: List[int], opponent_held: List[int], k: int) -> int:
    if not available_moves:
        return -1
    best_move = min(available_moves)
    return best_move