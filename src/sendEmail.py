#!/usr/bin/env python3

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import yaml

def sendEmail(locations, recipient, senderAddress, password):
    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = senderAddress
    message["To"] = recipient

    templateString = """\
    <html>
    <head>
        <style>
            table, tr, th, td {
                border: 1px solid black;
            }
        </style>
    </head>
    <body>
        <p>Hello,<br>
        The CPA Exam Web Crawler has found the following availabilities for you:<br>
            <table style="width:100%">
                <tr>
                    <th>Location (City)</th>
                    <th>Address</th>
                    <th>Phone Number</th>
                    <th>Availabilities</th>
                </tr>
                {% for location in locations %}
                <tr>
                    <td>{{ location.locality }}</td>
                    <td>{{ location.formattedAddress }}</td>
                    <td>{{ location.phoneNumber }}</td>
                    <td>{{ location.availability }}</td>
                </tr>
                {% endfor %}
            </table>
        </p>
    </body>
    </html>
    """

    tm = Template(templateString)
    html = tm.render(locations=locations)

    htmlPart = MIMEText(html, "html")

    message.attach(htmlPart)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("cpawebcrawler@gmail.com", password)
        server.sendmail(senderAddress, recipient, message.as_string())

if __name__ == "__main__":
    recipient = ""
    senderAddress = ""
    password = ""
    with open("cpa-scraper-config.yaml", 'r') as configStream, open("cpa-scraper-creds.yaml", 'r') as credsStream:
        config = yaml.safe_load(configStream)
        cred = yaml.safe_load(credsStream)
        recipient = config["cpaScraper"]["email"]["testRecipient"]
        senderAddress = cred["cpaScraper"]["creds"]["senderAddress"]
        password = cred["cpaScraper"]["creds"]["password"]

    locations = [{'locality': 'Hyattsville', 'distance': 20.98, 'destinationCoordinates': [38.94929, -76.86756], 'formattedAddress': '4301 Garden City Dr, Suite 203-Metro 400, Hyattsville, MD, 20785, USA', 'phoneNumber': '443-923-8000', 'availability': '2020-06-17,\n2020-06-18,\n2020-06-23,\n2020-06-24,\n2020-06-25'}, {'locality': 'Baltimore', 'distance': 44.93, 'destinationCoordinates': [39.27546, -76.56905], 'formattedAddress': '1501 South Clinton Street, 2nd Floor, Canton Crossing, Baltimore, MD, 21224, USA', 'phoneNumber': '443-923-8000', 'availability': '2020-06-27'}, {'locality': 'GLEN ALLEN', 'distance': 85.93, 'destinationCoordinates': [37.6881, -77.59478], 'formattedAddress': '11547 NUCKOLS ROAD, SUITE B, GLEN ALLEN, VA, 23059, USA', 'phoneNumber': '443-923-8000', 'availability': '2020-06-23'}, {'locality': 'GLEN ALLEN', 'distance': 85.93, 'destinationCoordinates': [37.68812, -77.59474], 'formattedAddress': '11547 NUCKOLS ROAD, SUITE B, GLEN ALLEN, VA, 23059, USA', 'phoneNumber': '443-923-8000', 'availability': '2020-06-19,\n2020-06-20'}, {'locality': 'HARRISBURG', 'distance': 102.39, 'destinationCoordinates': [40.338, -76.79143], 'formattedAddress': '1100 N. MOUNTAIN ROAD, HARRISBURG, PA, 17112, USA', 'phoneNumber': '443-923-8000', 'availability': '2020-06-26'}]
    sendEmail(locations, recipient, senderAddress, password)