import urllib.request
import urllib.parse
import json
import datetime
import os

# Türkçe ay isimleri
TURKISH_MONTHS = {
    1: 'Ocak', 2: 'Şubat', 3: 'Mart', 4: 'Nisan', 5: 'Mayıs', 6: 'Haziran',
    7: 'Temmuz', 8: 'Ağustos', 9: 'Eylül', 10: 'Ekim', 11: 'Kasım', 12: 'Aralık'
}

def format_turkish_date(date_obj):
    """Tarihi Türkçe formatta döndür"""
    day = date_obj.day
    month = TURKISH_MONTHS[date_obj.month]
    year = date_obj.year
    return f"{day} {month} {year}"

def load_env():
    """Load environment variables from .env file"""
    env_vars = {}
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print("⚠️ .env dosyası bulunamadı!")
    return env_vars

def get_github_commits(username, github_token=""):
    """GitHub API ile kullanıcının bugünkü commitlerini al"""
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Önce kullanıcının repository'lerini al
    repos_url = f"https://api.github.com/users/{username}/repos"
    
    try:
        request = urllib.request.Request(repos_url)
        if github_token:
            request.add_header('Authorization', f'token {github_token}')
            
        with urllib.request.urlopen(request) as response:
            repos = json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching repositories: {e}")
        return []
    
    all_commits = []
    
    for repo in repos:
        repo_name = repo['name']
        # Her repo için bugünkü commitleri al
        commits_url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
        params = {
            'author': username,
            'since': f'{today}T00:00:00Z'
        }
        
        # URL parametrelerini encode et
        params_encoded = urllib.parse.urlencode(params)
        full_url = f"{commits_url}?{params_encoded}"
        
        try:
            request = urllib.request.Request(full_url)
            if github_token:
                request.add_header('Authorization', f'token {github_token}')
                
            with urllib.request.urlopen(request) as response:
                commits = json.loads(response.read().decode())
                for commit in commits:
                    # Commit mesajını tam al ve temizle
                    full_message = commit['commit']['message'].strip()
                    title = full_message.split('\n')[0]  # İlk satır (başlık)
                    
                    commit_data = {
                        'repo': repo_name,
                        'hash': commit['sha'][:7],
                        'title': title,
                        'full_message': full_message,
                        'author': commit['commit']['author']['name'],
                        'date': commit['commit']['author']['date']
                    }
                    all_commits.append(commit_data)
        except Exception as e:
            print(f"Error fetching commits for {repo_name}: {e}")
            continue
    
    return all_commits

def format_github_commit(commit):
    """GitHub commit'ini markdown formatına çevir"""
    # ISO format tarihini parse et
    date_obj = datetime.datetime.fromisoformat(commit['date'].replace('Z', '+00:00'))
    time_str = date_obj.strftime('%H:%M')
    
    # Commit başlığı
    result = f"- `{commit['hash']}` **{commit['title']}** _(in {commit['repo']} by {commit['author']} at {time_str})_"
    
    # Eğer commit'te açıklama varsa (birden fazla satır), onu da ekle
    lines = commit['full_message'].split('\n')
    if len(lines) > 1:
        # İlk satırdan sonraki boş olmayan satırları açıklama olarak ekle
        description_lines = [line.strip() for line in lines[1:] if line.strip()]
        if description_lines:
            result += "\n"
            for desc_line in description_lines:
                result += f"  > {desc_line}\n"
            result = result.rstrip()  # Son newline'ı kaldır
    
    return result

def generate_gemini_report(commits, username, real_name, gemini_api_key):
    """Gemini API ile commit'lerden düzenli rapor oluştur"""
    if not gemini_api_key:
        print("⚠️ GEMINI_API_KEY bulunamadı, basit rapor oluşturuluyor...")
        return None
    
    # Commit'leri düz metne çevir
    commit_texts = []
    for commit in commits:
        commit_text = f"Repo: {commit['repo']}\nCommit: {commit['title']}"
        if commit['full_message'] != commit['title']:
            # Tam mesajın geri kalanını ekle
            lines = commit['full_message'].split('\n')[1:]
            description = '\n'.join([line.strip() for line in lines if line.strip()])
            if description:
                commit_text += f"\nAçıklama: {description}"
        commit_texts.append(commit_text)
    
    commits_summary = '\n\n'.join(commit_texts)
    
    # Gemini için prompt hazırla (gerçek isim kullan)
    prompt = f"""Aşağıdaki GitHub commit'lerini analiz ederek profesyonel bir günlük rapor oluştur.

ÖNEMLİ KURALLAR:
- Commit'lere referans verme (commit hash, repo adı, teknik terimler kullanma)
- Yapılan işleri basit, anlaşılır Türkçe ile açıkla
- Teknik detayları sıradan kullanıcının anlayacağı şekilde özetle
- Her kategori altında kısa, net cümleler kullan
- Gereksiz teknik jargon kullanma

TEMPLATE:
📌 {real_name} - Yapılanlar ({format_turkish_date(datetime.datetime.now())})

[Kategori başlıkları ekleyerek commit'leri grupla. Örnek kategoriler:]
📚 Kurs Yönetimi
🔄 Veri İyileştirmeleri
💳 Ödeme Sistemi
🐛 Hata Düzeltmeleri
⚡ Performans İyileştirmeleri
🔧 Sistem Ayarları
📖 Dokümantasyon
🎨 Arayüz Geliştirmeleri

Her kategori altında:
- Ne yapıldığını basit dilde açıkla (ör: "Kurs sayfalarına yeni bölümler eklendi")
- Kullanıcı açısından ne fayda sağladığını belirt
- Emoji kullanarak görsel zenginlik kat
- Teknik terimleri kullanıcı dostu açıkla

ÖRNEK FORMAT:
📚 Kurs Yönetimi
Kursların içerisine bölümler ekleme özelliği geliştirildi.
Her bölüme artık ayrı dersler eklenebiliyor.

🔄 Veri İyileştirmeleri
Kurs detay sayfalarında gerçek bilgiler gösterilmeye başlandı.

COMMIT'LER:
{commits_summary}

Lütfen yukarıdaki kurallara ve template'e uygun olarak düzenli bir rapor oluştur. Teknik detaylardan ziyade ne yapıldığına odaklan."""

    try:
        # Gemini API çağrısı (doğru endpoint)
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        request = urllib.request.Request(
            gemini_url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode())
            
            if 'candidates' in result and len(result['candidates']) > 0:
                generated_text = result['candidates'][0]['content']['parts'][0]['text']
                return generated_text
            else:
                print("⚠️ Gemini'den geçerli yanıt alınamadı")
                return None
                
    except Exception as e:
        print(f"⚠️ Gemini API hatası: {e}")
        return None

def main():
    # .env dosyasından konfigürasyonu yükle
    env_vars = load_env()
    
    # GitHub kullanıcı adını ve token'ı .env'den al
    username = env_vars.get('GITHUB_USERNAME', 'erenxcolakx')
    github_token = env_vars.get('GITHUB_TOKEN', '')
    gemini_api_key = env_vars.get('GEMINI_API_KEY', '')
    
    # Kullanıcıdan gerçek ismini sor
    print("🎯 Daily Commit Report Generator")
    print("=" * 40)
    real_name = input("📝 Raporlarda görünecek isminizi girin: ").strip()
    
    if not real_name:
        real_name = username  # İsim girilmezse username kullan
    
    if not username:
        print("❌ GITHUB_USERNAME .env dosyasında tanımlanmalı!")
        return
    
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    
    print(f"\n🔍 GitHub hesabınızdaki bugünkü commitler alınıyor: @{username}")
    print(f"👤 Rapor sahibi: {real_name}")
    
    # Rate limit problemini önlemek için genel commit arama kullanalım
    search_url = f"https://api.github.com/search/commits?q=author:{username}+author-date:{datetime.datetime.now().strftime('%Y-%m-%d')}"
    
    try:
        # GitHub requires Accept header for search API
        request = urllib.request.Request(search_url)
        request.add_header('Accept', 'application/vnd.github.cloak-preview')
        
        # Token varsa Authorization header ekle
        if github_token:
            request.add_header('Authorization', f'token {github_token}')
            print("✅ GitHub token kullanılıyor - yüksek rate limit")
        else:
            print("⚠️ Token yok - düşük rate limit (60 req/hour)")
        
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())
            commits = []
            
            for item in data.get('items', []):
                # Commit mesajını tam al ve temizle
                full_message = item['commit']['message'].strip()
                title = full_message.split('\n')[0]  # İlk satır (başlık)
                
                commit_data = {
                    'repo': item['repository']['name'],
                    'hash': item['sha'][:7],
                    'title': title,
                    'full_message': full_message,
                    'author': item['commit']['author']['name'],
                    'date': item['commit']['author']['date']
                }
                commits.append(commit_data)
    except Exception as e:
        print(f"GitHub API hatası: {e}")
        commits = []
    
    # Rapor dosya adları
    basic_filename = f'daily_report_basic_{timestamp}.md'
    ai_filename = f'daily_report_ai_{timestamp}.md'
    
    # Basit rapor oluştur
    basic_report_lines = [
        '# Daily Git Commit Report (Basic)',
        f'👤 Developer: {real_name}',
        f'🔗 GitHub: @{username}',
        f'📅 Date: {now.strftime("%Y-%m-%d %H:%M:%S")}',
        ''
    ]
    
    if not commits:
        basic_report_lines.append('No commits found for today or API error occurred.')
        basic_report_lines.append('')
        basic_report_lines.append('Note: GitHub API has rate limits. If you have many commits,')
        basic_report_lines.append('you might need to wait or use a personal access token.')
    else:
        basic_report_lines.append(f'Found {len(commits)} commits today:')
        basic_report_lines.append('')
        for commit in commits:
            formatted = format_github_commit(commit)
            if formatted:
                basic_report_lines.append(formatted)
    
    # Basit raporu kaydet
    with open(basic_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(basic_report_lines))
    print(f'✅ Basic report generated: {basic_filename}')
    
    # Eğer commit varsa AI raporu da oluştur
    if commits and gemini_api_key:
        print("\n🤖 AI raporu oluşturuluyor...")
        ai_report = generate_gemini_report(commits, username, real_name, gemini_api_key)
        
        if ai_report:
            with open(ai_filename, 'w', encoding='utf-8') as f:
                f.write(ai_report)
            print(f'🎉 AI report generated: {ai_filename}')
        else:
            print("⚠️ AI raporu oluşturulamadı, sadece basit rapor mevcut")
    elif commits and not gemini_api_key:
        print("⚠️ GEMINI_API_KEY eksik - sadece basit rapor oluşturuldu")
        print("💡 AI raporu için .env dosyasına GEMINI_API_KEY ekleyin")

if __name__ == '__main__':
    main()
