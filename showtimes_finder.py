"""
    * Program Name: Showtime Finder
    * Created Date: October 26, 2014
    * Created By: William Grenard
    * Purpose: This program is designed to query the web to find showtimes of movie theaters in the Berkeley area
    * Acknowledgements:
    """

import urllib2
import time

def present_instructions():
    """
    *Input(s): This function takes no input
        
    *Output(s): This function returns nothing
        
    *Purpose: The purpose of this function is simply to print instructions to the user that explain how to use the program.
        
    """

    print("\n\nWelcome to the movie showtimes generator!")
    print("Please enter the city and state where you wish to find movie times.")
    print("Then enter the date which you are interested in.")
    print("The movie showtimes generator will then return all theaters and showtimes in your area.")



def process_input():
    """
        *Input(s): This function takes no input
        
        *Output(s): This function returns the urllib2 object that contains information from the url queried
        
        *Purpose: The purpose of this function is to accept and record the location and date over which to search for showtimes, and to query fandango accordingly

    """
    
    #gather the city and state information. If the user doesn't input enough information i.e. at least two words, then tell them there is an error and ask for input again. This does not ensure that the user will not enter an invalid city and state, but it will prevent an error that will cause the program to crash if there is not enough information. Other incorrect input such as misspelling is handled in __main__ when the html is parsed.
    while True:
        location = raw_input("\n\nPlease enter your location in the following format: City St. e.g. Berkeley CA: ")       #accept the location from the user
    
        location_list = location.split()                            #split the location entered and place each word into an element of a list
    
        #only split the input and create the 'city' string if there is at least a city and state entered
        if len(location_list) >= 2:
            city = '+'.join(location_list[:len(location_list) - 1])     #join all elements except for the last (which is the state abbreviation) with a plus sign. This string goes into the url as the city
            break

        #if there was not at least a city and state entered, then inform the user and ask again
        else:
            print("\nIncorrect format. Please check that you entered the location in City ST format and that you included both a city and a state.")

    #gather date information. If the user doesn't input the proper length string as specified by the requested format, then inform them and ask again. Also, if the date entered is before today's date, inform them and ask for the information again.
    while True:
        date = raw_input("\n\nPlease enter the date you wish to see the movie in the following format mm/dd/yyyy: ")      #accept the date from the user
        date_list = date.split("/")
    
        #only create the url with the location and date if the input date is the correct length
        if len(date) == 10:
            
            #if the current date is before the date entered, then the format is acceptable. Create the url string
            if time.strftime("%m/%d/%Y") <= date and time.strftime("%Y") <= date_list[2]:
            
                url = 'http://www.fandango.com/%s_+%s_movietimes?date=%s' % (city.lower(), location_list[len(location_list) - 1].lower(), date) #construct the url of the proper form to search the site
                break
            
            #otherwise, the date needs to be entered again
            else:
                print("\nThe date you entered is outside of allowed range. Please check the date you entered is today's date or later.")

        #if the date is not the correct length then ask for a new date
        else:
            print("Incorrect format. Please check that you entered the date in proper mm/dd/yyyy format")

    return urllib2.urlopen(url)  #return the information from the url



def find_indicies_of(str, search_str):
    """
    *Input(s): This function takes a string to be searched for, and a string to search through
        
    *Output(s): This function returns a list containing all the indicies in witch str occurs in search_str
        
    *Purpose: The purpose of this function is to find all occurrences of a certain string inside the search string, and to return the indicies at which said string is at.
        
    """

    indicies = [] #list to hold indicies of str
    str_len = len(str) #stores the length of the string we are searching for
    i = 0         #variable to count through iterations
    
    while True:

        index = search_str.find(str, i)  #search for the input string starting at index i

        #if the string is not found, then all of the occurences have been added to the list, so exit the loop immediately
        if index == -1:
            break

        #otherwise append the current index at which the string was found to the indicies list. Then set the count 'i' to begin at the index just after the first occurrence
        else:
            indicies.append(index)
            i = (index + str_len)

    return indicies  #return the list of indicies


def split_at_string(trigger_str, str_to_split):
    """
        *Input(s): This function takes a string to split at , and the string upon which splitting will be done
        
        *Output(s): This function returns a list containing partitioned strings, split at every occurrence of the specified string
        
        *Purpose: The purpose of this function is to split a larger string into pieces. The location of each split is determined to be at the index specified by a string input by the user. E.g. split_at_string('b','abcdeabcde') returns ['bcdea', 'bcde']
        
    """

    indicies = find_indicies_of(trigger_str, str_to_split) #determine the indicies of the string at which splitting will occur
    sub_strings = []                                       #list to hold split strings

    #loop through the list of indicies
    for index in range( len(indicies) ):

        #once the last entry of the indicies list has been reached,the string should be split from that index to the end of the string
        if index == len(indicies) - 1:
            sub_strings.append( str_to_split[indicies[index]:] )

        #otherwise, the string should be split from the first index to the next index
        else:
            sub_strings.append( str_to_split[indicies[index]:indicies[index + 1]] )

    return sub_strings  #return the list of split strings


def pull_theater_titles():
    """
        *Input(s): This function takes no input.
        
        *Output(s): This function returns a list whose elements are the titles of all theaters found
        
        *Purpose: The purpose of this function is to take the html info from the theaters list, extract all of the theater titles, and return a list of these titles
        
    """
    
    title_list = []     #list to hold theater titles

    #loop through each element in the theaters list
    for index in range(len(theaters)):
        
        if theaters[index].find('there are no movies') == -1:         #if the string 'there are no movies' is not found, then there are showtimes to be displayed for that theater
            terminating_index = theaters[index].find('</a>')          #for any given element in theaters, find the index that </a> appears at
            temp_list = theaters[index][:terminating_index].split()   #create a temporary list that runs from the beginning of the string to the </a> not inclusive
            title_str = ' '.join(temp_list[2:])                       #join the elements of the temporary list minus the first two elements, leaving only the theater title
            title_list.append(title_str)                              #append the title to the title_list

    return title_list                                                 #retrun the title list


def pull_movie_titles():
    """
        *Input(s): This function takes no input.
        
        *Output(s): This function returns a list whose elements are the titles of all of the movies at all theaters
        
        *Purpose: The purpose of this function is to iterate through the movies list and for each element pull the titles for all of the movies. The function then returns a list of lists. The inner lists are filled with the movie titles. Each list element represents movies at a different theater.
    """
    
    title_list = []     #list to hold all movie titles from all theaters
    inner_list = []     #list to temporarily hold movie titles from one single theater

    #outer loop goes through the movies list, and inner loop goes through the strings of each element in the movies list
    for i in range(len(movies)):
        for j in range(len(movies[i])):
            
            if movies[i][j].find('there are no movies') == -1:                          #if there are movies to display, then add them to the list
                starting_index = movies[i][j].find('alt') + 5                           #for any given string inside a movies list element, the title starts 5 chars after 'alt'
                terminating_index = movies[i][j].find('showtimes and tickets')          #and the title ends just before 'showtimes and tickets'
                temp_list = movies[i][j][starting_index:terminating_index].split()      #split the string containing the title to remove whitespace
                title_str = ' '.join(temp_list)                                         #join the title into a string again
                inner_list.append(title_str)                                      #append this title string to inner_list to be stored until all titles for this movies element are found

        if len(inner_list) > 0:                                        #only append the title's to the list if the inner list is non-empty
            title_list.append(inner_list)                              #after obtaining all movies within a specific movie element, append the list of their titles to the title list

        inner_list = []                                            #reset the inner list for the next iteration

    return title_list                                                      #return the title list after the entire loop is complete


def determine_showtimes(search_str):
    """
    *Input(s): This function takes a string as an input.
        
    *Output(s): This function returns a list whose elements are the showtimes found in the input string
        
    *Purpose: The purpose of this function is to search the string passed to it and find all showtimes in this string as entries of a list. It then returns this new list. Note that for this function to work it must be passed a string from an element of the movies[] list
    
    """
    
    showtimes_list = []     #list to hold the showtimes
    search_index = 0        #number to keep track of the index at which the search will start

    while True:
        terminating_index = search_str.find('</time>', search_index)        #the terminating index, directly after the time is the index where </time> is found

        if terminating_index == -1:                                         #if </time> is not found, then all instances of this string have already been found, so break from the loop
            break

        if search_str[terminating_index - 7] != '>':                                               #if a '>' doesn't exist here, then this is the index where the time starts
            showtimes_list.append( search_str[terminating_index - 7: terminating_index] )          #slice the string where the time is found and append it to the showtimes list

        else:                                                                                      #if '>' is not there, then the time begins 6 chars before terminating index
            showtimes_list.append( search_str[terminating_index - 6: terminating_index] )          #slice the string where the time is found and append it to the showtimes list

        search_index = terminating_index + 1                                                       #since </time> has been found, increase the search_index, so the same one won't be found again

    return showtimes_list


def present_showtimes():
    """
        *Input(s): This function takes no inputs
        
        *Output(s): This function returns nothing
        
        *Purpose: The purpose of this function is to iterate through all information already found about the theater titles and movie titles and display this information in a formatted manner. For each movie, it also calls the determine_showtimes() function, and displays the showtimes it finds
        
    """
    
    theater_titles = pull_theater_titles()                  #retrieve the list of theater titles
    movie_titles = pull_movie_titles()                      #retrieve the list of movie titles

    #loop through each entry in the theater_titles list
    for i in range( len(theater_titles) ):
        print( '\nTheater: ' + theater_titles[i] + '\n')    #Before each entry title the line as "Theaters: " and then print the theater name

        for j in range( len(movie_titles[i]) ):             #each element of movie titles corresponds to the i'th theater title
            print('  Movie: ' + movie_titles[i][j])         #Before each movie title the line as "Movie: " and then present the movie name

            showtimes = determine_showtimes(movies[i][j])   #For each movie name use determine_showtimes() to find all of its showtimes
            for time in showtimes:                          #Iterate through the newly created list of showtimes and print them all
                print('         ' + time)

            print('')                                       #Print an extra line for formatting purposes


def is_url_valid():
    """
        *Input(s): This function takes no inputs
        
        *Output(s): This function returns a boolean value. False means that the url was not found
        
        *Purpose: The purpose of this function is to search the html for the string that indicates a nonexistant city/state has been entered.
        
    """
    
    return html.find("This location can't be found.") == -1


"""
    __main__
"""

present_instructions()          #present instructions to the user
response = ''
html = ''

#after the information is gathered, search the returned html to determine if the page of movie showtimes was actually found. If it was, then break from the loop. Else, take the input again
while True:
    response = process_input()      #take the user's input and retrieve the needed url based off of this input
    html = response.read()          #read the information from the url

    #if the url is valid then continue on in the program. Else continue looping
    if is_url_valid():
        break
    else:
        print("/nThe location you entered cannot be found. Please check that your location was spelled correctly and entered in the correct format")



theaters = split_at_string('showtimes-theater-title', html)  #split the html into a list of strings each containing information on 1 theater.
movies = []                                                  #list to hold information of each movie


#loop through the theater strings and split each string by movie. Each string in theaters will turn into a list in movies, which itself contains string elements.
#E.g. if theaters = ['At Berkeley 7 Showing John Wick at 7:40 and Showing Nightcrawler at 9:20', 'At Shattuck Cinemas showing Interstellar at 10:20 and showing Saw at 9:30']
#then movies = [['John Wick at 7:40', 'Nightcrawler at 9:20'], ['Interstellar at 10:20', 'Saw at 9:30']]
for theater in theaters:
    movies.append( split_at_string('showtimes-movie-container', theater) )

present_showtimes()     #present the theaters, movies, and showtimes in an organized manner


response.close()        #close the urllib2 connection file

"""
    end_of__main__
"""





