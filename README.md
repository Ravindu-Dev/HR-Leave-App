# Smart HR Leave Management System 🚀

A robust and efficient web application designed to streamline the leave management process for organizations. Built with Django, this system empowers employees to easily request leaves and allows managers to approve or reject them with a single click, ensuring seamless HR operations.

## 🌟 Key Features

### For Employees
- **Dashboard Overview**: View real-time leave balances (Sick, Casual, Annual) and the status of recent applications at a glance.
- **Easy Application**: Simple usage form to request leave, including date selection and optional evidence upload (e.g., medical certificates).
- **Request History**: Track the full history and status of all past and pending leave requests.
- **Permission Letters**: Download auto-generated PDF permission letters for any approved leave.

### For Managers
- **Approval Workflow**: Centralized dashboard to view and manage all pending leave requests from the team.
- **Quick Decisions**: Approve or reject requests efficiently.
- **Smart Validation**: System automatically checks user leave balances before allowing approval.
- **Team Calendar**: Visual calendar integration to monitor team availability and plan resources effectively.

### System Highlights
- **Role-Based Access Control (RBAC)**: Secure and distinct interfaces for Employees and Managers.
- **Automated Calculations**: Leave duration and remaining balances are calculated and updated automatically.
- **PDF Generation**: Integrated `xhtml2pdf` for generating professional, printable documents.
- **Secure Authentication**: Built on Django's robust authentication system.

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Django 6.0
- **Database**: PostgreSQL (Production-ready)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript, Django Templates
- **PDF Generation**: xhtml2pdf
- **Utilities**: Python Decouple (for env vars), Pillow

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites
- Python 3.x installed on your system.
- PostgreSQL installed and running (or configured to use SQLite).

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "HR Leave App"
   ```

2. **Create and Activate Virtual Environment**
   It's recommended to work within a virtual environment.
   ```bash
   # Create venv
   python -m venv venv
   
   # Activate (Windows)
   venv\Scripts\activate
   
   # Activate (Mac/Linux)
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   Ensure your database settings in `smart_leave_sys/settings.py` are correct. By default, it is configured for PostgreSQL.
   
   *Note: If you want to use SQLite for quick testing, update the DATABASES setting in `settings.py`.*

   Run migrations to set up the schema:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create Admin User**
   Create a superuser to access the admin panel and manage the system.
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**
   - Open your browser and go to `http://127.0.0.1:8000`.
   - Admin Panel: `http://127.0.0.1:8000/admin`

## 📸 Usage

1. **Register** a new user account.
2. **Log in** with the new credentials.
3. Access the **Admin Panel** with your superuser account to promote the user to a `Manager` role if needed.
4. **Employees** can now apply for leave from their dashboard.
5. **Managers** can view these requests and take action.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---
*Built with ❤️ using Django*
