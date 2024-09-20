# Imprting all the library
import csv
import datetime
from prettytable import PrettyTable
import os
import streamlit as st
import pandas as pd

# Side Functions:
def current_Date():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def current_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# For the Employee total count:
def update_present_count(count, change):
    try:
        count = int(count)
        change = int(change)
        
        value = count + change
        
        save_present_count(value)
        
        return value
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
        return None


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
    st.write(f"Total employee present right now is : {value}")


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
        return "Over Time"
    else:
        return "Full Day"
        
def show_all_data():
    # Display attendance data
    attendance_df = pd.DataFrame.from_dict(
        attendance_data, orient='index', columns=['Clock In', 'Clock Out']
    ).reset_index().rename(columns={'index': 'ID'})
    
    st.subheader("Attendance Data")
    st.write(attendance_df)

    # Display employee data
    employee_df = pd.DataFrame.from_dict(
        employee_data, orient='index', columns=['Name', 'Password', 'Designation']
    ).reset_index().rename(columns={'index': 'ID'})
    
    st.subheader("Employee Data")
    st.write(employee_df)

    # Display attendance record from CSV
    try:
        with open("attendance_record.csv", "r") as file:
            reader = csv.DictReader(file)
            record_df = pd.DataFrame(reader)
            st.subheader("Attendance Record")
            st.write(record_df)
    except FileNotFoundError:
        st.error("ATTENDANCE FILE IS NOT THERE.")



def generate_employee_report(employee_id):
    if employee_id not in employee_data:
        st.error("Invalid Employee ID.")
        return

    report = f"Report for Employee ID: {employee_id}\n"
    report += f"Name: {employee_data[employee_id]['Name']}\n"
    report += "Attendance History:\n"

    attendance_history = view_attendance_history(employee_id)
    if attendance_history:
        report += attendance_history + "\n"
    else:
        report += "No attendance history available.\n"

    st.text(report) 

def view_employee_payroll(employee_id):
    payroll_data = pd.read_csv('temp.csv')

    employee_payroll = payroll_data[payroll_data['Employee ID'] == int(employee_id)]

    if employee_payroll.empty:
        st.write(f"No payroll data found for employee ID: {employee_id}")
    else:
        st.table(employee_payroll)  
        
# Clock in and clock out functions:
def clock_in(employee_id,  present_count):
    if employee_id not in employee_data:
        st.error("Invalid Employee ID.")
        return present_count
    
    if employee_id in attendance_data:
        clock_out_time = attendance_data[employee_id].get("Clock Out", "").strip()
        clock_in_time = attendance_data[employee_id].get("Clock In", "").strip()

        if clock_in_time != "" and clock_out_time != "":
            attendance_data[employee_id]["Clock In"] = current_timestamp()
            save_attendance_data()
            st.success("Clocked in.")
            present_count = update_present_count(present_count, 2)  # Assuming 2 clicks
        else:
            st.warning("Already clocked in.")
    else:
        attendance_data[employee_id] = {
            "Clock In": current_timestamp(),
            "Clock Out": "",
        }
        save_attendance_data()
        st.success("Clocked in.")
        present_count = update_present_count(present_count, 2)  # Assuming 2 clicks

    return present_count

def clock_out(employee_id, present_count):
    if employee_id not in employee_data:
        st.error("Invalid Employee ID.")
        return present_count

    if employee_id in attendance_data:
        clock_in_time = attendance_data[employee_id].get("Clock In", "").strip()
        clock_out_time = attendance_data[employee_id].get("Clock Out", "").strip()

        if clock_in_time != "" and clock_out_time == "":
            attendance_data[employee_id]["Clock Out"] = current_timestamp()
            save_attendance_data()
            update_attendance_record(employee_id)
            st.success("Clocked out.")
            present_count = update_present_count(present_count, -1)
        elif clock_in_time == "":
            st.warning("Not clocked in yet.")
        else:
            attendance_data[employee_id]["Clock Out"] = current_timestamp()
            save_attendance_data()
            update_attendance_record(employee_id)
            st.success("Clocked out")
    else:
        st.error("No clock-in record found.")

    return present_count


# Functions to view old data:
def read_attendance_and_display():
    user_input = st.text_input("Enter the prefix for the attendance file (e.g., '2024-08'):", "")
    if user_input:
        filename = user_input + "_attendance.csv"
        try:
            with open(filename, mode="r") as file:
                csv_reader = csv.DictReader(file)
                df = pd.DataFrame(csv_reader)
                st.subheader("Attendance Data")
                st.write(df)
        except FileNotFoundError:
            st.error(f"Error: The file '{filename}' was not found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")


def read_payroll_and_display():
    user_input = st.text_input("Enter the prefix for the payroll file (e.g., '2024-08'):", "")
    if user_input:
        filename = user_input + "_payroll.csv"
        try:
            with open(filename, mode="r") as file:
                csv_reader = csv.DictReader(file)
                df = pd.DataFrame(csv_reader)
                st.subheader("Payroll Data")
                st.write(df)
        except FileNotFoundError:
            st.error(f"Error: The file '{filename}' was not found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")


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
        st.write("Employee removed.")
    else:
        st.write("Employee ID not found.")


def search_employee(employee_id):
    if employee_id in employee_data:
        info = employee_data[employee_id]
        att = attendance_data.get(employee_id, {"Clock In": "", "Clock Out": ""})
        st.write(f"ID: {employee_id}, Name: {info['Name']}")
        st.write(f"Clock In: {att['Clock In']}, Clock Out: {att['Clock Out']}")
    else:
       st.write("Employee ID not found.")

def update_employee_data(file_path, emp_id, field, new_value):
    field_index = {
        'Name': 1,
        'Password': 2,
        'Designation': 3
    }

    if field not in field_index:
        return "Invalid field. Please choose from 'Name', 'Password', or 'Designation'."

    updated = False
    rows = []

    # Open the file and read the data
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            if row[0] == str(emp_id): 
                row[field_index[field]] = new_value
                updated = True
            rows.append(row)

    if not updated:
        return f"Employee ID {emp_id} not found."

    # Write the updated data back to the file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(rows)    # Write updated rows

    return f"Employee ID {emp_id} updated successfully."

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
    st.subheader("Mark Absent")

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
        if emp_id not in existing_records or existing_records[emp_id]["Clock In"] == "":
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
                        )
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

    st.success("Attendance records updated.") 

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
                st.subheader(f"Attendance History for Employee ID: {employee_id}")
                st.write(history_table)
            else:
                st.write("No attendance records found for this employee.")
    except FileNotFoundError:
        st.error("Attendance record file not found.")


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
                st.subheader(f"Leave Status for Employee ID: {employee_id}")
                st.write(leave_table)
            else:
                st.write("No leave records found for this employee.")
    except FileNotFoundError:
        st.error("Leave requests file not found.")

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

            if leave_table.rows:
                st.subheader("Pending Leave Requests")
                st.write(leave_table)
            else:
                st.write("No pending leave requests found.")
    except FileNotFoundError:
        st.write("Leave requests file not found.")

def view_leave_status():
    try:
        df = pd.read_csv("leave_requests.csv")

        if not df.empty:
            st.subheader("All Leave Requests")
            st.table(df)  # Displaying the DataFrame as a nicely formatted table
        else:
            st.write("No leave requests found.")
    except FileNotFoundError:
        st.error("Leave requests file not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def change_leave_status(employee_id, start_date, status):
    try:
        with open("leave_requests.csv", "r") as file:
            reader = csv.DictReader(file)
            leave_requests = list(reader)

        updated = False
        for leave in leave_requests:
            if leave["Employee ID"] == employee_id and leave["Start Date"] == start_date:
                leave["Status"] = status
                updated = True
                break

        if updated:
            with open("leave_requests.csv", "w", newline="") as file:
                fieldnames = [
                    "Employee ID",
                    "Start Date",
                    "End Date",
                    "Reason",
                    "Status",
                    "Type_of_Leave",
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(leave_requests)

            st.success(f"Leave request {status.lower()}ed.")
        else:
            st.error("Leave request not found.")
    except FileNotFoundError:
        st.error("Leave requests file not found.")



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
    try:
        with open("leave_requests.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                leave_requests.append(row)
    except FileNotFoundError:
        st.warning("No leave requests file found.")

def apply_leave(employee_id):
    st.subheader("Apply for Leave")

    leave_type_choice = st.radio(
        "Choose the type of leave:",
        options=["Paid Leave", "Sick Leave", "Unpaid Leave"],
    )

    start_date = st.date_input("Enter leave start date:", value=datetime.date.today())
    end_date = st.date_input("Enter leave end date:", value=datetime.date.today())
    reason = st.text_area("Enter the reason for leave:")

    if st.button("Submit Leave Request"):
        if start_date > end_date:
            st.error("End date cannot be before start date.")
        elif not reason:
            st.error("Please enter a reason for the leave.")
        else:
            leave_requests.append(
                {
                    "Employee ID": employee_id,
                    "Start Date": start_date.strftime("%Y-%m-%d"),
                    "End Date": end_date.strftime("%Y-%m-%d"),
                    "Reason": reason,
                    "Type_of_Leave": leave_type_choice,
                    "Status": "Pending",
                }
            )
            save_leave_requests()
            st.success("Leave request submitted successfully.")



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


def view_all_payroll():
    try:
        payroll_data = pd.read_csv("temp.csv")
        payroll_data["Overtime Hours"] = payroll_data["Overtime Hours"].fillna("N/A")
        st.table(payroll_data)
    except FileNotFoundError:
        st.write("The file 'temp.csv' does not exist.")


# Menu functions:
def employee_management_menu():
    # Initialize session state if it doesn't exist
    if "menu_state" not in st.session_state:
        st.session_state.menu_state = "main"

    if st.session_state.menu_state == "main":
        st.title("Employee Management Menu")

        menu_option = st.selectbox(
            "Choose an option:",
            ["Select an option", "Add Employee", "Fire Employee","Update Data", "Search Employee", 
             "Show Present Count", "Show Employee Attendance Report", ]
        )

        if menu_option == "Add Employee":
            st.session_state.menu_state = "add_employee"
            st.rerun()

        elif menu_option == "Fire Employee":
            st.session_state.menu_state = "fire_employee"
            st.rerun()
        
        elif menu_option=="Update Data":
            if st.button("Update data"):
                st.session_state.menu_state = "update_Data"

        elif menu_option == "Search Employee":
            st.session_state.menu_state = "search_employee"
            st.rerun()

        elif menu_option == "Show Present Count":
            st.session_state.menu_state = "present_count"
            st.rerun()

        elif menu_option == "Show Employee Attendance Report":
            st.session_state.menu_state = "attendance_report"
            st.rerun()
    elif st.session_state.menu_state == "add_employee":
        st.subheader("Add Employee")
        emp_id = st.text_input("Employee ID", key="add_emp_id")
        name = st.text_input("Name", key="add_name")
        password = st.text_input("Password", type="password", key="add_password")
        designation = st.selectbox("Designation", ["Manager", "Employee", "CEO", "CA", "Other"], key="add_designation")

        if st.button("Add Employee", key="add_employee_button"):
            add_employee(emp_id, name, password, designation)
            st.success("Employee added successfully!")
            st.session_state.menu_state = "main"
            st.rerun()

    elif st.session_state.menu_state == "fire_employee":
        st.subheader("Fire Employee")
        emp_id = st.text_input("Employee ID", key="fire_emp_id")
        
        if st.button("Fire Employee", key="fire_employee_button"):
            remove_employee(emp_id)
            st.success("Employee removed successfully!")
            st.session_state.menu_state = "main"
            st.rerun()

    elif st.session_state.menu_state== "update_Data":
        emp_id = st.text_input('Enter Employee ID:')
        field = st.selectbox('Select Field to Update:', ['Name', 'Password', 'Designation'])
        new_value = st.text_input(f'Enter New {field}:')
        
        if st.button('Update Employee Data'):
            if emp_id and new_value:
                result = update_employee_data("employees.csv", emp_id, field, new_value)
                st.success(result)
            else:
                st.error('Please fill in all fields.')
        if st.button("Return to main menu"):
            st.session_state.menu_state = "main"
            st.rerun()

    elif st.session_state.menu_state == "search_employee":
        st.subheader("Search Employee")
        emp_id = st.text_input("Employee ID", key="search_emp_id")
        
        if st.button("Search Employee", key="search_employee_button"):
            search_employee(emp_id)
            st.session_state.menu_state = "main"


    elif st.session_state.menu_state == "present_count":
        st.subheader("Show Present Count")
        st.write(f"Present count: {present_count}")
        st.session_state.menu_state = "main"
        if st.button("Go back to main menu",key="returning_button2"):
                st.rerun()

    elif st.session_state.menu_state == "attendance_report":
        st.subheader("Show Employee Attendance Report")
        employee_id = st.text_input("Employee ID", key="report_emp_id")
        
        if st.button("Generate Report", key="generate_report_button"):
            generate_employee_report(employee_id)
            st.session_state.menu_state = "main"
            if st.button("Go back to main menu",key="returning_button3"):
                st.rerun()

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
# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'employee_id' not in st.session_state:
    st.session_state.employee_id = None
if 'present_count' not in st.session_state:
    st.session_state.present_count = {emp_id: 0 for emp_id in employee_data}
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Main menu
st.title("Employee Managment Tracker🧑")
st.subheader("Your Gateway to Efficient Employee Management")

if st.session_state.logged_in:
    if st.session_state.is_admin:
        admin_choice = st.selectbox("Admin Menu", [
            "Employee Management", "Show All Data", "Mark Absents(Run at end of the day)",
            "Manage Leave Requests", "Export Monthly Payroll and Attendance",
            "View Monthly Payroll", "View Old Attendance Data",
            "View Old Payroll Data", "Logout"
        ])

        if admin_choice == "Employee Management":
            employee_management_menu()
        elif admin_choice == "Show All Data":
            show_all_data()
        elif admin_choice == "Mark Absents(Run at end of the day)":
            if st.button("Mark Attendance for the day"):
                mark_absent()
                run_daily_operations()
        elif admin_choice == "Manage Leave Requests":
            leave_choice = st.selectbox("Admin Leave Menu", [
                "View All Leave Requests", "View Pending Leave Requests", 
                "Accept Leave Request", "Reject Leave Request", "Back to Admin Menu"
            ])

            if leave_choice == "View All Leave Requests":
                view_leave_status()
            elif leave_choice == "View Pending Leave Requests":
                view_pending_leave_requests()
            elif leave_choice == "Accept Leave Request":
                emp_id = st.text_input("Enter Employee ID:")
                start_date = st.text_input("Enter Leave Start Date (YYYY-MM-DD):")
                if st.button("Accept Leave Request"):
                    change_leave_status(emp_id, start_date, "Accepted")
            elif leave_choice == "Reject Leave Request":
                emp_id = st.text_input("Enter Employee ID:")
                start_date = st.text_input("Enter Leave Start Date (YYYY-MM-DD):")
                if st.button("Reject Leave Request"):
                    change_leave_status(emp_id, start_date, "Rejected")
            elif leave_choice == "Back to Admin Menu":
                st.session_state.logged_in = False
                st.session_state.is_admin = False
                st.session_state.employee_id = None
                st.session_state.present_count = {emp_id: 0 for emp_id in employee_data}
                st.rerun()
        elif admin_choice == "Export Monthly Payroll and Attendance":
            export_monthly_payroll_and_attendance()
            st.success("Attendance data and Pay roll data has been exported.")
        elif admin_choice == "View Monthly Payroll":
            view_all_payroll()
        elif admin_choice == "View Old Attendance Data":
            read_attendance_and_display()
        elif admin_choice == "View Old Payroll Data":
            read_payroll_and_display()
        elif admin_choice == "Logout":
            st.session_state.logged_in = False
            st.session_state.is_admin = False
            st.session_state.employee_id = None
            st.session_state.present_count = {emp_id: 0 for emp_id in employee_data}
            st.info("Logged out.")
            st.rerun()

    else:
        #st.success(f"Welcome, {employee_data[employee_id]['Name']}!")
        emp_choice = st.selectbox("Employee Menu", [
            "Clock In", "Clock Out", "Apply for Leave", 
            "View Leave Status", "View Attendance History", 
            "View Payroll History", "Logout"
        ])

        if emp_choice == "Clock In":
            if st.button("Submit Clock In"):
                clock_in(st.session_state.employee_id, st.session_state.present_count)
        elif emp_choice == "Clock Out":
            if st.button("Submit Clock Out"):
                clock_out(st.session_state.employee_id,  st.session_state.present_count)
        elif emp_choice == "Apply for Leave":
            apply_leave(st.session_state.employee_id)
        elif emp_choice == "View Leave Status":
            view_employee_leave_status(st.session_state.employee_id)
        elif emp_choice == "View Attendance History":
            view_attendance_history(st.session_state.employee_id)
        elif emp_choice == "View Payroll History":
            view_employee_payroll(st.session_state.employee_id)
        elif emp_choice == "Logout":
            st.session_state.logged_in = False
            st.session_state.employee_id = None
            st.session_state.present_count = {emp_id: 0 for emp_id in employee_data}
            st.info("Logged out.")
            st.rerun()

else:
    menu_choice = st.selectbox("Main Menu", ["Employee Login", "Admin Options", ])

    if menu_choice == "Employee Login":
        employee_id = st.text_input("Employee ID:")
        password = st.text_input("Password:", type="password")
        if st.button("Login"):
            if employee_id in employee_data and password == employee_data[employee_id]["Password"]:
                st.session_state.logged_in = True
                st.session_state.employee_id = employee_id
                st.rerun()
            elif employee_id not in employee_data:
                st.error("Invalid ID.")
            else:
                st.error("Incorrect password.")

    elif menu_choice == "Admin Options":
        admin_password = st.text_input("Enter Admin Password:", type="password")
        if st.button("Login as Admin"):
            if admin_password == "admin123":
                st.session_state.logged_in = True
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("Incorrect password.")
