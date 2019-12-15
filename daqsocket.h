#ifndef DAQSOCKET_H
#define DAQSOCKET_H

#include <QObject>
#include <QObject>
#include <QTcpSocket>
#include <string>

//#include <QAbstractSocket>
#include <QDebug>

class DaqSocket : public QObject
{
    Q_OBJECT
public:
    explicit DaqSocket(QObject *parent = nullptr);
    ~DaqSocket();
    bool connect(QString host, quint16 port);
    bool writeI2C(char address , char value);
    bool isConnected();
    QByteArray readI2C();
    QByteArray readI2CRegister(char address, char value);
signals:

public slots:
/*
    void connected();
    void disconnected();
    void bytesWritten(qint64 bytes);
    void readyRead();
    */

private:
private:
    QTcpSocket *socket;
};

#endif // DAQSOCKET_H
