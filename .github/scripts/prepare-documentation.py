"""
Prepare one Writerside version for its published URL.
"""

#      Copyright (c) 2026. ForteScarlet.
#
#      Project    https://github.com/simple-robot/simpler-robot
#      Email      ForteScarlet@163.com
#
#      This file is part of the Simple Robot Library (Alias: simple-robot, simbot, etc.).
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Lesser General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      Lesser GNU General Public License for more details.
#
#      You should have received a copy of the Lesser GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


_PUBLISHED_ROOTS = {
    "5.x": "https://simbot.forte.love/",
    "4.x": "https://simbot.forte.love/v4/",
}
_TEXT_SUFFIXES = {".html", ".xml", ".json", ".md", ".txt"}


def _prepare(version: str) -> None:
    """
    Normalize generated URLs without changing the version used by Algolia.
    """
    root = _PUBLISHED_ROOTS[version]
    generated_root = f"{root}{version}/"
    site = Path("site")
    config = json.loads((site / "config.json").read_text())
    if config["productId"] != "s4" or config["productVersion"] != version:
        raise ValueError("Built product/version does not match the requested version")
    variables = ET.parse(Path(__file__).resolve().parents[2] / "Writerside/v.list")
    display_version = variables.find("./var[@name='version']").attrib["value"]
    if config.get("productVersionName") != display_version:
        raise ValueError("The displayed version must match the dependency version in v.list")
    if config["versionsService"] != "https://simbot.forte.love/help-versions.json":
        raise ValueError("Both versions must use the shared version switcher")
    if not (site / "index.html").is_file():
        raise ValueError("Missing site entry point")

    # Builder 2026.10.0423 appends the instance version to absolute URLs.
    # The two maintained branches publish directly at their configured web roots.
    for directory in [site, Path("search/records")]:
        for path in directory.rglob("*"):
            if path.is_file() and path.suffix in _TEXT_SUFFIXES:
                original = path.read_text()
                updated = original.replace(generated_root, root)
                if original != updated:
                    path.write_text(updated)

    for page in site.glob("*.html"):
        html = page.read_text()
        if html.lstrip().startswith("<error>"):
            raise ValueError(f"Failed to render {page.name}")
        if version == "4.x" and "</head>" in html and 'http-equiv="refresh"' not in html:
            if '<meta name="robots" content="noindex">' not in html:
                raise ValueError(f"Missing noindex in {page.name}")

    if version == "4.x" and config["stage"] != "outdated":
        raise ValueError("The archived version must show the outdated-documentation notice")
    sitemap = ET.parse(site / "sitemap.xml")
    for location in sitemap.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        if not location.text.startswith(root) or location.text.startswith(generated_root):
            raise ValueError(f"Incorrect sitemap URL: {location.text}")
    print(f"{version}: site metadata and published URLs checked")


if __name__ == "__main__":
    _prepare(sys.argv[1])
