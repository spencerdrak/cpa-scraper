import requests
from bs4 import BeautifulSoup
import re
import json

key = ""

queryStartDate = "2020-06-15T00:00:00"
queryEndDate = "2020-06-29T00:00:00"
queryCoords = "38.90071105957031,-77.2527084350586"
queryTake = 5
querySkip = 0

keyURL = "https://proscheduler.prometric.com"

keyPayload = {}
keyHeaders = {
  'authority': 'proscheduler.prometric.com',
  'pragma': 'no-cache',
  'upgrade-insecure-requests': '1',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'sec-fetch-site': 'none',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-user': '?1',
  'sec-fetch-dest': 'document',
  'accept-language': 'en-US,en;q=0.9\'',
  'cookie': '_ga=GA1.2.773138575.1589555059; _gid=GA1.2.1039277300.1589555059'
}

keyResponse = requests.request("GET", keyURL, headers=keyHeaders, data = keyPayload)

print("Received response from " + keyURL + " with status code: " + str(keyResponse.status_code) + "...")

soup = BeautifulSoup(keyResponse.text, "html.parser")
for tag in soup.findAll('script', text = re.compile('.*bootstrapApp.*')):
    key = tag.contents[0].split(",")[13].strip()[1:-1]
    print("Found key: " + key)

print('Bearer ' + key)

url = "https://scheduling.prometric.com/api/v1/sites/availabilities/"

payload = "[{\"id\":\"jDIvheg1hE6tRak08WJV-w\",\"testingAccommodations\":[]}]"
headers = {
  'authority': 'proscheduler.prometric.com',
  'pragma': 'no-cache',
  'cache-control': 'no-cache',
  'accept': 'application/json, text/plain, */*',
  'Authorization': 'Bearer ' + key,
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
  'x-http-method-override': 'SEARCH',
  'Content-Type': 'application/json',
  'origin': 'https://proscheduler.prometric.com',
  'sec-fetch-site': 'same-site',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'accept-language': 'en-US,en;q=0.9',
  'referrer': 'https://proscheduler.prometric.com/scheduling/findAvailabilitytestcenter',
  'Content-Type': 'application/json',
}
params = {
  'startDate': queryStartDate,
  'endDate': queryEndDate,
  'coordinates': queryCoords,
  'Take': queryTake,
  'skip': querySkip
}

response = requests.request("POST", url, headers=headers, data = payload, params = params)

print(response.text.encode('utf8'))