QT       += \
    core gui \
    charts

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

RC_ICONS = icon/WPLogo.ico

SOURCES += \
    src/Constant.cpp \
    src/TerrainInfo.cpp \
    src/ball.cpp \
    src/charts.cpp \
    src/draganddropwindow.cpp \
    src/main.cpp \
    src/mainwindow.cpp \
    src/player.cpp \
    src/playerhandler.cpp \
    src/terrainwidget.cpp

HEADERS += \
    src/Constant.h \
    src/TerrainInfo.h \
    src/ball.h \
    src/charts.h \
    src/draganddropwindow.h \
    src/mainwindow.h \
    src/player.h \
    src/playerhandler.h \
    src/terrainwidget.h \
    src/terrainwidget.h

FORMS += \
    src/mainwindow.ui

TRANSLATIONS += \
    src/WPAnalyzer_fr_FR.ts

RESOURCES += \
    src/resources.qrc

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
