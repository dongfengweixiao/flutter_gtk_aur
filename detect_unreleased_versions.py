import json
import sys

def main():
    try:
        if len(sys.argv) != 3:
            sys.stderr.write("Usage: python detect_unreleased_versions.py <all_versions_json> <releases_json>\n")
            print(json.dumps([]))
            sys.exit(1)
        
        try:
            all_versions = json.loads(sys.argv[1])
            releases = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            sys.stderr.write(f"Error parsing JSON: {e}\n")
            print(json.dumps([]))
            sys.exit(1)
        
        released_versions = []
        for release in releases:
            if release['tag_name'] not in released_versions:
                released_versions.append(release['tag_name'])
        
        unreleased = []
        for version_info in all_versions:
            if version_info['full_version'] not in released_versions:
                unreleased.append(version_info)
        
        print(json.dumps(unreleased))
    except Exception as e:
        sys.stderr.write(f"Unexpected error: {e}\n")
        print(json.dumps([]))
        sys.exit(1)

if __name__ == "__main__":
    main()
