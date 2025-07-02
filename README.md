# Hotel-Management

## Overview

This is a desktop-based hotel management application built using Python (Tkinter) and SQLite3. It is designed to help staff manage room availability, reservations, and password-protected access to admin features.

## Specifications
###  Functional Specifications
1. Room Management

    - The system manages five room types:

        - A01–A12: Standard (₤50)

        - B01–B11: Deluxe (₤75)

        - C01–C10: Executive (₤125)

        - D01–D09: Suit (₤250)

        - E01–E08: Presidential Suite (₤445)

    - Each room has a status: Available or Occupied.

2. Authentication

    - A password system restricts access to administrative features.

    - Passwords are hashed using SHA-256 and stored in a SQLite table.

    - Users can change their password by verifying the old one.

3. Revenue Reporting

    - Users can select a start and end date.

    - The system fetches and displays revenue data for the selected period.

    - Data is presented in a scrollable table (Treeview).

4. Database Initialization

    - On first launch, the system populates the database with all room records.

    - The default password is admin.

### Technical Specifications

| Item                 | Specification                                            |
| -------------------- | -------------------------------------------------------- |
| **Language**         | Python 3.x                                               |
| **GUI Toolkit**      | Tkinter (Standard Python Library)                        |
| **Database**         | SQLite3                                                  |
| **Password Hashing** | SHA-256 via `hashlib`                                    |
| **Data Display**     | `ttk.Treeview` (with vertical scrollbar)                 |
| **Report Data**      | Retrieved via custom SQL queries and parsed using Pandas |
| **Room IDs**         | Fixed-format IDs (e.g., A01, B05, etc.)                  |

## Dependencies
| Dependency                 | Purpose                                             | Installation / Availability                          |
| -------------------------- | --------------------------------------------------- | ---------------------------------------------------- |
| **Python 3.x**             | Core programming language                           | [Download Python](https://www.python.org/downloads/) |
| **Tkinter**                | GUI framework for creating windows, buttons, inputs | Included with standard Python install                |
| **SQLite3**                | Lightweight local database system                   | Built-in Python module (`sqlite3`)                   |
| **hashlib**                | Used for password hashing (SHA-256)                 | Built-in Python module                               |
| **pandas**                 | For handling and displaying tabular data            | `pip install pandas`                                 |
| **ttk** (from tkinter)     | Used for `Treeview` widget in GUI                   | Included with Tkinter                                |
| **tkcalendar** *(if used)* | For date selection widgets (e.g., `DateEntry`)      | `pip install tkcalendar`                             |

