# piSecurityCamera
Security camera for raspberry pi. It takes pictures at every 2 seconds and if any difference is detected between the original and the current images, it sends by e-mail with the timestamp (GMT) and stores in a Google Drive account

## How to run
After installing the pip dependencies, simply call

```
python3 run.py
```

## Motion detection algorithm
The motion detection algorithm is pretty simple:
- First of all I take a picture and call it base image
- Then, inside an infinite loop I take another picture, called current picture
- There is a image diff method that calculates an image difference value
   - Apply gaussian filter to both images
   - Reduce both imates to a 8x8 pixels matrix
   - calculate pixel by pixel value difference (each pixel is the sum of the three band values) between both images
   - get the average of all pixels difference
- If this difference value is above a stablished threshold (I set as 15 but can be different), I save the image locally and inside my Google Drive. I also replace base image by current image and discard the base.
- If this difference is above a higher threshold (I set as 50), I also send an e-mail to my address

# Important information

## How to generate an api token to Google Drive API to send the picture (quick and dirty)
They way Google drive creates and manages api credentials looked quite complex to me and as I didn't want to spend too much time on this (I just wanted to see it working at first), I created a quickstart credential (which also is not a simple task as you might see below).

So, to get a credential for our project: 
1. open the page [https://developers.google.com/drive/api/v3/quickstart/python]
2. click on "Enable Drive API" button. It will download a file called credentials.json
3. Copy the code example below in the same page and save in a py file in a pc with Window manager (cause my raspberry pi doesn't have)
4. Change the line `SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']` to `SCOPES = ['https://www.googleapis.com/auth/drive']`. This will allow using Google Drive API not only for reading but also for file write
5. Run this python file (`Credentials.json` must be in the same folder). It will open a browser window asking for authorization to run the project. Next, Next, Next and finish
6. After all, you will get 2 files called `Credentials.json` (from the second step) and `token.picke` (created in step 5). Copy both files under `resources` folder of our project

## Enable less secure app from Gmail
If you are using GMail as e-mail provider to send the images, please remember to enable it from logging from less secure apps by clicking on the link below and enabling the option:

[https://www.google.com/settings/security/lesssecureapps]

## Configure your e-mail
Inside the /resources folder there is a template properties file that must be filled with your e-mail data and renamed to `email.properties`

# Dependencies

- PIL (as Pillow)
   - `pip3 install Pillow`
- Google API
   - `pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
- ConfigParser (to read e-mail properties)
   - `pip3 install configparser`
