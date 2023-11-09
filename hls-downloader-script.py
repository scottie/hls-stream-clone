# hls-downloader-script.py
from hls_downloader import download_hls
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hls-downloader-script.py <hls_url>")
        sys.exit(1)

    hls_url = sys.argv[1]
    download_hls(hls_url)