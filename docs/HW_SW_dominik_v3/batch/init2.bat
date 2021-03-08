@echo off

echo.
echo Reading constant register
python comm.py g 0x00

echo.
echo Heaters off
python comm.py s 0x20 0x0F

echo.
echo Setting DAC: BIAS to 0.8V
python comm.py s 0x40 0x4E10

echo.
echo Setting DAC: ROFS to 1.595V
python comm.py s 0x4B 0x9FFF

echo.
echo Setting DRS config register to 0xFF
python comm.py s 0x4F 0xC0F
python comm.py g 0x4F

echo.
echo Setting DRS write shift register to 0xFF
python comm.py s 0x4F 0xD0F
python comm.py g 0x4F

echo.
echo Reading the status
python comm.py ?