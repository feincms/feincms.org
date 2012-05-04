# coding: utf-8

from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from app_library.models import AppPromo, AppPromoTranslation


class AppPromoModelTest(TestCase):
    fixtures = ['admin_user.json']

    def setUp(self):
        self.user1 = User.objects.get(pk=1)

    def test_creating_some_promos(self):
        # Start by creating some promos
        promo = AppPromo()
        promo.title = 'My Great App'
        promo.url = 'http://feinheit.ch'
        promo.doc_url = 'http://docs.feinheit.ch/'
        promo.licence = 'gnu'
        promo.author = self.user1
        promo.save()

        # Now create a translation for the promo:
        promo_translation = AppPromoTranslation()
        promo_translation.short_description = u'short description'
        promo_translation.long_description = u'long description'
        promo_translation.language_code = 'en'
        promo_translation.parent = promo
        promo_translation.save()

        # Now create another translation for the promo:
        promo_translation = AppPromoTranslation()
        promo_translation.short_description = u'Kurzbeschreibung'
        promo_translation.long_description = u'Längere Beschreibung'
        promo_translation.language_code = 'de'
        promo_translation.parent = promo
        promo_translation.save()

        # try to retrieve the data from the database
        promos = AppPromo.objects.all()
        self.assertEquals(len(promos), 1)
        promo = promos[0]
        self.assertEqual(promo.title, 'My Great App')
        self.assertEqual(promo.author, self.user1)

        now = datetime.now()
        one_sec_ago = datetime.now() - timedelta(seconds=1)
        self.assertNotEqual(promo.created, None)
        self.assertGreater(promo.created, one_sec_ago)

        translations = promo.translations.all()
        self.assertEquals(len(translations), 2)
        translation = promo.translation
        self.assertEqual(promo.translation.short_description, u'short description')


