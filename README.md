# 📊 Daily Git Commit Report Generator

GitHub hesabınızdaki günlük commit'leri otomatik olarak analiz edip profesyonel raporlar oluşturan Python scripti.

## ✨ Özellikler

- 🔍 **Otomatik Commit Toplama**: Bugünün tüm commit'lerini GitHub API ile toplar
- 🤖 **AI Destekli Analiz**: Gemini AI ile commit'leri kategorilere ayırır ve açıklar
- 📝 **Çift Rapor Sistemi**: Hem detaylı hem özet rapor oluşturur
- 🌍 **Türkçe Destek**: Tamamen Türkçe arayüz ve raporlar
- 🔐 **Güvenli**: API key'ler .env dosyasında korunur
- 🎨 **Şık Format**: Emoji'li, düzenli Markdown raporları

## 📋 Gereksinimler

- Python 3.6+
- GitHub hesabı
- GitHub Personal Access Token
- Gemini API Key (opsiyonel)

## 🚀 Kurulum

1. **Repository'yi klonla:**

   ```bash
   git clone https://github.com/erenxcolakx/report-from-commit.git
   cd report-from-commit
   ```
2. **Environment dosyasını oluştur:**

   ```bash
   cp .env.example .env
   ```
3. **API key'leri yapılandır:**
   `.env` dosyasını düzenleyip gerekli bilgileri ekle:

   ```bash
   GITHUB_USERNAME=your_github_username
   GITHUB_TOKEN=your_github_token
   GEMINI_API_KEY=your_gemini_api_key
   ```

## 🔑 API Key'leri Alma

### GitHub Personal Access Token

1. GitHub.com > Settings > Developer settings > Personal access tokens
2. "Generate new token (classic)" seçeneğini seç
3. İzinleri seç:
   - Public repo'lar için: `public_repo`
   - Private repo'lar için: `repo`
   - Kullanıcı bilgileri için: `read:user`
4. Token'ı kopyala (ghp_ ile başlar)

### Gemini API Key

1. https://makersuite.google.com/app/apikey adresine git
2. Google hesabınla giriş yap
3. "Create API Key" butonuna tıkla
4. API key'i kopyala (AIza ile başlar)

## 💻 Kullanım

```bash
python generate_daily_report.py
```

Script sizi isminizi girmeye yönlendirecek ve otomatik olarak:

- Bugünün commit'lerini toplayacak
- İki farklı rapor oluşturacak:
  - `daily_report_basic_TARIH.md` - Detaylı commit listesi
  - `daily_report_ai_TARIH.md` - AI ile düzenlenmiş özet

## 📄 Örnek Çıktı

### AI Raporu

```markdown
📌 John Doe - Yapılanlar (19 Temmuz 2025)

📚 Kurs Yönetimi
Kursların içerisine bölümler ekleme özelliği geliştirildi.
Her bölüme artık ayrı dersler eklenebiliyor.

🔄 Veri İyileştirmeleri
Kurs detay sayfalarında gerçek bilgiler gösterilmeye başlandı.

💳 Ödeme Sistemi
Payment servisi için temel altyapı kuruldu.
```

## ⚙️ Konfigürasyon

### Rate Limit'ler

- **GitHub API** (token olmadan): 60 request/saat
- **GitHub API** (token ile): 5000 request/saat
- **Gemini API**: 60 request/dakika (ücretsiz)

### Dosya Yapısı

```
report-from-commit/
├── generate_daily_report.py   # Ana script
├── .env.example              # Environment template
├── .env                      # API key'ler (git'e commit edilmez)
├── .gitignore               # Git ignore kuralları
├── README.md                # Bu dosya
├── GITHUB_TOKEN_GUIDE.md    # GitHub token rehberi
└── GEMINI_API_GUIDE.md      # Gemini API rehberi
```

## 🛡️ Güvenlik

- ✅ API key'ler .env dosyasında saklanır
- ✅ .env dosyası .gitignore'da korunur
- ❌ Asla API key'leri git'e commit etmeyin
- ❌ API key'leri başkalarıyla paylaşmayın

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Branch'i push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🐛 Sorun Bildirimi

Herhangi bir sorunla karşılaştığınızda [Issues](https://github.com/erenxcolakx/report-from-commit/issues) sayfasından bildirebilirsiniz.

## 📞 İletişim

- GitHub: [@erenxcolakx](https://github.com/erenxcolakx)
- Email: your-email@example.com
