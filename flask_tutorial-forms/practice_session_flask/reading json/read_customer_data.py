import json

def read_customer_data():
    with open('customer.json') as json_file:
        customer_data = json.load(json_file)
    return customer_data



data = read_customer_data()

print(type(data), len(data))
print(data[0])