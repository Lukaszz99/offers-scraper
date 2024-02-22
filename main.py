from otodom import OtoDomScrapper
import pandas as pd


if __name__ == "__main__":
    scrapper = OtoDomScrapper(url="https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/"
                                  "warszawa?distanceRadius=25&limit=72&by=LATEST&direction=DESC&viewType=listing&page=1")
    all_offers = scrapper.run_scrapping()

    df = pd.DataFrame(all_offers)
    print(df)

    df.to_csv('offers_today.csv', index=False)
