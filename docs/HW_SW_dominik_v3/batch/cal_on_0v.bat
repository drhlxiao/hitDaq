@echo off

echo.
echo Setting DAC: CAL- to 0V
python comm.py s 0x4D 0x0

echo.
echo Setting DAC: CAL+ to 0V
python comm.py s 0x4C 0x0

echo.
echo Starting calibration pulse
python comm.py s 0x4E 0x03