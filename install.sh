#####################################################################
# install Bime Cloud-Management Python scripts
#####################################################################
# install amqplib
cd ~
wget http://py-amqplib.googlecode.com/files/amqplib-0.6.1.tgz
tar zxvf amqplib-0.6.1.tgz
cd amqplib-0.6.1
sudo python setup.py install
# instal json lib
wget http://pypi.python.org/packages/source/s/simplejson/simplejson-2.1.1.tar.gz#md5=0bbe3a2e5e4cac040013733aca159d89
tar zxvf simplejson-2.1.1.tar.gz
cd  simplejson-2.1.1
sudo python setup.py install
# install bime cm lib
sudo mkdir /usr/local/bime-home/python

scp jy2947@distribution.bimelab.com:~/distribution/bime-controller/python/focaplo-1.0.tar.gz ~/
sudo cp ~/focaplo-1.0.tar.gz /usr/local/bime-home/python/
cd /usr/local/bime-home/python
sudo tar zxvf focaplo-1.0.tar.gz
cd focaplo-1.0
sudo python setup.py install
sudo chown -R bime: /usr/local/bime-home/python
