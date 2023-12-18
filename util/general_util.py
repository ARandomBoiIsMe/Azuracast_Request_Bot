def generate_help_text():
    message = '&#x200B;\n\n'

    message += '|Command|Description|Usage|Example|\n'
    message += '|:-|:-|:-|:-|\n'
    message += '|!help|Displays this help message|!help|-|\n'
    message += '|!request|Makes a song request|!request {song_artist} - {song_title}|!request Beatles - A Day In Time|\n'
    message += '|!list|Displays batches of requestable songs|!list {index}|!list 1|\n'
    message += '|!nowplaying|Displays the currently playing song|!nowplaying|-|\n\n'
    
    message += '&#x200B;'

    return message

# Moves through list in steps of chunk_size, and generates a new tuple for each chunk
def split_large_song_list(song_json, chunk_size):
    return [(i // chunk_size, song_json[i:i + chunk_size]) for i in range(0, len(song_json), chunk_size)]