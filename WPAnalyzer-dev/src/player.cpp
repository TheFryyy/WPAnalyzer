#include "player.h"
#include<QDebug>
#include "playerhandler.h"

Player::Player()
{
    this->setPixmap(QPixmap(":/images/Ally.png").scaled(10, 10, Qt::KeepAspectRatio));

    this->setPos(245, 155);

}

void Player::mousePressEvent(QGraphicsSceneMouseEvent *event) {
    if(isAlly)
        this->setPixmap(QPixmap(":/images/AllySelected.png").scaled(10, 10, Qt::KeepAspectRatio));
    else
        this->setPixmap(QPixmap(":/images/OppSelected.png").scaled(10, 10, Qt::KeepAspectRatio));

    handler.s_PlayerClicked(id, isAlly);
}

void Player::updatePosition(int x, int y) {
    this->setPos(x, y);
}

void Player::setTeam(bool ally) {
    isAlly = ally;
    if(isAlly)
        this->setPixmap(QPixmap(":/images/Ally.png").scaled(10, 10, Qt::KeepAspectRatio));
    else
        this->setPixmap(QPixmap(":/images/Opp.png").scaled(10, 10, Qt::KeepAspectRatio));
}
