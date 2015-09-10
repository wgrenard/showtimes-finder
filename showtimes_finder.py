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


def split_html(html):
    """Return a tuple containing three lists, with theater, movie, and showtime info.

    Args:
        html (str) -- The text html code containing the showitmes information.

    The first element of the tuple is a list of strings, each containing
    information for a different theater. The second element is a list of lists.
    Each inner list corresponds to a theater, whose list elements are strings
    containing information about each movie playing at that theater. Finally,
    the third element is a 3 dimensional list, at its deepest level containing
    information for each showtime for a given movie at a given theater.
    """

    # Split the html by theater.
    theater_info = html.split('showtimes-theater-title')[1:]

    # Split each theather text by movie.
    movie_info = [theater.split('showtimes-movie-container')[1:] for theater in theater_info]

    # Split each movie for a given theater by showtimes.
    showtimes_info = []

    for movie_list in movie_info:
        temp_list = [movie.split('</time>')[:-1] for movie in movie_list]
        showtimes_info.append(temp_list)

    """
    showtimes_info = [movie.split('</time>')[:-1]
                      for movie_list in movie_info
                      for movie in movie_list]
    """
    return (theater_info, movie_info, showtimes_info)


def pull_theater_titles(theater_info):
    """Return a list of available theater titles from the theater info list.

    Args:
        theater_info (list) -- Each element is a string with information about
                               a different theater.
    """

    # Split each theater string between '</a>' and '>' where the time is located
    # if there are movies playing.
    title_list = [theater.split('</a>', 1)[0].split('>', 1)[1].strip()
                  for theater in theater_info
                  if 'there are no movies' not in theater]

    return title_list


def pull_movie_titles(movie_info):
    """Return a list containing lists of movie titles for each theater.

    Args:
        movie_info (list) -- Each element is a list which contains information
                             on all movies for a given theater.

    The list returned is a list of lists. The inner lists are filled with the
    movie titles. Each inner list contains the titles of movies for a different
    theater.
    """

    title_list = []

    # Each movie_list holds the movie info for a different theater.
    for movie_list in movie_info:
        # Split each move_list to get movie titles, if there are movies playing.
        inner_list = [movie.split('showtimes and tickets', 1)[0].split('alt="', 1)[1].strip()
                      for movie in movie_list
                      if 'there are no movies' not in movie]
        title_list.append(inner_list)

    return title_list


def pull_showtimes(showtimes_info):
    """Return a 3 dimensional list containing showtimes by movie and theater.

    Args:
        showtimes_info (list) -- A 3 dimensional list of information on showtimes
                                 by movie and theater.

    The list returned is a 3 dimensional list. The innermost list contains
    showtimes, for a given movie at a given theater.
    """

    showtimes_list = []
    theater_list = []

    for movie_list in showtimes_info:
        for movie in movie_list:
            times = [showtime[-6:] if showtime[-7] == '>'
                     else showtime[-7:]
                     for showtime in movie]
            theater_list.append(times)
        showtimes_list.append(theater_list)

    return showtimes_list


def present_showtimes(theater_titles, movie_titles, showtimes):
    """Present the theaters, movies, and showtimes, in a formatted manner.

    Args:
        theater_titles (list) -- A list of theater titles.
        movie_titles (list) -- A 2 dimensional list of movie titles separated by theater.
        showtimes (list) -- A 3 dimensional list of showtimes separated by movie
                            and theater
    """

    for (theater, theater_title) in enumerate(theater_titles):
        print '\nTheater: ' + theater_title + '\n'

        for (movie, movie_title) in enumerate(movie_titles[theater]):
            print '  Movie: ' + movie_title

            for showtime in showtimes[theater][movie]:
                print '         ' + showtime
            print ''


def run_showtimes_finder():
    """Run the showtimes_finder program."""

    present_instructions()
    response = ''
    html = ''

    while True:
        response = process_input()
        html = response.read()  # Read information from the URL

        # If the html is valid, then program execution can continue.
        if html.find("This location can't be found.") == -1:
            break
        else:
            print("\nThe location you entered cannot be found. Please check that "
                  "your location was spelled correctly and entered in the correct "
                  "format")

    # Split the html by where theater, movie, and showtimes info is located.
    theater_info, movie_info, showtimes_info = split_html(html)

    # Pull the titles and showtimes from the respective chunks of html text.
    theater_titles = pull_theater_titles(theater_info)
    movie_titles = pull_movie_titles(movie_info)
    showtimes = pull_showtimes(showtimes_info)

    present_showtimes(theater_titles, movie_titles, showtimes)
    response.close()        #close the urllib2 connection file


if __name__ == "__main__":
    run_showtimes_finder()
