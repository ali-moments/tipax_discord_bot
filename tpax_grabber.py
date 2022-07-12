from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import logging
from configparser import ConfigParser

logging.basicConfig(level=logging.WARNING)

parser = ConfigParser()
parser.read('conf.ini')

customsender = parser.get('custom', 'sender')
customreceiver = parser.get('custom', 'receiver')

def get_state(id):
    url = f"https://tipaxco.com/tracking?id={id}"
    try:
        page = urlopen(url)
    except:
        logging.error("Error opening the URL")

    soup = BeautifulSoup(page, 'html.parser')

    states_ = soup.find_all('span', attrs={"class": "SuccessState"})
    dates_ = soup.find_all('span', attrs={"class":"fpoDateSpan"})

    states = []
    for state in states_:
        states.append(state.text)
    dates = []
    for date in dates_:
        dates.append(date.text)

    fields = []
    for i in range(len(states)):
        temp = {}
        temp['name'] = f"مرحله {str(i+1)}"
        temp['value'] = f"{dates[i]} | {states[i]}"
        fields.append(temp)
    
    return fields


def get_info(id):
    url = f"https://tipaxco.com/tracking?id={id}"
    try:
        page = urlopen(url)
    except:
        logging.error("Error opening the URL")
        return ""
    soup = BeautifulSoup(page, 'html.parser')
    barcode = soup.find('span', attrs={"id": re.compile(".*lblBarcodeNo"),"class": "lightColor"}).text
    contract_number = soup.find('span', attrs={"id": re.compile(".*lblContractCode2"),"class": "lightColor"}).text
    sendercity = soup.find('span', attrs={"id": re.compile(".*lblSenderCityName")}).text
    if customsender == "":
        sendername = soup.find('span', attrs={"id": re.compile(".*lblSenderName")}).text
    else:
        sendername = customsender
    receivercity = soup.find('span', attrs={"id": re.compile(".*lblReceiverCityName")}).text
    if customreceiver == "":
        receivername = soup.find('span', attrs={"id": re.compile(".*lblReceiverName")}).text
    else:
        receivername = customreceiver
    paytype = soup.find('span', attrs={"id": re.compile(".*lblPayType")}).text
    totalcost = soup.find('span', attrs={"id": re.compile(".*lblTotalCost")}).text
    weight = soup.find('span', attrs={"id": re.compile(".*lblWeight")}).text

    texts = [f"شماره بارکد: {barcode} | شماره قرارداد: {contract_number}", 
    f"نام فرستنده: {sendername} | شهر فرستنده: {sendercity}", 
    f"نام گیرنده: {receivername} | شهرگیرنده: {receivercity}", 
    f"نوع پرداخت: {paytype} | وزن: {weight}", 
    f"هزینه نهایی: {totalcost}"]

    return "\n".join(texts)

if __name__ == "__main__":
    id = input("Enter your id: ")
    print(get_state(id))
