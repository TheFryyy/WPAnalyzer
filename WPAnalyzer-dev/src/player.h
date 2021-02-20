#ifndef PLAYER_H
#define PLAYER_H

#include <QGraphicsPixmapItem>
#include <QMouseEvent>
#include "playerhandler.h"



class Player : public QGraphicsPixmapItem
{
    public:
        bool isAlly = true;
        PlayerHandler handler;
        Player();
        int id = -1;
        QImage notSelected;
        QImage selected;
        void mousePressEvent(QGraphicsSceneMouseEvent *event);
        void updatePosition(int x, int y);
        void setTeam(bool ally);
        bool bSelected = false;

};

#endif // PLAYER_H
