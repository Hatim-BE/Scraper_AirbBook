from utils.db import get_database_connection
from collections import defaultdict
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from threading import Thread
from time import sleep
import requests
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
import mysql.connector
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, TimeoutException


app = Flask(__name__)
global tables
tables = ['booking_scraped_urls','airbnb_scraped_urls']

scraping_thread = None
scraping_active_airbnb = False
scraping_active_booking = False
global total_url_counts, airbnb_url_counts, booking_url_counts, final_total_url_counts, total_airbnb_url_counts, total_booking_url_counts, airbnb_url_real_time_counts, booking_url_real_time_counts
final_total_url_counts = 0
total_url_counts = 0
airbnb_url_counts = 0
booking_url_counts = 0
total_airbnb_url_counts = 0
total_booking_url_counts = 0
airbnb_url_real_time_counts = 0
booking_url_real_time_counts = 0




@app.route('/')
def index():
    return render_template('index.html')
@app.route('/get_chart5_data', methods=['GET'])
def get_chart5_data():
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)  # Ensure fetchall() returns dictionaries

    # Initialize dictionary to store total counts for each month
    total_monthly_counts = {month: 0 for month in range(1, 13)}

    for table_name in tables:
        query = f"""
        SELECT YEAR(date_created) AS year, MONTH(date_created) AS month, COUNT(*) AS count
        FROM {table_name}
        GROUP BY YEAR(date_created), MONTH(date_created)
        ORDER BY year, month
        """
        print(f"Executing query for table {table_name}....")
        cursor.execute(query)
        results = cursor.fetchall()

        for result in results:
            month = result['month']
            count = result['count']
            # Add counts from this table to the total for each month
            total_monthly_counts[month] += count

    cursor.close()
    conn.close()

    # Convert total counts to a list to be used for chart data
    chart_data = list(total_monthly_counts.values())

    return jsonify({
        'name': "Total announcements",
        'data': chart_data
    })
@app.route('/get_monthly_total_counts', methods=['GET'])
def get_monthly_total_counts():
    conn = get_database_connection()
    cursor = conn.cursor()

    counts = {}
    total_counts = 0
    
    for table_name in tables:
        # Generate a query to count rows in each table
        query = f"SELECT COUNT(*) FROM {table_name}"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        counts[table_name] = count
        total_counts += count

    cursor.close()
    conn.close()
    
    return jsonify({"data" : counts, "total":total_counts})
@app.route('/get_weekly_total_counts', methods=['GET'])
def get_weekly_total_counts():
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)

    # Initialize dictionaries to store total counts for each day of the week for both tables
    table1_weekly_counts = {day: 0 for day in range(1, 8)}
    table2_weekly_counts = {day: 0 for day in range(1, 8)}

    # Process the first table
    query1 = """
    SELECT YEAR(date_created) AS year, DAYOFWEEK(date_created) AS day_of_week, COUNT(*) AS count
    FROM airbnb_scraped_urls
    GROUP BY YEAR(date_created), DAYOFWEEK(date_created)
    ORDER BY year, day_of_week
    """
    cursor.execute(query1)
    results1 = cursor.fetchall()

    for result in results1:
        day_of_week = result['day_of_week']
        count = result['count']
        table1_weekly_counts[day_of_week] += count

    # Process the second table
    query2 = """
    SELECT YEAR(date_created) AS year, DAYOFWEEK(date_created) AS day_of_week, COUNT(*) AS count
    FROM booking_scraped_urls
    GROUP BY YEAR(date_created), DAYOFWEEK(date_created)
    ORDER BY year, day_of_week
    """
    cursor.execute(query2)
    results2 = cursor.fetchall()

    for result in results2:
        day_of_week = result['day_of_week']
        count = result['count']
        table2_weekly_counts[day_of_week] += count

    cursor.close()
    conn.close()

    # Convert counts to lists ordered from Monday to Sunday
    table1_data = [
        table1_weekly_counts[2],  # Monday
        table1_weekly_counts[3],  # Tuesday
        table1_weekly_counts[4],  # Wednesday
        table1_weekly_counts[5],  # Thursday
        table1_weekly_counts[6],  # Friday
        table1_weekly_counts[7],  # Saturday
        table1_weekly_counts[1]   # Sunday
    ]

    table2_data = [
        table2_weekly_counts[2],  # Monday
        table2_weekly_counts[3],  # Tuesday
        table2_weekly_counts[4],  # Wednesday
        table2_weekly_counts[5],  # Thursday
        table2_weekly_counts[6],  # Friday
        table2_weekly_counts[7],  # Saturday
        table2_weekly_counts[1]   # Sunday
    ]

    return jsonify({
        'airbnb_scraped_urls': {
            'name': "Table 1 Announcements",
            'data': table1_data,
            'total': sum(table1_data)
        },
        'booking_scraped_urls': {
            'name': "Table 2 Announcements",
            'data': table2_data,
            'total': sum(table2_data)
        }
    })
@app.route('/get_today_counts', methods=['GET'])
def get_today_counts():
    conn = get_database_connection()
    cursor = conn.cursor()

    counts = {}
    total_counts = 0
    
    for table_name in tables:
        # Generate a query to count rows in each table
        query = f"SELECT COUNT(*) FROM {table_name} WHERE DATE(date_created) = CURDATE()"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        counts[table_name] = count
        total_counts += count

    cursor.close()
    conn.close()
    
    return jsonify({"data" : counts, "total":total_counts})
@app.route("/get_airbnb_total_counter", methods=['GET'])
def get_airbnb_total_counter():
    global total_airbnb_url_counts
    return jsonify({'count': total_airbnb_url_counts})

@app.route("/get_booking_counter", methods=['GET'])
def get_booking_counter():
    global booking_url_counts
    return jsonify({'count': booking_url_counts})

@app.route("/get_booking_real_time_counter", methods=['GET'])
def get_booking_real_time_counter():
    global booking_url_real_time_counts
    return jsonify({'count': booking_url_real_time_counts})

@app.route("/get_booking_total_counter", methods=['GET'])
def get_booking_total_counter():
    global total_booking_url_counts
    return jsonify({'count': total_booking_url_counts})

@app.route("/get_total_count", methods=['GET'])
def get_total_count():
    global final_total_url_counts
    return jsonify({'count': final_total_url_counts})



@app.route("/get_airbnb_count", methods=['GET'])
def get_airbnb_count():
    conn = get_database_connection()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM airbnb_scraped_urls"
    cursor.execute(query)
    count = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify({"data":count})
@app.route("/get_booking_count", methods=['GET'])
def get_booking_count():
    conn = get_database_connection()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM booking_scraped_urls"
    cursor.execute(query)
    count = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify({"data":count})


def get_database_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        print("Connection to the database was successful.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None


def create_table_airbnb(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS airbnb_scraped_urls (
                id INT AUTO_INCREMENT PRIMARY KEY,
                serial TEXT UNIQUE NOT NULL,
                url VARCHAR(255) UNIQUE NOT NULL,
                date_created TIMESTAMP NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS airbnb_listings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city VARCHAR(255),
                serial TEXT UNIQUE NOT NULL,
                url VARCHAR(255) UNIQUE NOT NULL,
                title VARCHAR(255),
                price VARCHAR(50),
                description TEXT,
                host VARCHAR(255),
                composition TEXT,
                rating VARCHAR(255),
                latitude VARCHAR(255),
                longitude VARCHAR(255),
                photo_links TEXT
            )
        ''')
        conn.commit()
        cursor.close()
        print("Tables `airbnb_scraped_urls` and `airbnb_listings` created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")

def create_table_booking(conn):
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS booking_scraped_urls (
                id INT AUTO_INCREMENT PRIMARY KEY,
                serial TEXT UNIQUE NOT NULL,
                url VARCHAR(255) UNIQUE NOT NULL,
                date_created TIMESTAMP NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS booking_listings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                city VARCHAR(255),
                serial TEXT UNIQUE NOT NULL,
                url VARCHAR(255) UNIQUE NOT NULL,
                title VARCHAR(255),
                price VARCHAR(50),
                description TEXT,
                host VARCHAR(255),
                composition TEXT,
                rating VARCHAR(255),
                latitude VARCHAR(255),
                longitude VARCHAR(255),
                photo_links TEXT
            )
        ''')

        conn.commit()
        cursor.close()
        print("Tables `booking_scraped_urls` and `booking_listings` created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")


def insert_url_airbnb(conn, url, ID):
    global total_airbnb_url_counts
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO airbnb_scraped_urls (url, serial) VALUES (%s, %s)", (url, ID))
        conn.commit()
        #print(f"Inserted URL: {url}")
        print(f"Inserted URL with ID: {ID}")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting airbnb ID: {err}")
        cursor.close()

def insert_url_booking(conn, url, ID):
    global total_booking_url_counts
    cursor = None
    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute("INSERT INTO booking_scraped_urls (url, serial) VALUES (%s, %s)", (url, ID))
        conn.commit()
        print(f"Inserted URL with ID: {ID}")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting URL: {err}")
        cursor.close()



def check_url_exists_airbnb(conn, ID):
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM airbnb_scraped_urls WHERE serial = %s", (ID,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        print(f"Error checking ID existence: {err}")
        return False
    finally:
        cursor.close()

def check_url_exists_booking(conn, ID):
    cursor = None
    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT 1 FROM booking_scraped_urls WHERE serial = %s", (ID,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as err:
        print(f"Error checking IID existence: {err}")
        return False
    finally:
        cursor.close()

def clean_price(price):
    # Remove all non-numeric characters (e.g., 'MAD', spaces)
    return re.sub(r'[^\d]', '', str(price))

def remove_spaces(text):
    # Remove extra spaces
    return re.sub(r'\s{2,}', ' ', str(text))

def clean_ra_la_lo(ra_la_lo):
    ra_la_lo = re.sub(r'[^\d.,]', '', str(ra_la_lo))
    # Remove extra spaces
    return re.sub(r',', '.', str(ra_la_lo))

def clean_column(df, col):
    # If column contains 'price' in the name, clean it using clean_price
    if 'price' in col.lower():
        return df[col].apply(clean_price)

    elif 'latiude' in col.lower() or 'longitude' in col.lower() or 'rating' in col.lower():
        return df[col].apply(clean_ra_la_lo)
    else:
        return df[col]
   
def save_to_xlsx_airbnb(conn, listing_data, output_filename):
    # Check if the file exists, and load existing data if it does
    if os.path.exists(output_filename):
        df = pd.read_excel(output_filename)
    else:
        # Define the DataFrame with the appropriate columns
        df = pd.DataFrame(columns=['city', 'serial', 'url', 'title', 'price', 'description', 'host', 'composition', 'rating', 'latitude', 'longitude', 'photo_links'])

    # Ensure listing_data is a list of dictionaries or list of lists
    if isinstance(listing_data, dict):  # If it's a single dictionary, wrap it in a list
        listing_data = [listing_data]

    # Convert the listing data into a DataFrame
    df_new = pd.DataFrame(listing_data)
    for col in df_new.columns:
        df_new[col] = clean_column(df_new, col).apply(remove_spaces)
    
    listing_data = df_new.to_dict(orient="records")
    
    insert_listing_a(conn, listing_data)


    # Concatenate the new listings with the existing ones
    df = pd.concat([df, df_new], ignore_index=True)
    
    # Save the DataFrame to the Excel file
    df.to_excel(output_filename, index=False)
    print(f"Listings saved to {output_filename}")

def save_to_xlsx_booking(conn, listing_data, output_filename):
    # Check if the file exists, and load existing data if it does
    if os.path.exists(output_filename):
        df = pd.read_excel(output_filename)
    else:
        # Define the DataFrame with the appropriate columns
        df = pd.DataFrame(columns=['city', 'serial', 'url', 'title', 'price', 'description', 'host', 'composition', 'rating', 'latitude', 'longitude', 'photo_links'])

    # Ensure listing_data is a list of dictionaries or list of lists
    if isinstance(listing_data, dict):  # If it's a single dictionary, wrap it in a list
        listing_data = [listing_data]

    # Convert the listing data into a DataFrame
    df_new = pd.DataFrame(listing_data)
    for col in df_new.columns:
        df_new[col] = clean_column(df_new, col).apply(remove_spaces)
    
    listing_data = df_new.to_dict(orient="records")
    
    insert_listing_b(conn, listing_data)


    # Concatenate the new listings with the existing ones
    df = pd.concat([df, df_new], ignore_index=True)
    
    # Save the DataFrame to the Excel file
    df.to_excel(output_filename, index=False)
    print(f"Listings saved to {output_filename}")

def scrape_listing_details_airbnb(driver, url, ID, city):
    try:
        driver.get(url)
        sleep(2)  # Adjust the wait time as needed
    except Exception as e:
        print(f"Error loading page: {e}")
        return None

    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        print(f"Error parsing page source: {e}")
        return None

    # Extract listing details (use the actual class names found from the inspection)
    try:
        title = soup.find('h1', class_='hpipapi atm_7l_1kw7nm4 atm_c8_1x4eueo atm_cs_1kw7nm4 atm_g3_1kw7nm4 atm_gi_idpfg4 atm_l8_idpfg4 atm_kd_idpfg4_pfnrn2 i1pmzyw7 atm_9s_1nu9bjl dir dir-ltr').text.strip() if soup.find('h1', class_='hpipapi atm_7l_1kw7nm4 atm_c8_1x4eueo atm_cs_1kw7nm4 atm_g3_1kw7nm4 atm_gi_idpfg4 atm_l8_idpfg4 atm_kd_idpfg4_pfnrn2 i1pmzyw7 atm_9s_1nu9bjl dir dir-ltr') else ''
    except Exception as e:
        print(f"Error extracting title: {e}")
        title = ''

    try:
        price = soup.find('span', class_='_11jcbg2').text.strip() if soup.find('span', class_='_11jcbg2') else ''
    except Exception as e:
        print(f"Error extracting price: {e}")
        price = ''

    try:
        description = soup.find('div', class_='d1isfkwk atm_vv_1jtmq4 atm_w4_1hnarqo dir dir-ltr').text.strip() if soup.find('div', class_='d1isfkwk atm_vv_1jtmq4 atm_w4_1hnarqo dir dir-ltr') else ''
    except Exception as e:
        print(f"Error extracting description: {e}")
        description = ''

    try:
        host = soup.find('div', class_='t1pxe1a4').text.strip() if soup.find('div', class_='t1pxe1a4') else ''
    except Exception as e:
        print(f"Error extracting host: {e}")
        host = ''

    try:
        composition = soup.find('ol', class_='lgx66tx atm_gi_idpfg4 atm_l8_idpfg4 dir dir-ltr').text.strip() if soup.find('ol', class_='lgx66tx atm_gi_idpfg4 atm_l8_idpfg4 dir dir-ltr') else ''
    except Exception as e:
        print(f"Error extracting composition: {e}")
        composition = ''

    try:
        rating = soup.find('span', class_='_10nhpq7').text.strip() if soup.find('span', class_='_10nhpq7') else ''
    except Exception as e:
        print(f"Error extracting rating: {e}")
        rating = ''

    try:
        r = requests.get(url)
        p_lat = re.compile(r'"lat":([-0-9.]+),')
        p_lng = re.compile(r'"lng":([-0-9.]+),')
        latitude = p_lat.findall(r.text)[0] if p_lat.findall(r.text) else None
        longitude = p_lng.findall(r.text)[0] if p_lng.findall(r.text) else None
    except IndexError:
        print(f"Error extracting latitude/longitude: index out of range")
        latitude = None
        longitude = None
    except Exception as e:
        print(f"Error extracting latitude/longitude: {e}")
        latitude = None
        longitude = None

    try:
        photo_links = [img['src'] for img in soup.find_all('img', class_='itu7ddv atm_e2_idpfg4 atm_vy_idpfg4 atm_mk_stnw88 atm_e2_1osqo2v__1lzdix4 atm_vy_1osqo2v__1lzdix4 i1cqnm0r atm_jp_pyzg9w atm_jr_nyqth1 i1de1kle atm_vh_yfq0k3 dir dir-ltr')]
        photo_links = ','.join(photo_links)
    except Exception as e:
        print(f"Error extracting photo links: {e}")
        photo_links = ''

    return {
        "city": city,
        "serial": ID,
        "url": url,
        'title': title,
        'price': price,
        'description': description,
        'host': host,
        'composition': composition,
        'rating': rating,
        'latitude': latitude,
        'longitude': longitude,
        'photo_links': photo_links
    }

def scrape_listing_details_booking(driver, url, ID, city):
    try:
        driver.get(url)
        sleep(1)  # Adjust the wait time as needed

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract listing details (use the actual class names found from the inspection)
        try:
            title = soup.find('h2', class_='af32860db5 pp-header__title').text.strip() if soup.find('h2', class_='af32860db5 pp-header__title') else ''
        except Exception as e:
            print(f"Error fetching title: {e}")
            title = ''

        try:
            # First, find the price element
            price = soup.find('span', class_='prco-valign-middle-helper')
            price = price.text.strip() if price else '0.0'
        except Exception as e:
            print(f"Error fetching price: {e}")
            price = '0.0'

        try:
            description = soup.find('p', class_='e2585683de c8d1788c8c').text.strip() if soup.find('p', class_='e2585683de c8d1788c8c') else ''
        except Exception as e:
            print(f"Error fetching description: {e}")
            description = ''

        try:
            host = soup.find('div', class_='t1pxe1a4').text.strip() if soup.find('div', class_='t1pxe1a4') else ''
        except Exception as e:
            print(f"Error fetching host: {e}")
            host = ''

        try:
            composition = soup.find('div', class_='hprt-roomtype-bed').text.strip() if soup.find('div', class_='hprt-roomtype-bed') else ''
        except Exception as e:
            print(f"Error fetching composition: {e}")
            composition = ''

        try:
            rating_element = soup.find('div', class_='d0522b0cca fd44f541d8')
            rating = rating_element.find('div', class_='a447b19dfd').next_sibling.strip() if rating_element else '0.0'
        except Exception as e:
            print(f"Error fetching rating: {e}")
            rating = '0.0'

        latitude, longitude = '', ''
        try:
            map_element = soup.find('a', class_="loc_block_link_underline_fix")
            if map_element and "data-atlas-latlng" in map_element.attrs:
                coords = map_element["data-atlas-latlng"].split(',')
                latitude, longitude = coords[0], coords[1]
        except Exception as e:
            print(f"Error fetching coordinates: {e}")

        # Extracting photos
        photo_links = []
        try:
            driver.get(url)
            try:
                # Find and click the link to load more photos
                photos_link = driver.find_element(By.CSS_SELECTOR, 'a.bh-photo-grid-item.bh-photo-grid-thumb.js-bh-photo-grid-item-see-all')
                photos_link.click()
            except Exception as e:
                print(f"Error finding or clicking the photo link: {e}")
                try:
                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, 'html.parser')

                    sources = ["src", "srcset", "data-srcset", "data-src"]
                    img_elements = soup.find_all('img', class_='hide')
                    if img_elements:
                        for img in img_elements:
                            for attr in sources:
                                if attr in img.attrs:
                                    photo_links.append(img[attr])
                                    break  
                        
                        photo_links = ','.join(photo_links)
                    else:
                        print("No image elements found.")
                except Exception as e:
                    print(f"Error processing images: {e}")
            
            sleep(1)
            
            try:
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                sources = ["src", "srcset", "data-srcset", "data-src"]
                img_elements = soup.find_all('img', class_='bh-photo-modal-grid-image')
                if img_elements:
                    for img in img_elements:
                        for attr in sources:
                            if attr in img.attrs:
                                photo_links.append(img[attr])
                                break  
                    
                    photo_links = ','.join(photo_links)
                else:
                    print("No image elements found.")
            except Exception as e:
                print(f"Error processing images: {e}")
        except Exception as e:
            print(f"Error during the scraping process: {e}")

        return {
            'city': city,
            'serial': ID,
            'url': url,
            'title': title,
            'price': price,
            'description': description,
            'host': host,
            'composition': composition,
            'rating': rating,
            'latitude': latitude,
            'longitude': longitude,
            'photo_links': photo_links
        }
    except Exception as e:
        print(f"Overall error in scraping: {e}")
        return {}



def scrape_airbnb(cities, conn):
    edge_options = Options()
    # edge_options.add_argument("--headless")  # Run in headless mode (no GUI)
    # Initialize the Edge WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Edge(service=service, options=edge_options)
    global all_airbnb_links, airbnb_url_real_time_counts
    all_airbnb_links = []  # List to store all extracted links
    scraped_ids  = set()
    for city in cities:
        if not scraping_active_airbnb:
            break
        print(f"Scraping for {city}")
        base_url = f"https://www.airbnb.com/s/{city}/homes"
        sum = 0
        while base_url and scraping_active_airbnb:
            if not scraping_active_airbnb:
                break
            driver.get(base_url)
            
            # Wait for JavaScript to load content
            sleep(3)  # Adjust the wait time as needed

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find and process the listing links
            link_elements = soup.find_all('a', href=True, class_='l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 bn2bl2p atm_5j_223wjw atm_9s_1ulexfb atm_e2_1osqo2v atm_fq_idpfg4 atm_mk_stnw88 atm_tk_idpfg4 atm_vy_1osqo2v atm_26_1j28jx2 atm_3f_glywfm atm_kd_glywfm atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_aaiy6o_1w3cfyq_oggzyc atm_70_1b8lkes_1w3cfyq_oggzyc atm_uc_glywfm_1w3cfyq_pynvjw atm_uc_aaiy6o_pfnrn2_ivgyl9 atm_70_1b8lkes_pfnrn2_ivgyl9 atm_uc_glywfm_pfnrn2_61fwbc dir dir-ltr')

            if not link_elements:
                print("No listings found. The class name may have changed or there are no listings available.")
            else:
                print(f"Found {len(link_elements)} listings on this page. Extracting URLs...")
                sum += len(link_elements)
                
                for link in link_elements:
                    if not scraping_active_airbnb:
                        break
                    url = "https://www.airbnb.com" + link['href']
                    regex = r"/rooms/(\d+)"
                    ID = re.search(regex, url).group(1)
                    if ID not in scraped_ids and not check_url_exists_airbnb(conn, ID):
                        scraped_ids.add(ID)
                        airbnb_url_real_time_counts += 1
                        all_airbnb_links.append((url, ID, city))
                    else:
                        print(f"{ID} exists!!")

            # Check and click the "Next" button
            next_button = soup.find('a', attrs={"aria-label": "Next"})
            
            if next_button:
                next_url = next_button.get('href')
                base_url = "https://www.airbnb.com" + next_url
                print(f"Navigating to next page:")
                sleep(2)
            else:
                base_url = None
                print("No more pages to scrape.")

        print(f"{sum} announcements scraped")
        print(f"Finished scraping and inserting URLs for {city}")


    driver.quit()    

def insert_listing_a(conn, listing_data):
    cursor = None
    try:
        cursor = conn.cursor()
        if isinstance(listing_data, list):
            # If listing_data is a list, insert each dictionary
            for listing in listing_data:
                cursor.execute('''
                    INSERT INTO airbnb_listings (city, serial, url, title, price, description, host, composition, rating, latitude, longitude, photo_links)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    listing.get('city', ''),
                    listing.get('serial', ''),
                    listing.get('url', ''),
                    listing.get('title', ''),
                    listing.get('price', ''),
                    listing.get('description', ''),
                    listing.get('host', ''),
                    listing.get('composition', ''),
                    listing.get('rating', ''),
                    listing.get('latitude', ''),
                    listing.get('longitude', ''),
                    listing.get('photo_links', '')
                ))
        else:
            # If listing_data is a single dictionary, insert it directly
            cursor.execute('''
                INSERT INTO airbnb_listings (city, serial, url, title, price, description, host, composition, rating, latitude, longitude, photo_links)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                listing.get('city', ''),
                listing.get('serial', ''),
                listing.get('url', ''),
                listing_data.get('title', ''),
                listing_data.get('price', ''),
                listing_data.get('description', ''),
                listing_data.get('host', ''),
                listing_data.get('composition', ''),
                listing_data.get('rating', ''),
                listing_data.get('latitude', ''),
                listing_data.get('longitude', ''),
                listing_data.get('photo_links', '')
            ))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting listing: {err}")
    finally:
        cursor.close()

def insert_listing_b(conn, listing_data):
    cursor = None
    try:
        cursor = conn.cursor()
        if isinstance(listing_data, list):
            # If listing_data is a list, insert each dictionary
            for listing in listing_data:
                cursor.execute('''
                    INSERT INTO booking_listings (city, serial, url, title, price, description, host, composition, rating, latitude, longitude, photo_links)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    listing.get('city', ''),
                    listing.get('serial', ''),
                    listing.get('url', ''),
                    listing.get('title', ''),
                    listing.get('price', ''),
                    listing.get('description', ''),
                    listing.get('host', ''),
                    listing.get('composition', ''),
                    listing.get('rating', ''),
                    listing.get('latitude', ''),
                    listing.get('longitude', ''),
                    listing.get('photo_links', '')
                ))
        else:
            # If listing_data is a single dictionary, insert it directly
            cursor.execute('''
                INSERT INTO booking_listings (city, serial, url, title, price, description, host, composition, rating, latitude, longitude, photo_links)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                listing.get('city', ''),
                listing.get('serial', ''),
                listing.get('url', ''),
                listing_data.get('title', ''),
                listing_data.get('price', ''),
                listing_data.get('description', ''),
                listing_data.get('host', ''),
                listing_data.get('composition', ''),
                listing_data.get('rating', ''),
                listing_data.get('latitude', ''),
                listing_data.get('longitude', ''),
                listing_data.get('photo_links', '')
            ))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error inserting listing: {err}")
    finally:
        cursor.close()


def insert_listings_airbnb():
    global total_url_counts, airbnb_url_counts, final_total_url_counts, total_airbnb_url_counts, airbnb_url_real_time_counts, all_airbnb_links # Declare global variables
    
    edge_options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Edge(service=service, options=edge_options)
    
    # Process all the links after scraping all cities
    total_airbnb_url_counts = len(all_airbnb_links)
    for url, ID, city in all_airbnb_links:
        if not scraping_active_airbnb:
            break
        #print(f"Processing URL: {url}")
        print(f"Processing URL with ID: {ID}")
        driver.get(url)
        #if not check_url_exists_airbnb(conn, ID):
        insert_url_airbnb(conn, url, ID)
        total_url_counts += 1
        listing_data = scrape_listing_details_airbnb(driver, url, ID, city)
        output_filename = f"airbnb.xlsx"  # Assuming the same output file for all cities
        save_to_xlsx_airbnb(conn, listing_data, output_filename)
        airbnb_url_counts += 1
        print(f"{airbnb_url_counts}/{total_airbnb_url_counts}")
        #else:
        #    airbnb_url_counts += 1
        #    print(f"ID already exists: {ID}")
        
    #final_total_url_counts = total_url_counts
    
    driver.quit()
def scrape_and_process_airbnb(cities, conn):
    global final_total_url_counts, all_airbnb_links
    scrape_airbnb(cities, conn)
    print(f"``````{len(all_airbnb_links)}``````")
    for item in all_airbnb_links:
        print(item)
    insert_listings_airbnb()
    



def scrape_booking(cities, conn):
    global scraping_active_booking, total_url_counts, booking_url_counts, total_booking_url_counts, booking_url_real_time_counts
    booking_url_counts = 0
    total_booking_url_counts = 0
    total_url_counts = 0
    booking_url_real_time_counts = 0
    edge_options = Options()
    # edge_options.add_argument("--headless")  # Run in headless mode (no GUI)

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return

    links = []

    today = datetime.today().strftime('%Y-%m-%d')
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    scraped_ids = set()
    for city in cities:
        if not scraping_active_booking:
            break
        print(f"Scraping for {city}")
        base_url = f"https://www.booking.com/searchresults.fr.html?ss={city}&checkin={today}&checkout={tomorrow}&group_adults=1&no_rooms=1&group_children=0"
        total_links_for_city = 0
        
        if not scraping_active_booking:
            break

        try:
            driver.get(base_url)
            sleep(3)
        except Exception as e:
            #print(f"Error loading base URL {base_url}: {e}")
            print(f"Error loading base URL: {e}")
            continue

        count = 0
        while scraping_active_booking:
            try:
                last_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(3)

                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height > last_height:
                    last_height = new_height
                    continue
            except Exception as e:
                print(f"Error during scrolling: {e}")
                break

            # Handling the "POP UP" button
            try:
                wait = WebDriverWait(driver, 10)
                if count < 2:
                    count += 1
                    try:
                        pop = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.f4552b6561')))
                        driver.execute_script("arguments[0].scrollIntoView(true);", pop)
                        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.a83ed08757.c21c56c305.f38b6daa18.d691166b09.ab98298258.f4552b6561')))
                        actions = ActionChains(driver)
                        actions.move_to_element(pop).click().perform()
                        print("Pop-up clicked using ActionChains")
                    except (NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException) as e:
                        print(f"Error interacting with pop-up: {e}")
                        driver.execute_script("arguments[0].click();", pop)
            except TimeoutException:
                print(f"'POP UP' button not found or not clickable.")
            except Exception as e:
                print(f"Error handling 'POP UP' button: {e}")
                break

            # Process the new page content after scrolling
            try:
                more_results_button = driver.find_element(By.CSS_SELECTOR, 'button.a83ed08757.c21c56c305.bf0537ecb5.f671049264.af7297d90d.c0e0affd09')
                if more_results_button.is_displayed(): 
                    more_results_button.click()
                    sleep(3)
                    last_height = driver.execute_script("return document.body.scrollHeight")
                    '''page_source = driver.page_source
                    soup = BeautifulSoup(page_source, 'html.parser')

                    link_elements = soup.find_all('h3', class_='d3e8e3d21a')
                    for link_element in link_elements:
                        if not scraping_active_booking:
                            break
                        try:
                            link = link_element.find('a', href=True)["href"]
                            regex = r"sr_pri_blocks=([^&]+)"
                            ID = re.search(regex, link).group(1)
                            if not check_url_exists_booking(conn, ID):
                                booking_url_real_time_counts += 1
                                links.append((link_element.find('a', href=True), city))
                        except Exception as e:
                            print(f"Error processing link element: {e}")
                    print(f"Found {len(link_elements)} listings for {city}.")
                    total_links_for_city += len(link_elements)'''
                else:
                    print("No 'More results' button found.")
                    break
            except NoSuchElementException:
                print("No 'More results' button present or visible.")
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                link_elements = soup.find_all('h3', class_='aab71f8e4e')
                for link_element in link_elements:
                    if not scraping_active_booking:
                        break
                    try:
                        link = link_element.find('a', href=True)["href"]
                        regex = r"(\d+)_\d+_\d+_\d+_\d+"
                        ID = re.search(regex, link).group(1)
                        if ID not in scraped_ids and not check_url_exists_booking(conn, ID):
                            scraped_ids.add(ID)
                            booking_url_real_time_counts += 1
                            links.append((link_element.find('a', href=True), city))
                    except Exception as e:
                        print(f"Error processing link element: {e}")
                print(f"Found {len(link_elements)} listings for {city}.")
                total_links_for_city += len(link_elements)
                sleep(3)
                break
            except Exception as e:
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                link_elements = soup.find_all('h3', class_='aab71f8e4e')
                for link_element in link_elements:
                    if not scraping_active_booking:
                        break
                    try:
                        link = link_element.find('a', href=True)["href"]
                        regex = r"(\d+)_\d+_\d+_\d+_\d+"
                        ID = re.search(regex, link).group(1)
                        if ID not in scraped_ids and not check_url_exists_booking(conn, ID):
                            #insert_url_booking(conn, link, ID)
                            booking_url_real_time_counts += 1
                            links.append((link_element.find('a', href=True), city))
                    except Exception as e:
                        print(f"Error processing link element: {e}")
                print(f"Found {len(link_elements)} listings for {city}.")
                total_links_for_city += len(link_elements)
                sleep(3)
                print(f"Error interacting with 'More results' button: {e}")
                break

    # After finishing the scraping for the city
    if not links:
        print(f"No listings found for {city}. The class name may have changed or there are no listings available.")
    else:
        try:
            total_booking_url_counts = len(links)
            print(f"Found {len(links)} listings on this page. Extracting URLs...")
            
            output_filename = f"booking.xlsx"
            regex = r"(\d+)_\d+_\d+_\d+_\d+"

            for link, city in links:
                #print(f"links: {link}, city: {city}")
                if not scraping_active_booking:
                    break
                try:
                    url = link['href']
                    #print(f"Found URL: {url}")
                    match = re.search(regex, url)
                    if match:
                        sr_pri_blocks_id = match.group(1)
                        print(f"Found ID: {sr_pri_blocks_id}")
                    else:
                        print("No match found for ID.")

                    #if not check_url_exists_booking(conn, sr_pri_blocks_id):
                    insert_url_booking(conn, url, sr_pri_blocks_id)
                    total_url_counts += 1
                    listing_data = scrape_listing_details_booking(driver, url, sr_pri_blocks_id, city)
                    save_to_xlsx_booking(conn, listing_data, output_filename)
                    booking_url_counts += 1
                    print(f"{booking_url_counts}/{total_booking_url_counts}")
                    '''else:
                        #print(f"URL already exists: {url}")
                        print(f"URL with ID already exists: {ID}")
                        booking_url_counts += 1'''
                except Exception as e:
                    print(f"Error processing link: {e}")
        except Exception as e:
            print(f"Error during URL extraction: {e}")

    print(f"Total links processed for {city}: {total_links_for_city}")
    print(f"Finished scraping for {city}.")

    try:
        driver.quit()
    except Exception as e:
        print(f"Error closing the WebDriver: {e}")

'''final_total_url_counts = total_url_counts
total_airbnb_url_counts = airbnb_url_counts
total_booking_url_counts = booking_url_counts
print("total_url_counts")
print(final_total_url_counts)'''

@app.route('/start_scraping_airbnb', methods=['POST'])
def start_scraping_airbnb():
    global scraping_active_airbnb
    scraping_active_airbnb = True

    print("Scraping Airbnb...")
    cities = ["agadir", "rabat", "fes"]
    conn = get_database_connection()
        # Example usage:
    if conn:
        create_table_airbnb(conn)  # Ensure the table is created
        scrape_airbnb(cities, conn)
        conn.close()
    else:
        print("Failed to connect to the database.")
    print("Stopped Scraping Airbnb...")
    
    return [scraping_active_airbnb, "Stoped Scraping Booking..."]   

@app.route('/pause_scraping_airbnb', methods=['POST'])
def pause_scraping_airbnb():
    global scraping_active_airbnb
    scraping_active_airbnb = False
    return [scraping_active_airbnb, "Stoped Scraping Airbnb..."]

cities = [
    "Marrakech",
    "Casablanca",
    "Fes",
    "Rabat",
    "Tangier",
    "Chefchaouen",
    "Essaouira",
    "Agadir",
    "Ouarzazate",
    "Meknes",
    "Merzouga",
    "Ifrane",
    "Taroudant",
    "Asilah",
    "Tetouan",
    "El Jadida",
    "Zagora",
    "Safi",
    "Nador",
    "Tiznit",
    "Oujda",
    "Midelt",
    "Tinghir",
    "Errachidia",
    "Sidi Ifni",
    "Beni Mellal",
    "Azrou",
    "Kenitra",
    "Larache",
    "Al Hoceima",
    "Boumalne Dades",
    "Mohammedia",
    "Martil",
    "Sefrou",
    "Khemisset",
    "Tarfaya",
    "Sidi Bou Said",
    "Skoura",
    "Tantan",
    "Guelmim",
    "Ait Benhaddou",
    "Dakhla",
    "Laayoune",
    "Khenifra",
    "Settat",
    "Tata",
    "Rissani",
    "Chichaoua",
    "Aknoul",
    "Demnate",
    "Moulay Idriss",
    "Sidi Slimane",
    "Jerada",
    "Bouznika",
    "Saïdia"
]

conn = get_database_connection()

#/******* START-STOP FOR BOTH WEBSITES *******\#

@app.route('/start_scraping', methods=['POST'])
def start_scraping():
    global scraping_active_airbnb, scraping_active_booking, airbnb_url_counts, total_url_counts, final_total_url_counts, total_airbnb_url_counts, total_booking_url_counts, booking_url_real_time_counts, airbnb_url_real_time_counts
    scraping_active_airbnb = True
    scraping_active_booking = True
    airbnb_url_counts = 0
    total_url_counts = 0
    final_total_url_counts = 0
    total_airbnb_url_counts = 0
    total_booking_url_counts = 0
    airbnb_url_real_time_counts = 0
    booking_url_real_time_counts = 0
    
    create_table_booking(conn)
    create_table_airbnb(conn)

    

    # Create threads for both scraping functions
    airbnb_thread = Thread(target=scrape_and_process_airbnb, args=(cities, conn))
    booking_thread = Thread(target=scrape_booking, args=(cities, conn))

    # Start both threads
    airbnb_thread.start()
    airbnb_thread.join()
    scraping_active_airbnb = False
    sleep(5)
    booking_thread.start()    
    booking_thread.join()
    scraping_active_booking = False

    # Print or return the collected all_airbnb_links
    #print(f"All links collected: {all_airbnb_links}")
    return jsonify({"status" : "scraping started"})

@app.route("/get_airbnb_counter", methods=['GET'])
def get_airbnb_counter():
    global airbnb_url_counts
    return jsonify({'count': airbnb_url_counts})

@app.route("/get_airbnb_real_time_counter", methods=['GET'])
def get_airbnb_real_time_counter():
    global airbnb_url_real_time_counts
    return jsonify({'count': airbnb_url_real_time_counts})


@app.route('/stop_scraping', methods=['POST'])
def stop_scraping():
    global scraping_active_airbnb, scraping_active_booking, airbnb_url_counts, booking_url_counts, total_url_counts, final_total_url_counts, total_airbnb_url_counts, total_booking_url_counts, airbnb_url_real_time_counts, booking_url_real_time_counts
    final_total_url_counts = 0
    airbnb_url_counts = 0
    booking_url_counts = 0
    total_url_counts = 0
    total_airbnb_url_counts = 0
    total_booking_url_counts = 0
    airbnb_url_real_time_counts = 0
    booking_url_real_time_counts = 0

    scraping_active_airbnb = False
    scraping_active_booking = False
    return jsonify({"status" : "scraping stopped"})

@app.route('/is_active', methods=["GET"])
def is_active():
    global scraping_active_airbnb, scraping_active_booking
    return jsonify({"status":scraping_active_booking})

@app.route('/is_active_airbnb', methods=["GET"])
def is_active_airbnb():
    global scraping_active_airbnb, scraping_active_booking
    return jsonify({"status":scraping_active_airbnb})



if __name__ == '__main__':
    app.run(debug=True)
