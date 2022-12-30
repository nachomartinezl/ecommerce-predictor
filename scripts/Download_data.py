
import pandas as pd
import json
import requests
import os
os.chdir('/home/app/src/') 

#with open('../products.json', encoding='utf-8') as f:
with open('/home/app/src/data/products.json', encoding='utf-8') as f:
    prod = json.load(f)

#droppping some columns
df = pd.DataFrame(prod)
df = df.drop(['price', 'upc', 'shipping', 'model'], axis=1)


#add an ending to see if its a gif or a png
ending= []

for row in df['image']:
    ending.append(row.split('.')[-1])

df['ending'] = ending

#download images

n=0        
index = 0   
for row in df['image']:
        
    image = requests.get(row).content

    #if len is 9 is a broken url
    if len(image) == 9 or df['ending'][index] == 'gif':
        index += 1
        continue
    
    index += 1
    n +=1
    end = row.split('.')[-1]
    nombre_local_imagen = "row" + str(n) +'.'+ str(end)
   
    with open("/home/app/src/data_img/" + nombre_local_imagen, 'wb') as handler:
        handler.write(image)
