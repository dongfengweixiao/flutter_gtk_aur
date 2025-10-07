import os
import json
import toml

with open('version.toml', 'r') as f:
    versions = toml.load(f)

version_list = []
for version, info in versions.items():
    pkgrel = info.get('pkgrel', 1)
    full_version = f"{version}-{pkgrel}"
    version_list.append({
        'base_version': version,
        'full_version': full_version,
        'enginever': info['enginever'],
        'pkgrel': pkgrel
    })

print(json.dumps(version_list))
