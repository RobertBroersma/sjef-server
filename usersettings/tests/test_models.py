from django.test import TestCase
from django.contrib.auth.models import User
from usersettings.models import Profile, DRI
from core.models import NutritionalValue
from django.core.exceptions import ValidationError

class UserSettingsTest(TestCase):

    def create_profile(self):
        user = User.objects.create_user('Piebe', None, 'Bliksem')

        return user.profile

class ProfileTest(UserSettingsTest):

    def test_can_create_DRI(self):
        dri = DRI(amount=1000)
        dri.save()

        self.assertEqual(DRI.objects.count(), 1)

    def test_DRI_associated_with_profile(self):
        profile = self.create_profile()

        dri1 = DRI.objects.create(owner=profile, amount=1000)
        dri2 = DRI.objects.create(owner=profile, amount=1000)

        self.assertEqual(list(profile.dri_set.all()), [dri1, dri2])

class DRITest(UserSettingsTest):

    #can create

    def test_DRI_has_NutrionalValue(self):
        profile = self.create_profile()

        nutritional_value = NutritionalValue.objects.create()
        dri = DRI.objects.create(owner=profile, nutritional_value=nutritional_value, amount=1000)

        self.assertEqual(dri.amount, 1000)
        self.assertEqual(dri.nutritional_value, nutritional_value)
