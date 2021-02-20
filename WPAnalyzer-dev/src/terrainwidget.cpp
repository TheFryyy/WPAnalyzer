#include "terrainwidget.h"
#include <QLabel>
#include <QGraphicsPixmapItem>
#include "TerrainInfo.h"

TerrainWidget::TerrainWidget(TerrainInfo &_terrainInfo)
{
    terrainInfo = &_terrainInfo;

    graphic1 = new QGraphicsScene(this);
    graphic2 = new QGraphicsScene(this);

    view1 = new QGraphicsView(graphic1);
    view2 = new QGraphicsView(graphic2);

    terrainImage = QImage(500, 400, QImage::Format_ARGB32);
    terrainImage.fill(QColor(0, 0, 255, 125));

    //graphic1->addPixmap(QPixmap(":/images/player.png"));
    graphic1->addPixmap(QPixmap(":/images/terrain.png").scaled(500, 400));
    graphic2->addPixmap(QPixmap(":/images/terrain.png").scaled(500, 400));
    pixmap = graphic1->addPixmap(QPixmap::fromImage(terrainImage));

    Vlayout = new QVBoxLayout(this);

    graphic2->addItem(&(terrainInfo->ball));
    // add players to the scene
    for(int i = 0; i < 7; i++) {
        graphic1->addItem(&(terrainInfo->listAlly[i]));
        graphic1->addItem(&(terrainInfo->listOpponent[i]));
        graphic2->addItem(&(terrainInfo->listAlly[i]));
        graphic2->addItem(&(terrainInfo->listOpponent[i]));
    }


    Vlayout->addWidget(view1);
    Vlayout->addWidget(view2);
    terrainInfo->listAlly[0].setPixmap(QPixmap(":/images/AllySelected.png").scaled(10, 10, Qt::KeepAspectRatio));
    updateOccupation(0);
};

void TerrainWidget::updateOccupation(int frame) {
    terrainInfo->positionPlayers(frame);
    terrainImage = QImage(500, 400, QImage::Format_ARGB32);
    for(int i = 0; i < 500; i++) {
        for(int j = 0; j < 400; j++) {
            float occupation = terrainInfo->getOccupation(i, j, frame);
            if(occupation < 0)
                terrainImage.setPixel(i, j,qRgba(0, 0, 255, qBound(0.f, -occupation, 100.f)));
            else
                terrainImage.setPixel(i, j,qRgba(255, 0, 0, qBound(0.f, occupation, 100.f)));
        }
    }
    pixmap->setPixmap(QPixmap::fromImage(terrainImage, Qt::AutoColor));
}

