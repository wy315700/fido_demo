from django.test import TestCase

from authServer.models import TrustedApps
import struct
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


def getKrd():
    db_aaid = "testAAID"
    db_finalchallenge = "testFinalChallenge"
    db_keyId = "testKeyID"
    db_publicKey = "testPublicKey"
    db_signature = "testSignature"
    tag_krd = '\x00\x03'
    Length = '\x00\x00'
    aaid = struct.pack(str(len(db_aaid)) + "s", db_aaid)
    final_aaid = struct.pack('H', len(aaid)) + aaid
    authenticatorVersion = struct.pack("3s", "1.0")
    publicKeyAlgAndEncoding = '\x00\x01'
    SignatureAlgAndEndcoding = '\x01\x00'
    FinalChallenge = struct.pack(str(len(db_finalchallenge)) + "s", db_finalchallenge)
    final_FinalChallenge = struct.pack("H", len(FinalChallenge)) + FinalChallenge
    KeyId = struct.pack(str(len(db_keyId)) + "s", db_keyId)
    final_keyId = struct.pack("H", len(KeyId)) + KeyId
    RegCounter = struct.pack("I", 0)
    SignCounter = struct.pack("I", 0)
    PublicKey = struct.pack(str(len(db_publicKey)) + "s", db_publicKey)
    final_publicKey = struct.pack("H", len(PublicKey)) + PublicKey
    tag_signature = "\x00\x06"
    krd_content = final_aaid + authenticatorVersion + publicKeyAlgAndEncoding + \
                  SignatureAlgAndEndcoding + final_FinalChallenge + final_keyId + \
                  RegCounter + SignCounter + final_publicKey
    temp_krd = tag_krd + Length + krd_content
    real_length = struct.pack("H", len(temp_krd))
    signature = struct.pack(str(len(db_signature)) + "s", db_signature)
    final_signature = struct.pack("H", len(signature)) + signature
    real_krd = tag_krd + real_length + krd_content + tag_signature + final_signature
    print repr(real_krd)




