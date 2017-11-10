import subprocess
all = 'dir'
result = subprocess.Popen(all, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
for line in result.stdout:
    res = ''
    data = line.decode('gbk')
    if  not data.startswith(' '):
        res+=data
    print(res)



