# VIN-Analyst

VIN-Analyst is an intelligent assistant for purchasing auto parts. It's a Python application designed to scrape auto parts data from leopar.kz and emex.ru based on a list of VIN codes, analyze the findings, and generate a report with the best deals.

## Features

*   Scrapes data from leopar.kz and emex.ru.
*   Analyzes prices and finds the best deals.
*   Converts currencies automatically.
*   Generates a comprehensive report.

## Getting Started

### Prerequisites

*   Docker
*   Docker Compose

### Installation and Usage

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/vin-analyst.git
    ```
2.  Create a `config.ini` file in the `config` directory with your credentials for leopar.kz and emex.ru.
3.  Run the application:
    ```bash
    docker-compose up
    ```

## Project Structure

```
.
├── config
│   └── config.ini
├── src
│   ├── core
│   │   └── analysis.py
│   └── parsers
│       ├── leopar_parser.py
│       └── emex_parser.py
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── main.py
├── README.md
└── requirements.txt
```
