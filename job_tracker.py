import pandas as pd
from datetime import datetime
import os
from tabulate import tabulate

FILE = "applications.csv"

# Define the columns
COLUMNS = [
    "Date",
    "Company",
    "Role",
    "Application Method",
    "Contact",
    "Status",
    "Follow-up Date",
    "Notes"
]

# Initialize CSV if it doesn't exist
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=COLUMNS)
    df.to_csv(FILE, index=False)
    print(f"{FILE} created successfully with columns: {', '.join(COLUMNS)}")
else:
    print(f"{FILE} already exists with columns: {', '.join(COLUMNS)}")


def view_applications():
    """View all job applications."""
    df = pd.read_csv(FILE)
    if df.empty:
        print("\nNo applications found.\n")
        return
    
    print("\n=== All Job Applications ===")
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=[i+1 for i in range(len(df))]))
    print("\n============================\n")


def add_application():
    """Add a new job application via terminal and save to CSV."""
    date_applied = input("Enter application date (YYYY-MM-DD) or leave blank for today: ").strip()
    if not date_applied:
        date_applied = datetime.today().date()
    else:
        try:
            date_applied = datetime.strptime(date_applied, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format! Using today's date.")
            date_applied = datetime.today().date()
    
    company = input("Enter company name: ").strip()
    role = input("Enter role: ").strip()
    method = input("Application method (e.g., email, portal): ").strip()
    contact = input("Contact person (optional): ").strip()
    status = input("Status (Applied, Interview, Offer, Rejected): ").strip()
    follow_up = input("Follow-up date (YYYY-MM-DD or leave blank): ").strip()
    if follow_up:
        try:
            follow_up = datetime.strptime(follow_up, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid follow-up date! Leaving blank.")
            follow_up = ""
    notes = input("Notes (optional): ").strip()
    
    df = pd.read_csv(FILE)
    new_row = {
        "Date": date_applied,
        "Company": company,
        "Role": role,
        "Application Method": method,
        "Contact": contact,
        "Status": status,
        "Follow-up Date": follow_up,
        "Notes": notes
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FILE, index=False)
    print(f"\nApplication added: {company} - {role}\n")


def follow_ups_pending():
    """Display applications where the follow-up date is today or earlier."""
    df = pd.read_csv(FILE)
    if df.empty:
        print("\nNo applications found.\n")
        return
    
    df['Follow-up Date'] = pd.to_datetime(df['Follow-up Date'], errors='coerce')
    today = pd.to_datetime(datetime.today().date())
    pending = df[df['Follow-up Date'] <= today]
    
    if pending.empty:
        print("\nNo follow-ups pending today.\n")
        return
    
    print("\n=== Follow-ups Pending ===")
    print(tabulate(pending, headers='keys', tablefmt='fancy_grid', showindex=[i+1 for i in range(len(pending))]))
    print("\n============================\n")

def delete_application():
    """Delete a job application by selecting its displayed number."""
    df = pd.read_csv(FILE)
    if df.empty:
        print("\nNo applications found.\n")
        return

    print("\n=== All Job Applications ===")
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=[i+1 for i in range(len(df))]))

    try:
        # Subtract 1 to match zero-based pandas index
        idx = int(input("\nEnter the number of the application to delete: ").strip()) - 1
        if idx < 0 or idx >= len(df):
            print("Invalid number. No application deleted.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    confirm = input(f"Are you sure you want to delete '{df.loc[idx, 'Company']} - {df.loc[idx, 'Role']}'? (y/n): ").strip().lower()
    if confirm == 'y':
        df = df.drop(idx).reset_index(drop=True)
        df.to_csv(FILE, index=False)
        print("\nApplication deleted successfully.\n")
    else:
        print("\nDeletion cancelled.\n")
   


def application_stats():
    """Show summary statistics of applications, including conversion ratios and pending follow-ups."""
    df = pd.read_csv(FILE)
    if df.empty:
        print("\nNo applications found.\n")
        return

    # Status counts and percentages
    status_counts = df['Status'].value_counts()
    total = len(df)
    stats_table = [[status, count, f"{(count / total * 100):.1f}%"] for status, count in status_counts.items()]

    print("\n=== Application Stats ===")
    print(tabulate(stats_table, headers=["Status", "Count", "Percentage"], tablefmt="fancy_grid"))

    # Conversion ratios
    apps_to_interview = (status_counts.get("Interview", 0) / total) * 100
    apps_to_offer = (status_counts.get("Offer", 0) / total) * 100
    print(f"\nApplications → Interview: {apps_to_interview:.1f}%")
    print(f"Applications → Offer: {apps_to_offer:.1f}%")

    # Pending follow-ups
    df['Follow-up Date'] = pd.to_datetime(df['Follow-up Date'], errors='coerce')
    today = pd.to_datetime(datetime.today().date())
    pending = df[df['Follow-up Date'] <= today]
    print(f"Follow-ups pending today or earlier: {len(pending)}")

    print(f"\nTotal Applications: {total}")
    print("==========================\n")


def main_menu():
    """Main interactive menu for the job tracker."""
    while True:
        print("\n=== Job Application Tracker ===")
        print("1. Add a new application")
        print("2. View all applications")
        print("3. Follow-ups pending")
        print("4. View application stats")
        print("5. Delete an application")  # new option
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_application()
        elif choice == "2":
            view_applications()
        elif choice == "3":
            follow_ups_pending()
        elif choice == "4":
            application_stats()
        elif choice == "5":
            delete_application()  # call new function
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


# Run the menu
if __name__ == "__main__":
    main_menu()
