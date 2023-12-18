from util import general_util, azuracast_util, database_util
from util.error_util import AzuracastError, ErrorType
from util.logging_util import get_logger

LOGGER = get_logger(__name__)

def process_comment(comment, base_url, station_id, db_connection):
    if comment.body[0] != '!':
        LOGGER.info('Irrelevant comment.')
        return
    
    command = comment.body.split('!')[1].split(' ')[0].strip()
    
    if command == 'request':
        handle_request(comment, base_url, station_id)

    elif command == 'list':
        display_song_list(comment, base_url, station_id)

    elif command == 'help':
        display_help_text(comment)

    elif command == 'nowplaying':
        display_now_playing(comment, base_url)

    else:
        handle_invalid_command(comment)

    database_util.insert_processed_comment(db_connection, comment.id)

    LOGGER.info(f'Comment has been added to database - {comment.id}: {comment.author.name} - {comment.body}')

def handle_request(comment, base_url, station_id):
    song = comment.body.split('!request')[1].strip()
    response = azuracast_util.send_request(base_url, station_id, song)

    if isinstance(response, AzuracastError):
        if response.type == ErrorType.FailedToFetchRequestableSongs:
            comment.reply("There was an error while checking if the song could be requested. Please try again later.")
        elif response.type == ErrorType.FailedToRequestSong:
            comment.reply('The request cannot be made at this time. Please try again later.')
        elif response.type == ErrorType.SongIsNotRequestable:
            comment.reply("This song cannot be requested. Use the 'list' command to see valid requestable songs.")

        LOGGER.error(f"Azuracast Request Error: {response.description}")
        
    else:
        comment.reply('Your request has been added to the queue.')
        LOGGER.info(f"Successful request - '{song}'")

def display_song_list(comment, base_url, station_id):
    songs = azuracast_util.get_requestable_songs(base_url, station_id)
    if isinstance(songs, AzuracastError):
        comment.reply('Unable to fetch list of requestable songs at the moment. Please try again later.')

        LOGGER.error(f"Requestable Song Fetch Error: {songs.description}")

        return

    songs = general_util.split_large_song_list(songs, 50)

    list_index = comment.body.split('!list')[1].strip()
    try:
        list_index = int(list_index)
    except ValueError:
        list_index = 1  # Default to the first list if the input is not a valid integer

    if list_index <= 0 or list_index > len(songs):
        list_index = 1

    list_index -= 1 # Converts input to zero index format

    response_message = '&#x200B;\n\n'
    response_message += '|Song Artist|Song Title|\n'
    response_message += '|:-|:-|\n'

    # Gets song chunk tuple from list_index, then gets song list from the first index of the song
    # chunk tuple.
    for song in songs[list_index][1]:
        response_message += f"|{song['song']['artist']}|{song['song']['title']}|\n"

    response_message += '\n&#x200B;'

    comment.reply(response_message)

    LOGGER.info(f"Requestable Songs displayed.")

def display_help_text(comment):
    comment.reply(general_util.generate_help_text())

    LOGGER.info('Help text displayed.')

def display_now_playing(comment, base_url):
    current_song_response = azuracast_util.get_nowplaying(base_url)
    if isinstance(current_song_response, AzuracastError):
        comment.reply('Unable to fetch currently playing song at the moment. Please try again later.')

        LOGGER.error(f"Now Playing Fetch Error: {current_song_response.description}")

        return
    
    station_name = current_song_response[0]['station']['name']
    song_artist = current_song_response[0]['now_playing']['song']['artist']
    song_title = current_song_response[0]['now_playing']['song']['title']

    response_message = f"Now Playing at {station_name}: \n\n"
    response_message += '&#x200B;\n\n'
    response_message += '|Song Artist|Song Title|\n'
    response_message += '|:-|:-|\n'
    response_message += f'|{song_artist}|{song_title}|\n'
    response_message += '\n&#x200B;'

    comment.reply(response_message)

    LOGGER.info(f"Currently Playing Song displayed.")

def handle_invalid_command(command, comment):
    help_text = general_util.generate_help_text()
    comment.reply(f"Invalid command '{command}'. Please use the correct command format.\n\n{help_text}")

    LOGGER.info(f"Invalid command '{command}'.")