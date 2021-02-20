#ifndef TERRAININFO_H
#define TERRAININFO_H

#include <QtMath>
#include <QJsonArray>
#include "player.h"
#include "ball.h"

class TerrainInfo {
public:

    struct Coord{
        int X, Y;
    };

    TerrainInfo();
    float getDistance(int x1, int y1, int x2, int y2);
    float sigmoid(int x);
    float modify(int x, int alpha);
    float getOccupation(int x, int y, int frame);
    bool validCoords(Coord a);
    Coord listCoords[14];
    QJsonArray frameArray;
    void positionPlayers(int frame);
    Player listAlly[7];
    Player listOpponent[7];
    Ball ball;
    double getDistanceClosestPlayer(int indexPlayer, bool isAlly, int frame);
    void Init();

};



#endif // TERRAININFO_H
