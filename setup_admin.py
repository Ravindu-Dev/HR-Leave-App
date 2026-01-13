import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_leave_sys.settings")
django.setup()

from core.models import User

# HARDCODED: Default admin credentials for initial setup
# WARNING: These are development credentials only. Change immediately in production!
username = "admin"  # HARDCODED: Default admin username
password = "password123"  # HARDCODED: Default admin password - INSECURE, change in production!
email = "admin@example.com"  # HARDCODED: Default admin email

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser/manager '{username}'...")
    # HARDCODED: Creating user with MANAGER role for approval privileges
    User.objects.create_superuser(username=username, email=email, password=password, role='MANAGER')
    print("Superuser created successfully!")
else:
    print(f"User '{username}' already exists.")
