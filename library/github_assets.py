#!/usr/bin/python
from ansible.module_utils.basic import *
from urllib import request, parse
import json
import re
import os

DOCUMENTATION = '''
---
module: github_assets
short_description: Download assets from Github
'''

EXAMPLES = '''
- name: Download Dcevm-11.0.7+1
  github_assets:
    repository: TravaOpenJDK/trava-jdk-11-dcevm/
    assets_pattern: .*linux.*
    download_path: "/opt"
'''


def get_response(url):
    response = request.urlopen(url)
    return json.loads(response.read())


def download_asset(download_url, download_path, file_name):
    path = download_path + '/' + file_name
    if os.path.exists(path):
        return False
    request.urlretrieve(download_url, path)
    return True


def download_assets(data):
    has_changed = False
    return_result = {
        "tag": data['tag'],
        "assets": [],
        "errors": ""
    }
    repository = data['repository']
    releases_url = 'https://api.github.com/repos/%s/releases' % repository
    try:
        response = get_response(releases_url)
    except Exception as e:
        has_changed = True
        return_result[
            'errors'] = "An error occurred when trying to to download releases from: " + releases_url + "the error " \
                                                                                                        "was " + str(e)
    else:
        tag_name = data['tag']
        if tag_name == 'latest':
            tag_name = response[0]['tag_name']
            return_result['tag'] = tag_name
        for release in response:
            if release['tag_name'] == tag_name:
                for asset in release['assets']:
                    if re.compile(data['asset_pattern']).match(asset['name']):
                        download_url = asset['browser_download_url']
                        file_name = parse.unquote(download_url[download_url.rindex('download/') + 9:]).replace('/', '-')
                        result = download_asset(download_url, data['download_path'], file_name)
                        if result:
                            has_changed = True
                        return_result['assets'].append(file_name)

    return has_changed, return_result


def main():
    fields = {
        "repository": {"required": True, "type": "str"},
        "tag": {"required": False, "default": "latest", "type": "str"},
        "asset_pattern": {"required": False, "default": ".*", "type": "str"},
        "download_path": {"required": False, "default": "/tmp", "type": "str"}
    }

    module = AnsibleModule(argument_spec=fields)
    changed, response = download_assets(module.params)
    if response['errors']:
        raise Exception(response['errors'])
    module.exit_json(changed=changed, meta=response)


if __name__ == '__main__':
    main()
