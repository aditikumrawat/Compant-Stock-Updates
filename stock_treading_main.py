import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

ACCOUNT_SID = "ACa28cefa0f6a1f368f47dc93e279c22c1"
AUTH_TOKEN = "4bd2624c06975cd4e66f6bd6e8693777"
TWILIO_NUMBER = "+16693221450"
TARGET_NUMBER = "+919644295555"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API_KEY_STOCK = "EI2P120CWPXBG01H" #Alpha Vantage (api key of stock treding market)
API_KEY_NEWS = "5fb34aa0e68343db84a80ab5d192a3f1"

# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : API_KEY_STOCK
}

response = requests.get(STOCK_ENDPOINT,params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_stock = data_list[0]
yesterday_stock_closing = yesterday_stock["4. close"]


#TODO 2. - Get the day before yesterday's closing stock price
day_before_yesterday_stock = data_list[1]
day_before_yesterday_stock_closing = day_before_yesterday_stock["4. close"]

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = 20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference_in_stock = 0
stock_up_down = ""
difference_in_stock = round(float(day_before_yesterday_stock_closing) - float(yesterday_stock_closing))
if difference_in_stock > 0 :
    stock_up_down = "🔺"
else:
    stock_up_down = "🔻"


#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
news_params = {
    "apikey" : API_KEY_NEWS,
    "qInTitle" : COMPANY_NAME
}

news_response = requests.get(NEWS_ENDPOINT,params = news_params)
data_articles = news_response.json()["articles"]

# 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME. 


#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
articles = data_articles[:3]
if abs(difference_in_stock) > 5:
    # print(articles)
    pass

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

formatted_article = [f'{STOCK_NAME}:{stock_up_down}{difference_in_stock}%\nHeadline : {value["title"]}\nBrief : {value["description"]}' for value in articles]

#TODO 9. - Send each article as a separate message via Twilio. 

client = Client(ACCOUNT_SID, AUTH_TOKEN)
for article in formatted_article:
    message = client.messages \
                        .create(
                            body=f"\n{article}",
                            from_='+16693221450',
                            to= TARGET_NUMBER
                            )
    print(message.status)
        

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

