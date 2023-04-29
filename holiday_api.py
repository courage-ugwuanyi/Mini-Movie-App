import requests
from datetime import datetime

YEAR = '2022'
THREE_MONTHS = 3
LAST_MONTH = 12
SEPTEMBER = 9
API_KEY = '5d35de9a-6d5f-420b-8af1-c905f49804e4'
REQUEST_URL_COUNTRIES = 'https://holidayapi.com/v1/countries?pretty&key='
REQUEST_URL_HOLIDAYS = 'https://holidayapi.com/v1/holidays?pretty&'


def get_user_input() -> tuple:
    """PROMPTS USER FOR INPUT, REMOVES LEADING AND TRAILING SPACES AND RETURNS USER
    INPUT AS A TUPLE """
    country = input('Enter a country: \n').strip()
    month = input('Enter preferred month (e.g July): \n').strip()
    return country, month


def get_all_countries() -> list[dict]:
    """PERFORMS API REQUEST TO HOLIDAYAPI AND RETURNS ALL COUNTRIES"""
    url = REQUEST_URL_COUNTRIES + API_KEY
    res = requests.get(url)
    return res.json()['countries']


def display_country_names():
    """CALLS THE GET ALL COUNTRIES FUNCTION AND DISPLAYS ALL COUNTRIES"""
    all_countries = get_all_countries()
    print('Available countries: \n')
    for country in all_countries:
        print(country['name'])
    print('\nGet upcoming 3 months holidays for a country from a specified month in '
          '2022:')


def get_country_code(country: str) -> str or None:
    """GETS COUNTRY NAME; CALLS THE GET_ALL_COUNTRIES FUNCTION AND RETURNS COUNTRY CODE"""
    all_countries = get_all_countries()
    for countries in all_countries:
        if country.lower() == countries['name'].lower():
            return countries['code']
        continue
    return None


def get_holidays(country: str) -> list[dict]:
    """GETS COUNTRY NAME; CALLS THE GET_COUNTRY_CODE FUNCTION AND RETURNS HOLIDAYS AS
    LIST OF DICTIONARIES FOR THE COUNTRY NAME """
    country_code = get_country_code(country)
    if country_code:
        param = f"country={country_code}&year={YEAR}&key={API_KEY}"
        url = REQUEST_URL_HOLIDAYS + param
        return requests.get(url).json()['holidays']


def display_holidays(country: str, month: str):
    """GETS COUNTRY NAME AND MONTH. CALLS THE GET_HOLIDAYS FUNCTION AND DISPLAYS
    HOLIDAY NAMES AND THEIR DATES"""
    country_holidays = get_holidays(country)
    date_string = f"{month} {YEAR}"
    try:
        # CONVERTS DATE FROM TEXTUAL TO NUMERIC FORMAT IF FULL MONTH NAME IS GIVEN
        holiday_date = datetime.strptime(date_string, '%B %Y').date()
    except ValueError:
        # CONVERTS DATE FROM TEXTUAL TO NUMERIC FORMAT IF MONTH NAME IS ABBREVIATED
        holiday_date = datetime.strptime(date_string, '%b %Y').date()
    holiday_month = int(holiday_date.month)

    if SEPTEMBER < holiday_month < LAST_MONTH:
        print(f'list of holidays in {country.capitalize()} in the next '
              f'{LAST_MONTH - holiday_month} month(s) from {month}: \n')
    elif holiday_month == LAST_MONTH:
        print(f'list of holidays in {country.capitalize()} in {month}: \n')
    else:
        print(f'list of holidays in {country.capitalize()} in the next 3 months from'
              f' {month}: \n')

    for country_holiday in country_holidays:
        holiday_month_searched = int(country_holiday['date'].split('-')[1])
        if holiday_month <= holiday_month_searched < (holiday_month + THREE_MONTHS):
            date_searched = datetime.strptime(country_holiday['date'], '%Y-%m-%d')
            print(f"{country_holiday['name']} ({date_searched.strftime('%A %B %d')})")
        else:
            # BREAK ONCE IT HAS DISPLAYED MESSAGE FOR THE SPECIFIED PERIOD OF MONTHS
            if holiday_month_searched >= (holiday_month + THREE_MONTHS):
                break
            continue


def main():
    """CALLS THE MAIN FUNCTION"""
    display_country_names()
    user_input = get_user_input()
    country, month = user_input
    try:
        display_holidays(country, month)
    except TypeError:
        print(f"The country '{country}' you entered is not in the list. Please try again")
    except ValueError:
        print(f"The month '{month}' you entered is incorrect. Please try again.")


if __name__ == '__main__':
    main()
