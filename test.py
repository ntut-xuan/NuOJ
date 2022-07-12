import os

status = os.system('systemctl is-active --quiet nuoj')
print(status)
if status != 0:
    exit(status)

status = os.system('systemctl is-active --quiet nuoj-sandbox')
print(status)
if status != 0:
    exit(status)

status = os.system('systemctl is-active --quiet nuoj-database')
print(status)
if status != 0:
    exit(status)