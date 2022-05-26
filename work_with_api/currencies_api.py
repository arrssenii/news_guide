import requests
response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
currencies = []
if response.status_code == 200:
    content = response.json()
    data = [i for i in content['Valute']]
    for i in data:
        values = content['Valute'][i]
        CharCode = values['CharCode']
        Nominal = values['Nominal']
        Name = values['Name']
        Previous = values['Previous']
        Value = values['Value']
        if Value > Previous:
            currencies.append({'Name': f'{Nominal} {Name}', 'Previous': Previous,
                            'CharCode': CharCode, 'Value': f'{Value} ▲'})
        else:
            currencies.append({'Name': Name, 'Previous': Previous,
                            'CharCode': CharCode, 'Value': f'{Value} ▼'})
