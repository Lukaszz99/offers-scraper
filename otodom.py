import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_url_soup(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    r = requests.get(url=url, headers=headers)

    return BeautifulSoup(r.content, 'html5lib')


def is_digit_or_comma(x):
    return x.isdigit() or x == ','


class OtoDomScrapper:
    def __init__(self, url):
        self.url = url
        self.main_soup = self.get_url_soup(url)

    def run_scrapping(self) -> list:
        all_offers = list()
        total_pages = self.get_pages_nb()

        for page in range(1, total_pages + 1):
            offers = self.get_page_offers(page)

            page_offers = list()

            for i, offer in enumerate(offers):
                print(f"Scrapping page: {page}/{total_pages}, offer: {i + 1}/{len(offers)}")

                offer_link = self.get_offer_direct_link(offer)
                offer_soup = self.get_url_soup(offer_link)

                offer_general_info = self.get_offer_general_info(offer)
                offer_detail_info = self.get_offer_detail_info(offer_soup)
                # offer_additional_info = self.get_offer_additional_info(offer_soup)
                # offer_uid = self.get_offer_uid(offer_link)
                # offer_creation_date = self.get_offer_creation_date(offer_soup)

                # join all the information into one dictionary
                offer = {
                    "Link": offer_link,
                    **offer_general_info,
                    **offer_detail_info
                }

                all_offers.append(offer)
                page_offers.append(offer)

            df_tmp = pd.DataFrame(page_offers)
            df_tmp.to_csv(f"all_offers_22_11/offers_{page}.csv")
            print(f"Saved offers for page: {page}")

        return all_offers

    @staticmethod
    def get_offer_detail_info(offer_soup) -> dict:
        offer_details = offer_soup.find('div', attrs={'class': 'css-xr7ajr e10umaf20'}).find_all('div')

        info_dict = dict()

        for detail in offer_details:
            if 'aria-label' in detail.attrs:
                detail_key = detail['aria-label']
                try:
                    # in this case value in table is a href to other site, we need to change class name
                    if 'pokoi' in detail_key:
                        detail_value = detail.find('a', attrs={'class': "css-19yhkv9 enb64yk0"}).text
                    else:
                        detail_value = detail.find('div', attrs={'class': "css-1wi2w6s enb64yk5"}).text
                except AttributeError:
                    detail_value = "Zapytaj"

                info_dict[detail_key] = detail_value

        return info_dict

    def get_offer_additional_info(self, offer_soup):
        return None

    def get_offer_uid(self, offer_link):
        # offer_soup = self.get_url_soup(url=offer_link)
        # uid = offer_soup.find('div', attrs={'class': 'css-i4bwcc e16xl7021'}).text

        return None

    def get_offer_creation_date(self, offer_soup):
        # creation_date = offer_soup.find('div', attrs={'class': 'css-1soi3e7 e16xl7024'}).text

        return None

    def get_offer_description(self, offer_soup):
        # description = offer_soup.find('div', attrs={'class': 'css-1ytkscc e16xl7022'}).text

        return None

    @staticmethod
    def get_offer_creation_date(offer_soup):
        # creation_date = offer_soup.find('div', attrs={'class': 'css-1soi3e7 e16xl7024'}).text

        return None

    @staticmethod
    def get_offer_direct_link(offer):
        offer_div = offer.find('a', attrs={'data-cy': 'listing-item-link'})
        offer_link = f"https://www.otodom.pl{offer_div['href']}"

        return offer_link

    @staticmethod
    def get_offer_general_info(offer) -> dict:
        general_info = offer.find('div', attrs={'class': 'e1jyrtvq0 css-1tjkj49 ei6hyam0'}).find_all('span')

        info_list = list()

        for info in general_info:
            info_value = info.text[:len(info.text) - 1]  # remove last character to avoid power number

            info_list.append(
                ''.join(filter(is_digit_or_comma, info_value))
            )

        info_dict = {
            "Cena": info_list[0],
            "Cena za metr": info_list[1],
            "Pokoje": info_list[2],
            "Powierzchnia": info_list[3]
        }

        return info_dict

    @staticmethod
    def get_url_soup(url):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        r = requests.get(url=url, headers=headers)

        return BeautifulSoup(r.content, 'html5lib')

    def get_pages_nb(self):
        pages_nb = int(self.main_soup.find("nav", attrs={'data-cy': "pagination"}).find_all('a')[-1].text)

        return pages_nb

    def get_page_offers(self, page_nb):
        URL = (f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa"
               f"?distanceRadius=25&limit=72&by=LATEST&direction=DESC&viewType=listing&page={page_nb}")
        soup = self.get_url_soup(URL)

        search_listing = soup.find('div', attrs={'data-cy': 'search.listing.organic'})
        offers = search_listing.find_all('li', attrs={'data-cy': 'listing-item'})

        return offers
