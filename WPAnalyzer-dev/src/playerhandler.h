#ifndef PLAYERHANDLER_H
#define PLAYERHANDLER_H
#include <QObject>

class PlayerHandler : public QObject
{
    Q_OBJECT
public:
    PlayerHandler();

signals:
    void s_PlayerClicked(int id, bool ally);
};

#endif // PLAYERHANDLER_H
