"""
XXX
"""

import datetime

import pytz
from freezegun import freeze_time

import vws_auth_tools

def test_rfc_1123_date():
    """
    XXX
    """
    not_gmt_timezone = pytz.timezone('America/New_York')
    frozen_time = datetime.datetime(
        year=2015,
        month=2,
        day=5,
        hour=9,
        minute=55,
        second=12,
        microsecond=11,
        tzinfo=not_gmt_timezone,
    )
    with freeze_time(frozen_time):
        result = vws_auth_tools.rfc_1123_date()

    assert result == 'Thu, 05 Feb 2015 14:51:12 GMT'

def test_authorization_header():
    """
    XXX
    """
    pass

