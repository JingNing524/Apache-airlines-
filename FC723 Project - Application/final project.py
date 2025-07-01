#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 10:48:12 2025

@author: jninggggggh
"""
import sqlite3
import random
import string

# connect SQLite 
conn = sqlite3.connect("booking.db")
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    reference TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    passport TEXT,
    seat_id TEXT
)
''')
conn.commit()







# F = Free 
# R = Reserved 
# X = Aisle 
# S = Storage 

seat_matrix = [
    ['F', 'F', 'X', 'F', 'F'],
    ['F', 'S', 'X', 'S', 'F'],
    ['F', 'F', 'X', 'F', 'F'],
]

# show the floor plan of Burak757
def display_seat_layout():
    print("\nSeat Layout:")
    for i, row in enumerate(seat_matrix):
        row_label = chr(65 + i)  #0 → A，1 → B, 2 → C
        print(row_label + ' ' + ' '.join(row))
    print()

#main menu
def main_menu():
    while True:
        print("=== Seat Booking System ===")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Exit program")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            check_availability()
        elif choice == '2':
            book_seat()
        elif choice == '3':
            free_seat()
        elif choice == '4':
            display_seat_layout()
        elif choice == '5':
            print("Exiting program.\n")
            break
        else:
            print("Invalid choice.\n")


#check the availability of user's seat
def check_availability():
    seat_id = input("Enter seat ID to check (e.g., A0): ").upper()
    
    if len(seat_id) != 2 or not seat_id[0].isalpha() or not seat_id[1].isdigit():
        print("Invalid seat ID format. Please use format like A0, B2, etc.\n")
        return
    
    row_char = seat_id[0]
    col_index = int(seat_id[1])
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
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        cursor.execute("SELECT * FROM bookings WHERE reference = ?", (ref,))
        if cursor.fetchone() is None:
            return ref


#book a seat
def book_seat():
    seat_id = input("Enter seat ID to book (e.g., A0): ").upper()

    if len(seat_id) != 2 or not seat_id[0].isalpha() or not seat_id[1].isdigit():
        print("Invalid seat ID format.\n")
        return

    row_char = seat_id[0]
    col_index = int(seat_id[1])
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

    if len(seat_id) != 2 or not seat_id[0].isalpha() or not seat_id[1].isdigit():
        print("Invalid seat ID format.\n")
        return

    row_char = seat_id[0]
    col_index = int(seat_id[1])
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




if __name__ == "__main__":
    main_menu()
