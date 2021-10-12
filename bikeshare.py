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
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    time_fil_options = ['month', 'day', 'all']
    month = 'all'
    day = 'all'

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington)
    city = input('Would you like to see data for Chicago, New York City, or Washington?').lower()
    while city not in (CITY_DATA.keys()):
        print('-'*40)
        print('You entered an invalid city name! Please select a city name from the list.')
        city = input('Would you like to see data for Chicago, New York City, or Washington?').lower()

    # get user input for timeframe to filter the data
    time_filter = input('Would you like to filter the data by month, day, or view all? To view all type "all" ').lower()
    while time_filter not in time_fil_options:
        print('-'*40)
        print('You entered an invalid filter! Please select a valid filter from the list.')
        time_filter = input('Would you like to filter the data by month, day, or view all? To view all type "all" ').lower()

    # get user input for month (all, january, february, ... , june)
    if time_filter == 'month':
        month = input('Which month - January, February, March, April, May, or June? Please type out the month in full.').lower()
        while month not in months:
            print('-'*40)
            print('You entered a month not included the dataset! Please select a month from the list.')
            month = input('Which month - January, February, March, April, May, or June? Please type out the month in full.').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif time_filter == 'day':
        day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?').lower()
        while day not in days:
            print('-'*40)
            print('You entered an invalid day of the week! Please select a a valid day from the list')
            day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?').lower()

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
    # Load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    hours = ['12am', '1am', '2am', '3am', '4am', '5am', '6am', '7am', '8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm']

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print('Most common month: {}'.format(months[common_month-1].title()))

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of the week: {}'.format(days[common_day].title()))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common hour: {}'.format(hours[common_hour]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip Combinations...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    css_count = df['Start Station'].str.count(common_start_station).sum()

    print('Most common start station: {}, Count: {}'.format(common_start_station, css_count))

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    ces_count = df['End Station'].str.count(common_end_station).sum()
    print('Most common end station: {}, Count: {}'.format(common_end_station, ces_count))

    # display most frequent combination of start station and end station trip
    df['Start & End Station'] = df['Start Station'] + ' --> ' + df['End Station']
    common_journey = df['Start & End Station'].mode()[0]
    cj_count = df['Start & End Station'].str.count(common_journey).sum()
    print('Most common trip taken: {}, Count: {}'.format(common_journey, cj_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Trip Duration: {} seconds'.format(total_travel_time))

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('Average Trip Duration: {} seconds'.format(round(avg_travel_time, 2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Distribution')
    user_count = df['User Type'].value_counts()
    print(user_count)

    # Bypass for missing columns in the Washington dataset
    if city != 'washington':

        # Display counts of gender
        print('\nGender Distribution')
        gender_count = df['Gender'].value_counts()
        print(gender_count)

        # Display earliest, most recent, and most common year of birth
        min_birth_year = int(df['Birth Year'].min())
        max_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        year = 2021
        print('\nAge Distribution')
        print('Oldest birth year: {}, Age: {} years'.format(min_birth_year, year-min_birth_year))
        print('Youngest birth year: {}, Age: {} years'.format(max_birth_year, year-max_birth_year))
        print('Most common birth year: {}, Age: {} years'.format(common_birth_year, year-common_birth_year))
    else:
        print('\nGender Distribution')
        print('No data available to display')
        print('\nAge Distribution')
        print('No data available to display')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    """Loads raw data based on user input and prints to console 5 rows at a time.
    Args:
        (DataFrame) df - name of the Pandas dataframe filtered by all, month or day
    Returns:
        Pandas dataframe 5 rows at a time printed to console
    """
    show_raw_data = input('\nWould you like to see raw data? Enter yes or no.\n').lower()
    # Validate User input for seeing raw data
    while show_raw_data not in (['yes', 'no']):
        print('-'*40)
        print('You entered an invalid response! Please enter yes or no.')
        show_raw_data = input('\nWould you like to see raw data? Enter yes or no.\n').lower()
    # Generate rows of raw data 5 at a time till end of dataset
    if show_raw_data == 'yes':
        rows = df.shape[0]
        x, y = 0, 5
    while show_raw_data == 'yes' and y < rows:
        data_snip = df.iloc[x:y]
        print('.'*70)
        print('Showing rows {} to {}'.format(x+1, y))
        print('\n', data_snip)
        show_raw_data = input('\nWould you like to see more raw data? Enter yes or no.\n').lower()
        # Validate User input for seeing extra raw data
        while show_raw_data not in (['yes', 'no']):
            print('-'*40)
            print('You entered an invalid response! Please enter yes or no.')
            show_raw_data = input('\nWould you like to see raw data? Enter yes or no.\n').lower()
        if show_raw_data == 'yes' and (y +5 <= rows):
            x += 5
            y += 5
        elif (y + 5 > rows):
            x += rows - y
            y += rows -y
            print('.'*70)
            print('Showing rows {} to end'.format(x+1))
            print('\n', data_snip)
            break
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        print('Showing Stastistics for {}.'.format(city.title()))

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_data(df)

        # Validate user input for exiting the program loop
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        while restart not in (['yes', 'no']):
            print('-'*40)
            print('You entered an invalid response! Please enter yes or no.')
            restart = input('\nWould you like to restart? Enter yes or no.\n')

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
