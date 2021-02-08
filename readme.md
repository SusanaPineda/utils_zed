# Instalar GPS
```
pip3 install gpsd-py3

sudo apt install gpsd-clients gpsd 
sudo apt install libgps-dev
```

Si pasados unos minutos no obtiene la posición GPS:
```
sudo nano /etc/default/gpsd
``
Cambiar por:
```
START_DAEMON="true"
USBAUTO="true"
DEVICES="/dev/ttyACM0"
GPSD_OPTIONS="/dev/ttyACM0"
GPSD_SOCKET="/var/run/gpsd.sock"
```

Para activar el gps se utiliza:
```
sudo systemctl enable gpsd.socket
sudo systemctl start gpsd.socket
```

Si el gps se esta utilizando desde otra aplicación puede dar problemas, para evitarlo se utiliza:
```
sudo killall gpsd
```