@echo off

echo.
echo Reading constant register
python comm.py g 0x00

echo.
echo Heaters off
python comm.py s 0x20 0x0F

echo.
echo Setting DAC: BIAS to 0.7V
python comm.py s 0x40 0x364D

echo.
echo Setting DAC: ROFS to 1.57V
python comm.py s 0x4B 0x79CA

echo.
echo Setting DRS config register to 0xFF
python comm.py s 0x4F 0xC0F
python comm.py g 0x4F

echo.
echo Setting DRS write shift register to 0xFF
python comm.py s 0x4F 0xD0F
python comm.py g 0x4F

@REM echo.
@REM echo Setting readout config (test + ROI)
@REM python comm.py s 0x80 0x0005
@REM python comm.py g 0x80

echo.
echo Setting readout config (ROI)
python comm.py s 0x80 0x0001
python comm.py g 0x80

echo.
echo Setting readout channels (2 channels)
python comm.py s 0x81 0x0003
python comm.py g 0x81

echo.
echo Setting readout length to 0x64 (100)
python comm.py s 0x83 0x0064
python comm.py g 0x83

echo.
echo Setting FIFO burst length to 0xCB (203)
python comm.py s 0x72 0x00CB
python comm.py g 0x72

echo.
echo Reading the status
python comm.py ?