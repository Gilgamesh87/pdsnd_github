import time
import pandas as pd
import numpy as np

# Create dictionary containing city name and associated filename
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# Create list for the month abbrevations for user selection
MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'all']

# Create list for the weekdays for user selection
WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',
            'sunday', 'all']

# Create variable to count lines read in the file and to allow the file lines
# to be sliced if the user wants to continue seeing the raw data
LINES = 0


def choice(line, input_type, df):
    """Handles user input"""

    while True:
        response = input(line).lower()
        if input_type == 'city':
            if response in CITY_DATA:
                break
            else:
                print('No city data....\n')
        elif input_type == 'month':
            if response not in MONTHS:
                print('Enter a valid month, January - June.\n')
            else:
                break
        elif input_type == 'day':
            if response in WEEKDAYS:
                break
            else:
                print('Enter a valid weekday i.e. Monday or Friday\n')
        elif input_type == 'yn':
            if response == 'y' or response == 'yes':
                print(df.head())
                global LINES
                LINES += 5
                break
            elif response == 'n' or response == 'no':
                print('Skipping Raw Data!')
                break
        elif input_type == 'more':
            while response == 'y' or response == 'yes':
                print(df[LINES:LINES+5])
                LINES += 5
                response = input('View more?\n')
            print('Completed viewing the raw data!')
            break
    return response


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
        month filter
        (str) day - name of the day of week to filter by, or "all" to apply
        no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
# get user input for city (chicago, new york city, washington).
# HINT: Use a while loop to handle invalid inputs
    city = choice("Would you like to view New York City, Chicago or "
                  "Washington's data?\n", 'city', '')
# get user input for month (all, january, february, ... , june)
    month = choice("Do you want to view all (enter 'all') or a specific "
                   "month's data? (Enter Jan, Mar, Jun etc)\n", 'month', '')
# get user input for day of week (all, monday, tuesday, ... sunday)
    day = choice("Which day would you like view (Monday, Tuesday, ... "
                 "Sunday) or all (enter 'all') data available?\n", 'day', '')
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if
    applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
                      month filter
        (str) day - name of the day of week to filter by, or "all" to apply
                    no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # concatenate Start Station and End Station and create a new column
    df['journey'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    df['count'] = 1
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    m_month = df['month'].mode()[0]
    c_month = df.groupby(['month'])['count'].sum().max()
    print('\nMost common month is, {}. With {} rides.\n'.format(
          MONTHS[m_month-1].title(), c_month))
    # display the most common day of week
    m_day = df['day_of_week'].mode()[0]
    c_day = df.groupby(['day_of_week'])['count'].sum().max()
    print('\nMost common day of the week is, {}. With {} rides\n'.format(
          m_day, c_day))
    # display the most common start hour
    m_hour = df['hour'].mode()[0]
    c_hour = df.groupby(['hour'])['count'].sum().max()
    print('\nMost common start hour is, {}00hrs. With {} rides.'.format(
          m_hour, c_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    m_start = df['Start Station'].mode()[0]
    c_start = df.groupby(['Start Station'])['count'].sum().max()
    print('\nMost commonly used start station is, {}. Used {} times.'.format(
          m_start, c_start))

    # display most commonly used end station
    m_end = df['End Station'].mode()[0]
    c_end = df.groupby(['End Station'])['count'].sum().max()
    print('\nMost commonly used end station is, {}. Used {} times.'.format(
          m_end, c_end))

    # display most frequent combination of start station and end station trip
    m_trip = df['journey'].mode()[0]
    c_trip = df.groupby(['journey'])['count'].sum().max()
    print('\nMost common trip is, {}. Travelled {} times.'.format(
          m_trip, c_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    secs = total_time % 60
    mins = total_time / 60 % 60
    hrs = total_time / 3600 % 24
    days = total_time // 86400
    print('\nTotal travel time was: {}days {}hrs {}min {}sec'.format(int(days),
          int(hrs), int(mins), int(secs)))

    # display mean travel time
    print('\nThe average travel time is {}min'.format(df['Trip Duration']
          .mean() / 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nBreakdown of the user types:\n', user_types)

    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('User genders are:\n', gender)
    except KeyError:
        print('There is no gender data available for this city.')
    # Display earliest, most recent, and most common year of birth
    try:
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])
        print('\nThe oldest birth year is, {}\nThe most recent birth year is, '
              '{}\nThe most common year of birth is, {}'
              .format(oldest, youngest, common))
    except KeyError:
        print('There is no birth details available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        df = 0
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        response = choice('Would you like to view the raw data? '
                          '(yes/no or y/n)\n', 'yn', df)
        print(response)
        if response == 'y' or response == 'yes':
            response = choice('Show more data?\n', 'more', df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')

        if restart.lower() != 'yes':
            break
        else:
            main()


if __name__ == "__main__":
    main()
