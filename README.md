# 🚀 MyPkg - Termux Advanced Package Manager

![Python](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python)
![Termux](https://img.shields.io/badge/Termux-Environment-red?style=for-the-badge&logo=termux)
![License](https://img.shields.io/badge/License-GPL--V3-green?style=for-the-badge)

**MyPkg**, Termux kullanıcıları için özel olarak tasarlanmış, bağımlılıkları otomatik çözen ve karmaşık araçları (Hydra, Metasploit vb.) tek tıkla kurabilen gelişmiş bir paket yöneticisidir.

---

## 🛠️ Temel Özellikler

* ✅ **Otomatik Bağımlılık Çözücü:** `pkg`, `pip` ve `gem` paketlerini otomatik kurar.
* 🏗️ **Akıllı Derleme:** C/C++ projelerini (`configure`, `make`) otomatik derler.
* 🎨 **Renkli Arayüz:** Terminalde kolay okunabilir, modern çıktı sistemi.
* 🔄 **Self-Upgrade:** Tek komutla MyPkg'yi en son sürüme güncelleyin.
* 📦 **Geniş Arşiv:** 50'den fazla siber güvenlik aracı hazırda bekliyor.

---

## 🚀 Hızlı Kurulum

Termux üzerinden MyPkg'yi anında kullanmaya başlamak için aşağıdaki komutu yapıştırın:

```bash
curl -L [https://raw.githubusercontent.com/Requieminc/my-termux-repo/main/mypkg.py](https://raw.githubusercontent.com/Requieminc/my-termux-repo/main/mypkg.py) -o $PREFIX/bin/mypkg && chmod +x $PREFIX/bin/mypkg && mypkg update

