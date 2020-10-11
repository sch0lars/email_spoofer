import re
import subprocess
from sys import argv
from telnetlib import Telnet


try:
    if argv[1]:
        host_name = argv[1]
        open_bracket = ""
        close_bracket = ""
except:
    host_name = "gmail.com"
    open_bracket = "<"
    close_bracket = ">"
    
server = subprocess.getoutput("nslookup -type=mx %s" % host_name)
results = re.split("[,\n]", server)
server_list = []
for name in results:
    if "mail exchanger" in name:
        addresses = re.split("=", name)
        for addr in addresses:
            if "mail exchanger" not in addr:
                server_list.append(addr)
                
mail_exchanger = server_list[0].replace(" ", "")

sender = input("Enter the address you would like to send the email from: ")
sender = "{0}{1}{2}".format(open_bracket, sender, close_bracket)
receiver = input("Enter the address you would like to send the email to: ")
receiver = "{0}{1}{2}".format(open_bracket, receiver, close_bracket)
subject = input("Enter the subject of the email: ")
message = input("Enter the message of the email: ")
message = "To: {0}\nFrom: {1}\nSubject: {2}\n{3}".format(receiver, sender, subject, message)

tn = Telnet(mail_exchanger, 25, 5)
tn.open(mail_exchanger, '25', 5)
tn.write("HELO username".encode('ascii') + b"\r\n")
print(tn.read_until("\n\r".encode(), 5))
tn.write(("MAIL FROM: " + sender).encode('ascii') + b"\r\n")
print(tn.read_until("\n\r".encode(), 5))
tn.write(("RCPT TO: " + receiver).encode('ascii') + b"\r\n")
print(tn.read_until("\n\r".encode(), 5))
tn.write("DATA".encode('ascii') + b"\r\n")
print(tn.read_until("\n\r".encode(), 5))
tn.write(message.encode('ascii') + b"\r\n")
tn.write(".".encode('ascii') + b"\r\n")
print(tn.read_until("\n\r".encode(), 5))
tn.close()
