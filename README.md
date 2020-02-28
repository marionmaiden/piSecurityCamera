# piSecurityCamera
Security camera for raspberry pi. It takes pictures at every 2 seconds and if any difference is detected between the original and the current images, it sends by e-mail with the timestamp (GMT) and stores in a google drive account (to be implemented)

## Motion detection algorithm
- To be written

# Important information

## Enable less secure app from Gmail
If you are using GMail as e-mail provider to send the images, please remember to enable it from logging from less secure apps by clicking on the link below and enabling the option:

[https://www.google.com/settings/security/lesssecureapps]

# Dependencies

- PIL (as Pillow)
   - `pip3 install Pillow`
- Google API
   - `pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
- ConfigParser (to read e-mail properties)
   - `pip3 install configparser`
