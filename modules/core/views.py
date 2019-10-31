# coding: utf-8

import logging
import urllib.request
import pandas as pd
import datetime

from modules.core.models import Rates
from xml.etree import ElementTree as ET
from django.db import transaction
from modules.core.mixins import TemplateViewMixin
from modules.core.models import *
from django.shortcuts import render

LOGGER = logging.getLogger(__name__)


class PageViewRate(TemplateViewMixin):
    """
    Страница
    """
    template_name = 'rate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rates'] = Rates.objects.all()
        return context


def rate(request):
    """
    Получает значения доллара и евро в рублях (выбор дат)
    :return:
    """

    d1 = request.GET.get('UniDbQuery.FromDate', '')
    d2 = request.GET.get('UniDbQuery.ToDate', '')

    context = {
        'UniDbQuery_FromDate': d1 or '23.10.2019',
        'UniDbQuery_ToDate': d2 or '23.10.2019',
    }

    daterange = pd.date_range(d1, d2)

    for single_date in daterange:
        date = single_date.strftime('%Y-%m-%d')

        url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req='.format(date)

        tree = ET.parse(urllib.request.urlopen(url))
        root = tree.getroot()

        for head in root.findall('ValCurs'):
            date = head.attrib['Date']
            print(date)

        for values in root.findall('Valute'):
            try:
                rate_id = values.attrib['ID']
                name = values.find('Name').text
                value = values.find('Value').text
            except:
                rate_id = None
                name = None
                value = None

            with transaction.atomic():
                try:
                    user_obj, _ = Rates.objects.get_or_create(
                        date=datetime.datetime.strptime(date, '%Y-%m-%d'),
                        rate_id=rate_id,
                        name=name,
                        value=value
                    )
                except:
                    pass
    context['rates'] = Rates.objects.all().order_by('name', 'date')
    return render(request, 'rate.html', context)
