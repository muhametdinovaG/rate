# coding: utf-8

import urllib.request
import datetime

from xml.etree import ElementTree as ET
from django.db import models
from django.db import transaction

__all__ = ['Rates']


class Rates(models.Model):
    """
    Информация по курсам
    """
    date = models.DateField('Дата', null=True, blank=True)
    rate_id = models.CharField('rate ID', max_length=10, help_text='id курса валюты')
    name = models.CharField('Наименование валюты', max_length=100)
    value = models.CharField('Стоимость', max_length=10)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return str(self.name)

    def rate_request(self):
        """Получает значения доллара и евро в рублях на текущий день"""

        url = 'http://www.cbr.ru/scripts/XML_daily.asp'

        tree = ET.parse(urllib.request.urlopen(url))
        root = tree.getroot()

        for values in root.findall('Valute'):
            date = datetime.date.today()
            try:
                rate_id = values.attrib['ID']
                name = values.find('Name').text
                value = values.find('Value').text
            except:
                rate_id = None
                name = None
                value = None

            with transaction.atomic():
                user_obj, _ = Rates.objects.get_or_create(
                    date=date,
                    rate_id=rate_id,
                    name=name,
                    value=value
                )
