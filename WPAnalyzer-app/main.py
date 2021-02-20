from lib import detector
from lib import detection_joueuse as dj
from lib import homography as h
import json
import numpy as np
import sys

args = sys.argv[1:]
path = args[0]

# Détection de lignes

lines = detector.Detector(path)
lines.read_video()
lines.sort_list()
lines.clean_list()
lines.get_points()
# lines.trace()

# Détection de joueuse

players = dj.Detection_joueuse((0, 0, 0), (180, 100, 100), (20, 50, 50), (30, 255, 255), path)
#players.show_video()

# Spatialisation

for point in lines.points:
    point = point.invert_base()

pts_dist = h.real_point(False)
pts_src = h.src_point(lines.points)
homography, status = h.find_homography(pts_src, pts_dist)

with open("./output/data.json") as f:
    data = json.load(f)

donnees = {
    "frameArray": []
}

for frame in data["frameArray"]:
    playerArray = {
        "allyArray": [],
        "ball": [],
        "opponentArray": []
    }

    allyCoords = []
    ballCoord = []
    opponentCoords = []

    for ally in frame["allyArray"]:
        allyCoords.append(ally["coords"])
    for ball in frame["ball"]:
        ballCoord.append(ball["coords"])
    for opponent in frame["opponentArray"]:
        opponentCoords.append(opponent["coords"])

    new_allyCoords = h.warp(np.float32([allyCoords]), homography)
    new_ballCoord = h.warp(np.float32([ballCoord]), homography)
    new_opponentCoords = h.warp(np.float32([opponentCoords]), homography)

    for new_ally in new_allyCoords[0]:
        coords = {
            "coords": new_ally.tolist()
        }
        playerArray["allyArray"].append(coords)
    for new_ball in new_ballCoord[0]:
        coords = {
            "coords": new_ball.tolist()
        }
        playerArray["ball"].append(coords)
    for new_opponent in new_opponentCoords[0]:
        coords = {
            "coords": new_opponent.tolist()
        }
        playerArray["opponentArray"].append(coords)
    donnees["frameArray"].append(playerArray)

with open("./output/donnees.json", "w", encoding="utf-8") as outfile:
    json.dump(donnees, outfile, ensure_ascii=False, sort_keys=True, indent=3)

