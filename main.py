import requests
import json
import os
import sys
from urllib.parse import quote
try:
    with open("config.json", "r") as file:
        config = json.load(file)
    API_URL = config["api_base_url"].rstrip("/")
    API_KEY = config["api_key"]
    TIMEOUT = config.get("request_timeout", 15)
    OUTPUT_DIR = config.get("output_directory", "outputs")
except FileNotFoundError:
    print("Error: config.json file not found.")
    sys.exit(1)
except (json.JSONDecodeError, KeyError) as error:
    print("Configuration error:", error)
    sys.exit(1)
def make_api_request(url):
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise Exception("Request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        raise Exception(
            "Network connection failed. Check your internet."
        )
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 404:
            raise Exception("Country not found.")
        elif error.response.status_code == 401:
            raise Exception("Invalid API key.")
        elif error.response.status_code == 403:
            raise Exception("API access forbidden.")
        elif error.response.status_code == 429:
            raise Exception("API request limit exceeded.")
        else:
            raise Exception(
                f"API request failed: HTTP {error.response.status_code}"
            )
    except requests.exceptions.RequestException as error:
        raise Exception(f"Request error: {error}")
    except ValueError:
        raise Exception("Invalid JSON response received.")
def get_neighbour_names(border_codes):
    neighbours = []
    for code in border_codes:
        try:
            url = f"{API_URL}/codes.alpha_3/{quote(code)}"
            result = make_api_request(url)
            countries = result.get("data", {}).get("objects", [])
            if countries:
                country_name = countries[0].get(
                    "names", {}
                ).get("common", code)
                neighbours.append(country_name)
        except Exception:
            neighbours.append(code)
    return neighbours
def extract_currencies(currency_data):
    currencies = []

    # Handle currency data returned as a list
    if isinstance(currency_data, list):
        for item in currency_data:
            if isinstance(item, dict):
                name = item.get("name", "Unknown")
                code = item.get("code", "")
                symbol = item.get("symbol", "")

                currency = name

                if code:
                    currency += f" ({code})"

                if symbol:
                    currency += f" - {symbol}"

                currencies.append(currency)

    # Handle currency data returned as a dictionary
    elif isinstance(currency_data, dict):
        for code, details in currency_data.items():
            if isinstance(details, dict):
                name = details.get("name", "Unknown")
                symbol = details.get("symbol", "")

                currency = f"{name} ({code})"

                if symbol:
                    currency += f" - {symbol}"

                currencies.append(currency)

            elif isinstance(details, str):
                currencies.append(f"{details} ({code})")

    return currencies if currencies else ["Not available"]
def extract_languages(language_data):
    languages = []
    if isinstance(language_data, list):
        for language in language_data:
            if isinstance(language, dict):
                name = (
                    language.get("english_name")
                    or language.get("name")
                    or language.get("native_name")
                )
                if name:
                    languages.append(name)
            elif isinstance(language, str):
                languages.append(language)
    elif isinstance(language_data, dict):
        for language in language_data.values():
            if isinstance(language, dict):
                name = (
                    language.get("english_name")
                    or language.get("name")
                )
                if name:
                    languages.append(name)
            elif isinstance(language, str):
                languages.append(language)
    return languages if languages else ["Not available"]
def get_country_information(country_name):
    print("\nConnecting to REST Countries API...")
    encoded_name = quote(country_name.strip(), safe="")
    url = f"{API_URL}/names.common/{encoded_name}"
    try:
        result = make_api_request(url)
        countries = result.get(
            "data", {}
        ).get("objects", [])
        if not countries:
            print("\nCountry not found.")
            return None
        country = countries[0]
        name = country.get(
            "names", {}
        ).get("common", "Not available")
        capital_data = country.get("capitals", [])
        if isinstance(capital_data, list):
            capitals = [
                item.get("name", "")
                for item in capital_data
                if isinstance(item, dict) and item.get("name")
            ]
        else:
            capitals = []
        if not capitals:
            capitals = ["Not available"]
        currency = extract_currencies(
            country.get("currencies", {})
        )
        population = country.get(
            "population", "Not available"
        )
        languages = extract_languages(
            country.get("languages", [])
        )
        region = country.get(
            "region", "Not available"
        )
        border_codes = country.get("borders", [])
        if not isinstance(border_codes, list):
            border_codes = []
        neighbours = get_neighbour_names(border_codes)
        if not neighbours:
            neighbours = ["No land neighbours"]
        country_information = {

            "country": name,

            "capital": capitals,

            "currency": currency,

            "population": population,

            "languages": languages,

            "region": region,

            "neighbouring_countries": neighbours
        }
        return country_information
    except Exception as error:
        print("\nError:", error)
        return None
def display_country_information(data):
    if not data:
        return
    print("\n" + "=" * 50)
    print("       TRAVEL INTELLIGENCE REPORT")
    print("=" * 50)
    print("\nCountry       :", data["country"])
    print("Capital       :", ", ".join(data["capital"]))
    print("Currency      :", ", ".join(data["currency"]))
    print(
        "Population    :",
        f'{data["population"]:,}'
        if isinstance(data["population"], int)
        else data["population"]
    )
    print("Languages     :", ", ".join(data["languages"]))
    print("Region        :", data["region"])
    print("\nNeighbouring Countries:")
    for neighbour in data["neighbouring_countries"]:
        print("  -", neighbour)
    print("\n" + "=" * 50)
def save_country_information(data):
    if not data:
        return
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = (
            data["country"]
            .lower()
            .replace(" ", "_")
            + ".json"
        )
        filepath = os.path.join(
            OUTPUT_DIR,
            filename
        )
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )
        print("\nOutput saved successfully:", filepath)
    except OSError as error:
        print("\nUnable to save output:", error)
def main():
    print("----  API-POWERED TRAVEL INTELLIGENCE TOOL  ----")
    if len(sys.argv) > 1:
        country_name = " ".join(sys.argv[1:])
    else:
        country_name = input(
            "\nEnter a country name: "
        ).strip()
    if not country_name:
        print("\nPlease enter a valid country name.")
        return
    information = get_country_information(
        country_name
    )
    if information:
        display_country_information(information)
        save_country_information(information)
if __name__ == "__main__":
    main()