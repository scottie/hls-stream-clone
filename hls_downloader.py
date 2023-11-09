# hls_downloader.py
import os
import requests
from m3u8 import M3U8
from urllib.parse import urlparse, urljoin, parse_qs
import argparse

"""

This will clone a cloudflare HLS stream.
Example Usage:

python hls-dl.py https://customer-m033z5x00ks6nunl.cloudflarestream.com/b236bde30eb07b9d01318940e5fc3eda/manifest/video.m3u8

"""
def download_hls(hls_url):
    # Extract the unique ID from the HLS URL
    unique_id = urlparse(hls_url).path.split('/')[1]

    # Directory to save HLS streams
    output_dir = os.path.join("hls_streams", unique_id)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Download the master manifest
    response = requests.get(hls_url)
    master_manifest = response.text

    # Parse the master manifest
    m3u8_obj = M3U8(master_manifest)

    # Function to generate unique filenames for segments
    def generate_unique_filename(segment_uri):
        query = parse_qs(urlparse(segment_uri).query)
        filename = os.path.basename(urlparse(segment_uri).path)
        return filename.split('?')[0]  # Remove the query string

    # Create the "manifest" folder
    manifest_output_dir = os.path.join(output_dir, "manifest")
    os.makedirs(manifest_output_dir, exist_ok=True)

    # Save the master manifest as "video.m3u8"
    master_output_file = os.path.join(manifest_output_dir, "video.m3u8")
    with open(master_output_file, 'w') as f:
        f.write(master_manifest)

    print(f"Downloaded master manifest to {master_output_file}")

    # Iterate through the variant streams
    for playlist in m3u8_obj.playlists:
        variant_url = urljoin(hls_url, playlist.uri)
        variant_name = os.path.splitext(os.path.basename(variant_url.split("?")[0]))[0]
        output_file = os.path.join(manifest_output_dir, f"{variant_name}.m3u8")

        # Download the variant playlist
        response = requests.get(variant_url)
        with open(output_file, 'w') as f:
            f.write(response.text)

        print(f"Downloaded {variant_name} playlist to {output_file}")

        # Now, let's download the individual video segments
        variant_playlist = M3U8(response.text)
        for segment in variant_playlist.segments:
            segment_url = urljoin(variant_url, segment.uri)
            output_segment = os.path.join(output_dir, segment_url.split(f"/{unique_id}/")[1].split("?")[0])

            # Create the necessary directories
            os.makedirs(os.path.dirname(output_segment), exist_ok=True)

            response = requests.get(segment_url)
            with open(output_segment, 'wb') as f:
                f.write(response.content)

            print(f"Downloaded {segment.uri} to {output_segment}")

    print("Downloaded all variant playlists and video segments.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download HLS streams.")
    parser.add_argument("hls_url", help="URL of the HLS manifest (master.m3u8)")
    args = parser.parse_args()
    download_hls(args.hls_url)