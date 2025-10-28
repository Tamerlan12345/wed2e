from src.parsers.leopar_parser import LeoparParser
from src.parsers.emex_parser import EmexParser
from src.core.analysis import AnalysisCore
import logging

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # List of VIN codes to process
    vin_codes = ['VIN1', 'VIN2', 'VIN3'] # Replace with actual VIN codes

    # Initialize parsers
    leopar_parser = LeoparParser()
    emex_parser = EmexParser()

    for vin in vin_codes:
        logging.info(f"Processing VIN: {vin}")

        try:
            # Scrape data
            leopar_data = leopar_parser.search_by_vin(vin)
            emex_data = emex_parser.search_by_vin(vin)

            # Analyze and report
            if leopar_data or emex_data:
                core = AnalysisCore(leopar_data, emex_data)
                report = core.generate_report()

                # Print to console
                print(report)

                # Save to file
                with open('report.log', 'a') as f:
                    f.write(f"Report for VIN: {vin}\n")
                    f.write(report)
                    f.write("\n\n")
            else:
                logging.warning(f"No data found for VIN: {vin}")

        except Exception as e:
            logging.error(f"An error occurred while processing VIN {vin}: {e}")
            continue # Continue to the next VIN

    # Close the browser
    emex_parser.close()

if __name__ == '__main__':
    main()
