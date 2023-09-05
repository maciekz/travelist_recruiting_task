import csv
from collections import defaultdict

from django.core.management import BaseCommand
from django.utils import timezone

from payments.models import UserWithBalance

USERS_BATCH_SIZE = 100
REFERERS_BATCH_SIZE = 10
REFERENCE_POINTS = 20


class Command(BaseCommand):
    help = "Import users data from CSV file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)
        parser.add_argument(
            "-y", "--yes", action="store_true", help="Confirm removal of existing data"
        )

    def handle(self, *args, **options):
        if not options["yes"]:
            self.stdout.write(
                self.style.ERROR(
                    "This command will remove all existing user data. "
                    'Please confirm with "-y" or "--yes" argument.'
                )
            )
            return

        # Import new user data
        start_time = timezone.now()
        file_path = options["file_path"]
        self._import_csv_file(file_path)
        end_time = timezone.now()

        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time - start_time).total_seconds()} seconds."
            )
        )

    def _import_csv_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as csv_file:
            # Delete all existing users
            UserWithBalance.objects.all().delete()
            # Read CSV file
            data = csv.reader(csv_file, delimiter=",")
            # Skip CSV header
            next(data)

            users = []
            references_points = defaultdict(int)
            for row in data:
                try:
                    user = UserWithBalance(
                        first_name=row[1],
                        last_name=row[2].split()[0],
                        email=row[3],
                        balance=int(row[5]),
                    )
                except ValueError as exc:
                    self.stdout.write(
                        self.style.ERROR(f"Error importing row {row}: {exc}. Skipping.")
                    )
                    continue

                users.append(user)

                referrer_email = row[4]
                if referrer_email:
                    references_points[referrer_email] += REFERENCE_POINTS

                if len(users) == USERS_BATCH_SIZE:
                    UserWithBalance.objects.bulk_create(users)
                    users = []
            if users:
                UserWithBalance.objects.bulk_create(users)

            # Update referers points
            self._update_referers_balance(references_points)

    def _update_referers_balance(self, references_points: dict[str, int]):
        referers = []
        for referer in UserWithBalance.objects.filter(
            email__in=references_points.keys()
        ):
            referer.balance += references_points[referer.email]
            if len(referers) == REFERERS_BATCH_SIZE:
                UserWithBalance.objects.bulk_update(referers, ["balance"])
                referers = []

        if referers:
            UserWithBalance.objects.bulk_update(referers, ["balance"])
