# Azuracast Request Bot  
Program that checks for song requests from a specific Reddit post's comment section, and sends them to an Azuracast Web Radio Station.

## Installation
- Install Python. You can download it here https://www.python.org/downloads/ (Add to PATH during the installation).  
- Download the ZIP file of this repo (Click on ```Code``` -> ```Download ZIP```).
- Unzip the ZIP file.
- Open your command prompt and change your directory to that of the unzipped folder ```cd unzippedfoldername```.  
- Install the required packages  :
  ```
  pip install -U praw requests
  ```
## Configuration
- Create a Reddit App (script) at https://www.reddit.com/prefs/apps/ and get your ```client_id``` and ```client_secret```.  
- Edit the ```config.ini``` file with your details and save:
  ```
  [REDDIT]
  CLIENT_ID = your_client_id
  CLIENT_SECRET = your_client_secret
  PASSWORD = your_reddit_password
  USERNAME = your_reddit_username
  
  [AZURACAST]
  SITE_URL = public_url_for_the_azuracast_radio
  STATION_ID = station_id_for_accepting_song_requests
  
  [VARS]
  THREAD_ID = id_of_reddit_post (https://www.reddit.com/r/RequestABot/comments/188bkid/request_for_a_simple_python_bot_that_monitor/ -> 188bkid)
  ```

## Running the script
  ```
  python main.py
  ```

## Valid Bot Commands
The bot accepts these commands:  
- !request - Sends a request to the Azuracast Radio. Ex: !request Beatles - A Day In The Life
- !help - Displays valid instructions. Ex: !help
- !list - Displays list of requestable songs on the radio station. It displays them in batches. Ex: !list 1 OR !list 2 OR !list 3

## Extra Information
The bot only listens for top-level comments. Replies will be ignored.  
The bot listens for comments every two minutes.
