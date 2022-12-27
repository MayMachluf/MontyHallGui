# author: itzhik aviv

import random


def mpProblem(k, outfile, print):
    l = []
    for i in range(k):
        l.append("goat")
    ci = random.randint(0, k - 1)
    l[ci] = "car"
    if print:
        outfile.write("\n   partitions:  ")
        for i in range(k):
            outfile.write("  " + l[i])
    if print:
        outfile.write("\nthe car is behind partition number: "
                      + str(ci))
    fc = random.randint(0, k - 1)
    if print:
        outfile.write("\nfirst choice: " + str(l[fc])
                      + "   index of first choice: " + str(fc))
    s = ""
    for i in range(k):
        if i != ci:
            s = s + " " + str(i)
    while True:
        ex = random.randint(0, k - 1)
        if ex != fc and ex != ci:
            break
    if print:
        outfile.write("\nindices of goats partition: " + s)
    if print:
        outfile.write("\nindex of exposed goat partition: "
                      + str(ex))
    while True:
        sc = random.randint(0, k - 1)
        if sc != fc and sc != ex:
            break
    if print:
        outfile.write("\nsecond choice: " + l[sc]
                      + "  index of second choice: " + str(sc))
        if sc == ci:
            outfile.write("\n   second choice succeeded.")
        elif fc == ci:
            outfile.write("\n   second choice failed.")
        else:
            outfile.write("\n   second choice without influence.")
    return ci, fc, sc


def run_mh(k, n, print):
    outfile = open("mhResultsGp.txt", 'w')
    outfile.write("\nnumber of partitions: "
                  + "{0:,d}".format(k))
    winsBecauseOfChange = 0
    lossesBecauseOfChange = 0
    losessBeforeAndAfterChange = 0

    for i in range(n):
        if print:
            outfile.write(("\ngame number: " + str(i + 1)))
        ci, fc, sc = mpProblem(k, outfile, print)
        if ci == sc:
            winsBecauseOfChange += 1
        else:
            if fc == ci:
                lossesBecauseOfChange += 1
            else:
                losessBeforeAndAfterChange += 1

    outfile.write("\nnumber of games: "
                  + "{0:,d}".format(i + 1)
                  + "\nnumber of wins   because of choice change: "
                  + "{0:,d}".format(winsBecauseOfChange)
                  + "\nnumber of losses because of choice change: "
                  + "{0:,d}".format(lossesBecauseOfChange)
                  + "\nnumber of choice change without influence: "
                  + "{0:,d}".format(losessBeforeAndAfterChange))

    outfile.close()

# main(100, 100000, False)
