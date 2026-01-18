import csv
from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Import doctors from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                username = row["username"]
                original_username = username
                count = 1

                # Duplicate username থাকলে auto change
                while CustomUser.objects.filter(username=username).exists():
                    username = f"{original_username}_{count}"
                    count += 1

                # token_id auto generate
                last_user = CustomUser.objects.filter(role="doctor").order_by('-id').first()
                if last_user and last_user.token_id:
                    last_num = int(last_user.token_id.replace("DR-", ""))
                    token_id = f"DR-{last_num + 1:06d}"
                else:
                    token_id = "DR-000001"

                # Check email duplicate
                email = row["email"]
                if CustomUser.objects.filter(email=email).exists():
                    print(f"Duplicate email skipped: {email}")
                    continue

                # ✅ IMPORTANT: create_user() will hash password correctly
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=row["password"],  # plain text in CSV
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    role=row["role"],
                    doctor_license=row["doctor_license"],
                    hospital_name=row["hospital_name"],
                    phone_number=row["phone_number"],
                    about_me=row["about_me"],
                    token_id=token_id,
                    is_active=row["is_active"].lower() == "true",
                    is_staff=row["is_staff"].lower() == "true",
                )

        self.stdout.write(self.style.SUCCESS('Doctors imported successfully!'))
