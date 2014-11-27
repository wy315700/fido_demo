from django.test import TestCase

from authServer.models import TrustedApps
# Create your tests here.

class TrustAppTestCase(TestCase):
    def setUp(self):
        TrustedApps.objects.create(appid="1234", facetid="2345")
        TrustedApps.objects.create(appid="1234", facetid="4567")

    def test_getapp(self):
        print "hello"
        appid = "12345"
        facetID = "4567"
        flag = False
        trusted = TrustedApps.objects.filter(appid=appid)
        if trusted is not None:
            for app in trusted:
                if facetID == app.facetid:
                    flag = True
        self.assertEqual(flag, False)