import os

status = os.system('systemctl is-active --quiet nuoj')
print(status)
exit(status)