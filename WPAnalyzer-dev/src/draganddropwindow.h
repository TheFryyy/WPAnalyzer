#ifndef DRAGANDDROPWINDOW_H
#define DRAGANDDROPWINDOW_H
#include <QWidget>
#include <QTextEdit>
#include <QProcess>
#include <QLabel>
#include <QVBoxLayout>
#include "TerrainInfo.h"



class DragAndDropWindow :public QWidget
{
    Q_OBJECT
public:
    DragAndDropWindow(TerrainInfo &_terrainInfo);
    QProcess p;
protected:
    void dragEnterEvent(QDragEnterEvent *e);
    void dropEvent(QDropEvent *e);

private:
    TerrainInfo* terrainInfo;
    QVBoxLayout *layout;
    QLabel *imageLabel;

signals:
    void endProcess();
};

#endif // DRAGANDDROPWINDOW_H
