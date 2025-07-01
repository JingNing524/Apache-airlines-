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
            print("→ Check seat (to be implemented)\n")
        elif choice == '2':
            print("→ Book seat (to be implemented)\n")
        elif choice == '3':
            print("→ Free seat (to be implemented)\n")
        elif choice == '4':
            display_seat_layout()
        elif choice == '5':
            print("Exiting program.\n")
            break
        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main_menu()
