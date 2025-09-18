#!/usr/bin/env python3
import argparse
from yahooquery import Ticker
import sys
from typing import Dict, Any

# Fetches and displays business summary and key info for a given security (EQUITY or ETF)
# from Yahoo Finance using yahooquery. Prints each field with colored labels.


def get_info(ticker_symbol: str) -> Dict[str, Any]:
    """
    Fetch business summary and key info for a security (EQUITY or ETF) from Yahoo Finance.
    Returns a dictionary of fields.
    """
    t = Ticker(ticker_symbol)
    result: dict[str, str] = {}
    result["name"] = t.quote_type[ticker_symbol]["shortName"]
    result["type"] = t.quote_type[ticker_symbol]["quoteType"]
    result["incipit"] = t.quote_type[ticker_symbol]["firstTradeDateEpochUtc"]
    result["location"] = t.quote_type[ticker_symbol]["timeZoneFullName"]
    result["description"] = t.asset_profile[ticker_symbol]["longBusinessSummary"]
    result["exchange"] = (
        t.price[ticker_symbol]["exchange"]
        + " "
        + t.price[ticker_symbol]["exchangeName"]
    )
    result["currency"] = t.summary_detail[ticker_symbol]["currency"]
    result["avg_daily_volume10days"] = t.summary_detail[ticker_symbol][
        "averageDailyVolume10Day"
    ]

    if result["type"] == "ETF":
        result["expense_ratio"] = t.fund_profile[ticker_symbol][
            "feesExpensesInvestment"
        ]["annualReportExpenseRatio"]
        result["yield"] = t.quotes[ticker_symbol]["dividendYield"]
        result["1YearReturn"] = t.fund_performance[ticker_symbol]["trailingReturns"][
            "oneYear"
        ]
        result["3YearReturn"] = t.fund_performance[ticker_symbol]["trailingReturns"][
            "threeYear"
        ]
        result["5YearReturn"] = t.fund_performance[ticker_symbol]["trailingReturns"][
            "fiveYear"
        ]
        result["10YearReturn"] = t.fund_performance[ticker_symbol]["trailingReturns"][
            "tenYear"
        ]

    elif result["type"] == "EQUITY":
        pass
    else:
        print(
            f"Cannot process security type '{result['type']}'. Only EQUITY or ETF are supported.",
            file=sys.stderr,
        )
        sys.exit(2)

    return result


def print_info_colored(info: Dict[str, Any]) -> None:
    """
    Print each field name in yellow and its value on a new line.
    """
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    for key, value in info.items():
        print(f"{YELLOW}{key}{RESET}: {value}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch business summary and key info for a security (EQUITY or ETF) from Yahoo Finance."
    )
    parser.add_argument(
        "ticker", type=str, help="Security ticker symbol (e.g., AAPL, SPMO, TSLA, VOO)"
    )
    args = parser.parse_args()

    ticker: str = args.ticker.strip().upper()
    print(f"Fetching '{ticker}'..\n")
    info: Dict[str, Any] = get_info(ticker)
    print_info_colored(info)


if __name__ == "__main__":
    main()
