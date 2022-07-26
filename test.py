import os
import sys

status = os.system('systemctl is-active --quiet nuoj')
print(status)
if status != 0:
    sys.exit(1)

status = os.system('systemctl is-active --quiet nuoj-sandbox')
print(status)
if status != 0:
    sys.exit(1)