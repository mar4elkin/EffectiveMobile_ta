from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Load initial fixture once for an empty database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fixture",
            default="fixtures/initial_data.json",
            help="Path to fixture file relative to project root.",
        )

    def handle(self, *args, **options):
        fixture_rel_path = options["fixture"]
        fixture_path = Path(settings.BASE_DIR) / fixture_rel_path

        if not fixture_path.exists():
            self.stdout.write(self.style.WARNING(f"Fixture not found: {fixture_path}. Skip."))
            return

        check_models = [
            apps.get_model("users", "User"),
            apps.get_model("access", "Role"),
            apps.get_model("access", "UserRole"),
            apps.get_model("mockapp", "MockResource"),
        ]

        if any(model.objects.exists() for model in check_models):
            self.stdout.write(self.style.WARNING("Initial data already exists. Skip loading fixture."))
            return

        call_command("loaddata", str(fixture_path))
        self.stdout.write(self.style.SUCCESS("Initial fixture loaded."))
