#include "ball.h"

Ball::Ball()
{
    this->setPixmap(QPixmap(":/images/Ball.png").scaled(10, 10, Qt::KeepAspectRatio));
}
