#include "daqsocket.h"



DaqSocket::DaqSocket(QObject *parent) : QObject(parent)
{

    socket=nullptr;

}
DaqSocket::~DaqSocket()
{
    if(socket){
        qDebug()<<"Closing socket";
        socket->close();
    }

}

bool DaqSocket::connect(QString host, quint16 port)
{

       socket = new QTcpSocket(this);
        socket->connectToHost(host,port);
        if(socket->waitForConnected(3000))
        {
            return true;
        }
        else
        {
               return false;
        }


}
bool DaqSocket::isConnected()
{

    if(socket)
    {

            if(socket->state() == QAbstractSocket::ConnectedState){
                return true;
            }
    }
    return false;

}

bool DaqSocket::writeI2C(char address, char value)
{
    if(socket->state() == QAbstractSocket::ConnectedState){
      const char dummy[12]= { 0x02, 0x00,0x08, 0x03, address, 0x01, value, 0x52, 0, 0x02, 0x03, 0x0A};

      qDebug()<<"bytes write:";
      qDebug() << QByteArray(dummy, sizeof(dummy)).toHex().constData();
      socket->write(dummy, 12);
      return socket->waitForBytesWritten();

    }
    return false;
}
QByteArray DaqSocket::readI2C(){

    QByteArray data;
    if(socket->state() == QAbstractSocket::ConnectedState)
    {
            socket->waitForReadyRead(30000);
            qDebug() << "Reading: " << socket->bytesAvailable();

            data=socket->readAll();
            qDebug() << "0x"<<data.toHex().constData();
        }
    return data;
}
 QByteArray DaqSocket::readI2CRegister(char address, char value)
 {
    QByteArray bytes;
     if(writeI2C(address, value))
     {
        bytes=readI2C();
     }
     return bytes;
 }
