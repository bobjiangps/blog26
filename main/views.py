from django.shortcuts import render
from .models import Visitor
from django.utils import timezone
from utils.geoip_helper import GeoIpHelper
from bobjiang.settings import RECORD_VISITOR


def main_page(request):
    return render(request, "main/landing.html")