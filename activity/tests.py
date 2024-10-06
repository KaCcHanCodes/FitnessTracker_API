#from django.test import TestCase
from django.utils.dateparse import parse_date
from datetime import datetime

# Create your tests here.

date = "2024-10-02"
convert = parse_date(date)

date_ = datetime(convert.year, convert.month, convert.day)

print(date_)