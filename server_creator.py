#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import os

url = "https://getbukkit.org/download/vanilla"

def website():
    
    vanillaversions = BeautifulSoup(requests.get(url).text, "html.parser")

    version_categories = vanillaversions.find("div", id="download")
    version_numbers = version_categories.find_all("h2")
    version_numbers_text = [version.text for version in version_numbers]
    return version_numbers_text


def user_selection(version_numbers_text):
    version_input = input(
        "Please enter a minecraft version number. Or type 'list' to see a list of versions: ")
    if version_input in version_numbers_text:
        print("Your server is now being created")
        url = downloadLink(version_input)
        r = requests.get(url, allow_redirects=True)
        open("minecraft-server-" + version_input + ".jar", 'wb').write(r.content)

        makeDir("eula.txt")
        open("eula.txt", "w").write("eula=true")

        makeDir("start.bat")
        open("start.bat", "w").write("java -jar " +
                                     "minecraft-server-" + version_input + ".jar")

        os.popen("java -jar " + "minecraft-server-" +
                 version_input + ".jar").read()
                                 

    if version_input == "list":
        print(version_numbers_text)
        user_selection(version_numbers_text)
    else:
        print("That is an invalid version number. Please try again")
        user_selection(version_numbers_text)


def downloadLink(version):
    vanillaversions = BeautifulSoup(requests.get(url).text, "html.parser")
    download = vanillaversions.find("div", id="download")
    downloadpane = download.find_all("div", {"class": "download-pane"})
    for individualDownloadPane in downloadpane:
        h2 = individualDownloadPane.find("h2")
        if h2.getText() == version:
            link = individualDownloadPane.find(
                "a", id="downloadr").attrs['href']
            vanillaversions = BeautifulSoup(
                requests.get(link).text, "html.parser")
            paneHref = vanillaversions.find("div", id="get-download")
            return paneHref.find("a").attrs['href']

def makeDir(dir):
    if not os.path.exists(dir):
        open(dir, "x")
            


versions = website()
user_selection(versions)
