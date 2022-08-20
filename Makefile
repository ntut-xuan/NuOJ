all: install mariadb-install sandbox-install db-tcp

install:
	sudo apt-get update
	sudo apt-get install -y python3 python3-pip git build-essential asciidoc-base libcap-dev sysfsutils
	# clone NuOJ repository on github
	sudo mkdir /etc/nuoj
	sudo git clone --recursive https://github.com/ntut-xuan/NuOJ.git /etc/nuoj
	sudo mkdir /etc/nuoj/storage/
	sudo mkdir /etc/nuoj/storage/problem/
	sudo mkdir /etc/nuoj/storage/user_avater/
	sudo mkdir /etc/nuoj/storage/user_profile/
	sudo mkdir /etc/nuoj/storage/user_submission/
	sudo chmod -R 647 /etc/nuoj/*
	# clone setting file
	sudo cp /etc/nuoj/setting/setting.json /etc/nuoj/
	# clone service file
	sudo cp /etc/nuoj/service/nuoj.service /etc/systemd/system/
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
	sudo pip3 install pyjwt
	sudo pip3 install pycryptodome
	# load service 
	sudo systemctl daemon-reload
	sudo systemctl enable nuoj
	sudo systemctl start nuoj

mariadb-install:
	sudo apt-get install mariadb-server

cert:
	sudo snap install core; sudo snap refresh core
	sudo snap install --classic certbot
	-sudo ln -s /snap/bin/certbot /usr/bin/certbot
	sudo certbot certonly --manual --preferred-challenge dns

sandbox-install:
	wget https://raw.githubusercontent.com/ntut-xuan/NuOJ-Sandbox/main/Makefile -O NuoJSandboxMake
	make -f NuoJSandboxMake
	rm -rf NuoJSandboxMake

update:
	sudo git -C /etc/nuoj pull
	sudo git -C /etc/nuoj-sandbox pull
	sudo git -C /etc/nuoj-database pull

clean:
	-sudo pip3 uninstall -y flask_session
	-sudo pip3 uninstall -y flask_login
	-sudo pip3 uninstall -y loguru
	-sudo pip3 uninstall -y flask_cors
	-sudo pip3 uninstall -y pymysql
	-sudo pip3 uninstall -y flask
	-sudo rm -rf /etc/nuoj
	-sudo rm -rf ~/isolate
	-sudo systemctl stop nuoj
	-sudo rm -rf /etc/systemd/system/nuoj.service

db-socket:
	sudo mysql -u root -h '127.0.0.1' < database.sql
	# create a new admin account
	sudo mysql -u root -h '127.0.0.1' --database="NuOJ" --execute="INSERT INTO \`user\` (user_uid, handle, password, email, role, email_verified) VALUES ('7d4be98f-1792-4255-b3f9-42a32a201fbb', 'nuoj', 'f0affe539c194d46d66d96c4c7aab38d', 'NuOJ@ntut.edu.tw', 1, 1);"

db-tcp:
	# create table
	sudo mysql -u root < database.sql
	# create a new admin account
	sudo mysql -u root --database="NuOJ" --execute="INSERT INTO \`user\` (user_uid, handle, password, email, role, email_verified) VALUES ('7d4be98f-1792-4255-b3f9-42a32a201fbb', 'nuoj', 'f0affe539c194d46d66d96c4c7aab38d', 'NuOJ@ntut.edu.tw', 1, 1);"

db-drop:
	sudo mysql -u root --execute="DROP DATABASE NuOJ;

test-all:
	sudo systemctl start nuoj
	sudo systemctl start nuoj-sandbox
	sudo python3 /etc/nuoj/test.py
	sudo python3 /etc/nuoj/python/webapp_test.py
	sudo python3 /etc/nuoj-sandbox/test.py