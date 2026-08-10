"""Shared helpers for normalising a pasted video URL (YouTube/Drive share
link, or a direct file URL like a Cloudinary-hosted mp4) into something a
template can embed. Originally lived only on `cohorts.Track`; extracted so
`courses.CourseModule` can reuse the exact same logic instead of duplicating
it.
"""

import re


def is_embeddable_video(url):
    """True for YouTube/Drive links that need an <iframe>; False for a
    direct file URL (e.g. Cloudinary-hosted mp4) that a <video> tag can
    play directly."""
    return bool(url) and ("youtube.com" in url or "youtu.be" in url or "drive.google.com" in url)


def embed_video_url(url):
    """Normalises a pasted YouTube/Drive share link into its embeddable
    form. Admins/tutors can paste whatever link format they were given —
    watch/short URLs for YouTube, "view" links for Drive."""
    if not url:
        return ""
    youtu_be = re.match(r"https?://youtu\.be/([\w-]+)", url)
    if youtu_be:
        return f"https://www.youtube.com/embed/{youtu_be.group(1)}"
    watch = re.search(r"[?&]v=([\w-]+)", url)
    if "youtube.com" in url and watch:
        return f"https://www.youtube.com/embed/{watch.group(1)}"
    if "youtube.com/embed/" in url:
        return url
    drive = re.match(r"https?://drive\.google\.com/file/d/([\w-]+)", url)
    if drive:
        return f"https://drive.google.com/file/d/{drive.group(1)}/preview"
    return url
