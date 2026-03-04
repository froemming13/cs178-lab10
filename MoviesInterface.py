# name: Mikayla Froemming
# date: 03/03/2026
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 0 (out of 5) -- if I don't change this, I agree to get 0 points.

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Movies')
REGION = "us-east-1"
TABLE_NAME = "Movies"

def get_table():
    """Return a reference to the DynamoDB Movies table."""
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    return dynamodb.Table(TABLE_NAME)


def print_movie(movie):
    """Print a single movie's details in a readable format."""
    title = movie.get("Title", "Unknown Title")
    year = movie.get("Year", "Unknown Year")
    
    ratings = movie.get("Ratings", "No ratings")
    genre = movie.get("Genre", "Unknown Genre")

    print(f"  Title : {title}")
    print(f"  Year  : {year}")
    print(f"  Ratings: {ratings}")
    print(f"  Genre: {genre}")
    print()

def create_movie():
    """
    Prompt user for a Movie Title.
    Add the movie to the database with the title and an empty Ratings list.
    """
    table = get_table()
    user_title = input("Enter a Movie Title: ")

    response = table.scan(FilterExpression=Attr("Title").eq(user_title))
    items = response.get("Items",[])

    if items:
        print("Movie Found: ")
        for movie in items:
            print_movie(movie)
    
    else:
        print("Movie Not Found")
        add_movie = input("Add a movie?: ")
        if add_movie.strip().upper() == "Y":
            add_movie_title = input("Title of Movie: ")
            table.put_item(Item = {f'Title': add_movie_title,
                                   f'Ratings': []})
            print("creating movie")
        else:
            print("Okay!")

def print_all_movies():
    """Scan the entire Movies table and print each item."""
    table = get_table()
    
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No movies found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} movie(s):\n")
    for movie in items:
        print_movie(movie)

def update_rating():
    """
    Prompt user for a Movie Title.
    Prompt user for a rating (integer).
    Append the rating to the movie's Ratings list in the database.
    """
    try:
        table = get_table()    
        title = input("What is the movie title? ")
        rating = int(input("What is the rating (integer): "))
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Ratings, :r)",
            ExpressionAttributeValues={':r': [rating]}
        )
        print("updating rating")

    except Exception:
        print("error in updating movie rating")

def delete_movie():
    """
    Prompt user for a Movie Title.
    Delete that item from the database.
    """
    table = get_table()
    movie_delete = input("What movie would you like to delete: ")
    try:
        table.delete_item(Key={"Title": movie_delete})
        print("deleting movie")
    except Exception:
        print("error deleting movie")

def query_movie():
    """
    Prompt user for a Movie Title.
    Print out the average of all ratings in the movie's Ratings list.
    """
    table = get_table()
    title = input("Enter the movie title to query: ")

    try:
        response = table.get_item(Key={"Title": title})
        movie = response.get("Item")
        if not movie:
            print(f"No movie found with the title '{title}'")
            return
        ratings = movie.get("Ratings",[])
        if not ratings:
            print(f"'{title}' has no current ratings.")
            return
        average = sum(ratings)/len(ratings)
        print(f"Average rating for '{title}' is: {average:.2f}")

    except Exception:
        print("could not query the movie")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to QUERY a movie's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
