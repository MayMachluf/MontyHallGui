import mhProblemGp
import re


def run_mh(count):
    mhProblemGp.run_mh(count, 100000, False)

    with open("mhResultsGp.txt", 'r', encoding='utf-8') as f:
        text = f.read()
        result = re.findall('\d+', text.replace(',', ''))

        return result
