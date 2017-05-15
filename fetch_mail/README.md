# Odoo module - Fetch Mails
This module will provide some usefull actions for you:
+ create new model for mail alias
+ show all mails incoming through mail alias you created before
+ show button for fetch mail manually
You can fetch all mails coming to odoo through 'mars+fetch+mail@trueplus.vn'
If you want to recive mails through another mail , change information of the alias you created
or create new one -- see Configuration below

Configuration
-------------
1. Change Alias Domain
+ step 1: Go to Settings --> General Settings
+ step 2: Type 'trueplus.vn' to input box

2. Create an Icoming Mail Server for all email coming to 
mike@trueplus.vn
+ step 1: Go to Settings --> Fetch Mails --> Icoming Mail Servers 
+ step 2: Click Create 
+ step 3: 
    + Type 'Incoming Gmail Server 1' to Description 
    + Choose POP Server in Server type 
    + Type 'pop.gmail.com' in Server Name 
    + Type corresonpding username and password of email in Username and Password field 
    + Tick SSL/TLS
    + Click Test & Confirm
    + Click Save
    
3. Create an Outgoing Mail Server for all email send from mike@trueplus.vn
+ step 1: Go to Settings --> Fetch Mails --> Outgoing Mail Servers
+ step 2: Click Create
+ step 3:
    + Type 'Outgoing Gmail Server 1' to Name 
    + Type smtp.gmail.com in SMTP Server 
    + Type 'pop.gmail.com' in Server Name 
    + Choose SSL/TLS in Connection Security 
    + Type corresonpding username and password of email in Username and Password field
    + Click Test Connection . If the system shows a popup like 'Connection Test Succeeded! Everything seems properly set up!'
    Your setup is correct.
    + Click Save.

4. Create an alias for reciving mail
+ step 1: Go to Settings --> Fetch Mails --> Aliases
+ step 2: Click Create button to create new alias
+ step 3: Type 'mike+test+inbox' to first input box
+ step 4: Select Fetched Mail in Aliased Model
+ step 5: Click Save

Alias bạn vừa tạo hoạt động như một bộ lọc. 
Bạn có thể có nhiều bộ lọc cho cùng 1 địa chỉ mail mike@trueplus.vn.
Ví dụ: mike@trueplus.vn coi như là địa chỉ nhà của bạn thì mike+test1trueplus.vn, mike+test2trueplus.vn
giống như phòng ngủ, phòng khách của bạn.
Tất cả email gửi đến mike@trueplus.vn sẽ sử dụng 'Incoming Gmail Server 1' như là hộp thư của nhà bạn,
nó sẽ phân loại thư theo theo các ký tự nằm sau dấu +.
Tất cả email gửi đi từ mike@trueplus.vn sẽ sử dụng 'Outgoing Gmail Server 1' để gửi thư đi.


