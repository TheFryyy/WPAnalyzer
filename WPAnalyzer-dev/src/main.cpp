#include "mainwindow.h"

#include <QApplication>
#include "terrainwidget.h"
#include <QProcess>
#include <QDebug>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    /*QProcess p;
    QStringList params;

    params << "C:\\Users\\Julien\\Documents\\Qt\\WPAnalyzer\\test.py";
    p.start("C:/Users/Julien/AppData/Local/Programs/Python/Python36-32/python.exe", params);
    p.waitForFinished(-1);
    QString p_stdout = p.readAll();
    qDebug() << p_stdout;*/


    /*QJsonArray playerArray = frameArray[0].toObject().value("playerArray").toArray();
    QJsonArray coords = playerArray[0].toObject().value("coords").toArray();

    qDebug() << coords[0].toInt() << ", " << coords[1].toInt();*/

    MainWindow w;
    w.show();

    return a.exec();
}
