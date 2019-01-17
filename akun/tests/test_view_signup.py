from django.contrib.auth.models import User
from django.urls import resolve, reverse 
from django.test import TestCase

from ..views import signup
from ..forms import SignUpForm