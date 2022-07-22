all: install sandbox-install database-install

install:
	sudo apt-get install -y python3 python3-pip git build-essential asciidoc-base libcap-dev sysfsutils
	# clone NuOJ repository on github
	sudo mkdir /opt/nuoj
	sudo mkdir /opt/nuoj/storage/
	sudo mkdir /opt/nuoj/storage/problem/
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

db-socket:
	# create database
	sudo mysql -u root -h '127.0.0.1' --execute="CREATE DATABASE NuOJ"
	# create database account to two python script
	sudo mysql -u root -h '127.0.0.1' --execute="CREATE USER 'NuOJService'@'localhost' IDENTIFIED BY 'Nu0JS!@#$$';"
	sudo mysql -u root -h '127.0.0.1' --execute="CREATE USER 'NuOJJudger'@'localhost' IDENTIFIED BY 'Nu0JJ!@#$$';"
	# grant privileges on two account
	sudo mysql -u root -h '127.0.0.1' --execute="GRANT ALL PRIVILEGES ON *.* TO 'NuOJService'@'localhost';"
	sudo mysql -u root -h '127.0.0.1' --execute="GRANT ALL PRIVILEGES ON *.* TO 'NuOJJudger'@'localhost';"
	sudo mysql -u root -h '127.0.0.1' --execute="FLUSH PRIVILEGES;"
	# create table
	sudo mysql -u root -h '127.0.0.1' --database="NuOJ" --execute="CREATE TABLE \`user\` (\`user_id\` INT NOT NULL AUTO_INCREMENT, \`username\` VARCHAR(32) NOT NULL, \`password\` VARCHAR(32) NOT NULL, \`email\` VARCHAR(100	) NOT NULL, \`admin\` TINYINT(1) NOT NULL, PRIMARY KEY(user_id));"
	sudo mysql -u root -h '127.0.0.1' --database="NuOJ" --execute="CREATE TABLE \`submission\` ( \`submissionID\` INT NOT NULL AUTO_INCREMENT, \`submissionTime\` VARCHAR(40) NOT NULL, \`submissionBy\` VARCHAR(40) NOT NULL, \`Language\` VARCHAR(20) NOT NULL, \`ProblemID\` VARCHAR(20) NOT NULL,  \`VerdictResult\` VARCHAR(20), \`VerdictTime\` VARCHAR(40), \`VerdictMemory\` VARCHAR(40), PRIMARY KEY(submissionID));"
	sudo mysql -u root -h '127.0.0.1' --database="NuOJ" --execute="CREATE TABLE \`problem\` (\`ID\` int NOT NULL AUTO_INCREMENT, \`name\` VARCHAR(20) NOT NULL, \`visibility\` VARCHAR(20) NOT NULL, \`token\` VARCHAR(40) NOT NULL, \`author\` VARCHAR(20) NOT NULL, PRIMARY KEY(ID));"
	# create a new admin account
	sudo mysql -u root -h '127.0.0.1' --database="NuOJ" --execute="INSERT INTO \`user\` (username, password, email, admin) VALUES ('NuOJ', 'ff9c3cc1cd8a2cb0ffd4059a4717cdf1', 'NuOJ@ntut.edu.tw', 1);"

db-tcp:
	# create database
	sudo mysql -u root --execute="CREATE DATABASE NuOJ"
	# create database account to two python script
	sudo mysql -u root --execute="CREATE USER 'NuOJService'@'localhost' IDENTIFIED BY 'Nu0JS!@#$$';"
	sudo mysql -u root --execute="CREATE USER 'NuOJJudger'@'localhost' IDENTIFIED BY 'Nu0JJ!@#$$';"
	# grant privileges on two account
	sudo mysql -u root --execute="GRANT ALL PRIVILEGES ON *.* TO 'NuOJService'@'localhost';"
	sudo mysql -u root --execute="GRANT ALL PRIVILEGES ON *.* TO 'NuOJJudger'@'localhost';"
	sudo mysql -u root --execute="FLUSH PRIVILEGES;"
	# create table
	sudo mysql -u root --database="NuOJ" --execute="CREATE TABLE \`user\` (\`user_id\` INT NOT NULL AUTO_INCREMENT, \`username\` VARCHAR(32) NOT NULL, \`password\` VARCHAR(32) NOT NULL, \`email\` VARCHAR(100	) NOT NULL, \`admin\` TINYINT(1) NOT NULL, \`email_verification\` TINYINT(1) NOT NULL, PRIMARY KEY(user_id));"
	sudo mysql -u root --database="NuOJ" --execute="CREATE TABLE \`submission\` ( \`submissionID\` INT NOT NULL AUTO_INCREMENT, \`submissionTime\` VARCHAR(40) NOT NULL, \`submissionBy\` VARCHAR(40) NOT NULL, \`Language\` VARCHAR(20) NOT NULL, \`ProblemID\` VARCHAR(20) NOT NULL,  \`VerdictResult\` VARCHAR(20), \`VerdictTime\` VARCHAR(40), \`VerdictMemory\` VARCHAR(40), PRIMARY KEY(submissionID));"
	sudo mysql -u root --database="NuOJ" --execute="CREATE TABLE \`problem\` (\`ID\` int NOT NULL AUTO_INCREMENT, \`name\` VARCHAR(20) NOT NULL, \`visibility\` VARCHAR(20) NOT NULL, \`token\` VARCHAR(40) NOT NULL, \`author\` VARCHAR(20) NOT NULL, PRIMARY KEY(ID));"
	# create a new admin account
	sudo mysql -u root --database="NuOJ" --execute="INSERT INTO \`user\` (username, password, email, admin) VALUES ('NuOJ', 'ff9c3cc1cd8a2cb0ffd4059a4717cdf1', 'NuOJ@ntut.edu.tw', 1);"

test-all:
	sudo systemctl start nuoj
	sudo systemctl start nuoj-sandbox
	sudo systemctl start nuoj-database
	sudo python3 /opt/nuoj/test.py
	sudo python3 /opt/nuoj-sandbox/test.py
	sudo python3 /opt/nuoj-database/test.py