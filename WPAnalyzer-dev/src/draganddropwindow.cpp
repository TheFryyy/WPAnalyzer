#include "draganddropwindow.h"
#include <QDragEnterEvent>
#include <QMimeData>
#include <QDebug>
#include <QImage>
#include "Constant.h"

DragAndDropWindow::DragAndDropWindow(TerrainInfo &_terrainInfo)
{
    terrainInfo = &_terrainInfo;
    this->setAcceptDrops(true);
    layout = new QVBoxLayout(this);
    QPixmap image(":/images/cameraIcon.png");
    imageLabel = new QLabel();
    imageLabel->setPixmap(image);
    imageLabel->setAlignment(Qt::AlignCenter);
    layout->addWidget(imageLabel);

}

void DragAndDropWindow::dragEnterEvent(QDragEnterEvent *event)
{
        event->acceptProposedAction();

}

void DragAndDropWindow::dropEvent(QDropEvent *event)
{
    QPixmap image(":/images/loading.png");
    imageLabel->setPixmap(image);
    QString filename;
    QList<QUrl> urls;
    QList<QUrl>::Iterator i;
    urls = event->mimeData()->urls();
    filename = urls[0].url();

    QStringList params;

    params << "./main.py";
    params << filename;
    p.start(Constants::python, params);
    p.waitForFinished(-1);
    QString p_stdout = p.readAll();
    qDebug() << p_stdout;
    endProcess();

    /*for(i = urls.begin(); i != urls.end(); i++) {

    }*/
}
