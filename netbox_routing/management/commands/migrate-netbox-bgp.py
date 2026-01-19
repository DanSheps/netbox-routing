from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument('--plugin-version', dest='version', help="Version of Netbox-BGP")

    def handle(self, *args, **options):
        raise Exception("Not implemented")
