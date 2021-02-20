#include "TerrainInfo.h"
#include <math.h>
#include <QJsonObject>
#include <QJsonDocument>
#include "Constant.h"


TerrainInfo::TerrainInfo()
{
}

void TerrainInfo::Init()
{
    QString settings;
    QFile file;
    file.setFileName(Constants::data);
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    settings = file.readAll();
    file.close();

    QJsonDocument d = QJsonDocument::fromJson(settings.toUtf8());

    frameArray = d.object().value("frameArray").toArray();
    for(int i = 0; i < 7; i++) {
        listAlly[i].setTeam(true);
        listAlly[i].id = i;
        listOpponent[i].setTeam(false);
        listOpponent[i].id = i;
    }
    listAlly[0].setPixmap(QPixmap(":/images/AllySelected.png").scaled(10, 10, Qt::KeepAspectRatio));
    positionPlayers(0);
}

bool TerrainInfo::validCoords(Coord a)
{
    if(a.X >= 0 && a.Y >= 0 && a.X <= Constants::terrainLength && a.Y <= Constants::terrainHeight)
        return true;
    return false;
}

float TerrainInfo::getDistance(int x1, int y1, int x2, int y2) {
    float result = qSqrt(qPow((x1 - x2), 2) + qPow((y1 - y2), 2));
    return result;
}

float TerrainInfo::sigmoid(int x) {
    float b = -0.005f;
    float result = 1/(1+exp(-x));
    return result;
}

float TerrainInfo::modify(int x, int alpha)
{
    return qBound(0.0f, (float)(alpha / x), 1.0f) * sigmoid(x) + (1 - qBound(0.0f, (float)(alpha / x), 1.0f)) * x;
}

float TerrainInfo::getOccupation(int x, int y, int frame) {
    float closestAlly = 100000;
    float closestOpp = 100000;
    for(int i = 0; i < 7; i++)
    {
        //if(validCoords(listCoords[i]))
        {
            float distance = TerrainInfo::getDistance(listCoords[i].X, listCoords[i].Y, x, y); // distance de l'allié i au pixel (x, y)
            if(distance < closestAlly)
                closestAlly = distance;
        }

    }

    for(int i = 7; i < 14; i++)
    {
        //if(validCoords(listCoords[i]))
        {
            float distance = TerrainInfo::getDistance(listCoords[i].X, listCoords[i].Y, x, y); // distance de l'opposant i au pixel (x, y)
            if(distance < closestOpp)
                closestOpp = distance;
        }
    }
    float result = 0.0f;

    if(closestOpp == 100000 || closestAlly == 100000)
        return result;

    result = (closestAlly - closestOpp);
    return result;
}

void TerrainInfo::positionPlayers(int frame) {

    if(frame < frameArray.size()) {
        Coord Ball = {
            (int) frameArray[frame].toObject().value("ball").toArray()[0].toObject().value("coords").toArray()[0].toDouble() * 20,
            (int) frameArray[frame].toObject().value("ball").toArray()[0].toObject().value("coords").toArray()[1].toDouble() * 20
        };
        for(int i = 0; i < 7; i++) {
            Coord Ally = {
                (int) frameArray[frame].toObject().value("allyArray").toArray()[i].toObject().value("coords").toArray()[0].toDouble() * 20,
                (int) frameArray[frame].toObject().value("allyArray").toArray()[i].toObject().value("coords").toArray()[1].toDouble() * 20
            };
            Coord Opp = {
                (int) frameArray[frame].toObject().value("opponentArray").toArray()[i].toObject().value("coords").toArray()[0].toDouble() * 20,
                (int) frameArray[frame].toObject().value("opponentArray").toArray()[i].toObject().value("coords").toArray()[1].toDouble() * 20
            };

            listCoords[i] = Ally;
            listCoords[7 + i] = Opp;
            if(validCoords(Ball))
                ball.setPos(Ball.X, Ball.Y);
            if(validCoords(Ally))
            {
//                listAlly[i].setVisible(true);
                listAlly[i].updatePosition(Ally.X, Ally.Y);
            }
            else
            {
//                listAlly[i].setVisible(false);
            }

            if(validCoords(Opp))
            {
//                listOpponent[i].setVisible(true);
                listOpponent[i].updatePosition(Opp.X, Opp.Y);
            }
            else
            {
//                listOpponent[i].setVisible(false);
            }
            //listAlly[i].updatePosition(Ally.Y, Constants::terrainHeight - Ally.X);
            //listAlly[i].updatePosition(0, 400);
            //listOpponent[i].updatePosition(Opp.Y, Constants::terrainHeight - Opp.X);
            //listOpponent[i].updatePosition(500, 0);
        }
    }
}

double TerrainInfo::getDistanceClosestPlayer(int indexPlayer, bool isAlly, int frame)
{
    double minDistance = 100000;

    if(isAlly)
    {
        double XAlly = frameArray[frame].toObject().value("allyArray").toArray()[indexPlayer].toObject().value("coords").toArray()[0].toDouble();
        double YAlly = frameArray[frame].toObject().value("allyArray").toArray()[indexPlayer].toObject().value("coords").toArray()[1].toDouble();
        for(int i = 0; i < 7; i++)
        {
            double XOpp = frameArray[frame].toObject().value("opponentArray").toArray()[i].toObject().value("coords").toArray()[0].toDouble();
            double YOpp = frameArray[frame].toObject().value("opponentArray").toArray()[i].toObject().value("coords").toArray()[1].toDouble();

            float distance = TerrainInfo::getDistance(XAlly, YAlly, XOpp, YOpp); // distance de l'allié i au pixel (x, y)
            if(distance < minDistance)
                minDistance = distance;

        }
    }
    else
    {
        double XOpp = frameArray[frame].toObject().value("opponentArray").toArray()[indexPlayer].toObject().value("coords").toArray()[0].toDouble();
        double YOpp = frameArray[frame].toObject().value("opponentArray").toArray()[indexPlayer].toObject().value("coords").toArray()[1].toDouble();
        for(int i = 0; i < 7; i++)
        {
            double XAlly = frameArray[frame].toObject().value("allyArray").toArray()[i].toObject().value("coords").toArray()[0].toDouble();
            double YAlly = frameArray[frame].toObject().value("allyArray").toArray()[i].toObject().value("coords").toArray()[1].toDouble();

            float distance = TerrainInfo::getDistance(XAlly, YAlly, XOpp, YOpp); // distance de l'allié i au pixel (x, y)
            if(distance < minDistance)
                minDistance = distance;

        }
    }
    return minDistance;
}
