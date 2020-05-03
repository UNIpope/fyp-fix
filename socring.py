def calculateScore(data, word):
    contents = data["content"]
    score = 0

    for index in contents["word"]:
        val = calculateDistance(word["x"], word["y"], contents["x"][index], contents["y"][index])

        #print(word["x"], word["y"], contents["x"][index], contents["y"][index])
        score += val
    
    print(score / len(data["content"]))
    return score / len(data["content"])


def calculateavg(data):
    contents = data["content"]

    """
    iword = list(contents["word"].keys())[list(contents["word"].values()).index(word)][0]
    del contents["word"][iword]
    del contents["x"][iword]
    del contents["y"][iword]
    """

    points = list(zip(contents["x"].values(),contents["y"].values()))
    distances = [calculateDistance(p1[0],p1[1],p2[0], p2[1]) for p1, p2 in itertools.combinations(points, 2)]
    avg_distance = sum(distances) / len(distances)
    print(avg_distance)