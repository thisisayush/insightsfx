from django.core.management.base import BaseCommand, CommandError
from apps.core.models import Options
from apps.core.utils import addOption, getOption

class Command(BaseCommand):

    help = "Initializes Database Tables with initial values"

    def handle(self, *args, **kwargs):
        
        options = (
            ("site_title", "Letstream", "Site Title"),
            ("support_email", "support@theletstream.com", "Support Email"),
            ("site_description", "Site Developed by Letstream.", "Site Description"),
            ("smtp_server", "mail.example.com", "SMTP Server"),
            ("smtp_user", "admin", "SMTP User"),
            ("smtp_pass", "pass", "SMTP Pass"),
            ("smtp_port", "000", "SMTP Port"),
            ("send_mails_as", "admin@localhost", "Send Mails As"),
            ("site_url", "http://localhost:8000", "Site Url"),
        )

        for option in options:
            if getOption(option[0]) == None:
                addOption(option[0], option[1], option[2])

        print("Added Initial Entries!")