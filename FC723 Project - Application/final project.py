#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 18:24:31 2025

@author: jninggggggh
"""
#this script implements a simple console-based seat booking system using SQLite for persistent storage of reservations.
import sqlite3 # SQLite database API
import random  # Random generation for booking reference codes
import string  # String constants for reference code generation
import re      # Regular expressions for input validation

# connect SQLite 
conn = sqlite3.connect("booking.db")
cursor = conn.cursor()  # Cursor object for executing SQL commands


cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    reference TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    passport TEXT,
    seat_id TEXT UNIQUE
)
''')
conn.commit()   # Save changes to the database


# F = Free 
# R = Reserved 
# X = Aisle 
# S = Storage 

seat_matrix = [
    ['F', 'F', 'X', 'F', 'F'],
    ['F', 'S', 'X', 'S', 'F'],
    ['F', 'F', 'X', 'F', 'F'],
]

def is_valid_seat_format(seat_id):
    
    # Ensure the basic pattern: one uppercase letter followed by one or more digits
    if not re.match(r"^[A-Z]\d+$", seat_id):
        return False

    # Convert the row letter to a zero-based index
    row_char = seat_id[0]
    row_index = ord(row_char) - ord('A')
    # Number part of seat ID (column) is not fully validated here
    return row_index < len(seat_matrix)

 


# show the floor plan of Burak757
def display_seat_layout():
    print("\nSeat Layout:")

    
    header = "   " + " ".join([str(i + 1) for i in range(len(seat_matrix[0]))])
    print(header)

    
    for i, row in enumerate(seat_matrix):
        row_label = chr(65 + i)  # A, B, C...
        print(row_label + '  ' + ' '.join(row))
    print()


#main menu
def main_menu():
    while True:
        
        print("=== Seat Booking System ===")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Search by booking reference")
        print("6. Show booking summary")
        print("7. Exit program")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            check_availability()
        elif choice == '2':
            book_seat()
        elif choice == '3':
            free_seat()
        elif choice == '4':
            display_seat_layout()
        elif choice == '5':
            search_by_reference()
        elif choice == '6':
            show_booking_summary()
        elif choice == '7':
            print("Exiting program. Goodbye!")
            break



#check the availability of user's seat
def check_availability():
    seat_id = input("Enter seat ID to check (e.g., A0): ").upper()
    
    if not is_valid_seat_format(seat_id):
        print("Invalid seat ID format. Please use something like A1, B2, C5.")
        return

    
    row_char = seat_id[0]
    col_index = int(seat_id[1:]) - 1
    row_index = ord(row_char) - ord('A')

    #check if it is in the area of the floor plan
    if row_index < 0 or row_index >= len(seat_matrix) or col_index < 0 or col_index >= len(seat_matrix[0]):
        print("Seat ID out of range.\n")
        return

    status = seat_matrix[row_index][col_index]
    
    if status == 'F':
        print(f"✅ Seat {seat_id} is **available**.\n")
    elif status == 'R':
        print(f"❌ Seat {seat_id} is **already reserved**.\n")
    elif status == 'X':
        print(f"❌ Seat {seat_id} is an aisle. Not a bookable seat.\n")
    elif status == 'S':
        print(f"❌ Seat {seat_id} is storage. Not a bookable seat.\n")
        

# generate the unique 8 words reference
def generate_booking_reference():
    while True:
        
        #randomly choose 8 characters from uppercase letters and digits
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        #check if the reference already exists in the database
        cursor.execute("SELECT * FROM bookings WHERE reference = ?", (ref,))
       
        #if not found in database, it's unique → return it
        if cursor.fetchone() is None:
            return ref


#book a seat
def book_seat():
    seat_id = input("Enter seat ID to book (e.g., A0): ").upper()

    if not is_valid_seat_format(seat_id):
        print("Invalid seat ID format. Please use something like A1, B2, C5.")
        return


    row_char = seat_id[0]
    col_index = int(seat_id[1:]) - 1
    row_index = ord(row_char) - ord('A')

    if row_index < 0 or row_index >= len(seat_matrix) or col_index < 0 or col_index >= len(seat_matrix[0]):
        print("Seat ID out of range.\n")
        return

    current_status = seat_matrix[row_index][col_index]

    if current_status != 'F':
        print(f"❌ Seat {seat_id} is not available for booking.\n")
        return

    #enter the info 
    first = input("Enter first name: ")
    last = input("Enter last name: ")
    passport = input("Enter passport number: ")

    # generate unique booking reference
    ref = generate_booking_reference()

    #update floor plan
    seat_matrix[row_index][col_index] = 'R'

    #enter SQLite
    cursor.execute('''
        INSERT INTO bookings (reference, first_name, last_name, passport, seat_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (ref, first, last, passport, seat_id))
    conn.commit()

    print(f"✅ Seat {seat_id} booked successfully! Booking reference: {ref}\n")



#free a seat
def free_seat():
    seat_id = input("Enter seat ID to free (e.g., A0): ").upper()

    if not is_valid_seat_format(seat_id):
        print("Invalid seat ID format. Please use something like A1, B2, C5.")
        return


    row_char = seat_id[0]
    col_index = int(seat_id[1:]) - 1
    row_index = ord(row_char) - ord('A')

    if row_index < 0 or row_index >= len(seat_matrix) or col_index < 0 or col_index >= len(seat_matrix[0]):
        print("Seat ID out of range.\n")
        return

    if seat_matrix[row_index][col_index] != 'R':
        print(f"❌ Seat {seat_id} is not reserved.\n")
        return

    #delete the infro from store
    cursor.execute("DELETE FROM bookings WHERE seat_id = ?", (seat_id,))
    conn.commit()

    #update floor plan
    seat_matrix[row_index][col_index] = 'F'
    print(f"✅ Seat {seat_id} is now free.\n")

#search booking reference
def search_by_reference():
    ref = input("Enter booking reference (8 characters): ").upper()

    if len(ref) != 8:
        print("Booking reference must be 8 characters long.\n")
        return

    cursor.execute("SELECT * FROM bookings WHERE reference = ?", (ref,))
    result = cursor.fetchone()

    if result:
        print("\nBooking Found:")
        print(f"Reference: {result[0]}")
        print(f"Name     : {result[1]} {result[2]}")
        print(f"Passport : {result[3]}")
        print(f"Seat     : {result[4]}\n")
    else:
        print("❌ Booking reference not found.\n")

# summarize recent booking status
def show_booking_summary():
    total_reserved = 0
    total_free = 0
    total_unbookable = 0  # X + S

    for row in seat_matrix:
        for seat in row:
            if seat == 'R':
                total_reserved += 1
            elif seat == 'F':
                total_free += 1
            elif seat in ('X', 'S'):
                total_unbookable += 1

    print("\n📊 Booking Summary:")
    print(f"✅ Reserved seats    : {total_reserved}")
    print(f"🪑 Available seats   : {total_free}")
    print(f"❌ Not bookable (X/S): {total_unbookable}\n")



if __name__ == "__main__":
     main_menu()
     conn.close()