#ifndef PLAYERGRAPHIC_H
#define PLAYERGRAPHIC_H
#include <QGraphicsPixmapItem>

class PlayerGraphic : public QGraphicsPixmapItem
{
public:
    PlayerGraphic();
    void mousePressEvent(QGraphicsSceneMouseEvent *event);

};

#endif // PLAYERGRAPHIC_H
