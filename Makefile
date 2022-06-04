.PHONY: all

all:
	sudo apt-get install -y python3 python3-pip mariadb-server git build-essential asciidoc-base libcap-dev
	# clone Isolate repository on github 
	sudo mkdir ~/isolate
	sudo git clone https://github.com/ioi/isolate.git ~/isolate
	# Isolate make install 
	sudo make -C ~/isolate install
	# clone NuOJ repository on github
	sudo mkdir /opt/nuoj
	sudo git clone --recursive https://github.com/ntut-xuan/NuOJ.git /opt/nuoj
	sudo chmod 647 /opt/nuoj/*
	sudo chmod 647 /opt/nuoj/python/nuoj_service.py
	sudo chmod 647 /opt/nuoj/python/nuoj_judger.py
	# clone service file
	sudo cp /opt/nuoj/service/nuoj.service /etc/systemd/system/
	sudo cp /opt/nuoj/service/nuoj-judge.service /etc/systemd/system/
	sudo chmod 647 /etc/systemd/system/nuoj.service
	sudo chmod 647 /etc/systemd/system/nuoj-judge.service
	# create database
	sudo mysql --user="root" --execute="CREATE DATABASE NuOJ"
	# create database account to two python script
	sudo mysql --user="root" --execute="CREATE USER 'NuOJService'@'localhost' IDENTIFIED BY 'Nu0JS!@#$$';"
	sudo mysql --user="root" --execute="CREATE USER 'NuOJJudger'@'localhost' IDENTIFIED BY 'Nu0JJ!@#$$';"
	# grant privileges on two account
	sudo mysql --user="root" --execute="GRANT ALL PRIVILEGES ON *.* TO 'NuOJService'@'localhost';"
	sudo mysql --user="root" --execute="GRANT ALL PRIVILEGES ON *.* TO 'NuOJJudger'@'localhost';"
	sudo mysql --user="root" --execute="FLUSH PRIVILEGES;"
	# create table
	sudo mysql --user="root" --database="NuOJ" --execute="CREATE TABLE \`user\` (\`user_id\` INT NOT NULL AUTO_INCREMENT, \`username\` VARCHAR(32) NOT NULL, \`password\` VARCHAR(32) NOT NULL, \`email\` VARCHAR(100	) NOT NULL, \`admin\` TINYINT(1) NOT NULL, PRIMARY KEY(user_id));"
	sudo mysql --user="root" --database="NuOJ" --execute="CREATE TABLE \`submission\` ( \`submissionID\` INT NOT NULL AUTO_INCREMENT, \`submissionTime\` VARCHAR(40) NOT NULL, \`submissionBy\` VARCHAR(40) NOT NULL, \`Language\` VARCHAR(20) NOT NULL, \`ProblemID\` VARCHAR(20) NOT NULL,  \`VerdictResult\` VARCHAR(20), \`VerdictTime\` VARCHAR(40), \`VerdictMemory\` VARCHAR(40), PRIMARY KEY(submissionID));"
	sudo mysql --user="root" --database="NuOJ" --execute="CREATE TABLE \`problem\` (\`ID\` int NOT NULL AUTO_INCREMENT, \`name\` VARCHAR(20) NOT NULL, \`visibility\` VARCHAR(20) NOT NULL, \`token\` VARCHAR(40) NOT NULL, \`author\` VARCHAR(20) NOT NULL, PRIMARY KEY(ID));"
	# create a new admin account
	sudo mysql --user="root" --database="NuOJ" --execute="INSERT INTO \`user\` (username, password, email, admin) VALUES ('NuOJ', 'ff9c3cc1cd8a2cb0ffd4059a4717cdf1', 'NuOJ@ntut.edu.tw', 1);"
	# install pip package
	sudo pip3 install flask
	sudo pip3 install pymysql
	sudo pip3 install flask_cors
	sudo pip3 install loguru
	sudo pip3 install flask_login
	sudo pip3 install flask_session
	# load service 
	sudo systemctl daemon-reload
	sudo systemctl enable nuoj
	sudo systemctl enable nuoj-judge
	sudo systemctl start nuoj
	sudo systemctl start nuoj-judge

cert:
	sudo snap install core; sudo snap refresh core
	sudo snap install --classic certbot
	-sudo ln -s /snap/bin/certbot /usr/bin/certbot
	sudo certbot certonly --manual --preferred-challenge dns

clean:
	-sudo pip3 uninstall -y flask_session
	-sudo pip3 uninstall -y flask_login
	-sudo pip3 uninstall -y loguru
	-sudo pip3 uninstall -y flask_cors
	-sudo pip3 uninstall -y pymysql
	-sudo pip3 uninstall -y flask
	-sudo mysql --user="root" --execute="DROP DATABASE \`NuOJ\`;"
	-sudo mysql --user="root" --execute="DROP USER 'NuOJService'@'localhost'"
	-sudo mysql --user="root" --execute="DROP USER 'NuOJJudger'@'localhost'"
	-sudo rm -rf /opt/nuoj
	-sudo make -C ~/isolate clean
	-sudo rm -rf ~/isolate
	-sudo systemctl stop nuoj
	-sudo systemctl stop nuoj_judge
	-sudo rm -rf /etc/systemd/system/nuoj.service
	-sudo rm -rf /etc/systemd/system/nuoj-judge.service