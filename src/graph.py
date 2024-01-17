import mhProblemGp
import re
# new comment

def mh_helper(games, count):
    """
    A connector function to the algorithm code provided for this program.

    Parameters:
        games: amount of games to simulate
        count: amount of doors to simulate

    Returns:
        result of the algorithm program from file
    """
    mhProblemGp.run_mh(count, games, False)

    with open("mhResultsGp.txt", 'r', encoding='utf-8') as f:
        text = f.read()
        result = re.findall('\d+', text.replace(',', ''))

        return result
