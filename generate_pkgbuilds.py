#!/usr/bin/env python3

import os
import subprocess
import toml

def generate_pkgbuilds():
    with open('version.toml', 'r') as f:
        versions = toml.load(f)
    
    for version, info in versions.items():
        dir_name = f'flutter-gtk-{version}'
        os.makedirs(dir_name, exist_ok=True)
        
        pkgbuild_content = f'''
pkgname=flutter-gtk-{version}
pkgver={version}
pkgrel={info['pkgrel']}
pkgdesc="Flutter GTK embedder runtime."
url="https://flutter.dev/"
arch=("x86_64" "aarch64")
license=("Apache-2.0")
provides=("libflutter_linux_gtk.so.${{pkgver}}")
depends=("glibc" "glib2" "fontconfig" "pango" "at-spi2-core" "gtk3" "libepoxy" "cairo")

_enginever="{info['enginever']}"
_storagebase="${{FLUTTER_STORAGE_BASE_URL:-\"https://storage.googleapis.com\"}}"

source_x86_64=(
  # engine/linux-$ARCH-release
  "gtk-release-x64-${{_enginever}}.zip::${{_storagebase}}/flutter_infra_release/flutter/${{_enginever}}/linux-x64-release/linux-x64-flutter-gtk.zip"
)
source_aarch64=(
  # engine/linux-$ARCH-release
  "gtk-release-arm64-${{_enginever}}.zip::${{_storagebase}}/flutter_infra_release/flutter/${{_enginever}}/linux-arm64-release/linux-arm64-flutter-gtk.zip"
)
sha256sums_x86_64=('{info['sha256_x86_64']}')
sha256sums_aarch64=('{info['sha256_aarch64']}')

build() {{
  true
}}

package() {{
  install -Dm755 "libflutter_linux_gtk.so" "${{pkgdir}}/usr/lib/flutter_gtk/${{pkgver}}/libflutter_linux_gtk.so"
  ln -sfr "${{pkgdir}}/usr/lib/flutter_gtk/${{pkgver}}/libflutter_linux_gtk.so" "${{pkgdir}}/usr/lib/libflutter_linux_gtk.so.${{pkgver}}"
}}
'''.strip()
        
        pkgbuild_path = os.path.join(dir_name, 'PKGBUILD')
        with open(pkgbuild_path, 'w') as f:
            f.write(pkgbuild_content)
                
        current_dir = os.getcwd()
        try:
            os.chdir(dir_name)
            result = subprocess.run(['makepkg', '--printsrcinfo'], capture_output=True, text=True)
            if result.returncode == 0:
                with open('.SRCINFO', 'w') as f:
                    f.write(result.stdout)
        except Exception as e:
            raise e
        finally:
            os.chdir(current_dir)

if __name__ == '__main__':
    generate_pkgbuilds()
