cd ../
make
cd -
cython3 --embed -o main.c  ../core/main.py
g++ -o main.exe main.c -lpython3.8 -lpthread -lm -lutil -ldl -I /usr/include/python3.8/ core/archive.cpython-38-x86_64-linux-gnu.so core/config.cpython-38-x86_64-linux-gnu.so core/daq_comm.cpython-38-x86_64-linux-gnu.so core/main.cpython-38-x86_64-linux-gnu.so core/mainwindow.cpython-38-x86_64-linux-gnu.so core/mainwindow_rc5_rc.cpython-38-x86_64-linux-gnu.so core/style.cpython-38-x86_64-linux-gnu.so core/window.cpython-38-x86_64-linux-gnu.so
