# coding: utf-8

from datetime import datetime, timedelta
import urllib
from django.contrib.auth.models import User
from django.test import TestCase
from app_library.models import AppPromo, AppPromoTranslation
from feincmsorg.app_library.models import AppPromoForm

class AppPromoViewTest(TestCase):
    fixtures = ['admin_user.json',
                'page_page.json',
                'page_applicationcontent.json',
                ]

    def setUp(self):
        self.user1 = User.objects.get(pk=1) # admin, adm1n
        self.user2 = User.objects.get(pk=2) # demo, Demo

        # Start by creating some promos
        promo = AppPromo()
        promo.title = 'My Great App'
        promo.slug = 'my-great-app'
        promo.url = 'http://feinheit.ch'
        promo.doc_url = 'http://docs.feinheit.ch/'
        promo.licence = 'gnu'
        promo.author = self.user1
        promo.save()
        promo_translation = AppPromoTranslation()
        promo_translation.short_description = u'short description'
        promo_translation.long_description = u'long description'
        promo_translation.language_code = 'en'
        promo_translation.parent = promo
        promo_translation.save()
        self.promo1 = promo

        promo = AppPromo()
        promo.title = 'Elephantblog'
        promo.slug = 'elephantblog'
        promo.url = 'https://github.com/feincms/feincms-elephantblog'
        promo.doc_url = 'http://feincms-elephantblog.readthedocs.org/en/latest/'
        promo.licence = 'gnu'
        promo.author = self.user2
        promo.save()
        promo_translation = AppPromoTranslation()
        promo_translation.short_description = u'A blog for feinmcs'
        promo_translation.long_description = u"""Every Django Developer has written its own Django-based blog. But most of them have a lot of features, that you’ll never use and never wanted to, or they are just too simple for your needs, so you’ll be quicker writing your own.
                                                 Following the principles of FeinCMS, ElephantBlog tries to offer simple and basic blog functionality, but remains to be extensible so that you just pick what you need. And if you don’t find an extension, you can quickly write
                                                 your own and integrate it to ElephantBlog."""
        promo_translation.language_code = 'en'
        promo_translation.parent = promo
        promo_translation.save()
        self.promo2 = promo


    def test_list_view(self):
        """ Make sure all objects are shown in the app list. """
        response = self.client.get('/plugins/')
        self.assertEqual(response.status_code, 200)
        # Make sure the correct template is used.
        self.assertTemplateUsed(response, 'app_library/app_list.html')

        # Make sure the elements get rendered.
        self.assertIn(self.promo1.title, response.content)
        self.assertIn(self.promo2.title, response.content)

        # The correct short description is displayed
        self.assertContains(response, self.promo1.translation.short_description)
        self.assertContains(response, self.promo2.translation.short_description)

        # There should be Pagination

        #Every app has a link to it's detail page:
        self.assertContains(response, '/plugins/%s/' % self.promo1.slug)
        self.assertContains(response, '/plugins/%s/' % self.promo2.slug)

        # There is a link to the app submit page:
        self.assertContains(response, '/plugins/submit/')
        # and to the login page:
        self.assertContains(response, '/accounts/login/')

        # login as user2:
        response = self.client.post('/accounts/login/?next=/plugins/',
                {'username': 'demo', 'password': 'Demo' })
        self.assertEqual(response.status_code, 302)
        # Follow the redirect:
        response = self.client.get(response.get('Location'))
        # make sure there is an edit link for the 2nd post:
        self.assertContains(response, '/plugins/edit/elephantblog/')


    def test_details_view(self):
        # page exists
        response = self.client.get('/plugins/%s/' % self.promo1.slug )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_library/app_detail.html')

        # contains detail info
        self.assertContains(response, self.promo1.title)
        self.assertContains(response, u'long description')


    def test_submit_view(self):
        # I can sumbit a new app.
        # I am not logged in and redirected to the login site:
        response = self.client.get('/plugins/submit/')
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/accounts/login/', {'username': 'demo', 'password': 'Demo' })
        self.assertEqual(response.status_code, 302)
        # The page exists:
        response = self.client.get('/plugins/submit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_library/submit.html')
        self.assertContains(response, 'submission-form')

        # build a new app:
        post_data = { 'title': 'Gallery',
                      'project_url': 'https://github.com/feinheit/feincms_gallery',
                      'licence': 'apache',
                      'slug': 'gallery',
                      'short_description': u'This is a gallery app and contenttype for Feincms.',
                      'long_description': u"This is a gallery app and contenttype for Feincms. It allows for several gallery 'types', each with its own tempate, css and javascript files. It comes packed with several pretty types ready for use.",
        }
        # send it to the view
        response = self.client.post('/plugins/submit/', data=post_data)
        self.assertEqual(response.status_code, 302)

        # make sure the data is in the db
        app = AppPromo.objects.get(pk=3)
        self.assertEqual(app.title, 'Gallery')
        self.assertEqual(app.slug, 'gallery')
        self.assertEqual(app.translation.short_description, post_data['short_description'])
        self.assertEqual(app.translation.long_description, post_data['long_description'])
        self.assertEqual(app.author.username, 'demo')


    def test_promo_form(self):
        # build the form
        form = AppPromoForm()

        # check it has all the fields:
        self.assertEquals(form.fields.keys(), ['title', 'slug', 'icon', 'project_url', 'doc_url',
                                               'licence', 'short_description', 'long_description'])
        self.assertIn('textarea', form.as_p())
        self.assertIn('class="richtext"', form.as_p())


    def test_edit_view(self):
        # try to open the edit page:
        response = self.client.get('/plugins/edit/my-great-app/')
        # should redirect you to the login page.
        self.assertEqual(response.status_code, 302)
        #login as user2.
        response = self.client.post('/accounts/login/',
                        {'username': 'demo', 'password': 'Demo' })
        self.assertEqual(response.status_code, 302)
        # Try to open it again:
        response = self.client.get('/plugins/edit/my-great-app/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response._get_content(), 'Only the original uploader can edit an app.')
        #
        response = self.client.get('/plugins/edit/elephantblog/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Elephantblog')
        # make sure the correct target url:
        self.assertContains(response, 'action="/plugins/edit/elephantblog/"')

