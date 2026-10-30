from .game import Game

maps = [
        "maps/1_easy/01_linear_path.txt",
        "maps/1_easy/02_simple_fork.txt",
        "maps/1_easy/03_basic_capacity.txt",
        "maps/2_medium/01_dead_end_trap.txt",
        "maps/2_medium/02_circular_loop.txt",
        "maps/2_medium/03_priority_puzzle.txt",
        "maps/3_hard/01_maze_nightmare.txt",
        "maps/3_hard/02_capacity_hell.txt",
        "maps/3_hard/03_ultimate_challenge.txt",
        "maps/4_challenger/01_the_impossible_dream.txt"
        ]

for m in maps:
    # print(m.split('/')[2], '\n')
    ...

game = Game()
game.start_game()
# game.load_map(maps[7])
