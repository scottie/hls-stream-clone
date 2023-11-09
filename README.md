This will clone a cloudflare HLS stream.

**Example Usage:**
```python
python hls-downloader-script.py https://customer-m033z5x00ks6nunl.cloudflarestream.com/b236bde30eb07b9d01318940e5fc3eda/manifest/video.m3u8
```  

**Install:**
```bash
python -m pip install --upgrade build
python -m build
pip install dist/hls_downloader-0.1-py3-none-any.whl
```

**Installed Usage:**
```python
hls-downloader https://customer-m033z5x00ks6nunl.cloudflarestream.com/b236bde30eb07b9d01318940e5fc3eda/manifest/video.m3u8
```