all: install db-tcp

install:
	sudo apt-get install -y python3 python3-pip git build-essential asciidoc-base libcap-dev sysfsutils
	# clone Isolate repository on github 
	sudo mkdir ~/isolate
	sudo git clone https://github.com/ioi/isolate.git ~/isolate
	# Isolate make install 
	sudo make -C ~/isolate install
	# clone NuOJ repository on github
	sudo mkdir /opt/nuoj
	sudo mkdir /opt/nuoj-sandbox
	sudo mkdir /opt/nuoj-sandbox/result
	sudo mkdir /opt/nuoj-sandbox/submission
	sudo mkdir /opt/nuoj-database
	sudo git clone --recursive https://github.com/ntut-xuan/NuOJ.git /opt/nuoj
	sudo git clone --recursive https://github.com/ntut-xuan/NuOJ-Sandbox.git /opt/nuoj-sandbox
	sudo git clone --recursive https://github.com/ntut-xuan/NuOJ-Database.git /opt/nuoj-database
	sudo chmod -R 647 /opt/nuoj/*
	sudo chmod -R 647 /opt/nuoj-sandbox/*
	sudo chmod -R 647 /opt/nuoj-database/*
	# clone setting file
	sudo cp /opt/nuoj/setting/setting.json /opt/nuoj/
	# clone service file
	sudo cp /opt/nuoj/service/nuoj.service /etc/systemd/system/
	sudo cp /opt/nuoj-sandbox/nuoj-sandbox.service /etc/systemd/system/
	sudo cp /opt/nuoj-database/nuoj-database.service /etc/systemd/system/
	sudo chmod 647 /etc/systemd/system/nuoj.service
	sudo chmod 647 /etc/systemd/system/nuoj-sandbox.service
	sudo chmod 647 /etc/systemd/system/nuoj-database.service
	# install pip package
	sudo pip3 install flask
	sudo pip3 install pymysql
	sudo pip3 install flask_cors
	sudo pip3 install loguru
	sudo pip3 install flask_login
	sudo pip3 install flask_session
	sudo pip3 install asana
	sudo pip3 install python-dateutil
	sudo pip3 install pytz
	sudo pip3 install redis
	# load service 
	sudo systemctl daemon-reload
	sudo systemctl enable nuoj
	sudo systemctl enable nuoj-sandbox
	sudo systemctl enable nuoj-database
	sudo systemctl start nuoj
	sudo systemctl start nuoj-sandbox
	sudo systemctl start nuoj-database

cert:
	sudo snap install core; sudo snap refresh core
	sudo snap install --classic certbot
	-sudo ln -s /snap/bin/certbot /usr/bin/certbot
	sudo certbot certonly --manual --preferred-challenge dns

clean: clean-file db-tcp-clean

clean-file:
	-sudo pip3 uninstall -y flask_session
	-sudo pip3 uninstall -y flask_login
	-sudo pip3 uninstall -y loguru
	-sudo pip3 uninstall -y flask_cors
	-sudo pip3 uninstall -y pymysql
	-sudo pip3 uninstall -y flask
	-sudo rm -rf /opt/nuoj
	-sudo rm -rf /opt/nuoj-sandbox
	-sudo rm -rf /opt/nuoj-database
	-sudo make -C ~/isolate clean
	-sudo rm -rf ~/isolate
	-sudo systemctl stop nuoj
	-sudo systemctl stop nuoj-sandbox
	-sudo systemctl stop nuoj-database
	-sudo rm -rf /etc/systemd/system/nuoj.service
	-sudo rm -rf /etc/systemd/system/nuoj-sandbox.service
	-sudo rm -rf /etc/systemd/system/nuoj-database.service
