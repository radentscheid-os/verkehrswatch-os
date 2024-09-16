import pytest
from datetime import datetime
from verkehrswatch_os.base.utils import utc2cet, cet2utc

@pytest.mark.parametrize("time_utc,time_cet", [
    ('2023-01-24 19:34:05', '2023-01-24 20:34:05'),
    ('2023-06-24 19:34:05', '2023-06-24 21:34:05'),
    ( datetime.strptime('2023-06-24 19:34:05',"%Y-%m-%d %H:%M:%S"), '2023-06-24 21:34:05')
])
def test_utc2cet(time_utc,time_cet):
    assert time_cet == utc2cet(time_utc)

@pytest.mark.parametrize("time_utc,time_cet", [
    ('2023-01-24 19:34:05', '2023-01-24 20:34:05'),
    ('2023-06-24 19:34:05', '2023-06-24 21:34:05'),
    ('2023-06-24 19:34:05',  datetime.strptime('2023-06-24 21:34:05',"%Y-%m-%d %H:%M:%S"))
])
def test_cet2utc(time_utc,time_cet):
    assert time_utc == cet2utc(time_cet)