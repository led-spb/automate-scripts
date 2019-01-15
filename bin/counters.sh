#!/bin/sh

cd `dirname $0`
./json2mqtt --url @../etc/counters.conf --mqtt @../etc/mqtt.conf --retain \
\
-t home/sensor/water       '{{response.water | tojson}}'