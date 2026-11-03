# API-Powered Travel Intelligence Tool

A Python-based travel information tool that retrieves
country information using the REST Countries API.

## Features

- Retrieves country information using a public REST API.
- Displays capital cities.
- Extracts currency information.
- Retrieves population statistics.
- Displays official languages.
- Identifies geographic regions.
- Retrieves neighbouring countries.
- Handles API and network errors.
- Stores API configuration separately.
- Saves country information as JSON files.

## Technologies Used

- Python
- Requests
- REST Countries API
- JSON

## Sample Test Cases

1. India
2. Canada
3. Japan
4. Bhutan
5. InvalidCountry123

## Output

The program displays a formatted travel report
and automatically saves the result as a JSON file
inside the outputs directory.

## Error Handling

The application handles:

- Invalid country names.
- Network connection failures.
- Request timeouts.
- Invalid API credentials.
- HTTP errors.
- Missing country information.

## API Reference

https://restcountries.com/docs/countries