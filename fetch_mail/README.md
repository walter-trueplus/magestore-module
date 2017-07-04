# Odoo module - Fetch Mails
This module will provide some usefull actions for you:
+ create new model for mail alias
+ show button for fetch mail manually
+ show all mails incoming through mail alias you created

You can fetch all mails coming to odoo through your mail domain you added.
If you want to recive mails through another mail , change information of the alias you created
or create new one -- see Configuration below

Configuration
-------------
1. Change Alias Domain
+ step 1: Go to Settings --> General Settings
+ step 2: Type your mail domain (after '@' character of your email) to input box
e.g: yourmail@test.com ==> input domain 'test.com'

2. Create an Icoming Mail Server for all email coming to 
mike@trueplus.vn
+ step 1: Go to Settings --> Fetch Mails --> Icoming Mail Servers 
+ step 2: Click Create 
+ step 3: 
    + Type 'Incoming Gmail Server 1' to Name 
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
    + Type 'Outgoing Mail Server 1' to Description 
    + Type smtp.gmail.com in SMTP Server 
    + Choose SSL/TLS in Connection Security 
    + Type corresonpding username and password of email in Username and Password field
    + Click Test Connection . If the system shows a popup like 'Connection Test Succeeded! Everything seems properly set up!'
    Your setup is correct.
    + Click Save.

4. Create an alias for reciving mail
+ step 1: Go to Settings --> Fetch Mails --> Aliases
+ step 2: Click Create button to create new alias
+ step 3: Type 'your+test+inbox' to first input box
+ step 4: Select Fetched Mail in Aliased Model
+ step 5: Click Save

Now, when you click button Fetch Mail in Settings/Fetch Mails/All Fetched Mails so all mail be sended to
your+test+inbox@test.com will show in All Fetched Mails