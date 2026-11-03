# Obstacle Log

## Project: API-Powered Travel Intelligence Tool

### 1. API Connection

Obstacle:
Initially, connecting the Python application
to the REST Countries API required understanding
the correct endpoint and authentication method.

Solution:
Used the requests library and configured
the API endpoint and bearer token separately.

### 2. Understanding JSON Response

Obstacle:
The API response contained nested JSON objects,
making it difficult to retrieve individual fields.

Solution:
Inspected the JSON structure and used dictionary
methods to extract the required information.

### 3. Missing Information

Obstacle:
Some countries may not contain information
for every requested field.

Solution:
Used dictionary get() methods and fallback
values to prevent missing-field errors.

### 4. Neighbouring Countries

Obstacle:
The API returns ISO alpha-3 codes for neighbouring
countries instead of their full names.

Solution:
Implemented additional API requests to resolve
the country codes into readable country names.

### 5. Error Handling

Obstacle:
Invalid country names and network failures
could interrupt the application.

Solution:
Implemented exception handling for HTTP errors,
connection failures and request timeouts.

### 6. Output Management

Obstacle:
The country information needed to be stored
in a structured and reusable format.

Solution:
Used Python's json module to save the retrieved
information into separate JSON files.

## Conclusion

The challenges were addressed by improving
API integration, JSON parsing, error handling
and output management.