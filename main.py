import os
import sys
from db_manager import init_db
from business import (
    create_business, list_businesses, remove_business,
    record_transaction, select_business, view_dashboard
)
from reports import generate_full_report, break_even_calculator

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    clear()
    print("=" * 50)
    print("     💼 BIZCALC PRO - Business Finance Suite")
    print("=" * 50)
    print("1.  🏢 Manage Businesses")
    print("2.  💰 Record Investment")
    print("3.  📈 Record Revenue")
    print("4.  📉 Record Expense")
    print("5.  📊 View Dashboard")
    print("6.  📄 Generate Report")
    print("7.  🔧 Break-Even Calculator")
    print("8.  🚪 Exit")
    print("=" * 50)
    return input("Select option (1-8): ").strip()

def manage_businesses():
    while True:
        print("\n🏢 BUSINESS MANAGEMENT")
        print("1. Create Business")
        print("2. List Businesses")
        print("3. Delete Business")
        print("4. Back")
        choice = input("Select: ").strip()
        
        if choice == '1':
            create_business()
        elif choice == '2':
            list_businesses()
        elif choice == '3':
            remove_business()
        elif choice == '4':
            break
        input("\nPress Enter to continue...")

def main():
    init_db()
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            manage_businesses()
        
        elif choice == '2':
            bid = select_business()
            if bid:
                record_transaction(bid, 'investment')
                input("\nPress Enter to continue...")
        
        elif choice == '3':
            bid = select_business()
            if bid:
                record_transaction(bid, 'revenue')
                input("\nPress Enter to continue...")
        
        elif choice == '4':
            bid = select_business()
            if bid:
                record_transaction(bid, 'expense')
                input("\nPress Enter to continue...")
        
        elif choice == '5':
            bid = select_business()
            if bid:
                view_dashboard(bid)
                input("\nPress Enter to continue...")
        
        elif choice == '6':
            bid = select_business()
            if bid:
                from db_manager import get_connection
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM businesses WHERE id = ?", (bid,))
                name = cursor.fetchone()[0]
                conn.close()
                generate_full_report(bid, name)
                input("\nPress Enter to continue...")
        
        elif choice == '7':
            break_even_calculator()
            input("\nPress Enter to continue...")
        
        elif choice == '8':
            print("👋 Goodbye!")
            sys.exit(0)
        
        else:
            print("❌ Invalid option.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()