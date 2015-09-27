"""This program queries the web to find movie showtimes.

Upon obtaining the location and date the user is interested in, the coresponding
information is queried from http://www.fandango.com. The theaters, movies, and
showtimes information available there is then presented in an organized manner.
"""

import urllib2
import time


class Theater(object):
    """Holds information for a theater, including its title and movie titles.

    Attributes:
        theater_info (str) -- Raw html that contains all information about the
                              theater.
        title (str) -- The title of the theater, pulled from theater_info.
        movies (list) -- A list of Movie objects, one for each movie that is
                         playing at the theater.
    """

    def __init__(self, theater_info):
        self.theater_info = theater_info
        self.title = self.pull_theater_title()
        self.movies = self.pull_movies()

    def pull_theater_title(self):
        """Return the title of the theater from the theater_info string."""

        # Split the theater string between '>' and
        # '</a>' where the title is located.
        title = self.theater_info.split('</a>', 1)[0].split('>', 1)[1].strip()
        return title

    def pull_movies(self):
        """Return a list of Movie objects, one for each movie at the theater."""

        # Split the theater_info list by movie.
        movie_info = self.theater_info.split('showtimes-movie-container')[1:]
        movies = [Movie(info) for info in movie_info]

        return movies


class Movie(object):
    """Holds information for a movie, including its title and showtimes.

    Attributes:
        movie_info (str) -- Raw html that contains all information about the
                            movie.
        title (str) -- The title of the movie.
        showtimes (list) -- A list of strings giving showtimes for the movie.
    """

    def __init__(self, movie_info):
        self.movie_info = movie_info
        self.title = self.pull_movie_title()
        self.showtimes = self.pull_showtimes()

    def pull_movie_title(self):
        """Return the title of the movie from the movie_info string."""

        # Split each move_list to get movie titles, if there are movies playing.
        if 'there are no movies' not in self.movie_info:
            leading_chars = self.movie_info.split('showtimes and tickets', 1)[0]
            title = leading_chars.split('alt="', 1)[1].strip()
            return title
        else:
            return "There are no movies playing at this theater."

    def pull_showtimes(self):
        """Return a list of showtimes for this movie."""

        # Split the movie_info by info on the showtimes.
        showtimes_info = self.movie_info.split('</time>')[:-1]

        # Pull the actual showtimes from the html.
        if 'there are no movies' not in self.movie_info:
            showtimes = [showtime[-6:] if showtime[-7] == '>'
                         else showtime[-7:]
                         for showtime in showtimes_info]
            return showtimes
        else:
            return ["There are no showtimes for this theater."]


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

        # Only create city string if there is at least a city and state entered.
        if len(location_list) >= 2:
            city = '+'.join(location_list[:len(location_list) - 1])
            break
        else:
            print ("\nIncorrect format. Please check that you entered the "
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


def present_showtimes(theaters):
    """Present the theaters, movies, and showtimes, in a formatted manner.

    Args:
        theaters (list) -- Contains a theater object for each theater that is
                           playing movies.
    """

    for theater in theaters:
        print '\nTheater: ' + theater.title

        for movie in theater.movies:
            print '  Movie: ' + movie.title

            for showtime in movie.showtimes:
                print '         ' + showtime

            print ''


def run_showtimes_finder():
    """Run the showtimes_finder program."""

    present_instructions()
    response = ''
    html = ''

    while True:
        response = process_input()  # Get the proper URL based upon user input.
        html = response.read()      # Read information from the URL

        # If the html is valid, then program execution can continue.
        if html.find("This location can't be found.") == -1:
            break
        else:
            print("\nThe location you entered cannot be found. Please check that "
                  "your location was spelled correctly and entered in the correct "
                  "format")

    # Split html such that each piece has information for one theater only.
    theater_info = html.split('showtimes-theater-title')[1:]

    # Create a list of theaters from the information in the html.
    theaters = [Theater(info) for info in theater_info]

    present_showtimes(theaters)

    response.close()        #close the urllib2 connection file

if __name__ == "__main__":
    run_showtimes_finder()
