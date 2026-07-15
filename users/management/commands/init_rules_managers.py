from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Команда создает группы и назначает права.'

    def handle(self, *args, **options):
        managers_group, _ = Group.objects.get_or_create(name="Managers")
        permission_1 = Permission.objects.get(codename='view_attemptedmailing')
        permission_2 = Permission.objects.get(codename='view_message')
        permission_3 = Permission.objects.get(codename='change_newsletter')
        permission_4 = Permission.objects.get(codename='view_newsletter')
        permission_5 = Permission.objects.get(codename='view_newsletterrecipient')
        permission_6 = Permission.objects.get(codename='change_user')
        permission_7 = Permission.objects.get(codename='view_user')

        managers_group.permissions.set([
            permission_1,
            permission_2,
            permission_3,
            permission_4,
            permission_5,
            permission_6,
            permission_7
        ])

        self.stdout.write(self.style.SUCCESS("Группы и права успешно созданы"))