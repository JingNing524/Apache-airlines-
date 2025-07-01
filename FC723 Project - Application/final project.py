#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 10:48:12 2025

@author: jninggggggh
"""

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
        
#book a seat
def book_seat():
    seat_id = input("Enter seat ID to book (e.g., A0): ").upper()
    
    if len(seat_id) != 2 or not seat_id[0].isalpha() or not seat_id[1].isdigit():
        print("Invalid seat ID format.\n")
        return
    
    row_char = seat_id[0]
    col_index = int(seat_id[1])
    row_index = ord(row_char) - ord('A')

    #check if the seat is in the right area
    if row_index < 0 or row_index >= len(seat_matrix) or col_index < 0 or col_index >= len(seat_matrix[0]):
        print("Seat ID out of range.\n")
        return

    current_status = seat_matrix[row_index][col_index]
    
    if current_status == 'F':
        seat_matrix[row_index][col_index] = 'R'  #change it to already book
        print(f"✅ Seat {seat_id} booked successfully!\n")
    elif current_status == 'R':
        print(f"❌ Seat {seat_id} is already reserved.\n")
    elif current_status == 'X':
        print(f"❌ Seat {seat_id} is an aisle. You cannot book it.\n")
    elif current_status == 'S':
        print(f"❌ Seat {seat_id} is storage. You cannot book it.\n")


#free a seat
def free_seat():
    seat_id = input("Enter seat ID to free (e.g., A0): ").upper()
    
    if len(seat_id) != 2 or not seat_id[0].isalpha() or not seat_id[1].isdigit():
        print("Invalid seat ID format.\n")
        return
    
    row_char = seat_id[0]
    col_index = int(seat_id[1])
    row_index = ord(row_char) - ord('A')

    #check seat area
    if row_index < 0 or row_index >= len(seat_matrix) or col_index < 0 or col_index >= len(seat_matrix[0]):
        print("Seat ID out of range.\n")
        return

    status = seat_matrix[row_index][col_index]
    
    if status == 'R':
        seat_matrix[row_index][col_index] = 'F'  #change back to aviliably
        print(f"✅ Seat {seat_id} is now free.\n")
    elif status == 'F':
        print(f"ℹ️ Seat {seat_id} is already free.\n")
    elif status == 'X':
        print(f"❌ Seat {seat_id} is an aisle. It was never reservable.\n")
    elif status == 'S':
        print(f"❌ Seat {seat_id} is storage. It was never reservable.\n")



if __name__ == "__main__":
    main_menu()
