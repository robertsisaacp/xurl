#!/usr/bin/env python3

from urllib.parse import urlencode, quote, urlunsplit
import subprocess
import argparse


def build_url(app: str, action: str, query: dict):
    """<scheme>://<netloc>/<path>?<query>#<fragment>

    Examples:
      - craftdocs://open?spaceId=<spaceId>&blockId=<blockId>
      - craftdocs://createdocument?spaceId=<spaceId>&title=<title>&content=<content>&folderId=<folderId>
      - omnifocus://x-callback-url/add?name=Pick%20up%20milk&note=Low%20fat
      - def  asdfasdf
      - drafts://x-callback-url/[actionName]?[queryParameters]
      - mvim://open?url=file:///etc/profile&line=20
    """
        
    url = (
        app,
        "x-callback-url",
        action,
        urlencode(query, quote_via=quote),
        "",
    )
    url = urlunsplit(url)
    if app == "mvim":
        url = url.replace("x-callback-url/", "")
    return url


def main():
    parser = argparse.ArgumentParser(description="xurl: x-callback-builder")
    parser.add_argument("app", type=str, help='app name (e.g. drafts, omnifocus, etc.)')
    parser.add_argument("action", type=str, help='app name (e.g. create, add, etc.)')
    parser.add_argument(
        "query", type=str, nargs="+", help='query values (e.g. "text=hello")'
    )
    parser.add_argument("-p", help="print but do not open url.", action="store_true")

    args = parser.parse_args()
    args.query = dict([v.split("=") for v in args.query])

    url = build_url(args.app, args.action, args.query)

    if args.p:
        print(url)
    else:
        subprocess.run(["open", url])


if __name__ == "__main__":
    main()
