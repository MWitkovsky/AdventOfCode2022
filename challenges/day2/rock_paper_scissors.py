# Path hack
import os
import sys
sys.path.insert(0, os.path.abspath("../../"))  # noqa

from lib import parsing


class RPS:
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    WIN = 10
    DRAW = 11
    LOSE = 12

    SCORING = {
        ROCK: 1,
        PAPER: 2,
        SCISSORS: 3,
        WIN: 6,
        DRAW: 3,
        LOSE: 0
    }

    PLAYER_STRATEGY = {
        "X": LOSE,
        "Y": DRAW,
        "Z": WIN
    }

    STR_2_RPS = {
        "A": ROCK,
        "B": PAPER,
        "C": SCISSORS,
        "X": ROCK,
        "Y": PAPER,
        "Z": SCISSORS,
    }

    MOVE_2_ELF_STR = {
        ROCK: "A",
        PAPER: "B",
        SCISSORS: "C"
    }

    MOVE_2_PLAYER_STR = {
        ROCK: "X",
        PAPER: "Y",
        SCISSORS: "Z"
    }


def _get_score_from_rps_bout(bout_str: str) -> int:
    bout = bout_str.split(" ")
    elf_move = RPS.STR_2_RPS[bout[0]]
    player_move = RPS.STR_2_RPS[bout[1]]
    move_score = RPS.SCORING[player_move]

    if elf_move == player_move:
        return move_score + RPS.SCORING[RPS.DRAW]

    if elf_move == RPS.ROCK and player_move == RPS.PAPER or \
            elf_move == RPS.PAPER and player_move == RPS.SCISSORS or \
            elf_move == RPS.SCISSORS and player_move == RPS.ROCK:
        return move_score + RPS.SCORING[RPS.WIN]

    return move_score + RPS.SCORING[RPS.LOSE]


def _translate_strategy_desc_to_bout(bout_str: str) -> str:
    elf_move = RPS.STR_2_RPS[bout_str[0]]
    player_strategy = RPS.PLAYER_STRATEGY[bout_str[2]]

    if player_strategy == RPS.DRAW:
        player_move = elf_move
    elif player_strategy == RPS.WIN:
        if elf_move == RPS.ROCK:
            player_move = RPS.PAPER
        elif elf_move == RPS.PAPER:
            player_move = RPS.SCISSORS
        else:
            player_move = RPS.ROCK
    elif player_strategy == RPS.LOSE:
        if elf_move == RPS.ROCK:
            player_move = RPS.SCISSORS
        elif elf_move == RPS.PAPER:
            player_move = RPS.ROCK
        else:
            player_move = RPS.PAPER

    elf_move_str = RPS.MOVE_2_ELF_STR[elf_move]
    player_move_str = RPS.MOVE_2_PLAYER_STR[player_move]
    return f"{elf_move_str} {player_move_str}"


def _rock_paper_scissors(bout_list: list[str]):
    """
    Part 1: 
        What would your total score be if everything goes exactly according 
        to your strategy guide?
    Part 2:
        "Anyway, the second column says how the round needs to end: X means 
        you need to lose, Y means you need to end the round in a draw, and 
        Z means you need to win. Good luck!"
    """
    literal_plan_score = sum(map(_get_score_from_rps_bout, bout_list))
    print(f"Part 1: {literal_plan_score}")
    real_player_moves = list(map(_translate_strategy_desc_to_bout, bout_list))
    real_plan_score = sum(map(_get_score_from_rps_bout, real_player_moves))
    print(f"Part 2: {real_plan_score}")


if __name__ == "__main__":
    parser = parsing.InputParser("inp.txt")
    inp = parser.to_array()
    parser.close()

    _rock_paper_scissors(inp)
