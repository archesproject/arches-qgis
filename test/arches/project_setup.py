from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.utils.crypto import get_random_string
from arches.app.utils.permission_backend import assign_perm

from arches.app.models import models
from oauth2_provider.models import Application


class Command(BaseCommand):
    """
    Management command to set up the QGIS Arches testing project.
    """

    def handle(self, *args, **options):
        self.create_oauth_app()
        self.create_test_users()


    def create_oauth_app(self):
        """
        Command for creating an oauth application.
        """

        # create the app under admin user
        user = User.objects.get(username='admin')

        # hardcode the clientid and secret for testing simplicity 
        # & so settings_local value can persist.
        application = Application.objects.create(
            name='QGIS integration',
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD,
            client_secret="Vezmuv2kkOujZogP998XwziypsNnvj14vQlSz64Wu2IaZeCrW8TtNHvQMWKvYwGkU9RScyKboPYEzHW4vIfe65i3kryVJtId7bObj6P1XKPIQq4z2hPzxlc1eEqGheug",
            client_id="ZmRsVUmUtwas8lmgX40PmgAQacESxxv9EPQdIm8S",
            user=user)
        

    def create_test_users(self):
        """
        Command for creating test users.
        """

        # create user with only guest group (essentially anonymous)
        user=User.objects.create_user('guestuser', password='guestuser')
        user.is_superuser=False
        user.is_staff=False
        user.save()

        print(Group.objects.all())
