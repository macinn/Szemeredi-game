import itertools
from collections import defaultdict
import time
from typing import Dict, List, Any, Tuple, Set
import random

from algorithms import registry
from game import Game

def play_game(game: Game, algo1: str, algo2: str) -> tuple[int, float, float]:
    """
    Simulates a game between two algorithms.
    
    Args:
        game: Game instance
        algo1: Name of the first algorithm (player 1)
        algo2: Name of the second algorithm (player 2)
        
    Returns:
        1 if player 1 wins, 2 if player 2 wins, 0 for draw
        and the time taken for each algorithm
    """
    algo1_func = registry.get(algo1.lower(), registry.get("random"))
    algo2_func = registry.get(algo2.lower(), registry.get("random"))
    
    algo1_time = 0.0
    algo2_time = 0.0
    
    while not game.game_over:
        if game.player1_turn:
            if game.available_numbers:
                start_time = time.time()
                move = algo1_func(list(game.available_numbers), game.player1_moves, game.player2_moves, game.k)
                assert move in game.available_numbers
                game.make_move(move)
                end_time = time.time()
                algo1_time += end_time - start_time
        else:
            if game.available_numbers:
                start_time = time.time()
                move = algo2_func(list(game.available_numbers), game.player2_moves, game.player1_moves, game.k)
                assert move in game.available_numbers
                game.make_move(move)
                end_time = time.time()
                algo2_time += end_time - start_time

    return game.winner if game.winner else 0, algo1_time, algo2_time

def run_tournament(settings: Dict[str, Any], num_games: int = 10) -> Dict:
    """
    Runs a tournament between all registered algorithms.
    
    Args:
        settings: Base game settings to use
        num_games: Number of games to play for each matchup
        
    Returns:
        Dictionary with tournament results
    """
    algorithms = list(registry.keys())

    print(f"Starting tournament with {len(algorithms)} algorithms: {', '.join(algorithms)}")
    print(f"Each matchup will play {num_games} games")
    print(f"Game settings: k={settings['k']}, x={settings['x']}, range={settings['lower']}-{settings['bound']}")
    
    # Initialize results
    results = {
        "wins": defaultdict(int),
        "draws": defaultdict(int),
        "losses": defaultdict(int),
        "points": defaultdict(float),  # 1 for win, 0.5 for draw
        "matchups": defaultdict(lambda: defaultdict(lambda: {"wins": 0, "draws": 0, "losses": 0})),
        "total_games": 0,
        "execution_time": defaultdict(float)
    }
    
    matchups = [(alg1, alg2) for alg1, alg2 in itertools.product(algorithms, algorithms) if alg1 < alg2]
    total_matchups = len(matchups)
    
    # Play games
    for idx, (algo1, algo2) in enumerate(matchups):
        print(f"\nMatchup {idx+1}/{total_matchups}: {algo1} vs {algo2}")
        
        for game_idx in range(num_games):
            # Create a new game instance
            k = settings["k"]
            x = settings["x"]
            lower = settings["lower"]
            bound = settings["bound"]
            game = Game(k, x, lower, bound)
            
            # Play the game and time it
            winner, algo1_time, algo2_time = play_game(game, algo1, algo2)
            game_time = algo1_time + algo2_time
            # Record results
            if winner == 1:  # algo1 wins
                results["wins"][algo1] += 1
                results["losses"][algo2] += 1
                results["points"][algo1] += 1
                results["matchups"][algo1][algo2]["wins"] += 1
                results["matchups"][algo2][algo1]["losses"] += 1
                print(f"  Game {game_idx+1}/{num_games}: {algo1} wins in {game.turn_count} turns ({game_time:.2f}s)")
            elif winner == 2:  # algo2 wins
                results["wins"][algo2] += 1
                results["losses"][algo1] += 1
                results["points"][algo2] += 1
                results["matchups"][algo2][algo1]["wins"] += 1
                results["matchups"][algo1][algo2]["losses"] += 1
                print(f"  Game {game_idx+1}/{num_games}: {algo2} wins in {game.turn_count} turns ({game_time:.2f}s)")
            else:  # draw
                results["draws"][algo1] += 1
                results["draws"][algo2] += 1
                results["points"][algo1] += 0.5
                results["points"][algo2] += 0.5
                results["matchups"][algo1][algo2]["draws"] += 1
                results["matchups"][algo2][algo1]["draws"] += 1
                print(f"  Game {game_idx+1}/{num_games}: Draw after {game.turn_count} turns ({game_time:.2f}s)")
            
            # Record time
            results["execution_time"][algo1] += algo1_time 
            results["execution_time"][algo2] += algo2_time
            
            results["total_games"] += 1
    
    # Print results
    print("\n====== TOURNAMENT RESULTS ======")
    print("\nAlgorithm Performance:")
    for algo in sorted(algorithms, key=lambda a: results["points"][a], reverse=True):
        win_pct = (results["wins"][algo] / results["total_games"]) * 100 if results["total_games"] > 0 else 0
        avg_time = results["execution_time"][algo] / (results["wins"][algo] + results["losses"][algo] + results["draws"][algo]) if (results["wins"][algo] + results["losses"][algo] + results["draws"][algo]) > 0 else 0
        print(f"{algo}: {results['points'][algo]} points - {results['wins'][algo]}W/{results['draws'][algo]}D/{results['losses'][algo]}L ({win_pct:.1f}%) - Avg time: {avg_time:.3f}s")
    
    print("\nHead-to-Head Results:")
    print("Format: [row] vs [column]: W-D-L")
    header = "Algorithm".ljust(15)
    for algo in algorithms:
        header += f"{algo[:8].ljust(10)}"
    print(header)
    
    for algo1 in algorithms:
        row = f"{algo1[:14].ljust(15)}"
        for algo2 in algorithms:
            if algo1 == algo2:
                row += f"---".ljust(10)
            else:
                wins = results["matchups"][algo1][algo2]["wins"]
                draws = results["matchups"][algo1][algo2]["draws"]
                losses = results["matchups"][algo1][algo2]["losses"]
                row += f"{wins}-{draws}-{losses}".ljust(10)
        print(row)
    
    return results

if __name__ == "__main__":
    # Default settings
    settings = {
        "k": 4,
        "x": 30,
        "lower": 1,
        "bound": 100,
    }
    
    run_tournament(settings, num_games=10)