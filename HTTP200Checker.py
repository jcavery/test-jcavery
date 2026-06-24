import requests
import sys

def check_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; URLChecker/1.0)"}
        r = requests.get(url.strip(), headers=headers, timeout=1, allow_redirects=True)
        return r.status_code == 200, r.status_code
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_200.py urls.txt [output.txt]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "successful_200_urls.txt"

    successful_urls = []

    with open(input_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    print(f"Checking {len(urls)} URLs...\n")

    for url in urls:
        is_200, status = check_url(url)
        if is_200:
            successful_urls.append(url)
            print(f"[200] {url}")
        else:
            print(f"[XX] {url} ({status})")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(successful_urls) + "\n")

    print(f"\nDone. {len(successful_urls)} URLs returned HTTP 200 OK.")
    print(f"Saved to: {output_file}")