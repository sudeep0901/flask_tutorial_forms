import json

f = open('customer.json', 'r')
data = json.load(f)
print(data)