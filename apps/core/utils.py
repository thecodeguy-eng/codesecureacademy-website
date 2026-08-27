def cloudinary_optimized_url(url):
    """Insert an auto-format/auto-quality/capped-width transformation into a
    Cloudinary delivery URL, so the browser gets a right-sized WebP/AVIF
    instead of the original upload (which can be several MB for something
    rendered as a small card thumbnail)."""
    if not url or "/upload/" not in url:
        return url
    return url.replace("/upload/", "/upload/f_auto,q_auto,w_1600,c_limit/", 1)
