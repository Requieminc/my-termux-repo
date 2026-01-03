#!/usr/bin/env python3
import os, sys, json, shutil, urllib.request, zipfile, argparse, stat, subprocess

# --- AYARLAR ---
REPO_URL = "https://raw.githubusercontent.com/Requieminc/my-termux-repo/main/repo.json"

if "TERMUX_VERSION" in os.environ:
    BASE_DIR = "/data/data/com.termux/files/usr"
else:
    BASE_DIR = "/usr/local"

BIN_DIR = os.path.join(BASE_DIR, "bin")        
OPT_DIR = os.path.join(BASE_DIR, "opt")        
DB_FILE = os.path.join(os.path.expanduser("~"), ".mypkg_installed.json")
REPO_CACHE = os.path.join(os.path.expanduser("~"), ".mypkg_repo.json")

os.makedirs(OPT_DIR, exist_ok=True)

# --- YARDIMCI FONKSİYONLAR ---
def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f: 
            try: return json.load(f)
            except: return {}
    return {}

def save_json(path, data):
    with open(path, "w") as f: json.dump(data, f, indent=4)

def download_file(url, dest):
    print(f"🌍 İndiriliyor: {url}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(dest, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    except Exception as e:
        print(f"❌ Hata: {e}"); sys.exit(1)

def create_launcher(pkg_name, main_file_path):
    launcher_path = os.path.join(BIN_DIR, pkg_name)
    ext = os.path.splitext(main_file_path)[1]
    
    # Binary/Script ayrımı
    if ext == ".py":
        content = f'#!/bin/sh\nexec python3 "{main_file_path}" "$@"'
    elif ext == ".rb":
        content = f'#!/bin/sh\nexec ruby "{main_file_path}" "$@"'
    elif ext == ".sh":
        content = f'#!/bin/sh\nexec bash "{main_file_path}" "$@"'
    else:
        # Uzantısız dosyalar (Hydra gibi binaryler)
        content = f'#!/bin/sh\nexec "{main_file_path}" "$@"'
        
    with open(launcher_path, "w") as f: f.write(content)
    os.chmod(launcher_path, os.stat(launcher_path).st_mode | stat.S_IEXEC)

# --- ANA MOTOR ---
def install_package(pkg_name):
    repo_data = load_json(REPO_CACHE)
    if pkg_name not in repo_data:
        print("❌ Paket repoda yok. 'mypkg update' yapın.")
        return

    install_path = os.path.join(OPT_DIR, pkg_name)
    if os.path.exists(install_path):
        if input(f"⚠️ {pkg_name} zaten var. Silinsin mi? (y/n): ").lower() != 'y': return
        shutil.rmtree(install_path)

    url = repo_data[pkg_name]["url"]
    print(f"🚀 {pkg_name} kuruluyor...")
    tmp_zip = f"tmp_{pkg_name}.zip"
    download_file(url, tmp_zip)
    
    try:
        with zipfile.ZipFile(tmp_zip, 'r') as z:
            first = z.namelist()[0].split('/')[0]
            z.extractall(OPT_DIR)
            shutil.move(os.path.join(OPT_DIR, first), install_path)
    except Exception as e:
        print(f"❌ Zip hatası: {e}"); return
    finally:
        if os.path.exists(tmp_zip): os.remove(tmp_zip)

    # 🛠️ BAĞIMLILIKLAR (JSON'daki 'deps' alanı)
    if "deps" in repo_data[pkg_name]:
        print(f"🏛️ Sistem bağımlılıkları kuruluyor: {repo_data[pkg_name]['deps']}")
        os.system(f"pkg install -y {repo_data[pkg_name]['deps']}")

    # 🏗️ DERLEME (Hydra vb. için configure kontrolü)
    if os.path.exists(os.path.join(install_path, "configure")):
        print("🏗️ C/C++ projesi algılandı, derleniyor...")
        os.system(f"cd {install_path} && chmod +x configure && ./configure && make -j4")

    # 📦 PYTHON/RUBY BAĞIMLILIKLARI
    req_f = os.path.join(install_path, "requirements.txt")
    if os.path.exists(req_f): os.system(f"pip install -r {req_f}")
    
    gem_f = os.path.join(install_path, "Gemfile")
    if os.path.exists(gem_f): os.system(f"cd {install_path} && bundle install")

    # 🎯 AKILLI BAŞLATICI BULUCU
    main_file = None
    targets = [pkg_name, f"{pkg_name}.py", f"{pkg_name}.sh", "main.py", "msfconsole", f"{pkg_name}.rb"]
    
    for t in targets:
        p = os.path.join(install_path, t)
        if os.path.exists(p) and not os.path.isdir(p):
            main_file = p; break

    if main_file:
        create_launcher(pkg_name, main_file)
        print(f"✅ Başarılı! Komut: {pkg_name}")
        
        db = load_json(DB_FILE)
        db[pkg_name] = {"files": [install_path, os.path.join(BIN_DIR, pkg_name)]}
        save_json(DB_FILE, db)
    else:
        print(f"⚠️ Kuruldu ama ana dosya bulunamadı: {install_path}")

def main():
    parser = argparse.ArgumentParser(description="MyPkg Pro")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("update")
    sub.add_parser("list")
    sub.add_parser("search")
    p_in = sub.add_parser("install"); p_in.add_argument("name")
    p_rm = sub.add_parser("remove"); p_rm.add_argument("name")

    args = parser.parse_args()
    if args.command == "update":
        download_file(REPO_URL, REPO_CACHE)
        print(f"✅ Güncellendi. Toplam {len(load_json(REPO_CACHE))} araç.")
    elif args.command == "install": install_package(args.name)
    elif args.command == "remove":
        db = load_json(DB_FILE)
        if args.name in db:
            for p in db[args.name]["files"]:
                if os.path.exists(p):
                    if os.path.isdir(p): shutil.rmtree(p)
                    else: os.remove(p)
            del db[args.name]; save_json(DB_FILE, db)
            print(f"🗑️ {args.name} silindi.")
    elif args.command == "list":
        for k in load_json(DB_FILE): print(f"📦 {k}")
    elif args.command == "search":
        for k, v in load_json(REPO_CACHE).items(): 
            print(f"🔎 {k.ljust(15)} | {v.get('description','')}")

if __name__ == "__main__": main()

