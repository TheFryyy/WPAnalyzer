#ifndef CHARTS_H
#define CHARTS_H

#include <QWidget>
#include <QtCharts>
#include "player.h"
#include "TerrainInfo.h"

class Charts : public QChartView
{
    Q_OBJECT
public:
    Charts(TerrainInfo &_terrainInfo);
    void drawCurve(int playerIndex, bool ally);
    TerrainInfo *terrainInfo;
    int currentFrame = 0;
    int currentPlayer = 0;
    bool currentPlayerAlly = true;
    QValueAxis *axisX;
    QValueAxis *axisY;

public slots:
    void changeFrame(int frame);

private:
    QChart* chart;
    QLineSeries* series;

};

#endif // CHARTS_H
