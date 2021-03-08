@echo off

echo.
echo Setting DAC: addr_dac_tlevel1 to max
python comm.py s 0x38 0xFFFF

echo.
echo Setting DAC: addr_dac_tlevel2 to max
python comm.py s 0x39 0xFFFF

echo.
echo Setting DAC: addr_dac_tlevel3 to max
python comm.py s 0x3A 0xFFFF

echo.
echo Setting DAC: addr_dac_tlevel4 to max
python comm.py s 0x3B 0xFFFF

echo.
echo Setting DAC: addr_dac_tlevel5 to max
python comm.py s 0x3C 0xFFFF

echo.
echo Setting DAC: addr_dac_tlevel6 to max
python comm.py s 0x3D 0xFFFF

echo.
echo Setting DAC: addr_dac_tlevel7 to max
python comm.py s 0x3E 0xFFFF
echo.

echo Setting DAC: addr_dac_tlevel8 to max
python comm.py s 0x3F 0xFFFF


echo.
echo Setting pattern_0 to 0
python comm.py s 0xE0 0x0000

echo.
echo Setting pattern_1 to 0
python comm.py s 0xE1 0x0000

echo.
echo Setting pattern_2 to 0
python comm.py s 0xE2 0x0000

echo.
echo Setting pattern_3 to 0
python comm.py s 0xE3 0x0000

echo.
echo Setting pattern_4 to 0
python comm.py s 0xE4 0x0000

echo.
echo Setting pattern_5 to 0
python comm.py s 0xE5 0x0000

echo.
echo Setting pattern_6 to 0
python comm.py s 0xE6 0x0000

echo.
echo Setting pattern_7 to 0
python comm.py s 0xE7 0x0000
