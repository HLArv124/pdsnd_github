import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
        city_options = ['Chicago','New York City','Washington']
        month_options = ['January','February','March','April','May','June','All']
        day_options = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']
        
        try:    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
            city = city_options.index(input("Enter the name of the city of interest (Chicago, New York City or Washington): ").lower().title())

    # get user input for month (all, january, february, ... , june)
            month = month_options.index(input("Enter the name of the month you are interested in (January - August) or type 'All' if you do not want to focus a specific month: ").lower().title())

    # get user input for day of week (all, monday, tuesday, ... sunday)
            day = day_options.index(input("Enter the weekday you are interested in or type 'All' if you do not want to focus a specific day: ").lower().title())

        except ValueError:
            print("\n Your provided input is not available.\n Please start from the beginning again and refer to suggested input.")
    
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df["Start Time"].dt.month
    df['day_of_week'] = df["Start Time"].dt.strftime("%A")
    df['hour_of_day'] = df["Start Time"].dt.hour
        # In this example, we create a datetime object for January 1, 2022, and then use the .strftime() method to extract the name of the weekday as a string. 
        # The %A format code is used to specify that we want the full name of the weekday (e.g., "Saturday").
    
    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df["month"] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df["day_of_week"] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df["month"].mode()[0]
    print("The most common month is", most_common_month)

    # display the most common day of week
    most_common_day_of_week = df["day_of_week"].mode()[0]
    print("The most common day of week is", most_common_day_of_week)

    # display the most common start hour
    most_common_hour_of_day = df["hour_of_day"].mode()[0]
    print("The most common hour of day is", most_common_hour_of_day)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df["Start Station"].mode()[0]
    print("The most common Start Station is", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df["End Station"].mode()[0]
    print("The most common End Station is", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_combination = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print("The most common Start-End-Station combination:", most_common_start_end_combination[0], "and", most_common_start_end_combination[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df["Trip Duration"].sum() / 60 / 60)
    print("The total duration of all trips is" ,round(total_travel_time, 0), "Hours")
    
    # display mean travel time
    average_travel_time = df["Trip Duration"].mean()/60
    print("The average travel time per trip is", round(average_travel_time, 0), "Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df["User Type"].value_counts().to_string()
    print("Find here the user types and amounts: \n", count_user_type)

    # Display counts of gender
    while True:
        try:
            count_gender = df["Gender"].value_counts().to_string()
            print("\nFind here the gender information and amounts: \n", count_gender)
        except KeyError:
            print("\nWe are sorry, but there is no data for gender existing in the chosen dataset.")
        break

    # Display earliest, most recent, and most common year of birth
   while True:
        try:
            earliest_birthyear = df["Birth Year"].min()
            print("\nThe earliest Year of Birth is ", earliest_birthyear)
        except KeyError:
            print("\nWe are sorry, but there is no column with age information existing in the chosen dataset")
        break
    
    while True:
        try:
            latest_birthyear = df["Birth Year"].max()
            print("\nThe latest Year of Birth is ", latest_birthyear)
        except KeyError:
            print("\nWe are sorry, but there is no column with age information existing in the chosen dataset")
        break
    
    while True:
        try:
            most_common_birthyear = df["Birth Year"].mode()[0]
            print("\nThe most common Year of Birth is: ", most_common_birthyear)
        except KeyError:
            print("\nWe are sorry, but there is no column with age information existing in the chosen dataset existing")
        break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def get_raw_data(df):
    """
    displays the first five rows of raw data and adds another five rows of raw data every time the user inputs "yes".

    Args:
        There is only a pandas DataFrame necessary that it provided by the load_data function.
    
    Returns:
        df - Raw data depending on the number of rows defined before.       
    """   
    print("The first five rows of the chosen data are shown:\n", df.head())

    number_rows = 5
    raw_data_wanted = "Yes"
    # probably set up a list with "Yes" and "No" as necessary input to avoid misspelling of the user.

    while raw_data_wanted == "Yes":
        raw_data_wanted = input("Do you want to see five more rows of raw data? Enter 'Yes' if you want to see more data. Otherwise enter 'No'").lower().title()
        if raw_data_wanted == "Yes":
            number_rows += 5
            print("\nCurrently ", number_rows, "rows of raw data are presented.\n", df.head(number_rows))
        else:
            print("\nNo further data is wanted and displayed.")

    return df.head(number_rows)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        get_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
