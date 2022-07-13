all: install sandbox-install database-install

install:
	sudo apt-get install -y python3 python3-pip git build-essential asciidoc-base libcap-dev sysfsutils
	# clone NuOJ repository on github
	sudo mkdir /opt/nuoj
	sudo git clone --recursive https://github.com/ntut-xuan/NuOJ.git /opt/nuoj
	sudo chmod -R 647 /opt/nuoj/*
	# clone setting file
	sudo cp /opt/nuoj/setting/setting.json /opt/nuoj/
	# clone service file
	sudo cp /opt/nuoj/service/nuoj.service /etc/systemd/system/
	sudo chmod 647 /etc/systemd/system/nuoj.service
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
	# load service 
	sudo systemctl daemon-reload
	sudo systemctl enable nuoj
	sudo systemctl start nuoj

cert:
	sudo snap install core; sudo snap refresh core
	sudo snap install --classic certbot
	-sudo ln -s /snap/bin/certbot /usr/bin/certbot
	sudo certbot certonly --manual --preferred-challenge dns

sandbox-install:
	wget https://raw.githubusercontent.com/ntut-xuan/NuOJ-Sandbox/main/Makefile -O NuoJSandboxMake
	make -f NuoJSandboxMake
	rm -rf NuoJSandboxMake

database-install:
	wget https://raw.githubusercontent.com/ntut-xuan/NuOJ-Database/main/Makefile -O NuoJDatabaseMake
	make -f NuoJDatabaseMake
	rm -rf NuoJDatabaseMake

update:
	sudo git -C /opt/nuoj pull
	sudo git -C /opt/nuoj-sandbox pull
	sudo git -C /opt/nuoj-database pull

clean:
	-sudo pip3 uninstall -y flask_session
	-sudo pip3 uninstall -y flask_login
	-sudo pip3 uninstall -y loguru
	-sudo pip3 uninstall -y flask_cors
	-sudo pip3 uninstall -y pymysql
	-sudo pip3 uninstall -y flask
	-sudo rm -rf /opt/nuoj
	-sudo rm -rf ~/isolate
	-sudo systemctl stop nuoj
	-sudo rm -rf /etc/systemd/system/nuoj.service

test-all:
	sudo systemctl start nuoj
	sudo systemctl start nuoj-sandbox
	sudo systemctl start nuoj-database
	sudo python3 /opt/nuoj/test.py
	sudo python3 /opt/nuoj-sandbox/test.py
	sudo python3 /opt/nuoj-database/test.py