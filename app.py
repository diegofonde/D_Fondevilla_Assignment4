# imports
from helper import helper
from db_operations import db_operations


# global variables
db_ops = db_operations("playlist.db")

# functions
def startScreen():
    print("Welcome to you playlist!")

    #db_ops.create_songs_table()

    # prompt user if they want to load new songs to the database
    choice = input("Do you want to load new songs into the database? (yes/no): ")
    if choice == "yes":
        filepath =  input("Enter the path to the file containing new songs: ")
        db_ops.update_songs_table(filepath)

    if db_ops.is_songs_empty():
        db_ops.populate_songs_table("songs.csv")

# print menu and have users select option
def options():
    print('''Select from the following menu options:
    1. Find songs by artist
    2. Find songs by genre
    3. Find songs by feature
    4. Update song information
    5. Delete song
    6. Exit''')
    return helper.get_choice([1,2,3,4,5,6])

# print all artists, let users select one, and then display all songs by that artist
def search_by_artist():
    # get all artists
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    print("Artists in playlist: ")
    artists = db_ops.single_attribute(query)

    # display all artists and let the user pick one
    choices = {}
    for i in range(len(artists)):
        choices[i] = artists[i]
        print(i, artists[i])
    index = helper.get_choice(choices.keys())

    # user can ask for 1, 5, or all songs returned
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    # display all songs by that artist
    query = '''
    SELECT DISTINCT name
    FROM songs
    WHERE Artist =:artist
    ORDER BY RANDOM()
    '''
    dictionary = {"artist":choices[index]}
    if num != 0:
        query += "LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

def search_by_genre():
    # get all genre
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    print("Genres in playlist: ")
    genres = db_ops.single_attribute(query)

    # display all genres2 and let the user pick one
    choices = {}
    for i in range(len(genres)):
        choices[i] = genres[i]
        print(i, genres[i])
    index = helper.get_choice(choices.keys())

    # user can ask for 1, 5, or all songs returned
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    # display all songs by that genre
    query = '''
    SELECT DISTINCT name
    FROM songs
    WHERE Genre =:genre
    ORDER BY RANDOM()
    '''
    dictionary = {"genre":choices[index]}
    if num != 0:
        query += "LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

def search_by_feature():
    # features to sort by
    features = ['Danceability', 'Liveness', 'Loudness']

    # show features and have user select one
    choices = {}
    for i in range(len(features)):
        choices[i] = features[i]
        print(i, features[i])
    index = helper.get_choice(choices.keys())

    # user can ask for 1, 5, or all songs returned
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    # print results
    query = "SELECT DISTINCT name FROM songs ORDER BY "+choices[index]+" DESC "

    dictionary = {}
    if num != 0:
        query += "LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

def update_song_info():
    # Obtain song using user input and get songID
    song_name = input("What is the name of the song you want to update?: ")
    query = '''
    SELECT songID
    FROM songs
    WHERE Name =:name 
    '''
    song_searched = {"name": song_name}
    songs_searched_results = db_ops.single_attribute_params(query, song_searched)

    # If there is no results
    if len(songs_searched_results) == 0:
        print("There is no existing song in the database\n")
        return
    else:
        # Let user alter the attribute they desire
        print("Select what you want to alter: ")
        attributes = ['Name', 'Album', 'Artist', 'releaseDate', 'Explicit']
        choices = {}
        for i in range(len(attributes)):
            print(i, attributes[i])
            choices[i] = attributes[i]
        index = helper.get_choice(choices.keys())

        new = input("Input the new value: ")

        # While loop for if user inputs invalid value
        while True:
            if index == 0 or index == 1 or index == 2:
                if len(new) > 20:
                    print("Invalid value, please type a value containing 20 characters or less.")
                    new = input("Input the new value: ")
                else:
                    break
            elif index == 3:
                date = []
                for i in range(len(new)):
                    date.append(new[i])
                if len(new) != 10:
                    print("Invalid value, please type again.")
                    new = input("Input the new value: ")    
                else:
                    if date[4] == '-' and date[7] == '-':
                        break
                    else: 
                        print("Invalid value, please type in a date.")
                        new = input("Input the new value: ")    
            else:  
                if new == "True" or new == "False":
                    if new == "True":
                        new == True
                    else:
                        new == False
                    break
                else:
                    print("Invalid value, please type in either True or False.")
                    new = input("Input the new value: ")
        
        #Query to alter information of a song
        attribute = attributes[index]

        query = f'''
        UPDATE songs
        SET {attribute} =:value
        WHERE songID =:songid
        '''

        new_info = {"value":new,"songid":songs_searched_results[0][0]}
        db_ops.modify_query_params(query,new_info)

def delete_song():
    song_name = input("What is the name of the song you want to delete?: ")
    query = '''
    SELECT songID
    FROM songs
    WHERE Name =:name 
    '''
    song_searched = {"name": song_name}
    songs_searched_results = db_ops.single_attribute_params(query, song_searched)

    if len(songs_searched_results) == 0:
        print("There is no existing song in the database.")
        return
    else:
        query = '''
        DELETE FROM songs
        WHERE songID =:songid
        '''

        song_to_delete = {"songid": songs_searched_results[0][0]}
        db_ops.modify_query_params(query, song_to_delete)


# main method
startScreen()
while True:
    user_choice = options()
    if user_choice == 1:
        search_by_artist()
    if user_choice == 2:
        search_by_genre()
    if user_choice == 3:
        search_by_feature()
    if user_choice == 4:
        update_song_info()
    if user_choice == 5:
        delete_song()
    if user_choice == 6:
        print("Goodbye!")
        break
db_ops.destructor()
