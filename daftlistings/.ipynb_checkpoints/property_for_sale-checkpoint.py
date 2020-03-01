import logging

from daftlistings.listing import Listing


class PropertyForSale(Listing):
    def __init__(self, data_from_search=None, url=None):
        super().__init__(data_from_search, url)

    @property
    def formalised_address(self):
        if self.data_from_search:
            t = self.data_from_search.find(
                "a", {"class": "PropertyInformationCommonStyles__addressCopy--link"}
            )
            address = t.text
        else:
            address = self._ad_page_content.find(
                "h1", {"class": "PropertyMainInformation__address"}
            ).text.strip()

        s = address.split("-")
        a = s[0].strip()
        if "SALE AGREED" in a:
            a = a.split()
            a = a[3:]
            a = " ".join([str(x) for x in a])
        return a.lower().title().strip()

    @property
    def price(self):
        try:
            if self.data_from_search:
#                 print(self.data_from_search.find(
#                     "strong", {"class": "PropertyInformationCommonStyles__costAmountCopy"}
#                 ))
                price = self.data_from_search.find(
                    "strong", {"class": "PropertyInformationCommonStyles__costAmountCopy"}
                ).text
            else:
#                 print( self._ad_page_content.find(
#                     "strong", {"class": "PropertyInformationCommonStyles__costAmountCopy"}
#                 ).text)
                price = self._ad_page_content.find(
                    "strong", {"class": "PropertyInformationCommonStyles__costAmountCopy"}
                ).text
            
            price = int("".join([str(s) for s in price if s.isdigit()]))
#             print(price)
            return price
        except Exception as e:
            logging.error("Error getting price. Error message: " + e.args[0])

    @property
    def bedrooms(self):
        try:
            if self.data_from_search:
                bedrooms = self.data_from_search.find_all(
                    "div", {"class": "QuickPropertyDetails__iconContainer"}
                )[0]
            else: 
                print(self._ad_page_content.find(
                    "div", {"class": "QuickPropertyDetails__iconCopy--WithBorder"}
                ))
                
                bedrooms = self._ad_page_content.find(
                    "div", {"class": "QuickPropertyDetails__iconCopy--WithBorder"}
                ).text
                
            return int(bedrooms.find("span").text)
        except AttributeError:
            return int(bedrooms.find("img")["alt"][-1])

    @property
    
    def bathrooms(self):
        try:
            if self.data_from_search:
                
                bathrooms = self.data_from_search.find_all(
                    "div", {"class": "QuickPropertyDetails__iconContainer"}
                )[1]
            
            else: 

                bathrooms = self._ad_page_content.find(
                    "div", {"class": "QuickPropertyDetails__iconCopy--WithBorder"}
                ).text
        
            return int(bathrooms.find("span").text)
        except AttributeError:
            return int(bathrooms.find("img")["alt"][-1])

    @property
    def images(self):
        uls = self._ad_page_content.find("div", {"id": "pbxl_carousel"}).find("ul")
        images = []
        if uls is None:
            return
        for li in uls.find_all("li"):
            if li.find("img")["src"]:
                images.append(li.find("img")["src"])

        return images
