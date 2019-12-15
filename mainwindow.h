#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "daqsocket.h"
namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_connect_clicked();

    void on_readCurrent_clicked();

    void on_readVoltage_clicked();

private:
    Ui::MainWindow *ui;
    DaqSocket *sock;

};

#endif // MAINWINDOW_H
