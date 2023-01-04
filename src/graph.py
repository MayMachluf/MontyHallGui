import mhProblemGp
import re


def mh_helper(games, count):
    mhProblemGp.run_mh(count, games, False)

    with open("mhResultsGp.txt", 'r', encoding='utf-8') as f:
        text = f.read()
        result = re.findall('\d+', text.replace(',', ''))

        return result
