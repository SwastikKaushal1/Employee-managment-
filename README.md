

# Employee Management System

A comprehensive **Employee Management System** built with Python and Streamlit, designed to simplify tasks like attendance tracking, payroll calculation, and leave management. This project is lightweight, using CSV files for data storage, making it an excellent solution for small-to-medium-sized organizations.

---

## 🚀 Features

### 1. Attendance Management
- Employees can clock in and clock out with automated work hour calculation.
- Attendance records are updated and stored daily.
- Supports status updates like "Absent," "Half Day," or "Full Day."

### 2. Payroll System
- Calculates salaries based on attendance, overtime, and leave status.
- Monthly payroll and attendance can be exported as CSV files.

### 3. Leave Management
- Employees can apply for leave directly from the portal.
- Administrators can approve or reject leave requests.
- Automated email notifications are sent for leave status updates.

### 4. Employee Data Management
- Add, update, search, or remove employee records.
- Employee profiles include name, designation, email, and a photo.
- Employee photos are securely uploaded and stored.

### 5. Interactive UI
- Streamlit-powered interface for a clean and intuitive experience.
- Separate dashboards for administrators and employees.
- Personalized employee dashboards with photos and details.

---

## 🛠️ Technologies Used
- **Python**: Core programming language.
- **Streamlit**: For building the interactive user interface.
- **Pandas & CSV**: For data handling and lightweight storage.
- **smtplib**: For sending email notifications.
- **Pillow (PIL)**: For managing employee photos.

---

## 📁 File Structure
- `employees.csv`: Stores employee information (ID, name, email, designation, photo link).
- `attendance_record.csv`: Tracks attendance data (clock-in/out times, work hours).
- `leave_requests.csv`: Manages leave requests and their statuses.
- `employee_photos/`: Directory for storing employee photos.

---

## ⚙️ Setup Instructions
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/employee-management-system.git
   cd employee-management-system
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

4. Make sure to add these environment variables for secure email notifications:
   ```bash
   export EMAIL_USER="your-email@gmail.com"
   export EMAIL_PASSWORD="your-email-password"
   ```

---

## 📧 Email Notifications
- Clock-in and clock-out alerts are sent to employees.
- Leave approval or rejection emails are sent by administrators.

---

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve this project.

---

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Let me know if you need further customization, or share your repository link so I can adapt it to your specific GitHub repo details!
