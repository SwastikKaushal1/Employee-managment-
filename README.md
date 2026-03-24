# Employee Management System 🏢

A comprehensive **Employee Management System** built with Python and Streamlit, designed to simplify tasks like attendance tracking, payroll calculation, and leave management. This project is lightweight, using CSV files for data storage, making it an excellent solution for small-to-medium-sized organizations.

-----

## ✨ Why This Project?

  * ⚡ **Lightweight & Fast**: Uses CSV files for data storage, eliminating the need for complex database setups and making it highly portable.
  * 🎨 **Interactive UI**: Built with Streamlit for a clean, responsive, and intuitive user experience right out of the box.
  * 📧 **Automated Alerts**: Integrated email notifications ensure employees are instantly updated on their leave request statuses.
  * 💰 **Streamlined Payroll**: Automatically calculates salaries based on tracked attendance, overtime, and leave, saving hours of manual administrative work.

-----

## 🧩 Features

  * 🕒 **Attendance Management**: Employees can clock in and clock out with automated work hour calculation. Daily records are stored and support statuses like "Absent," "Half Day," or "Full Day."
  * 💵 **Payroll System**: Calculates salaries dynamically and allows administrators to export monthly payroll and attendance reports directly as CSV files.
  * 🏖️ **Leave Management**: Employees apply for leave via the portal, administrators approve/reject requests, and the system sends automated email alerts.
  * 👥 **Employee Data Management**: Add, update, search, or remove records easily. Profiles include designations, contact details, and securely stored photos.
  * 📊 **Interactive Dashboards**: Separate, personalized interface views for administrators and regular employees.

-----

## 🛠️ Technologies Used

[](https://www.python.org/)  
[](https://streamlit.io/)  
[](https://pandas.pydata.org/)

*(Additional libraries: `smtplib` for email handling, `Pillow (PIL)` for image processing, and `CSV` for standard data storage).*

-----

## 📁 File Structure

```text
├── employees.csv           # Stores IDs, names, emails, designations, and photo links
├── attendance_record.csv   # Tracks clock-in/out times and calculated work hours
├── leave_requests.csv      # Manages leave applications and current approval statuses
└── employee_photos/        # Secure local directory for storing uploaded profile pictures
```

-----

## 🚀 Setup & Deployment

### 1\. 🔑 Environment Variables

For the secure email notifications to function correctly, configure your environment variables:

```bash
export EMAIL_USER="your-email@gmail.com"
export EMAIL_PASSWORD="your-email-password"
```

### 2\. 📦 Local Installation

```bash
# Clone the repository
git clone https://github.com/your-username/employee-management-system.git
cd employee-management-system

# Install required dependencies
pip install -r requirements.txt

# Run the Streamlit application
streamlit run app.py
```

-----

## 💡 How It Works

1.  **Authentication**: Users open the web portal and are greeted with customized views depending on their role (Admin or Employee).
2.  **Daily Tracking**: Employees use their dashboard to clock in for the day, clock out, and submit any upcoming leave requests.
3.  **Admin Management**: Administrators review pending leave requests (triggering an automated email upon decision) and manage the employee database.
4.  **Payroll Generation**: At the end of the cycle, the system aggregates work hours and leave data to instantly generate accurate salary calculations.

-----

## 👨‍💻 Author & Credits

Made with ❤️ by [Paritosh](https://github.com/paritoshcode) & [Swastik Kaushal](https://github.com/SwastikKaushal1)

-----

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
