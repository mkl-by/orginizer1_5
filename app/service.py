import datetime


from ics import Calendar
import requests
from rest_framework import status
from rest_framework.response import Response

from tatsu.exceptions import FailedParse

from app.data import country
from app.models import HolidaysModel


def holidays():
    """
    Парсим сайт с праздниками
    """
    for con in country:
        try:
            url = f"https://www.officeholidays.com/ics/ics_country.php?tbl_country={con}"
            response = requests.get(url)
            print('---------------------')
            if response.status_code != 200:
                print(f"BAD 404: {con}")
                continue
            print(f'{response.status_code} => {con}')
            c = Calendar(response.text)
            data = list(c.timeline)
        except FailedParse:
            print('Parsing the file ended with an error')
            continue

        for i in data:
            HolidaysModel.objects.update_or_create(
                country=con,
                holidays=i.name,
                datestartholiday=str(i.begin),
                dateendholiday=str(i.end)
            )


def creation_date(string):
    """
    return datetime obj
    """
    try:
        ymd = datetime.datetime.strptime(string, '%Y-%m-%d')
    except ValueError:
        return Response({
            "message": f"Date parameters in url .../year/month/day value error."
        },
            status=status.HTTP_400_BAD_REQUEST
        )
    return ymd
