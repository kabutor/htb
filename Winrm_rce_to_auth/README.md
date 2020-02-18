If you have RCE on a windows box, on any user, and credentials of another user (has to be able to log in via winrm) and Winrm is enabled, you can use this to call shell as the user with credentials, instead of doing a shell with a low priv user, and then open shell with the elevated user.

I just copy the Nishang Powershell-TCP-Reverse and adapt it.
To use this you need to supply credentials (edit the file) and via Winrm it will auth and return a shell with the authenticated user.

Forgot to say, as is a derivate work from Nishang, it's under the same license (GPL-3 or later)
https://github.com/samratashok/nishang/blob/master/LICENSE
