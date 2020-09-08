def get_rank(league, rank):
    if league == 4:
        return f'Master {rank}'

    return f"""{(
        'Bronze',
        'Silver',
        'Gold',
        'Diamond',
    )[league]} {(
        'E',
        'D',
        'C',
        'B',
        'A',
    )[rank]}"""


def format_score(win, loser_score):
    return (f'{loser_score}-3', f'3-{loser_score}')[win]
