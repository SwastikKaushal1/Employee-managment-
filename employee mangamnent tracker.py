# Imprting all the library
import csv
import datetime
from prettytable import PrettyTable
import os

admin_password = ""  # You can see the admin password from here.


# Side Functions:
def current_Date():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# For the Employee total count:
def update_present_count(count, change):
    value = count + change
    save_present_count(value)
    return value


def load_present_count():
    try:
        with open("present_count.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0


def save_present_count(count):
    with open("present_count.txt", "w") as file:
        file.write(str(count))


def show_present_count(value):
    print(f"Present count: {value}")


def calculate_work_hours(clock_in_time, clock_out_time):
    if clock_in_time == "" or clock_out_time == "":
        return "N/A"
    fmt = "%Y-%m-%d %H:%M:%S"
    try:
        clock_in = datetime.datetime.strptime(clock_in_time, fmt)
        clock_out = datetime.datetime.strptime(clock_out_time, fmt)
        work_duration = clock_out - clock_in
        return str(work_duration)
    except ValueError:
        return "N/A"


def get_status(work_duration):
    if work_duration == "N/A":
        return "Absent"
    hours, minutes = map(int, work_duration.split(":")[:2])
    total_hours = hours + minutes / 60
    if total_hours < 3:
        return "Half Day"
    elif total_hours >= 6:
        return "Full Day"
    else:
        return "Over Time"


def generate_employee_report(employee_id):
    report = f"Report for Employee ID: {employee_id}\n"
    report += f"Name: {employee_data[employee_id]['Name']}\n"
    report += "Attendance History:\n"

    attendance_history = view_attendance_history(employee_id)
    if attendance_history:
        report += attendance_history + "\n"

    print(report)


def show_all_data():
    attendance_table = PrettyTable()
    attendance_table.field_names = ["ID", "Clock In", "Clock Out"]
    for emp_id, times in attendance_data.items():
        attendance_table.add_row([emp_id, times["Clock In"], times["Clock Out"]])

    print("Attendance Data:")
    print(attendance_table)

    employee_table = PrettyTable()
    employee_table.field_names = ["ID", "Name", "Password", "Designation"]
    for emp_id, info in employee_data.items():
        employee_table.add_row(
            [emp_id, info["Name"], info["Password"], info["Designation"]]
        )

    print("\nEmployee Data:")
    print(employee_table)

    try:
        with open("attendance_record.csv", "r") as file:
            reader = csv.DictReader(file)
            record_table = PrettyTable()
            record_table.field_names = reader.fieldnames
            for row in reader:
                record_table.add_row([row[field] for field in record_table.field_names])
            print("\nAttendance Record:")
            print(record_table)
    except FileNotFoundError:
        print("\nAttendance Record file does not exist.")


# Clock in and clock out functions:
def clock_in(employee_id, password, present_count):
    if employee_id not in employee_data:
        print("Invalid Employee ID.")
        return present_count
    if password != employee_data[employee_id]["Password"]:
        print("Incorrect password.")
        return present_count

    if employee_id in attendance_data:
        clock_out_time = attendance_data[employee_id].get("Clock Out", "").strip()
        clock_in_time = attendance_data[employee_id].get("Clock In", "").strip()

        if clock_in_time != "" and clock_out_time != "":
            attendance_data[employee_id]["Clock In"] = current_timestamp()
            save_attendance_data()
            print("Clocked in.")
            present_count = update_present_count(present_count, 1)
        else:
            print("Already clocked in.")
    else:
        attendance_data[employee_id] = {
            "Clock In": current_timestamp(),
            "Clock Out": "",
        }
        save_attendance_data()
        print("Clocked in.")
        present_count = update_present_count(present_count, 1)

    return present_count


def clock_out(employee_id, password, present_count):
    if employee_id not in employee_data:
        print("Invalid Employee ID.")
        return present_count
    if password != employee_data[employee_id]["Password"]:
        print("Incorrect password.")
        return present_count

    if employee_id in attendance_data:
        clock_in_time = attendance_data[employee_id].get("Clock In", "").strip()
        clock_out_time = attendance_data[employee_id].get("Clock Out", "").strip()

        if clock_in_time != "" and clock_out_time == "":
            attendance_data[employee_id]["Clock Out"] = current_timestamp()
            save_attendance_data()
            update_attendance_record(employee_id)
            print("Clocked out.")
            present_count = update_present_count(present_count, -1)
        elif clock_in_time == "":
            print("Not clocked in yet.")
        else:
            attendance_data[employee_id]["Clock Out"] = current_timestamp()
            save_attendance_data()
            update_attendance_record(employee_id)
            print("Clocked out.")
    else:
        print("No clock-in record found.")

    return present_count


# Functions to view old data:
def read_attendance_and_display():
    try:
        user_input = input(
            "Enter the prefix for the attendance file (e.g., '2024-08'): "
        )
        filename = user_input + "_attendance.csv"
        with open(filename, mode="r") as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            table = PrettyTable(headers)
            for row in csv_reader:
                table.add_row(row)
        print(table)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_payroll_and_display():
    try:
        user_input = input(
            "Enter the prefix for the attendance file (e.g., '2024-08'): "
        )
        filename = user_input + "__payroll.csv"
        with open(filename, mode="r") as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            table = PrettyTable(headers)
            for row in csv_reader:
                table.add_row(row)
        print(table)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Functions to manange Employee:
def load_employee_data():
    try:
        with open("employees.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                employee_data[row[0]] = {
                    "Name": row[1],
                    "Password": row[2],
                    "Designation": row[3],
                }
    except FileNotFoundError:
        pass


def save_employee_data():
    with open("employees.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["ID", "Name", "Password", "Designation"]
        )  # Header for employee data
        for emp_id, info in employee_data.items():
            writer.writerow(
                [emp_id, info["Name"], info["Password"], info["Designation"]]
            )


def add_employee(employee_id, name, password, designation):
    if employee_id in employee_data:
        print("Employee ID already exists.")
    else:
        employee_data[employee_id] = {
            "Name": name,
            "Password": password,
            "Designation": designation,
        }
        save_employee_data()
        print("Employee added.")


def remove_employee(employee_id):
    if employee_id in employee_data:
        del employee_data[employee_id]
        save_employee_data()
        print("Employee removed.")
    else:
        print("Employee ID not found.")


def search_employee(employee_id):
    if employee_id in employee_data:
        info = employee_data[employee_id]
        att = attendance_data.get(employee_id, {"Clock In": "", "Clock Out": ""})
        print(f"ID: {employee_id}, Name: {info['Name']}")
        print(f"Clock In: {att['Clock In']}, Clock Out: {att['Clock Out']}")
    else:
        print("Employee ID not found.")


# Temporary attendance data so it can calculate the time hours even when the program is closed.
def save_attendance_data():
    with open("attendance.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Clock In", "Clock Out"])  # Header for attendance data
        for emp_id, times in attendance_data.items():
            writer.writerow([emp_id, times["Clock In"], times["Clock Out"]])


def load_attendance_data():
    try:
        with open("attendance.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                attendance_data[row[0]] = {"Clock In": row[1], "Clock Out": row[2]}
    except FileNotFoundError:
        pass


# Function of attendance record:
def update_attendance_record(employee_id):
    # Retrieve attendance data
    clock_in_time = attendance_data[employee_id]["Clock In"]
    clock_out_time = attendance_data[employee_id]["Clock Out"]
    work_duration = calculate_work_hours(clock_in_time, clock_out_time)
    status = get_status(work_duration)
    today_Date = current_Date()

    # Prepare new record
    new_record = {
        "Employee ID": employee_id,
        "Name": employee_data[employee_id]["Name"],
        "Clock In": clock_in_time,
        "Clock Out": clock_out_time,
        "Date": today_Date,
        "Total Work Hours": work_duration,
        "Status": status,
    }

    # Append new record to the CSV file
    file_exists = os.path.isfile("attendance_record.csv")

    with open("attendance_record.csv", "a", newline="") as file:
        fieldnames = [
            "Employee ID",
            "Name",
            "Clock In",
            "Clock Out",
            "Date",
            "Total Work Hours",
            "Status",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write header only if file is newly created
        if not file_exists:
            writer.writeheader()

        writer.writerow(new_record)


def mark_absent():
    # Load existing leave requests
    try:
        with open("leave_requests.csv", "r") as file:
            reader = csv.DictReader(file)
            leave_requests = list(reader)
    except FileNotFoundError:
        leave_requests = []

    # Load existing attendance records
    try:
        with open("attendance_record.csv", "r") as file:
            reader = csv.DictReader(file)
            existing_records = {row["Employee ID"]: row for row in reader}
    except FileNotFoundError:
        existing_records = {}

    # Load all employee data
    all_records = {
        emp_id: {"Name": employee_data[emp_id]["Name"]} for emp_id in employee_data
    }

    # Determine status and prepare new records
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_date = datetime.datetime.strptime(today, "%Y-%m-%d").date()

    new_records = []

    for emp_id, record in all_records.items():
        # Check if there is already a record for today
        if emp_id not in existing_records or existing_records[emp_id]["Clock In"] == "":
            # Default status is Absent
            status = "Absent"
            leave_type = ""
            for request in leave_requests:
                if request["Employee ID"] == emp_id and request["Status"] == "Accepted":
                    start_date = datetime.datetime.strptime(
                        request["Start Date"], "%Y-%m-%d"
                    ).date()
                    end_date = datetime.datetime.strptime(
                        request["End Date"], "%Y-%m-%d"
                    ).date()
                    if start_date <= today_date <= end_date:
                        status = request.get(
                            "Type_of_Leave", "On Leave"
                        )  # Use leave type from request
                        leave_type = status
                        break

            new_records.append(
                {
                    "Employee ID": emp_id,
                    "Name": record["Name"],
                    "Clock In": "",
                    "Clock Out": "",
                    "Date": today,
                    "Total Work Hours": "N/A",
                    "Status": leave_type if leave_type else status,
                }
            )

    # Write new records to the file, appending if necessary
    file_exists = os.path.isfile("attendance_record.csv")

    with open("attendance_record.csv", "a", newline="") as file:
        fieldnames = [
            "Employee ID",
            "Name",
            "Clock In",
            "Clock Out",
            "Date",
            "Total Work Hours",
            "Status",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for record in new_records:
            writer.writerow(record)


def view_attendance_history(employee_id):
    try:
        with open("attendance_record.csv", "r") as file:
            reader = csv.DictReader(file)
            history_table = PrettyTable()
            history_table.field_names = reader.fieldnames

            records_found = False
            for row in reader:
                if row["Employee ID"] == employee_id:
                    history_table.add_row(
                        [row[field] for field in history_table.field_names]
                    )
                    records_found = True

            if records_found:
                print(f"\nAttendance History for Employee ID: {employee_id}")
                print(history_table)
            else:
                print("No attendance records found for this employee.")
    except FileNotFoundError:
        print("Attendance record file not found.")


# Leave Managment Functions:
def view_employee_leave_status(employee_id):
    try:
        with open("leave_requests.csv", "r") as file:
            reader = csv.DictReader(file)
            leave_table = PrettyTable()
            leave_table.field_names = reader.fieldnames

            records_found = False
            for row in reader:
                if row["Employee ID"] == employee_id:
                    leave_table.add_row(
                        [row[field] for field in leave_table.field_names]
                    )
                    records_found = True

            if records_found:
                print(f"\nLeave Status for Employee ID: {employee_id}")
                print(leave_table)
            else:
                print("No leave records found for this employee.")
    except FileNotFoundError:
        print("Leave requests file not found.")


def view_pending_leave_requests():
    try:
        with open("leave_requests.csv", "r") as file:
            reader = csv.DictReader(file)
            leave_table = PrettyTable()
            leave_table.field_names = reader.fieldnames
            for row in reader:
                if row["Status"] == "Pending":
                    leave_table.add_row(
                        [row[field] for field in leave_table.field_names]
                    )

            print("\nPending Leave Requests:")
            print(leave_table)
    except FileNotFoundError:
        print("No leave requests found.")


def view_leave_status():
    try:
        with open("leave_requests.csv", "r") as file:
            reader = csv.DictReader(file)
            leave_table = PrettyTable()
            leave_table.field_names = reader.fieldnames

            for row in reader:
                leave_table.add_row([row[field] for field in leave_table.field_names])

            print("\nAll Leave Requests:")
            print(leave_table)
    except FileNotFoundError:
        print("No leave requests found.")


def change_leave_status(employee_id, start_date, status):
    updated = False
    for leave in leave_requests:
        if leave["Employee ID"] == employee_id and leave["Start Date"] == start_date:
            leave["Status"] = status
            updated = True
            save_leave_requests()
            print(f"Leave request {status.lower()}ed.")
            break
    if not updated:
        print("Leave request not found.")


def save_leave_requests():
    with open("leave_requests.csv", "w", newline="") as file:
        fieldnames = [
            "Employee ID",
            "Start Date",
            "End Date",
            "Reason",
            "Status",
            "Type_of_Leave",
        ]  # Include 'Type of Leave'
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(leave_requests)


def load_leave_requests():
    global leave_requests
    leave_requests = []
    try:
        with open("leave_requests.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                leave_requests.append(row)
    except FileNotFoundError:
        leave_requests = []

        pass


def apply_leave(employee_id):
    print("Choose the type of leave:")
    print("1. Paid Leave")
    print("2. Sick Leave")
    print("3. Unpaid Leave")
    leave_type_choice = input("Enter your choice (1-3): ")

    leave_types = {
        "1": "Paid Leave",
        "2": "Sick Leave",
        "3": "Unpaid Leave",
    }

    leave_type = leave_types.get(leave_type_choice, "Unknown Leave Type")

    start_date = input("Enter leave start date (YYYY-MM-DD): ")
    end_date = input("Enter leave end date (YYYY-MM-DD): ")
    reason = input("Enter the reason for leave: ")  # Added reason input

    leave_requests.append(
        {
            "Employee ID": employee_id,
            "Start Date": start_date,
            "End Date": end_date,
            "Reason": reason,  # Added reason to leave requests
            "Type_of_Leave": leave_type,  # Added type of leave
            "Status": "Pending",
        }
    )
    save_leave_requests()
    print("Leave request submitted")


# Payroll mangagement:


def calculate_salary(designation, attendance_status, base_salary=None):
    if base_salary is None:
        base_salary = base_salaries.get(designation)
        if base_salary is None:
            raise ValueError(
                f"Base salary data not found for designation: {designation}"
            )

    if attendance_status in ["Paid Leave", "Sick Leave"]:
        return base_salary
    elif attendance_status == "Half Day":
        return base_salary / 2
    elif attendance_status in ["Absent", "Unpaid Leave"]:
        return 0
    else:
        raise ValueError(f"Invalid attendance status: {attendance_status}")


def calculate_overtime_salary(designation, hours_overtime):
    base_salary = base_salaries.get(designation)
    if base_salary is None:
        raise ValueError(f"Base salary data not found for designation: {designation}")

    hourly_rate = base_salary / (6 * 30)
    overtime_rate = hourly_rate * 1.5
    return overtime_rate * hours_overtime


def calculate_total_salary(designation, attendance_status, hours_overtime):
    base_salary = base_salaries.get(designation)
    if base_salary is None:
        raise ValueError(f"Base salary data not found for designation: {designation}")

    attendance_salary = calculate_salary(designation, attendance_status, base_salary)
    overtime_salary = calculate_overtime_salary(designation, hours_overtime)

    return attendance_salary + overtime_salary


def time_to_hours(time_str):
    if time_str == "N/A":
        return 0
    try:
        time_parts = time_str.split(":")
        hours = int(time_parts[0])
        minutes = int(time_parts[1])
        seconds = int(time_parts[2])
        return hours + minutes / 60 + seconds / 3600
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")


def update_temp_csv_from_attendance():
    today = current_Date()

    try:
        with open("attendance_record.csv", mode="r") as file:
            reader = csv.DictReader(file)
            file_exists = os.path.isfile("temp.csv")

            with open("temp.csv", mode="a", newline="") as temp_file:
                fieldnames = [
                    "Date",
                    "Employee ID",
                    "Employee Name",
                    "Designation",
                    "Attendance Status",
                    "Overtime Hours",
                    "Total Salary",
                ]
                writer = csv.DictWriter(temp_file, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                for record in reader:
                    emp_id = record["Employee ID"]
                    emp_name = record["Name"]
                    designation = employee_data.get(emp_id, {}).get(
                        "Designation", "Unknown"
                    )
                    attendance_status = record["Status"]
                    total_work_hours = record["Total Work Hours"]

                    if total_work_hours == "N/A":
                        hours_overtime = 0
                    else:
                        try:
                            # Convert HH:MM:SS to total hours
                            hours, minutes, seconds = map(
                                int, total_work_hours.split(":")
                            )
                            total_hours = hours + minutes / 60 + seconds / 3600
                        except ValueError:
                            raise ValueError(
                                f"Incorrect time format in 'Total Work Hours': {total_work_hours}"
                            )

                        hours_overtime = max(0, total_hours - 6)

                    total_salary = calculate_total_salary(
                        designation, attendance_status, hours_overtime
                    )

                    writer.writerow(
                        {
                            "Date": today,
                            "Employee ID": emp_id,
                            "Employee Name": emp_name,
                            "Designation": designation,
                            "Attendance Status": attendance_status,
                            "Overtime Hours": hours_overtime,
                            "Total Salary": total_salary,
                        }
                    )

        print("Temp CSV updated from attendance record.")

    except FileNotFoundError:
        print("The file 'attendance_record.csv' does not exist.")


def update_employee_payroll_salary():
    monthly_totals = {}

    if not os.path.exists("temp.csv"):
        print("temp.csv does not exist.")
        return

    with open("temp.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            emp_id = row["Employee ID"]
            emp_name = row["Employee Name"]
            date_str = row["Date"]
            total_salary = float(row["Total Salary"])

            # Parse the date to extract the month and year
            date_obj = current_Date
            month = datetime.datetime.now().strftime("%Y-%m")

            key = (emp_id, emp_name, month)

            if key not in monthly_totals:
                monthly_totals[key] = 0

            monthly_totals[key] += total_salary

    with open("employee_payroll_salary.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Employee ID", "Employee Name", "Month", "Cumulative Salary"])
        for (emp_id, emp_name, month), total in monthly_totals.items():
            writer.writerow([emp_id, emp_name, month, total])


def clear_temp_csv():
    if os.path.exists("temp.csv"):
        os.remove("temp.csv")


def export_monthly_payroll_and_attendance():
    today = datetime.datetime.now().strftime("%Y-%m")
    monthly_payroll_filename = f"{today}_payroll.csv"
    monthly_attendance_filename = f"{today}_attendance.csv"

    if os.path.exists("employee_payroll_salary.csv"):
        os.rename("employee_payroll_salary.csv", monthly_payroll_filename)
        print(f"Payroll data exported to {monthly_payroll_filename}")
    else:
        print("employee_payroll_salary.csv does not exist.")

    if os.path.exists("attendance_record.csv"):
        os.rename("attendance_record.csv", monthly_attendance_filename)
        print(f"Attendance record exported to {monthly_attendance_filename}")
    else:
        print("attendance_record.csv does not exist.")
    clear_temp_csv()


def run_daily_operations():
    update_temp_csv_from_attendance()
    update_employee_payroll_salary()


def view_employee_payroll(emp_id):
    if not os.path.exists("temp.csv"):
        print("temp.csv does not exist.")
        return

    table = PrettyTable()
    # Define column names based on the columns present in the CSV file
    column_names = [
        "Date",
        "Employee ID",
        "Employee Name",
        "Designation",
        "Attendance Status",
        "Overtime Hours",
        "Total Salary",
    ]

    with open("temp.csv", mode="r") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames

        # Ensure that the columns in the table match the fieldnames in the CSV
        actual_columns = [col for col in column_names if col in fieldnames]
        table.field_names = actual_columns

        employee_records = [row for row in reader if row["Employee ID"] == emp_id]

        if not employee_records:
            print(f"No records found for Employee ID {emp_id}.")
            return

        for record in employee_records:
            # Prepare row data with the correct number of columns
            row = [record.get(col, "N/A") for col in actual_columns]
            table.add_row(row)

    print(f"Payroll Data for Employee ID {emp_id}:")
    print(table)


def view_all_payroll():
    table = PrettyTable()
    table.field_names = [
        "Date",
        "Employee ID",
        "Employee Name",
        "Designation",
        "Attendance Status",
        "Overtime Hours",
        "Total Salary",
    ]

    try:
        with open("temp.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Handle missing 'Overtime Hours' key
                overtime_hours = row.get("Overtime Hours", "N/A")
                table.add_row(
                    [
                        row["Date"],
                        row["Employee ID"],
                        row["Employee Name"],
                        row.get("Designation", "N/A"),
                        row["Attendance Status"],
                        overtime_hours,
                        row["Total Salary"],
                    ]
                )

    except FileNotFoundError:
        print("The file 'temp.csv' does not exist.")


# Menu functions:
def show_designation_menu():
    designations = print(
        " 1: CEO\n",
        "2: Manager\n",
        "3: Employee\n",
        "4: CA\n",
        "5: Trainee\n",
    )
    desig_input = input("Enter your choice (1-5): ")
    if desig_input == "1":
        return "CEO"
    if desig_input == "2":
        return "Manager"
    if desig_input == "3":
        return "Employee"
    if desig_input == "4":
        return "CA"
    if desig_input == "5":
        return "Trainee"


def employee_management_menu():
    while True:
        print("Employee Management Menu:")
        print("1. Add Employee")
        print("2. Fire Employee")
        print("3. Search Employee")
        print("4. Show Present Count")
        print("5. Show Employee attendance report")
        print("6. Back to Admin Menu")
        emp_mgmt_choice = input("Choose an option: ")

        if emp_mgmt_choice == "1":
            add_employee(
                input("Employee ID: "),
                input("Name: "),
                input("Password: "),
                show_designation_menu(),
            )
        elif emp_mgmt_choice == "2":
            remove_employee(input("Employee ID: "))
        elif emp_mgmt_choice == "3":
            search_employee(input("Employee ID: "))
        elif emp_mgmt_choice == "4":
            show_present_count(present_count)
        elif emp_mgmt_choice == "5":
            generate_employee_report(input("Employee ID: "))
        elif emp_mgmt_choice == "6":
            break
        else:
            print("Invalid choice.")


def admin_leave_menu():
    while True:
        print("Admin Leave Menu:")
        print("1. View All Leave Requests")
        print("2. View Pending Leave Requests")
        print("3. Accept Leave Request")
        print("4. Reject Leave Request")
        print("5. Back to Admin Menu")
        leave_choice = input("Choose an option: ")

        if leave_choice == "1":
            view_leave_status()
        elif leave_choice == "2":
            view_pending_leave_requests()
        elif leave_choice == "3":
            change_leave_status(
                input("Enter Employee ID: "),
                input("Enter Leave Start Date (YYYY-MM-DD): "),
                "Accepted",
            )
        elif leave_choice == "4":
            change_leave_status(
                input("Enter Employee ID: "),
                input("Enter Leave Start Date (YYYY-MM-DD): "),
                "Rejected",
            )
        elif leave_choice == "5":
            break
        else:
            print("Invalid choice.")


def admin_menu():
    while True:
        print("Admin Menu:")
        print("1. Employee Management")
        print("2. Show All Data")
        print("3. Mark Absents")
        print("4. Manage Leave Requests")
        print("5. Export monthly payrole and attendance record")
        print("6. View monthly payrole")
        print("7. View old attendance data")
        print("8. View old pay roll data")
        print("9 . Logout")
        admin_choice = input("Enter your choice (1-5): ")

        if admin_choice == "1":
            employee_management_menu()
        elif admin_choice == "2":
            show_all_data()
        elif admin_choice == "3":
            mark_absent()
            run_daily_operations()
        elif admin_choice == "4":
            admin_leave_menu()
        elif admin_choice == "5":
            export_monthly_payroll_and_attendance()
        elif admin_choice == "6":
            view_all_payroll()
        elif admin_choice == "7":
            read_attendance_and_display()
        elif admin_choice == "8":
            read_payroll_and_display()
        elif admin_choice == "9":
            break
        else:
            print("Invalid choice.")


# Calling and loading of data.
attendance_data = {}
employee_data = {}
leave_requests = []
present_count = load_present_count()

load_attendance_data()
load_employee_data()
load_leave_requests()
base_salaries = {
    "CEO": 4838,
    "Manager": 3225,
    "Employee": 1612,
    "CA": 2258,
    "Trainee": 967,
}
# Main menu
while True:
    print("Employee Attendance Tracker")
    print("1. Employee Login")
    print("2. Admin Options")
    print("3. Exit")
    choice = input("Choose an option: ")

    if choice == "1":
        employee_id = input("Employee ID: ")
        if employee_id not in employee_data:
            print("Invalid ID.")
            continue
        password = input("Password: ")
        if password != employee_data[employee_id]["Password"]:
            print("Incorrect password.")
            continue

        print(f"Welcome, {employee_data[employee_id]['Name']}!")
        # Employee Menu
        while True:
            print("1. Clock In")
            print("2. Clock Out")
            print("3. Apply for Leave")
            print("4. View Leave Status")
            print("5. View Attendance History")
            print("6. View Payroll  History")
            print("7. Logout")
            emp_choice = input("Choose an option: ")

            if emp_choice == "1":
                present_count = clock_in(employee_id, password, present_count)
            elif emp_choice == "2":
                present_count = clock_out(employee_id, password, present_count)
            elif emp_choice == "3":
                apply_leave(employee_id)
            elif emp_choice == "4":
                view_employee_leave_status(employee_id)
            elif emp_choice == "5":
                view_attendance_history(employee_id)
            elif emp_choice == "6":
                view_employee_payroll(employee_id)
            elif emp_choice == "7":
                break
            else:
                print("Invalid choice.")

    elif choice == "2":
        admin_password = input("Enter Admin Password: ")
        if admin_password != "admin123":
            print("Incorrect password.")
            continue
        admin_menu()
    elif choice == "3":
        break
    else:
        print("Invalid choice.")
