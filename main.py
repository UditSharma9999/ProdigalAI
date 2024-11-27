# !pip install google-cloud-aiplatform
from dotenv import load_dotenv
import mysql.connector
import pandas as pd
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os

def config():
    API_KEY = os.getenv("API_KEY")
    genai.configure(api_key=API_KEY)
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="110091",
        database="web_scraping"
    )
    return db_connection

def summarize_text(text):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = "Summarize the given text"
    response = model.generate_content([prompt, text])
    return response.text

def fetch_data(categories, url):
    for html in categories:
        heading_tag = html.find('h3')
        if heading_tag:
            heading = heading_tag.text.strip()
        else:
            heading = "N/A"

        link_tag = html.find('a')
        if link_tag and 'href' in link_tag.attrs:
            link = url + link_tag['href']
        else:
            link = "N/A"

        description_tag = html.find('div', {'itemprop': 'description'})
        if description_tag:
            description = description_tag.text.strip()
            description = summarize_text(description)
        else:
            description = "N/A"


        data['Category_Name'].append(heading)
        data['links'].append(link)
        data['Description'].append(description)

def add_to_db(db_connection):
    try:
        cursor = db_connection.cursor()
        stmt = "SHOW TABLES LIKE 'scraped_data'"
        cursor.execute(stmt)
        result = cursor.fetchone()
        
        if result==None:
            create_table = """
                CREATE TABLE scraped_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    category_name VARCHAR(255),
                    link TEXT,
                    description TEXT
                );
            """
            cursor.execute(create_table)

            
        sql_query = """
        INSERT INTO scraped_data (category_name, link, description)
        VALUES (%s, %s, %s)
        """

        for i in range(len(data['Category_Name'])):
            cursor.execute(sql_query, (data['Category_Name'][i], data['links'][i], data['Description'][i]))

        db_connection.commit()
        print("Data inserted successfully into the MySQL database!")

    except mysql.connector.Error as err:
        print(f"An error occurred: {err}")

    finally:
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("MySQL connection is closed.")



def main(db):
    url = "https://gov.optimism.io"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html.parser")
    categories = soup.find_all("td", class_="category")

    fetch_data(categories, url)
    add_to_db(db)



if __name__=="__main__":
    load_dotenv()
    data = {
        'Category_Name': [],
        'links': [],
        'Description': []
    }
    db = config()
    main(db)

# mysql -u root -p