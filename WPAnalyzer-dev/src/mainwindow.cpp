#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "draganddropwindow.h"
#include "terrainwidget.h"
#include <QMdiArea>
#include <QSlider>
#include <QProcess>
#include "Constant.h"
#include "player.h"
#include "playerhandler.h"

MainWindow::MainWindow() {

    // configure the top of the app (toolbar, title ...)

    setWindowIcon(QIcon(":/images/WPLogo.png"));
    this->setWindowState(Qt::WindowMaximized);
    QString  menuStyle(
                "QMainWindow {"
                "background-color: rgb(60, 60, 60);"
                "}"
                "QMenuBar {"
                "background-color: rgb(50, 50, 50);"
                "color: rgb(255, 255, 255);"
                "}"
                "QMenuBar::item:selected{"
                "background-color: rgb(0, 138, 255);"
                "color: rgb(255, 255, 255);"
                "}"
                "QMenu::item:selected{"
                "background-color: rgb(0, 138, 255);"
                "color: rgb(255, 255, 255);"
                "}"
                "QMenu {"
                "background-color: rgb(50, 50, 50);"
                "color: rgb(255, 255, 255);"
                "}"
            );
    this->setStyleSheet(menuStyle);
    QMenu *menuFichier = menuBar()->addMenu("&Fichier");
    QAction *actionImporter = new QAction("&importer", this);
    menuFichier->addAction(actionImporter);
    QAction *actionQuitter = new QAction("&quitter", this);
    menuFichier->addAction(actionQuitter);
    connect(actionQuitter, SIGNAL(triggered()), qApp, SLOT(quit()));
    actionQuitter->setShortcut(QKeySequence("ctrl+Q"));
    QMenu *menuEdition = menuBar()->addMenu("&Edition");
    QMenu *menuAffichage = menuBar()->addMenu("&Help");

    slider = new QSlider(Qt::Horizontal, this);
    slider->setRange(0, 200);
    gridLayout = new QGridLayout();
    chartFenetre = new QWidget();
    dragAndDrop = new DragAndDropWindow(terrainInfo);
    // Create the terrain
    terrain = new TerrainWidget(terrainInfo);
    // Create chart
    charts = new Charts(terrainInfo);

    gridLayout->addWidget(slider, 4, 0, 1, 3);
    gridLayout->addWidget(terrain, 0, 0);
    gridLayout->addWidget(charts, 0, 2);

    chartFenetre->setLayout(gridLayout);


    //charts->drawCurve(1, Player::Ally);   //charts->drawCurve(d.object().value("frameArray").toArray(), 1, Player::Ally);
    //subWindow1 = zoneCentrale->addSubWindow(terrain);
    //subWindow2 = zoneCentrale->addSubWindow(charts);


    // Configure the central zone
    setCentralWidget(dragAndDrop);
    QObject::connect(&dragAndDrop->p, SIGNAL(finished(int, QProcess::ExitStatus)), this, SLOT(switchWindow(int, QProcess::ExitStatus)));
    QObject::connect(dragAndDrop, SIGNAL(endProcess()), this, SLOT(Init()));
    QObject::connect(slider, SIGNAL(valueChanged(int)), terrain, SLOT(updateOccupation(int)));
    QObject::connect(slider, SIGNAL(valueChanged(int)), charts, SLOT(changeFrame(int)));
//    QObject::connect(playerChoice, SIGNAL(valueChanged(int)), this, SLOT(updateChart(int)));

    for(int i = 0; i < 7; i++)
    {
        QObject::connect(&(terrainInfo.listAlly[i].handler), SIGNAL(s_PlayerClicked(int, bool)), this, SLOT(updateChart(int, bool)));
        QObject::connect(&(terrainInfo.listOpponent[i].handler), SIGNAL(s_PlayerClicked(int, bool)), this, SLOT(updateChart(int, bool)));
    }



}

void MainWindow::Init()
{
    terrainInfo.Init();
    slider->setRange(0, terrainInfo.frameArray.size());
    updateChart(0, true);
    terrain->updateOccupation(0);

}

void MainWindow::switchWindow(int exitCode, QProcess::ExitStatus exitStatus)
{
    setCentralWidget(chartFenetre);
}

void MainWindow::updateChart(int id, bool ally)
{
    charts->drawCurve(id, ally);
    for(int i = 0; i < 7; i++)
    {
        if(i != id || !ally)
            terrainInfo.listAlly[i].setTeam(true);

        if(i != id || ally)
            terrainInfo.listOpponent[i].setTeam(false);
    }
}
