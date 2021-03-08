@echo off

echo.
echo Setting DAC: CAL- to 0.8V
python comm.py s 0x4D 0x51EB

echo.
echo Setting DAC: CAL+ to 0.8V
python comm.py s 0x4C 0x51EB

echo.
echo Starting calibration pulse
python comm.py s 0x4E 0x03