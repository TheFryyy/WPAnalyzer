#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "terrainwidget.h"
#include "draganddropwindow.h"
#include "charts.h"
#include <QGridLayout>

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    MainWindow();

private:
    QSlider *slider;
    QWidget *chartFenetre;
    TerrainInfo terrainInfo;
    Charts* charts;
    TerrainWidget *terrain;
    DragAndDropWindow *dragAndDrop;
    QGridLayout *gridLayout;

public slots:
    void switchWindow(int exitCode, QProcess::ExitStatus exitStatus);
    void updateChart(int id, bool ally);
    void Init();
};
#endif // MAINWINDOW_H
