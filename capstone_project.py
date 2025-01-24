# Capstone Project: End-to-End Automation Pipeline

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from PyPDF2 import PdfMerger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def scrape_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    for item in soup.select('div.item'):  # Adjust selector to match the website structure
        name = item.select_one('h2.name').text.strip()
        price = item.select_one('span.price').text.strip()
        data.append({'Name': name, 'Price': price})
    return data

def save_to_excel(data, file_path):
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    print(f"Data saved to {file_path}")

def merge_pdfs(pdf_list, output_path):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()
    print(f"PDFs merged into {output_path}")

def send_email_with_attachment(sender_email, receiver_email, password, subject, body, attachment):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with open(attachment, 'rb') as file:
        part = MIMEText(file.read(), 'base64', 'utf-8')
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
        msg.attach(part)

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
    print(f"Email sent to {receiver_email}")

# Main Execution
def main():
    # Step 1: Scrape data
    url = 'https://example.com/products'
    data = scrape_data(url)

    # Step 2: Save data to Excel
    excel_file = os.path.join(base_dir, 'Capstone_Project', 'scraped_data.xlsx')
    save_to_excel(data, excel_file)

    # Step 3: Merge PDFs
    pdfs = [os.path.join(base_dir, 'Capstone_Project', f'file{i}.pdf') for i in range(1, 3)]  # Example PDF paths
    merged_pdf = os.path.join(base_dir, 'Capstone_Project', 'merged_output.pdf')
    merge_pdfs(pdfs, merged_pdf)

    # Step 4: Send Email
    send_email_with_attachment(
        sender_email='your_email@example.com',
        receiver_email='receiver_email@example.com',
        password='your_password',
        subject='Capstone Project Output',
        body='Please find the attached files.',
        attachment=excel_file
    )

if __name__ == '__main__':
    main()
