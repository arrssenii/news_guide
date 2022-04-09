from locale import currency
import requests
 
 
response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
currencies = []
if response.status_code == 200:
    content = response.json()
    print(content)
    data = [i for i in content['Valute']]
    for i in data:
        values = content['Valute'][i]
        CharCode = values['CharCode']
        Name = values['Name']
        Previous = values['Previous']
        Value = values['Value']
        currencies.append({'Name': Name, 'Previous': Previous, 'CharCode': CharCode, 'Value': Value})
