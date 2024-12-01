import argparse
import asyncio
import json
import sys
import urllib.parse

import aiohttp
import bs4
import yarl


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        type=str,
        help="URL to parse, can be specified multiple times",
        default=[],
        action="append",
        required=True,
    )
    parser.add_argument(
        "-o",
        type=str,
        help="Output mode: stdout or json",
        choices=["stdout", "json"],
        required=True,
    )
    return parser.parse_args()


def _is_url_valid(url: str) -> bool:
    try:
        parsed_url = urllib.parse.urlparse(url)
        return all(
            [
                parsed_url.scheme in ["http", "https"],  # Protocols allowed
                parsed_url.netloc,  # Checks for non-empty network location
                "." in parsed_url.netloc,  # Ensures domain has a dot
                not parsed_url.netloc.startswith("."),
                not parsed_url.netloc.endswith("."),
            ]
        )
    except Exception:
        return False


def _parse_paths(address: yarl.URL, text: str) -> list[str]:
    urls = list(
        u.get("href") for u in bs4.BeautifulSoup(text, "html.parser").find_all("a")
    )
    filtered = set(
        u.replace("https://www.", "https://").removeprefix(
            str(address)
        )  # to unify results
        for u in urls
        if (
            u  # Could be None
            and "?" not in u  # No query params
            and (
                not u.startswith("http") or str(address.host) in u
            )  # to filter out external links
            and not u.startswith("#")  # filter out anchors
            and not u.startswith("mailto")  # filter out email addresses
            and u != str(address)  # filter out self links
        )
    )
    return [u.split("#")[0] for u in filtered if u and u != "/"]


def verify_urls(urls: list[str]) -> list[str]:
    to_parse = []
    for url in urls:
        if not _is_url_valid(url):
            print(
                f"Invalid URL: {url}, please specify it as https://example.com",
                file=sys.stderr,
            )
            sys.exit(1)
        to_parse.append(url.replace("https://www.", "https://"))
    return to_parse


async def fetch_all_urls_from(*, url: str) -> tuple[str, list[str]]:
    address = yarl.URL(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(address) as response:
            text = await response.text()
            paths = []
            for p in _parse_paths(address, text):
                if p.startswith("/"):
                    paths.append(p)
                else:
                    paths.append(f"/{p}")
            return url, paths


def print_output(results: list[tuple[str, list[str]]], mode: str) -> None:
    if mode == "stdout":
        for result in results:
            url, paths = result
            for path in paths:
                print(f"{url}{path}")
    elif mode == "json":
        output = {}
        for result in results:
            url, paths = result
            output[url] = paths
        json.dump(output, sys.stdout)


async def main() -> None:
    args = parse_args()
    urls_to_parse = verify_urls(args.u)
    tasks = [fetch_all_urls_from(url=url) for url in urls_to_parse]
    results = await asyncio.gather(*tasks)

    print_output(results, args.o)


if __name__ == "__main__":
    asyncio.run(main())
