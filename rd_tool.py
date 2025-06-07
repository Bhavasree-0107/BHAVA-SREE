import os
import hashlib
import yaml
import argparse

def compute_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_release_descriptor(directory, release_name, version, vendor="MyVendor"):
    descriptor = {
        'descriptor_version': 1,
        'name': release_name,
        'version': version,
        'summary': f'{release_name} release descriptor',
        'vendor': vendor,
        'artifacts': {}
    }

    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path):
            sha256 = compute_sha256(full_path)
            size = os.path.getsize(full_path)
            descriptor['artifacts'][filename] = {
                'type': 'file',
                'size': size,
                'sha256': sha256
            }

    with open("release-descriptor.yml", "w") as outfile:
        yaml.dump(descriptor, outfile, default_flow_style=False)

    print(" release-descriptor.yml generated successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a release descriptor YAML.")
    parser.add_argument("directory", help="Directory containing artifact files")
    parser.add_argument("name", help="Release name (e.g., myapp)")
    parser.add_argument("version", help="Release version (e.g., 1.0.0)")
    args = parser.parse_args()

    print(f"📁 Looking in: {args.directory}")
    print(f"📦 Release: {args.name} Version: {args.version}")
    print(f"🔍 Files found: {os.listdir(args.directory)}")
    
    generate_release_descriptor(args.directory, args.name, args.version)

