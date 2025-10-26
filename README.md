# YOUR PROJECT TITLE
#### Video Demo:  <https://youtu.be/5ugyRrexmJ0>
#### Description: Cosmetología SPA Booking App

This project is a full-stack web application (SPA) designed for client booking and an admin managing appointments at a cosmetology spa. It is built with Flask, SQLite, and Bootstrap 5, providing a responsive, interactive, and user-friendly interface for both clients and the spa administrator. The goal of this application is to allow clients to book appointments seamlessly online while giving the spa owner an intuitive backend to view, edit, and manage appointments efficiently.

# Project Overview

The Cosmetología SPA Booking App is designed to streamline the appointment booking process, prevent double bookings, prevent past date bookings, prevent outside business hour bookings and provide a visually appealing experience for users. The interface emphasizes clarity and accessibility, ensuring that even first-time users can navigate the booking system effortlessly. The app also incorporates subtle visual enhancements, such as a glitter effect on successful bookings, to make the experience more engaging and celebratory.

# Features

## Customer-Facing Features

Interactive Booking Form: Users can submit their name, select a service, choose a date, and select a time slot. The form dynamically disables already booked times for a given date, preventing scheduling conflicts.

Date Validation: The system ensures that users can only select future dates, and restricts bookings to weekdays (Monday to Friday). This validation is done both on the frontend and backend to ensure robustness.

Dynamic Time Updates with AJAX: When a date is selected, available times update in real-time via an AJAX call to the backend, providing a smooth and responsive user experience without requiring a page reload.

Flash Messages: Users receive immediate feedback on their booking attempt through flash messages. Success messages trigger a sparkling animation that lasts for about five seconds, adding a touch of delight to the interaction.

Responsive Design: All sections of the website are mobile-friendly, ensuring that clients can book appointments from smartphones or tablets just as easily as from desktop devices.

Service Overview and Reviews: The app includes sections for displaying available services and customer reviews. This provides transparency and builds trust for new clients browsing the website.

Admin / Management Features

View Bookings: Administrators can view all scheduled appointments in a clean, sortable table, showing customer names, selected services, dates, and formatted times (e.g., “9 AM” instead of “09:00”).

Edit and Delete Appointments: Admins can modify bookings to accommodate changes or cancel appointments when necessary. Edit and delete buttons are aligned centrally for aesthetic consistency.

Double-Booking Prevention: The system ensures that no two appointments overlap, even when editing an existing booking. This maintains reliability and avoids scheduling conflicts.

# Technical Highlights

Flask & SQLAlchemy: The backend uses Flask for routing and SQLAlchemy for object-relational mapping, providing a flexible, maintainable, and scalable backend structure.

SQLite Database: A lightweight database stores all bookings and user-submitted information. The database schema is straightforward, with fields for name, service, date, and time.

AJAX Integration: Available time slots are updated asynchronously when a user selects a date, enhancing usability.

CSS Animations: Custom animations provide visual feedback to users for actions like successful bookings. The sparkles are timed to disappear after five seconds, ensuring they are festive without being distracting.

Modular and Extensible Codebase: Separation of concerns between templates, static assets, and backend logic allows easy addition of features such as product listings, completed booking indicators, or advanced reporting.

# Folder Structure and File Overview

The project is organized to keep frontend assets, templates, and backend code cleanly separated. Here’s a summary of the folder structure and file responsibilities:

```tree
cosmetologia/
│
├── app.py                 # Main Flask application with routing, forms handling, and database logic
├── bookings.db            # SQLite database file storing all bookings
├── requirements.txt       # Python dependencies for the project
│
├── templates/             # HTML templates
│   ├── base.html          # Base template defining head, header, footer, and block structure
│   ├── index.html         # Homepage with hero, services, booking form, and reviews sections
│   ├── bookings.html      # Admin view for all bookings with edit/delete buttons
│   ├── update_booking.html # Form to edit existing bookings
│
├── static/                # Static files for CSS, JavaScript, and images
│   ├── css/
│   │   └── main.css       # Custom styles including buttons, glitter, responsive tweaks
│   ├── js/
│   │   └── main.js        # JavaScript for animations, scroll behavior, AJAX updates (future update)
│   └── images/
│       ├── new_logo.png   # SPA logo displayed in hero section
│       └── ...            # Additional images for services or reviews (future update)
```

### File Responsibilities

- **app.py**: Handles all backend logic, including routing, form submission validation, database transactions, and flash message management. It also ensures that double bookings are prevented both on creation and update.

- **templates/base.html**: Main jinja template for extension on other html files for the app. Provides a common structure for all pages, defining placeholders (blocks) for content, scripts, and page-specific titles. This reduces repetition and ensures consistent design.

- **index.html**: The homepage combines the hero section, list of services, booking form, and reviews carousel. It integrates AJAX logic for time availability and triggers sparkle effects on successful bookings. Contains JavaScript for scroll behavior, AJAX updates for available times, sparkle animations, and flash message fade-outs.

- **bookings.html**: Admin interface that lists all appointments in a sortable table with action buttons for editing and deleting bookings.

- **update_booking.html**: Form pre-populated with the selected booking’s details, allowing admins to modify appointments easily.

- **main.css**: Styles the app including responsive layouts, button designs, animations, and table aesthetics. Gold-colored accents (#B8860B) and a sparkle effect provide visual elegance.

## Design Choices

Several design decisions were made to enhance usability, accessibility, and aesthetics:

- **Gold Color Scheme**: Chosen gold (#B8860B) with slightly yellow undertones to evoke luxury, elegance, and warmth appropriate for a SPA environment.

- **Sparkle Animation**: On successful booking, sparkles appear randomly across the screen for 5 seconds. This visual feedback rewards users for completing an action and enhances user experience.

- **Mobile-First Design**: All sections are responsive, with buttons and forms optimized for smaller screens. The booking form resizes appropriately, and hero section elements are centered.

- **Prevent Double Bookings**: Both frontend (disabling unavailable time slots) and backend (checking database entries) validation ensures reliability.

- **Intuitive Navigation**: Scroll buttons, flash messages, and a clean layout ensure that users can find information and complete bookings quickly without confusion.

- **Readable Admin Table**: Centralized action buttons, clear time formatting, and table-striped styling enhance usability for the administrator managing bookings. Table headers and table date are also centralized for readability. 

This application balances aesthetics, interactivity, and reliability. It serves as a professional and engaging solution for small business appointment management while providing a strong foundation for future enhancements like product catalogs, completed appointment tracking, or customer account management.

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/cosmetologia.git
cd cosmetologia
```

2. Create a virtual environment:
```bash    
python -m venv venv
```

3. Activate the virtual environment:
- Windows: 
```bash
venv\Scripts\activate
```
- Mac/Linux: 
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the Flask app:
```bash    
python3 app.py
```

6. Open your browser at `http://127.0.0.1:5000/` to use the application.
