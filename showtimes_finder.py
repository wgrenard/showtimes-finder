"""This program queries the web to find movie showtimes.

Upon obtaining the location and date the user is interested in, the coresponding
information is queried from http://www.fandango.com. The theaters, movies, and
showtimes information available there is then presented in an organized manner.
"""

import urllib2
import time


def present_instructions():
    """Print instructions on how to use the program"""

    print "\n\nWelcome to the movie showtimes generator!"
    print "Please enter the city and state where you wish to find movie times."
    print "Then enter the date which you are interested in."
    print "The movie showtimes generator will then return all theaters and showtimes in your area."


def process_input():
    """Return HTML from proper page determined by the user's input."""

    # FIXME: Use exception handling here.
    while True:
        location = raw_input("\n\nPlease enter your location in the following"
                             "format: City St. e.g. Berkeley CA: ")

        # Split the location input
        location_list = location.split()

        # Only creat city string if there is at least a city and state entered
        if len(location_list) >= 2:
            city = '+'.join(location_list[:len(location_list) - 1])
            break
        else:
            print ("\nIncorrect format. Please check that you entered the"
                   "location in City ST format and that you included both a city"
                   "and a state.")

    # Gather date info and account for errors.
    # FIXME: Use exception handling here.
    while True:
        date = raw_input("\n\nPlease enter the date you wish to see the movie"
                         "in the following format mm/dd/yyyy: ")
        date_list = date.split("/")

        if len(date) == 10:
            #if the current date is before the date entered, then the format is acceptable.
            if time.strftime("%m/%d/%Y") <= date and time.strftime("%Y") <= date_list[2]:
                # Format the URL.
                url = (
                    'http://www.fandango.com/%s_+%s_movietimes?date=%s' %
                    (city.lower(), location_list[len(location_list) - 1].lower(),
                     date)
                )
                break

            # Else the date is incorrect.
            else:
                print("\nThe date you entered is outside of allowed range."
                      "Please check the date you entered is today's date or"
                      "later.")

        #if the date is not the correct length then ask for a new date
        else:
            print("Incorrect format. Please check that you entered the date in"
                  "proper mm/dd/yyyy format")

    return urllib2.urlopen(url)  # Return info from the URL.



def find_indicies_of(target_str, search_str):
    """Return a list of indices where target_str occurs in search_str.

    Args:
        target_str (str) -- The string to be searched for.
        search_str (str) -- The string to be searched through.
    """

    indicies = []  # Holds indeces to be returned
    str_len = len(target_str)
    i = 0  # Keeps track of where to start the search

    while True:
        index = search_str.find(target_str, i)

        # Exit loop if str is not found.
        if index == -1:
            break

        # If str is found, add it to indeces[] and change the starting point of
        # the next search.
        else:
            indicies.append(index)
            i = (index + str_len)

    return indicies


def split_at_string(trigger_str, str_to_split):
    """Return a list of strings split from str_to_split at the indeces of trigger_str.

    Args:
        trigger_str (str) -- String at which splitting will occur.
        str_to_split (str) -- String that is being split.

    The location of each split is determined to be at the index specified by
    trigger_str. E.g. split_at_string('b','abcdeabcde') returns ['bcdea', 'bcde']
    """

    # FIXME: Make this function simpler by just using string.split(seperator)

    # Get a list of indices where splitting will occur.
    indicies = find_indicies_of(trigger_str, str_to_split)
    sub_strings = []  # This list will hold the split strings

    # FIXME: Use a list comprehension or enumeration here.
    for index in range(len(indicies)):

        # Split from the last index to the end of the string.
        if index == len(indicies) - 1:
            sub_strings.append(str_to_split[indicies[index]:])

        # Split from current index to the next index.
        else:
            sub_strings.append(str_to_split[indicies[index]:indicies[index + 1]])

    return sub_strings


def pull_theater_titles():
    """Return a list of available theater titles from the html in theaters list."""

    title_list = []  # List to hold theater titles.

    # FIXME: Use a list comprehension or enumeration here. Avoid global vars use.
    for index in range(len(theaters)):
        # If 'there are no movies' is not found, there are showtimes to be displayed
        if theaters[index].find('there are no movies') == -1:
            terminating_index = theaters[index].find('</a>')
            temp_list = theaters[index][:terminating_index].split()
            title_str = ' '.join(temp_list[2:])
            title_list.append(title_str)

    return title_list


def pull_movie_titles():
    """Return a list of movie titles for each theater.

    The list returned is a list of lists. The inner lists are filled with the
    movie titles. Each list element represents movies at a different theater.
    """

    inner_list = []  # List to temporarily hold movie titles from one single theater
    title_list = []  # List to hold inner lists.

    # Here the outer loop goes through the movies list, and inner loop goes
    # through the strings of each element in the movies list.
    # FIXME: Use list comprehension or enumeration. Remove global vars use.
    for i in range(len(movies)):
        for j in range(len(movies[i])):
            # If there are movies to display, then add them to the list
            if movies[i][j].find('there are no movies') == -1:
                # The title starts 5 chars after 'alt'.
                starting_index = movies[i][j].find('alt') + 5
                # The title ends just before 'showtimes and tickets'
                terminating_index = movies[i][j].find('showtimes and tickets')
                # Remove whitespace
                temp_list = movies[i][j][starting_index:terminating_index].split()
                title_str = ' '.join(temp_list)
                inner_list.append(title_str)

        if len(inner_list) > 0:
            title_list.append(inner_list)

        inner_list = []

    return title_list


def determine_showtimes(search_str):
    """Return a list of showtimes from search_str.

    Args:
        search_str (str) -- The string to be searched for showtimes.

    Note that for this function to work it must be passed a string from an
    element of the movies[] list.
    """

    showtimes_list = []
    search_index = 0    # Marks the starting index of the search.

    while True:
        terminating_index = search_str.find('</time>', search_index)

        # Break if all times have been found.
        if terminating_index == -1:
            break

        # If this condition is met then this is the index where the time starts.
        if search_str[terminating_index - 7] != '>':
            showtimes_list.append(search_str[terminating_index - 7: terminating_index])
        # Otherwise the time begins 6 chars before terminating index
        else:
            showtimes_list.append(search_str[terminating_index - 6: terminating_index])

        search_index = terminating_index + 1

    return showtimes_list


def present_showtimes():
    """Present the theaters, movies, and showtimes in a formatted manner."""
    # FIXME: Remove dependence on global vars.
    theater_titles = pull_theater_titles()
    movie_titles = pull_movie_titles()

    # FIXME: Use list comprehensions or enumerations.
    for i in range(len(theater_titles)):
        print '\nTheater: ' + theater_titles[i] + '\n'

        for j in range(len(movie_titles[i])):
            print '  Movie: ' + movie_titles[i][j]

            showtimes = determine_showtimes(movies[i][j])
            for showtime in showtimes:
                print '         ' + showtime
            print ''


def is_url_valid():
    """Return true if url was found. Return false if not."""
    # FIXME: Does this really need to be a function?
    return html.find("This location can't be found.") == -1


present_instructions()
response = ''
html = ''

while True:
    response = process_input()
    html = response.read()  # Read information from the URL

    if is_url_valid():
        break
    else:
        print("\nThe location you entered cannot be found. Please check that "
              "your location was spelled correctly and entered in the correct "
              "format")

# Split the html into a list whose elements each have info on only one theater.
theaters = split_at_string('showtimes-theater-title', html)
movies = []

# Loop through the theater strings and split each string by movie.
for theater in theaters:
    movies.append(split_at_string('showtimes-movie-container', theater))

present_showtimes()
response.close()        #close the urllib2 connection file
