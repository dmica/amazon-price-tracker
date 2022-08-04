from bs4 import BeautifulSoup
import lxml
import requests
import smtplib

# Amazon URL of item that you want to follow price for
url = "https://www.amazon.co.uk/Sony-WH-1000XM4-Cancelling-Wireless-Headphones-Black/dp/B08C7KG5LP/ref=sr_1_6?keywords=headphones&qid=1659627826&sprefix=headp%2Caps%2C78&sr=8-6"

# Your SMTP details to send email notification
YOUR_SMTP_ADDRESS = ""
YOUR_EMAIL = ""
YOUR_PASSWORD = "" 

# Your user agent and accept language; Can be found here: http://myhttpheader.com/ 

user_agent = "en-GB,en-US;q=0.9,en;q=0.8"
accept_language = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"

headers = { 'Accept-Language' : accept_language,
            'User-Agent': user_agent}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "lxml")

full_price = soup.find("span", class_="a-offscreen").getText()
price_without_currency = full_price.split("£")
price = float(price_without_currency[1])

# When the price is below 180 then send an email to yourself. The email includes the title of the item, the current price and a link to buy the item.
title = soup.find("span", id="productTitle").getText()
buy_price = 180.00

if price < buy_price:
  message = f"{title} is now {price}"

  with smtplib.SMTP(YOUR_SMTP_ADDRESS, port=587) as connection:
    connection.starttls()
    result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
    connection.sendmail(
        from_addr=YOUR_EMAIL,
        to_addrs=YOUR_EMAIL,
        msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}"
    )
