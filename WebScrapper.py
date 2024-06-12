from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0", 
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8" }
flipkart_Url = input("Enter the Flipkart URL ::")
snapdeal_Url = input("Enter the Snapdeal URL ::")
amazon_Url = input("Enter the Amazon URL ::")
def scrape_snapdeal(url):
    try:
        r=requests.get(url,headers=headers)
        htmlContent = r.content
        soup = BeautifulSoup(htmlContent,'html.parser')
        name=soup.find('h1',{'class': 'pdp-e-i-head'}).text.strip()
        price = soup.find('span',{'class': 'payBlkBig'}).text.strip().replace(',','')
        return name,price
    except Exception :
        return None,None
def scrape_flipkart(url):
    try:
        r=requests.get(url,headers=headers)
        htmlContent = r.content
        soup = BeautifulSoup(htmlContent,'html.parser')
        name=soup.find('span',{"class": "B_NuCI" })
        price = soup.find('div',{'class': "_30jeq3 _16Jk6d"})
        return name.text.strip(),(price.text.strip()).replace('₹','').replace(',','')
    except Exception :
        return None,None
def scrape_amazon(url):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0", 
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8" 
        }
        r=requests.get(url,headers=headers)
        if r.status_code == 200 :
            htmlContent = r.content
            soup = BeautifulSoup(htmlContent,'html.parser')
            element = soup.find('span',class_='a-size-large product-title-word-break')
            if element:
                name = element.get_text().strip()[:50]
                price = soup.find('span',class_='a-price-whole')
                if price:
                    price = price.get_text().strip().replace(',','').replace('.','')
                    return name,price
    except Exception as e:
        return None,str(e)
Snapdeal_Product_Name,Snapdeal_Product_Price = scrape_snapdeal(snapdeal_Url)
Flipkart_Product_Name,Flipkart_Product_Price = scrape_flipkart(flipkart_Url)
Amazon_Product_Name,Amazon_Product_Price = scrape_amazon(amazon_Url)
if (Snapdeal_Product_Price is not None) and (Flipkart_Product_Price is not None):
    data=[
        ["Website","Product Name","Price"],
        ["Snapdeal",Snapdeal_Product_Name,"Rs."+Snapdeal_Product_Price],
        ["Flipkart",Flipkart_Product_Name,"Rs."+Flipkart_Product_Price],
        ["Amazon",Amazon_Product_Name,"Rs."+Amazon_Product_Price]
    ]
    table = tabulate(data,headers='firstrow',tablefmt='grid')
    print()
    print(table)
    print()
    price_list =[]
    price_list.append(Amazon_Product_Price)
    price_list.append(Snapdeal_Product_Price)
    price_list.append(Flipkart_Product_Price)
    min_price = min(price_list)
    l=[]
    if(min_price == Amazon_Product_Price):
        l.append("Amazon")
        #print("Suggestion :: You can buy from Snapdeal")
    elif (min_price == Flipkart_Product_Price):
        l.append("Flipkart")
        #print("Suggestion :: You can buy from Flipkart")
    elif (min_price == Snapdeal_Product_Price):
        l.append("Snapdeal")
        #print("Suggestion :: You can buy from either of the e-commerce platforms!!")
    if(len(l)==3):
        print("Suggestion :: You can buy from any of the three e-commerce platforms!!")
    elif (len(l)== 2):
        print("Suggestion :: You can buy from either",l[0],"or",l[1],"!!")
    else:
        print("Suggestion :: You can buy from",l[0])
    print("Thank You !!")

else:
    print()
    print("Product price not available")

