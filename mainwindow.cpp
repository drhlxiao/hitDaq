#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
        ui->setupUi(this);
}

MainWindow::~MainWindow()
{
        delete ui;
        sock=NULL;
        ui->statusBar->showMessage("No hardware is connected!");
}

void MainWindow::on_connect_clicked()
{

        //   QString host=ui->
        QString host=ui->host->text();
        quint16 port=ui->port->value();

        if(!host.isEmpty() && port>0)
        {

                sock=new DaqSocket();
                bool isConnect=sock->connect(host,port);
                if(isConnect)
                {
                        ui->statusBar->showMessage("Connected!");
                }
                else{

                        ui->statusBar->showMessage("Failed to connect to host!");
                }
        }
        else{

                ui->statusBar->showMessage("Invalid host or port!");

        }
        //  sock->connect();
}


void MainWindow::on_readCurrent_clicked()
{
        if(sock)
        {
                if(sock->isConnected())
                {
                        QByteArray buf=sock->readI2CRegister(0x67, 0x14);
                        int len=buf.length();
                        if(len>0)
                        {
                                char *data=buf.data();
                                ui->testOutput->setPlainText(buf.data());
                                if (len>=4)
                                {
                                    unsigned short high= (unsigned short) data[2];
                                    unsigned short low= (unsigned short) data[3];
                                   unsigned short buffer = (high<<8)+ low;
                                    buffer = buffer>>4;
                                    qDebug()<<"buffer:"<<buffer;
                                    float current=buffer*250e-3;
                                    ui->testOutput->appendPlainText(QString("current: %1").arg(current));

                                }


                        }
                        ui->statusBar->showMessage("No data received!");

                }
                ui->statusBar->showMessage("Not connected!");

        }
}

void MainWindow::on_readVoltage_clicked()
{
    if(sock)
    {
            if(sock->isConnected())
            {
                    QByteArray buf=sock->readI2CRegister(0x67, 0x1E);
                    int len=buf.length();
                    if(len>0)
                    {
                            char *data=buf.data();
                            ui->testOutput->setPlainText(buf.data());
                            if (len>=4)
                            {
                                    unsigned short high= (unsigned short) data[2];
                                    unsigned short low= (unsigned short) data[3];
                                   unsigned short buffer = (high<<8)+ low;
                                    buffer = buffer>>4;
                                    qDebug()<<"buffer:"<<buffer;
                                    float current=buffer*250e-3;
                                    ui->testOutput->appendPlainText(QString("current: %1").arg(current));

                            }


                    }
                    ui->statusBar->showMessage("No data received!");

            }
            ui->statusBar->showMessage("Not connected!");

    }
}
