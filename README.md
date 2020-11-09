# HIT data acquisition software
    

####  Python3 and pip3 installation
on Linux (Ubuntu)

```console
sudo  apt-get install python3
sudo apt install python3-pip
```
On windows

  - Download  python3.8.5 (other versions >= 3.6 should also work) executable installer
 
     64-bit Windows: https://www.python.org/ftp/python/3.8.5/python-3.8.5-amd64.exe 
   
     32-bit Windows: https://www.python.org/ftp/python/3.8.5/python-3.8.5.exe 
 
  - Install python3
 
    When installing python, choose `customize installation`, 
   `install pip` and `add python path to the system environment`. 

#### Install dependencies
Open the terminal, run:
```cmd
   pip3 install numpy PyQt5 pyqtchart 
````

#### Run the DAQ

- On Linux OS
```sh
	cd HIT_daq
	chmod 755 daq
	./daq
```
- On Windows
``` cmd
	cd HIT_daq
	python3 daq
```
  
