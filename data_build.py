from daftlistings import Daft, SaleType, HouseType, SortType
import statsmodels.api as sm
import pandas as pd
import numpy as np
from IPython.display import HTML

daft = Daft()

county = "Dublin"
areas = ["Dublin 15","Dublin 7"]
#areas = ["Ashtown"]

daft.set_listing_type(SaleType.HOUSES)
daft.set_house_type(HouseType.DETACHED)
daft.set_area(areas)
daft.set_county(county)
daft.set_sort_by(SortType.PRICE)

df = pd.DataFrame()

listings = daft.search()


for listing in listings:
#     print(listing)
    try:
        
        data = pd.DataFrame([listing.price,  listing.bedrooms,  listing.bathrooms,
                             listing.dwelling_type, listing.ber_code, listing.floor_area,
                             listing.town, listing.county, listing.daft_link]).T

        df = df.append(data)

    except:
        continue



# Rename the columns
df.columns = ["Price", 'Beds', 'Baths', 'Type', 'BER', 'Area', 'Town','County', 'URL']




# Convert the datatypes to int or float
df = df[~df['Price'].isnull()]

# Display the output
df.Price = df.Price.astype(int)
df.Beds = df.Beds.astype(int)
df.Baths = df.Baths.astype(int)
df['Area'] = df['Area'].str.strip()
df.Area = df.Area.replace(r'^\s*$', np.nan, regex=True)
df.Area = df.Area.fillna(50).astype(float)
df.BER = df.BER.replace('exempt', 'G')
df.BER.fillna(value='G', inplace = True)


# Display the output
display(HTML(df.to_html()))