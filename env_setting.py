import os
import subprocess


def set_grub():
    f = open("/etc/default/grub", mode="r")
    temp = f.readlines()
    for index,text in enumerate(temp):
        if "GRUB_CMDLINE_LINUX=" in text:
            spltext = text.split("\"")
            spltext[0] += '\"'
            spltext[-1] = "\"" + spltext[-1]
            temp1 = []

            if not "cgroup_enable=memory" in text:
                temp1.append("cgroup_enable=memory")
            if not "swapaccount=1" in text:
                temp1.append("swapaccount=1")

            temp[index] = spltext[0] + spltext[1] + " " + " ".join(temp1) + spltext[-1]       
    f.close()

    f = open("/etc/default/grub", mode="w")
    f.writelines(temp)
    f.close()

def set_kernel():
    if not subprocess.check_output(['cat', '/proc/sys/kernel/randomize_va_space']).decode("utf-8") == "0\n": 
        os.system("echo 'kernel.randomize_va_space = 0' >> /etc/sysctl.conf")
    if not subprocess.check_output(['cat', '/sys/kernel/mm/transparent_hugepage/enabled']).decode("utf-8") == "always madvise [never]\n":
        os.system("echo 'kernel/mm/transparent_hugepage/enabled = never' >> /etc/sysfs.conf")
    if not subprocess.check_output(['cat', '/sys/kernel/mm/transparent_hugepage/defrag']).decode("utf-8") == "always defer defer+madvise madvise [never]\n":
        os.system("echo 'kernel/mm/transparent_hugepage/defrag = never' >> /etc/sysfs.conf")
    if not subprocess.check_output(['cat', '/sys/kernel/mm/transparent_hugepage/khugepaged/defrag']).decode("utf-8") == "0\n": 
        os.system("echo 'kernel/mm/transparent_hugepage/khugepaged/defrag = 0' >> /etc/sysfs.conf")

def run_save():
    os.system("sysctl -p")
    os.system("update-grub")
    reboot = input("A computer restart is needed to complete your installation. Do you want to restart now?(Y|n)")
    if reboot == "Y" or reboot == "":
        os.system("reboot")


if __name__ == "__main__":
    set_grub()
    set_kernel()
    run_save()