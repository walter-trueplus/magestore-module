Editting My Account Page
---
This module will adds some property for /my/account page and /web/signup page:
+ Add change password button in /my/account: if that is not first time the user change password,
Odoo will direct redirect to /web/reset_password page and the user can change the password directly
You need enable reset password and signup options by:

step 1: Install this module (website_my_profile)
step 2: Go to Settings --> General Settings
step 3: Enable two options:
				- Enable password reset from Login page
				- Allow external users to sign up
step 4: Click Apply

If you choose reset password from /web/login url, an email will be send to
your email if your email address is valid, if not: the email will be send to
mars@trueplus.vn (can change)
If you click Reset Password button in /my/account and it's your first time 
you reset password, an email will be send to
your email. If not first time, you will be redirect to /web/reset_password?reset_directly=directly


+ Add the birthday property to /web/signup page and 
 /my/account page