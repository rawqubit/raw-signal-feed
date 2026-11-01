#!/usr/bin/env python3
"""Build the Raw Signal mirror feed.

Fetches the Muse-generated RSS feed, rewrites the channel metadata with the
Raw Signal branding (title, description, iTunes author/owner, category, new
logo), and leaves every episode item untouched. Spotify for Creators rejects
the original feed because it lacks Author and owner Email; the mirror adds
exactly those fields.

Usage: build_mirror.py --base-url https://<host>/raw-signal-feed/
The base URL is where feed.xml and logo.png will be publicly hosted.
"""
import argparse
import sys
import urllib.request
import xml.etree.ElementTree as ET

SOURCE_FEED = "https://muse.ai/podcasts/feed/499128806620654/9bbc6577-7e48-40f2-baf6-6ad0bc58bd7f"
ITUNES = "http://www.itunes.com/dtds/podcast-1.0.dtd"
ATOM = "http://www.w3.org/2005/Atom"
ET.register_namespace("itunes", ITUNES)
ET.register_namespace("atom", ATOM)

TITLE = "Raw Signal"
DESCRIPTION = (
    "Raw Signal is your daily briefing on tech, AI, and crypto - the signal, "
    "not the noise. Every morning, Maya and Devon break down the stories that "
    "actually matter: the mechanisms, the money, and the second-order effects "
    "the headlines skip. No hype, no filler. New episodes daily."
)
AUTHOR = "Srinikhil Chakilam"
OWNER_EMAIL = "Nikhil@rawqubit.com"
CATEGORY = "Technology"


def q(tag):
    return "{%s}%s" % (ITUNES, tag)


def set_text(parent, tag, text):
    el = parent.find(q(tag))
    if el is None:
        el = ET.SubElement(parent, q(tag))
    el.text = text
    return el


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True, help="Public base URL ending with /")
    ap.add_argument("--out", default="feed.xml")
    args = ap.parse_args()
    base = args.base_url if args.base_url.endswith("/") else args.base_url + "/"

    with urllib.request.urlopen(SOURCE_FEED, timeout=60) as r:
        raw = r.read()
    root = ET.fromstring(raw)
    channel = root.find("channel")

    # Title and description
    t = channel.find("title")
    t.text = TITLE
    d = channel.find("description")
    d.text = DESCRIPTION

    # Author + owner (the two fields Spotify requires)
    set_text(channel, "author", AUTHOR)
    owner = channel.find(q("owner"))
    if owner is None:
        owner = ET.SubElement(channel, q("owner"))
    set_text(owner, "name", AUTHOR)
    set_text(owner, "email", OWNER_EMAIL)

    # Category
    cat = channel.find(q("category"))
    if cat is None:
        cat = ET.SubElement(channel, q("category"))
    cat.set("text", CATEGORY)

    # New logo as channel image
    logo_url = base + "logo.png"
    img = channel.find(q("image"))
    if img is None:
        img = ET.SubElement(channel, q("image"))
    img.set("href", logo_url)
    rss_img = channel.find("image/url")
    if rss_img is not None:
        rss_img.text = logo_url
    rss_img_title = channel.find("image/title")
    if rss_img_title is not None:
        rss_img_title.text = TITLE
    rss_img_link = channel.find("image/link")
    if rss_img_link is not None:
        rss_img_link.text = base

    # atom self link points at the mirror
    for link in channel.findall("{%s}link" % ATOM):
        if link.get("rel") == "self":
            link.set("href", base + "feed.xml")

    tree = ET.ElementTree(root)
    tree.write(args.out, encoding="utf-8", xml_declaration=True)
    items = channel.findall("item")
    print(f"wrote {args.out}: {len(items)} episodes, base={base}")


if __name__ == "__main__":
    sys.exit(main())
