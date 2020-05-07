import pandas as pd
import numpy as np
import re
from datetime import datetime
import sys
import numpy_financial as npf
import requests
from bs4 import BeautifulSoup
    
%matplotlib inline
pd.set_option('display.float_format', lambda x: '%.3f' % x)


def monthly_mortgage_cost(purchase_price, years, mortgage_rate, down_payment):
    return npf.pmt(pv=purchase_price*(1-down_payment),nper=years*12,rate=mortgage_rate/12)


def property_rent_percentiles(rent_data , buckets=10): # TBD
    percentiles = np.percentile(rent_data, buckets)
    return percentiles


def operating_expenses(maintanence, management_fees, 
                           house_insurance, local_property_taxes, mortgage_protection_insurance, 
                           utilities, trash):
    return maintanence + management_fees + house_insurance+ local_property_taxes + mortgage_protection_insurance + utilities + trash


def gross_operating_income(gross_potential_income, vacancy_rate):
    return gross_potential_income*(1-vacancy_rate)


def net_operating_income(gross_operating_income_val, operating_expenses_val):
    return gross_operating_income_val - operating_expenses_val


def cap_rate(purchase_price, net_operating_income_val):
    return net_operating_income/purchase_price


def upfront_cash(down_payment, closing_costs, renovation_costs):
    return down_payment + closing_costs + renovation_costs


def cash_on_cash(net_operating_income_val, upfront_cash_val):
    return net_operating_income_val/upfront_cash


def price_to_rent(purchase_price, gross_potential_income):
    return purchase_price/gross_potential_income


def cash_flow_from_operations(net_operating_income_val, renovations_norm=0):
    return net_operating_income_val - renovations_norm


def cash_flow_after_financing(cash_flow_from_operations_val, mortgage):
    return cash_flow_from_operations_val - mortgage


def vacancy_rate(days_unoccupied, total_time):
    return days_unoccupied/total_time


def break_even_ratio(gross_operating_income_val, operating_expenses, mortgage):
    return (mortgage + operating_expenses)/gross_operating_income_val


def pull_aib_rates():
    url = "https://aib.ie/our-products/mortgages/residential-buy-to-let-mortgage#rates-wrapper"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')


    tables = soup.findAll("div", {"class": "tab-content"})
    overall_data = {}
    for table in tables:
        i = 'PrinciplePrimaryResidence'
        table_data = {}
        for row in table.find_all("tr")[1:]:
            col = row.find_all("td")
            try:
                name = str(col[0]).replace('<td>\n<span>', '').replace('</span>\n</td>', '').replace('&gt;', '>').replace('&lt;', '<')
                if 'span' in name:
                    continue
                if 'Standard Variable' in name:
                    overall_data[i] = table_data
                    table_data = {}
                    i = 'BuyToLet'
                val = str(col[1]).replace('<td>\n<span>', '').replace('</span>\n</td>', '')
                table_data[name] = val
            except:
                pass
        overall_data[i] = table_data
        return overall_data
    
    
