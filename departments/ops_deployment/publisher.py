import subprocess

def git_yayinla():
    print("[OpsDeployment] Git yayınlama ve senkronizasyon başlatılıyor...")
    komutlar = [
        ['git', 'config', '--global', 'user.name', 'Jarvis Otonom Bot'],
        ['git', 'config', '--global', 'user.email', 'bot@actions.github.com'],
        ['git', 'config', '--global', 'http.version', 'HTTP/1.1'],
        ['git', 'add', 'outputs/', 'PazarAnalizRaporu.xlsx', 'analiz_raporu.json'],
        ['git', 'commit', '-m', 'chore: Otonom departmanlar arasi veri ve medya guncellendi [skip ci]'],
        ['git', 'push']
    ]
    
    for cmd in komutlar:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0 and "nothing to commit" not in res.stdout and "no changes added" not in res.stdout:
            print(f"Uyarı/Hata ({cmd[1]}): {res.stderr.strip()}")
            
    print("[OpsDeployment] Senkronizasyon tamamlandı.")

if __name__ == "__main__":
    git_yayinla()