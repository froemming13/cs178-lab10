# name: Mikayla Froemming
# date: 03/04/2026
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# using my read_my_table file from previous lab.

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Playlist')
REGION = "us-east-1"
TABLE_NAME = "Playlist"

def get_table():
    """Return a reference to the DynamoDB Playlist table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)


def print_song(song):
    """Print a single song's details in a readable format."""
    title = song.get("Title", "Unknown Title")
    artist = song.get("Artist", "Unknown Artist")
    album = song.get("Album", "No Associated Album")
    streams = song.get("Streams", "Unknown Number of Streams")

    print(f"  Title : {title}")
    print(f"  Artist  : {artist}")
    print(f"  Album: {album}")
    print(f"  Streams: {streams}")
    print()

def add_song():
    """
    Prompt user for a song title.
    Add the song to the database with the title.
    """
    table = get_table()
    user_title = input("Enter a song title: ")

    response = table.scan(FilterExpression=Attr("Title").eq(user_title))
    items = response.get("Items",[])

    if items:
        print("Song Found: ")
        for song in items:
            print_song(song)
    
    else:
        print("Song Not Found")
        add_movie = input("Add a song?: ")
        if add_movie.strip().upper() == "Y":
            user_added_song = input("Title of the song: ")
            table.put_item(Item = {f'Title': user_added_song,})
            print("Adding song...")
        else:
            print("Okay!")

def print_playlist():
    """Scan the entire Playlist table and print each song."""
    table = get_table()
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No songs found...")
        return
    
    print(f"Found {len(items)} song(s):\n")
    for song in items:
        print_song(song)

def update_streams():
    """
    Prompt user for a song title.
    Prompt user for the number of streams (integer).
    Append the number of streams to the song's "Streams" section in the database.
    """
    try:
        table = get_table()    
        title = input("What is the song title? ")
        streams = int(input("What is the song's streams (integer)?): "))
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(streams, :r)",
            ExpressionAttributeValues={':r': [streams]}
        )
        print("Updating song's streams...")

    except Exception:
        print("Error in updating song's streams...")

def delete_song():
    """
    Prompt user for a song title.
    Delete that item from the database.
    """
    table = get_table()
    song_delete = input("What song would you like to delete: ")
    try:
        table.delete_item(Key={"Title": song_delete})
        print("Deleting song...")
    except Exception:
        print("Error in deleting the song...")

def query_song():
    """
    Prompt user for a song title.
    Print out the average of all streams in the Playlist's Streams list.
    Average streams based across different listening platforms.
    """
    table = get_table()
    title = input("Enter the song title to query: ")

    try:
        response = table.get_item(Key={"Title": title})
        song = response.get("Item")
        if not song:
            print(f"No song found with the title '{title}'")
            return
        streams = song.get("Streams",[])
        if not streams:
            print(f"'{title}' has no current tracked streams.")
            return
        average = sum(streams)/len(streams)
        print(f"Average streams for '{title}' is: {average}")

    except Exception:
        print("Could not query the song...")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new song")
    print("Press R: to READ all songs")
    print("Press U: to UPDATE a song (add an artist)")
    print("Press D: to DELETE a song")
    print("Press Q: to QUERY a song's average streams")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            add_song()
        elif input_char.upper() == "R":
            print_playlist()
        elif input_char.upper() == "U":
            update_streams()
        elif input_char.upper() == "D":
            delete_song()
        elif input_char.upper() == "Q":
            query_song()
        elif input_char.upper() == "X":
            print("Exiting...")
        else:
            print("Not a valid option. Try again.")

main()
