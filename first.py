from bs4 import BeautifulSoup
import requests
import pandas as pd

website = 'https://www.cars.com/shopping/results/?stock_type=cpo&makes%5B%5D=mercedes_benz&models%5B%5D=&list_price_max=&maximum_distance=20&zip='

response = requests.get(website)
soup = BeautifulSoup(response.content, 'html.parser')

results = soup.findAll('div', {'class': 'vehicle-card'})

name = []
mileage = []
dealer_name = []
rating = []
review_count = []
price = []

for result in results:
    # name
    try:
        name.append(result.find('h2').get_text())
    except:
        name.append('n/a')
    # mileage
    try:
        mileage.append(result.find('div', {'class': 'mileage'}).get_text())
    except:
        mileage.append('n/a')
    # dealer_name
    try:
        dealer_name.append(result.find('div', {'class': 'dealer-name'}).get_text().strip())
    except:
        dealer_name.append('n/a')
    # rating
    try:
        rating.append(result.find('span', {'class': 'sds-rating__count'}).get_text())
    except:
        rating.append('n/a')
    # review_count
    try:
        review_count.append(result.find('span', {'class': 'sds-rating__link'}).get_text())
    except:
        review_count.append('n/a')

    # price
    try:
        price.append(result.find('span', {'class': 'primary-price'}).get_text())
    except:
        price.append('n/a')

car_dealer = pd.DataFrame({'Name': name, 'Mileage': mileage, 'Dealer Name': dealer_name,
                           'Rating': rating, 'Review Count': review_count, 'Price': price})

car_dealer['Review Count'] = car_dealer['Review Count'].apply(lambda x: x.strip('reviews)').strip('('))
car_dealer.to_excel('car_dealer.xlsx', index=False)

