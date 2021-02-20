#include "charts.h"

Charts::Charts(TerrainInfo &_terrainInfo)
{
    terrainInfo = &_terrainInfo;

    series = new QLineSeries();
    chart = new QChart();
    chart->addSeries(series);
    chart->setTitle("Distance au plus proche adversaire en fonction du temps");

    axisX = new QValueAxis();
    axisX->setRange(-30, 0);
    axisX->setTitleText("30 dernières frames");
    chart->setAxisX(axisX);
    series->attachAxis(axisX);

    axisY = new QValueAxis();
    axisY->setRange(0, 35);
    axisY->setTitleText("Distance au plus proche adversaire (m)");
    chart->setAxisY(axisY);
    series->attachAxis(axisY);



    this->setChart(chart);
    this->setRenderHint(QPainter::Antialiasing);
    this->setUpdatesEnabled(true);
}

void Charts::drawCurve(int playerIndex, bool ally)
{
    currentPlayer = playerIndex;
    currentPlayerAlly = ally;
    series->clear();
    QString sTeam = "";
    int x, y, m = 0;
    if(ally)
    {
        m = 0;
    }
    else
    {
        m = 1;
    }
    series->append(0, 35);
    series->append(0, 0);
    for(int frame = qMax(0, currentFrame - 30); frame < currentFrame; frame++)
    {
        terrainInfo->positionPlayers(frame);
        x = (int) terrainInfo->listCoords[7 * m + playerIndex].X;
        y = (int) terrainInfo->listCoords[7 * m + playerIndex].Y;
        if(x >= 0 && y >=0)
        {
            float dist = terrainInfo->getDistanceClosestPlayer(currentPlayer, currentPlayerAlly, frame);
            series->append(frame - currentFrame + 30 , dist);
        }
    }
    series->attachAxis(axisX);
    series->attachAxis(axisY);
    chart->removeSeries(series);
    chart->addSeries(series);

}

void Charts::changeFrame(int frame)
{
    currentFrame = frame;
    drawCurve(currentPlayer, currentPlayerAlly);
}
