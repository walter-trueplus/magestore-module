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
+ step 2: Type 'your.domain' to input box

2. Create an alias for reciving mail
+ step 1: Go to Settings --> Email --> Aliases
+ step 2: Click Create button to create new alias
+ step 3: Type 'your+alias' to first input box
+ step 4: Select Fetched Mail in Aliased Model
+ step 5: Click Save

Now, You can fetch all mails coming to 'your+alias@your.domain'
