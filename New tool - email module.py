import win32com.client as client
import pandas

df = pandas.read_excel('C:\\Users\\username\\Path to a excel file\\XXX.xlsx', engine='openpyxl',sheet_name='Sheet1') #change to the path of excel file
x = 1 # how many rows (how many emails)
recipient_list = []
DetectionHost_list = []
ScanResult_list = []
for i in range(x):
    Column1 = df.loc[i, 'Column1']   #column1 is name
    recipient_list.append(Column1)
    DetectionHost = df.loc[i, 'DetectionHost']
    DetectionHost_list.append(DetectionHost)
    ScanResult = df.loc[i, 'ScanResult']
    ScanResult_list.append(ScanResult)

cc = '''Name1 listed in AD <an email address>; 
        Name2 listed in AD <an email address>; 
        Name3 listed in AD <an email address>; 
        Name4 listed in AD <an email address>; '''

def create_email(recipient, cc, host, ScanResult):
    msg = client.Dispatch('Outlook.Application').CreateItem(0)
    msg.To = recipient
    msg.CC = cc
#   msg.Attachments.Add(file) # attach a file if needed
    msg.Subject = 'Filling in your email subject'
    html_body = f"""
        <html>
            <body>
                <div class="html_email_body">
                    <div class="intro">
                        Hi {recipient},
                        <br>
                        <br>
                        this is an exmaple of a email info
                        <br>
                        <br>
                        <div class="host">DetectionHost: <span style="color:red;">{host}</span> 
                            <br>
                            <br>
                        </div>
                        <div class="result">
                            <span style="color:red;">{ScanResult}</span>
                        </div>
                        <div class="end">
                            <br>
                            Please take action ASAP with example task(s). Thank you.
                            <br>
                            <br>
                        </div>
                    </div>
                </div>
            </body>
        </html>
    """
    path = f'C:\\Users\\username\\Path to destination\\{i}filename_to_who_{recipient}.msg' #where to save the file, file name has sequence number and name#
    msg.Display() # this will open a draft and insert your email signature
    msg.HTMLBody = html_body + msg.HTMLBody #this will insert the "html message body" in front of the signature 
    msg.SaveAs(path)

print('How many email drafts to be generated : ' + str(len(recipient_list)))
for i in range(len(recipient_list)):
    create_email(recipient_list[i], cc, DetectionHost_list[i], ScanResult_list[i])
