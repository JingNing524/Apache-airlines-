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

print(display_seat_layout())