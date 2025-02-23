#!/bin/python
from json import dumps, load as jload
from tomllib import load as tload
from zipfile import ZipFile
from os import listdir, getcwd, stat
from os.path import join, realpath
from requests import get
from requests.exceptions import RequestException
from argparse import ArgumentParser
from re import match, sub

def nestedDIF(data, pathToFollow):
    for path in pathToFollow:
        try:
            data = data[path]
        except TypeError:
            try:
                data = data[0]
                data = data[path]
            except:
                return -1
        except KeyError:
            return -1
    return data

def fabricJSON(modContents):
    try:
        with modContents.open('fabric.mod.json', 'r') as fabricInfo:
            return nestedDIF(jload(fabricInfo), ['contact', 'sources'])
    except KeyError:
        return -1

def bruteForceURL(authors, modid):
    url = 'https://api.github.com'
    for author in authors:
        try:
            response = get(f"{url}/{author}/{modid}")
            if response.status_code == 200:
                return f"https://github.com/{author}/{modid}"
            if response.status_code == 403:
                print('Rate limited by GitHub API. Will ignore for now.')
                break;
        except RequestException as e:
            print (e)
    return -1

def convertRawGitHubURL(url):
    matched = match(r'https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/.*', url)
    if matched:
        url = f"https://github.com/{match.group(1)}/{match.group(2)}"
    return sub(r"/issues.*|/releases.*|/blob.*|/raw.*", "", url)

def main():
    parser = ArgumentParser()
    parser.add_argument('-u', '--unsafe', action='store_true')
    args = parser.parse_args()

    largeMods = [realpath(f) for f in listdir(getcwd())
                 if stat(realpath(f)).st_size > 1000000]

    mod_data = {}

    for modFile in largeMods:
        with ZipFile(modFile, 'r') as modContents:
            with modContents.open('META-INF/mods.toml', 'r') as modInfo:
                TOML = tload(modInfo)
                version = nestedDIF(TOML, ['mods', 'version'])
                mod_id = nestedDIF(TOML, ['mods', 'modId'])

                if version == '${file.jarVersion}':
                    with modContents.open('META-INF/MANIFEST.MF', 'r') as jarInfo:
                        for line in jarInfo.read().decode('utf-8').splitlines():
                            if line.startswith('Implementation-Version: '):
                                version = line.split(': ', 1)[1]

                githubLinks = [
                        nestedDIF(TOML, ['issueTrackerURL']), 
                        nestedDIF(TOML, ['mods', 'issueTrackerURL']),
                        nestedDIF(TOML, ['mods', 'updateJSONURL']),
                        fabricJSON(modContents),
                        ]

                if args.unsafe:
                        githubLinks.append(bruteForceURL(nestedDIF(TOML, ['authors']), mod_id))

                githubLinks = [convertRawGitHubURL(link) for link in githubLinks if isinstance(link, str) and 'github.com' in link]
                
                if githubLinks:
                    mod_data[mod_id] = {"version": version, "github": githubLinks[0]}
                else:
                   pass 

    print(dumps(mod_data, indent=4))

if __name__ == "__main__":
    main()
