#ifndef TERRAINWIDGET_H
#define TERRAINWIDGET_H
#include <QWidget>
#include <QGraphicsScene>
#include <QGraphicsView>
#include <QJsonArray>
#include <QJsonObject>
#include <QSlider>
#include "player.h"
#include "TerrainInfo.h"
#include <QVBoxLayout>

class TerrainWidget : public QWidget
{
    struct Coord{
        int X, Y;
    };

Q_OBJECT
public:
    TerrainWidget(TerrainInfo &_terrainInfo);
    TerrainInfo *terrainInfo;
    QImage terrainImage;
    QVBoxLayout *Vlayout;
    QGraphicsScene *graphic1;
    QGraphicsScene *graphic2;
    QGraphicsPixmapItem *pixmap;
    QGraphicsView *view1;
    QGraphicsView *view2;
    float getOccupation(int x, int y);

public slots:
    void updateOccupation(int frame);

};

#endif // TERRAINWIDGET_H
