import pandas as pd

inventory = pd.read_csv('Q2_Pandas_Assignments\inventory.csv')
staten_island=inventory[:10]
product_request = staten_island.product_description
condition = (inventory['location']=='Brooklyn') & (inventory['product_type']=='seeds')
seed_request = inventory[condition]
inventory['in_stock'] = inventory['quantity']>0
inventory['total_value'] = inventory['price'] * inventory['quantity']
combine_lambda = lambda row:'{0} - {1}'.format(row[1], row[2])
inventory['full_description'] = inventory.apply(combine_lambda,axis=1)
print(inventory.head(5))