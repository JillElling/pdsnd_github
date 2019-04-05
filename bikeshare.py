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
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city =(input('\nWould you like to get data for Chicago, New York City, or Washington? \n')).lower()
        if (city in ['chicago', 'new york city', 'washington']):
            break
        else:
            print('\nPlease enter Chicago, New York City, or Washington!\n')
            continue

    # Get user input for month (all, january, february, ... , june)

    while True:
        month = input('\nIf you want to receive data on a specific month (January - June) type the month otherwise type all:\n').lower()
        if (month in ['january','february','march','april','may','june','all']):
            break
        else:
            print('\nPlease enter: all, january, february, march, april, may, or june!\n')
            continue

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nOn which day of the week would you like to receive data:\n').lower()
        if (day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday', 'all']):
            break
        else:
            print('Please enter: all, monday, tuesday, wednesday, thursday, friday, saturday or sunday!')
            continue



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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df
    #print(df)

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    # Used info from https://stackoverflow.com/questions/1349332/python-passing-a-function-into-another-function
    # to get access from a variable of a function and access it in another function / pass it to another function

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Check which filter is applicable and which statistics need to be presented
    most_common_month = df['month'].value_counts().index[0]
    most_common_day = df['day_of_week'].mode()[0]

    if day != 'all' and month != 'all':
        # Display the filter-option chosen
        print('\nYou chose to filter by month', month.title(), 'and day', day.title(), ':\n')
    elif month == 'all' and day != 'all':
        # Display the filter-option chosen and the most common month
        print('\nYou chose to get data for the day:', day.title(),' - for ALL of the first six month of 2017:\n')
        print('\nThe most common month of travel for your chosen day is: ', most_common_month)
        print('With a count of: ', df['month'].value_counts()[most_common_month])
    elif day == 'all' and month != 'all':
        # Display the filter-option chosen and the most common day of the week
        print('\nYou chose to filter by month =', month.title(), ' - and receive data for ALL days of the week:\n')
        print('\nThe most common weekday of travel: ', most_common_day )
        print('With a count of: ', df['day_of_week'].value_counts()[most_common_day])
    else:
        print('\nThe most common month of travel in the first six month of 2017 is: ', most_common_month)
        print('With a count of: ', df['month'].value_counts()[most_common_month])
        print('\nThe most common weekday of travel in the first six month of 2017: ', most_common_day )
        print('With a count of: ', df['day_of_week'].value_counts()[most_common_day])

    # extract hour from Start Time to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # Display the most common start hour for all filter-option
    most_common_hour = df['hour'].mode()[0]
    print('\nThe most common start hour for travel is: ',  most_common_hour)
    print('with a count of: ', df['hour'].value_counts()[most_common_hour], 'in your chosen timeframe')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_popular_start_station = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station in {} is: {}'.format(city.title(), most_popular_start_station))
    print('with a count of: ',  df['Start Station'].value_counts()[most_popular_start_station])


    # Display most commonly used end station
    most_popular_end_station = df['End Station'].mode()[0]
    print('\nThe most commonly used end station in {} is: {}'.format(city.title(), most_popular_end_station))
    print('with a count of: ',  df['End Station'].value_counts()[most_popular_end_station])


    # Display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' - ' + df['End Station']
    most_frequent_trip = df['trip'].value_counts().index[0]
    print('\nThe most frequent combination of start / end station in {} is {}.'.format(city.title(), most_frequent_trip))
    print('with a count of: ', df['trip'].value_counts()[most_frequent_trip])
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculating the total travel time and average travel time in seconds
    total_seconds = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()


    def readable_timedelta(total_seconds):
        """Displays the total travel time in a readable time format."""
        # looked for further info here: https://docs.python.org/2/library/datetime.html
        # and used code from source: https://www.python-  forum.de/viewtopic.php?t=18266
        WEEK = 60 * 60 * 24 * 7
        DAY = 60 * 60 * 24
        HOUR = 60 * 60
        MINUTE = 60
        weeks = total_seconds // WEEK
        remainer = total_seconds % WEEK
        days = remainer // DAY
        remainer = total_seconds % DAY
        hours = remainer // HOUR
        remainer = total_seconds % HOUR
        minutes = remainer // MINUTE
        seconds = remainer % MINUTE
        return 'The total travel time is {} day(s) {} hour(s), {} minute(s), and {} second(s)'.format(int(days), int(hours), int(minutes), int(seconds))

    print(readable_timedelta(total_seconds))


    # Display mean travel time
    def traveltime_timedelta(mean_travel_time):
        """Displays the total travel time in a readable time format."""
        MINUTE = 60
        minutes = mean_travel_time // MINUTE
        seconds = mean_travel_time % MINUTE
        return '\nThe mean travel time is {} minute(s), and {} second(s)\n'.format(int(minutes), int(seconds))
    print(traveltime_timedelta(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    if city == 'chicago' or city == 'new york city':
        user_types = df['User Type'].value_counts()
        print('\nThis is the breakdown for users:\n',user_types)
    else:
        print('\nUnfortunately, there is no infomration available on user types for Whashington.\n')


    # Display counts of gender
    if city == 'chicago' or city == 'new york city':
        gender_count = df['Gender'].value_counts()
        print('\nThis is the breakdown for gender:\n',gender_count)
    else:
        print('\nUnfortunately, there is no infomration available on gender for Whashington.\n')


    # Display earliest, most recent, and most common year of birth
    if city == 'chicago' or city == 'new york city':
        earliest_birth_year = df['Birth Year'].min()
        print('\nThe ealiest year of birth for bikeshare users is: ', int(earliest_birth_year))
        recent_birth_year = df['Birth Year'].max()
        print('\nThe most recent year of birth for bikeshare users is: ', int(recent_birth_year))
        most_common_birth_year = df['Birth Year'].value_counts().index[0]
        print('\nThe most common year of birth for bikeshare users is: ', int(most_common_birth_year))
    else:
        print('\nUnfortunately, there is no data available on the birth year of users in Whashington.\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    # Display how many rows are in the selected data set
    rows = (len(df))
    print('\nThe raw data of your chosen timeframe has {} lines.\n'.format(rows))
    row_count = 5
    # raw_data = to be defined by user input
    raw_data = 'tbd'

    # for loop to get user input whether they want to see the first / next five lines of raw data for their chosen timeframe
    for rows in range (0, rows):
        # if user input is yes, display raw data for NEXT 5 lines (for the first prompt, see below)
        if raw_data.lower() == 'yes':
            raw_data = input('\nWould you like to see the next 5 lines of raw data with your chosen filter? Enter yes or no.\n')
            print('These are the next 5 lines of raw data')
            print(df.iloc[(row_count - 5):row_count,])
            row_count += 5
        # prompt user for the first time, if they want to see the FIRST 5 lines of raw later
        elif raw_data == 'tbd':
            raw_data = input('\nWould you like to see first {} lines of raw data with your chosen filter? Enter yes or no.\n'.format(row_count))
            print('These are the first 5 lines of raw data')
            print(df.iloc[(row_count - 5):row_count,])
            row_count += 5
        # end the loop, if user input is 'no' or any other input than 'yes'
        elif raw_data.lower() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df, city)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
