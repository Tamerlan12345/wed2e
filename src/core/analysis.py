import configparser
import pandas as pd

class AnalysisCore:
    def __init__(self, leopar_data, emex_data):
        self.config = configparser.ConfigParser()
        self.config.read('config/config.ini')
        self.rub_to_kzt = self.config.getfloat('currency', 'rub_to_kzt')

        self.leopar_df = pd.DataFrame(leopar_data)
        self.emex_df = pd.DataFrame(emex_data)

    def convert_currency(self):
        # Convert price columns to numeric, coercing errors
        self.emex_df['price'] = pd.to_numeric(self.emex_df['price'], errors='coerce')
        self.leopar_df['price'] = pd.to_numeric(self.leopar_df['price'], errors='coerce')

        # Drop rows where price could not be converted
        self.emex_df.dropna(subset=['price'], inplace=True)
        self.leopar_df.dropna(subset=['price'], inplace=True)

        # Apply currency conversion
        self.emex_df['price_kzt'] = self.emex_df['price'] * self.rub_to_kzt
        # For consistency, add a 'price_kzt' column to leopar_df as well
        self.leopar_df['price_kzt'] = self.leopar_df['price']

    def find_best_deals(self):
        self.convert_currency()

        # Add a 'source' column to each dataframe
        self.leopar_df['source'] = 'Leopar.kz'
        self.emex_df['source'] = 'Emex.ru'

        combined_df = pd.concat([self.leopar_df, self.emex_df], ignore_index=True)

        if combined_df.empty:
            return None, None, None, 0

        # Find the overall cheapest deal
        best_overall = combined_df.loc[combined_df['price_kzt'].idxmin()]

        # Find the best deal from each source
        best_leopar = self.leopar_df.loc[self.leopar_df['price_kzt'].idxmin()] if not self.leopar_df.empty else None
        best_emex = self.emex_df.loc[self.emex_df['price_kzt'].idxmin()] if not self.emex_df.empty else None

        # Calculate the average market price
        average_price = combined_df['price_kzt'].mean()

        return best_overall, best_leopar, best_emex, average_price

    def generate_report(self):
        best_overall, best_leopar, best_emex, average_price = self.find_best_deals()

        if best_overall is None:
            return "No parts found."

        report = f"""
        ============================================================
                               VIN-ANALYST REPORT
        ============================================================

        Overall Best Deal:
        ------------------
        Part: {best_overall['name']}
        Brand: {best_overall['brand']}
        Part Number: {best_overall['part_number']}
        Price: {best_overall['price_kzt']:.2f} KZT
        Source: {best_overall['source']}
        Link: {best_overall['link']}

        Best Deal on Leopar.kz:
        -----------------------
        {f"Part: {best_leopar['name']}\\nPrice: {best_leopar['price_kzt']:.2f} KZT\\nLink: {best_leopar['link']}" if best_leopar is not None else "No results from Leopar.kz"}

        Best Deal on Emex.ru:
        ---------------------
        {f"Part: {best_emex['name']}\\nPrice: {best_emex['price']:.2f} RUB ({best_emex['price_kzt']:.2f} KZT at a rate of {self.rub_to_kzt})\\nLink: {best_emex['link']}" if best_emex is not None else "No results from Emex.ru"}

        Market Analysis:
        ----------------
        Average Market Price: {average_price:.2f} KZT

        ============================================================
        """
        return report

if __name__ == '__main__':
    # Example usage:
    # leopar_data = [{'name': 'Part A', 'price': '1000'}]
    # emex_data = [{'name': 'Part A', 'price': '150'}]
    # core = AnalysisCore(leopar_data, emex_data)
    # report = core.generate_report()
    # print(report)
    pass
