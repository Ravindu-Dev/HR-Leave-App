import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_leave_sys.settings")
django.setup()

from core.models import User

username = "admin"
password = "password123"
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser/manager '{username}'...")
    User.objects.create_superuser(username=username, email=email, password=password, role='MANAGER')
    print("Superuser created successfully!")
else:
    print(f"User '{username}' already exists.")
