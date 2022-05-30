from bs4 import BeautifulSoup
from urllib.request import urlopen
import logging

logging.basicConfig(level=logging.WARNING)

def get_state(id):
    url = f"https://tipaxco.com/tracking?id={id}"
    try:
        page = urlopen(url)
    except:
        logging.error("Error opening the URL")

    soup = BeautifulSoup(page, 'html.parser')

    values = soup.find_all('span', attrs={"class": "SuccessState"})
    values2 = soup.find_all('span', attrs={"class":"fpoDateSpan"})

    states = []
    for state in values:
        states.append(state.text)
    dates = []
    for date in values2:
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

    soup = BeautifulSoup(page, 'html.parser')
    
    barcode = soup.find('span', attrs={"id":"ctl15_ctl12_ctl01_ctl00__lblBarcodeNo","class": "lightColor"}).text
    contract_number = soup.find('span', attrs={"id":"ctl15_ctl12_ctl01_ctl00__lblContractCode2","class": "lightColor"}).text
    sendercity = soup.find('span', attrs={"id":"ctl15_ctl12_ctl01_ctl00__lblSenderCityName"}).text
    sendername = soup.find('span', attrs={"id":"ctl15_ctl12_ctl01_ctl00__lblSenderName"}).text
    receivercity = soup.find('span', attrs={"id":"ctl15_ctl12_ctl01_ctl00__lblReceiverCityName"}).text
    receivername = soup.find('span', attrs={"id":"ctl15_ctl12_ctl01_ctl00__lblReceiverName"}).text
    paytype = soup.find('span', attrs={"id":"ctl15_ctl12_ctl01_ctl00__lblPayType"}).text
    totalcost = soup.find('span', attrs={"id":"ctl15_ctl12_ctl01_ctl00__lblTotalCost"}).text
    weight = soup.find('span', attrs={"id":"ctl15_ctl12_ctl01_ctl00__lblWeight"}).text

    texts = [f"شماره بارکد: {barcode} | شماره قرارداد: {contract_number}", 
    f"نام فرستنده: {sendername} | شهر فرستنده: {sendercity}", 
    f"نام گیرنده: {receivername} | شهرگیرنده: {receivercity}", 
    f"نوع پرداخت: {paytype} | وزن: {weight}", 
    f"هزینه نهایی: {totalcost}"]

    return "\n".join(texts)

if __name__ == "__main__":
    id = input("Enter your id: ")
    print(get_state(id))
