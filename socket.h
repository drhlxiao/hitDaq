#ifndef LGRTCPSOCKET_H
#define LGRTCPSOCKET_H

#include <QObject>
#include <QTcpSocket>
#include <QAbstractSocket>
#include <QDebug>

class LgrTcpSocket : public QObject
{
    Q_OBJECT
public:
    explicit LgrTcpSocket(QObject *parent = 0);

    void doConnect();

signals:

public slots:
    void connected();
    void disconnected();
    void bytesWritten(qint64 bytes);
    void readyRead();

private:
    QTcpSocket *socket;

};

#endif // MYTCPSOCKET_H
