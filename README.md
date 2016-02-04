# Hack the Hive Receiver

Collects temperature measurements from the related
[Arduino program](https://github.com/greendragonsoft/arduino-hack-the-hive)
and forwards them on to [data.sparkfun.com](http://data.sparkfun.com)

See the [real live feed](https://data.sparkfun.com/streams/QG8QpXOX9mInr1D5DoAj/)

## Install

Dependencies:

- Python 2.7 with virtualenv

This needs to run on a server somewhere with a fixed IP. Do the following
to get going:

```
git clone https://github.com/greendragonsoft/hack-the-hive-receiver /opt/hack-the-hive-receiver

cd /opt/hack-the-hive-receiver
cp credentials.sh.example credentials
```

Then edit the credentials with the IP of your Arduino and your Sparkfun
credentials.

# Run with supervisord

```
apt-get install supervisor
cp /opt/hack-the-hive-receiver/supervisord.conf.example /etc/supervisor/conf.d/hack-the-hive-receiver.conf
service supervisor restart

supervisorctl start receiver
```
