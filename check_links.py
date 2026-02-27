import re
import urllib.request
from urllib.error import URLError, HTTPError
import ssl

context = ssl._create_unverified_context()

files = [
    r"d:\python\RD_model_LST2\docs\zero_variance_references.md",
    r"d:\python\RD_model_LST2\docs\random_sampling_references.md",
    r"d:\python\RD_model_LST2\docs\feature_selection_references.md"
]

all_urls = []

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        urls = re.findall(r'\[(?:DOI|URL).*?\]\((https?://.*?)\)', content)
        urls.extend(re.findall(r'\[(?:DOI|URL).*?\]\((http?://.*?)\)', content))
        all_urls.extend([(file_path.split('\\')[-1], url) for url in urls])

# Remove duplicates
all_urls = list(set(all_urls))

print(f"Testing {len(all_urls)} URLs...")

req_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for filename, url in all_urls:
    req = urllib.request.Request(url, headers=req_headers)
    try:
        response = urllib.request.urlopen(req, context=context, timeout=10)
        status = response.getcode()
        if status == 200:
            print(f"[OK] {filename} -> {url}")
        else:
            print(f"[WARN] {filename} -> {url} (Status: {status})")
    except HTTPError as e:
        if e.code in [403, 401]: # Many academic sites block programmatic access
            print(f"[OK/BLOCKED] {filename} -> {url} (HTTP {e.code}, likely valid but bots blocked)")
        else:
            print(f"[ERROR] {filename} -> {url} (HTTP Error: {e.code})")
    except URLError as e:
        print(f"[ERROR] {filename} -> {url} (URL Error: {e.reason})")
    except Exception as e:
        print(f"[ERROR] {filename} -> {url} (General Error: {str(e)})")
