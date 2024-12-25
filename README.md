# Web Scraping Project: Airbnb & Booking.com
<div style="display: flex; justify-content: space-around; align-items: center;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Airbnb_Logo_B%C3%A9lo.svg/320px-Airbnb_Logo_B%C3%A9lo.svg.png" alt="Airbnb Logo" width="200">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Booking.com_Icon_2022.svg/245px-Booking.com_Icon_2022.svg.png" alt="Booking.com Logo" width="200">
</div>
This project focuses on web scraping data from Airbnb and Booking.com using Python with Flask. The aim is to gather and process relevant data to enable detailed analysis or integration into other applications.

---

## Table of Contents
- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Overview
This project provides tools to scrape data from Airbnb and Booking.com, process it, and expose it via a Flask API. It includes:
- Python scripts for data extraction and processing.
- A Flask application to serve the data.

---

## Technologies Used
- **Python (Flask)**: For processing and exposing data through APIs.
- **Beautiful Soup / Selenium /Requests**: For web scraping in Python.
- **MySQL**: To store scraped data.

---

## Features
- Scrapes property listings and related metadata.
- Processes data to remove duplicates and ensure accuracy.
- Provides an API endpoint to access the data programmatically.

---

## Setup Instructions

### Prerequisites
- Python (preferably latest versions)
- MySQL database
- Required libraries: `Flask`, `requests`, `BeautifulSoup4`, `selenium`, `pandas`, `webdriver-manager`, `mysql-connector-python`, `python-dotenv`


### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Hatim-BE/Scraper_Airbnb_Booking.git
   cd Scraper_Airbnb_Booking
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the MySQL database:
   - Create a new database.
   - Create a .env file in the root directory and add the following variables:
     - `DB_HOST`: The host of the MySQL database.
     - `DB_USER`: The username of the MySQL database.
     - `DB_PASSWORD`: The password of the MySQL database.
     - `DB_NAME`: The name of the MySQL database.
    - Create a .env file in the root directory and add the following variables:
        ```python
        DB_HOST= #your credentials
        DB_USER= #your credentials
        DB_PASSWORD= #your credentials
        DB_NAME= #your credentials
        ```
4. Start the Flask server:
   ```bash
   python app.py
   ```

---

## Usage
1. Run the Python App.
2. Access the web based interface to intreact with it via:
   ```
   http://localhost:5000/
   ```

---

## Contributing
I would love contributions! Please fork the repository and do what you should do :).

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## requirements.txt
```
flask
requests
selenium
pandas
beautifulsoup4
mysql-connector-python
webdriver-manager
python-dotenv
```

