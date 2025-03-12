from . import register_algorithm
@register_algorithm("Random")
def choose_move(available_moves):
    import random
    if not available_moves:
        return None
    return random.choice(available_moves)
