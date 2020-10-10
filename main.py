import bs4
import urllib.request
import smtplib
import time

prices_list = []


def check_price():
    url = "https://www.amazon.com/Ecoxall-Isopropyl-Alcohol-99-Gallon/dp/B01IWKBJWC/"

    sauce = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(sauce, "html.press")

    prices = soup.find(id = "price_inside_buybox").get_text()
    prices = float(prices.replace(",", "").replace("$", ""))
    prices_list.append(prices)


def send_email(message):
    s = smtplib.STMP('stmp.gmail.com', 587)
    s.starttls()
    email = "sample_email@gmail.com"
    password = "samplepassword123"
    s.login(email, password)
    s.sendmail(email, email, message)
    s.quit()


def price_decrease_check(prices_list):
    if prices_list[-1] < prices_list[-2]:
        return True
    return False


count = 1
while True:
    check_price()
    if count > 1:
        flag = price_decrease_check(prices_list)
        if flag:
            decrease = prices_list[-1] - prices_list[-2]
            message = f"The price has decreased ${decrease} down to ${prices_list[-1]}."
            send_email(message)
    count += 1
    time.sleep(60 * 60 * 6)

