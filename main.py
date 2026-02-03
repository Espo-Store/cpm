import requests
import os
import sys
import time
import json

# ================= KONFIGURASI =================
API_URL = "https://espostory.my.id/data_api.php"
API_KEY = ""

# ================= WARNA & UI =================
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""{CYAN}
╔══════════════════════════════════════╗
║     CPM MULTIPLAYER TOOL - PY      ║
║      POWERED BY ESPOSTORY          ║
╚══════════════════════════════════════╝{RESET}""")
    print(f"{WHITE}Connected to: {API_URL}{RESET}\n")

# ================= FUNGSI API UTAMA =================
def request_api(action, data=None):
    if data is None:
        data = {}
    
    payload = {
        'api_key': API_KEY,
        'action': action,
        'device_id': 'TERMUX-PY-CLIENT'
    }
    payload.update(data)
    
    try:
        print(f"{YELLOW}[!] Mengirim request ke server...{RESET}")
        r = requests.post(API_URL, data=payload)
        return r.json()
    except Exception as e:
        return {'success': False, 'message': f"Connection Error: {str(e)}"}

def print_result(res):
    if res.get('success'):
        print(f"{GREEN}[SUCCESS] {res.get('message', 'Done')}{RESET}")
    else:
        print(f"{RED}[FAILED] {res.get('message', 'Unknown error')}{RESET}")
    input(f"{WHITE}\nTekan Enter untuk kembali...{RESET}")

def get_input(prompt):
    return input(f"{WHITE}{prompt}: {RESET}")

# ================= FITUR-FITUR (SUB MENU) =================

# --- 1. ACCOUNT MANAGER ---
def menu_account():
    while True:
        clear()
        banner()
        print(f"{MAGENTA}[ ACCOUNT MANAGER ]{RESET}")
        print("1. Check Account Detail")
        print("2. Change Password")
        print("3. Change Email")
        print("4. Change Name")
        print("5. Set Player ID")
        print("6. Bug Fix Account (Gender Error)")
        print("0. Kembali ke Menu Utama")
        
        choice = input("\nPilih: ")
        if choice == '0': break
        
        email = get_input("Masukan Email Akun")
        password = get_input("Masukan Password Akun")
        
        if choice == '1':
            res = request_api('check_account', {'email': email, 'password': password})
            if res.get('success'):
                d = res.get('data', {})
                print(f"\n{CYAN}--- DATA AKUN ---{RESET}")
                print(f"Nama: {d.get('name')}")
                print(f"ID: {d.get('localID')}")
                print(f"Money: {d.get('money')}")
                print(f"Coin: {d.get('coin')}")
                print(f"Level: {d.get('level')}")
                print(f"Status Bug: {d.get('personEquipmentsMale', {}).get('Gender')}")
                print(f"{RESET}")
            print_result(res)
            
        elif choice == '2':
            new_pass = get_input("Masukan Password Baru")
            print_result(request_api('change_password', {'email': email, 'password': password, 'newPassword': new_pass}))
            
        elif choice == '3':
            new_email = get_input("Masukan Email Baru")
            print_result(request_api('change_email', {'email': email, 'password': password, 'newEmail': new_email}))
            
        elif choice == '4':
            new_name = get_input("Masukan Nama Baru")
            print_result(request_api('change_name', {'email': email, 'password': password, 'newName': new_name}))
            
        elif choice == '5':
            new_id = get_input("Masukan ID Baru (contoh: ESP-01)")
            print_result(request_api('set_player_id', {'email': email, 'password': password, 'newId': new_id}))
            
        elif choice == '6':
            print_result(request_api('bug_fix_account', {'email': email, 'password': password}))

# --- 2. MONEY & RANK ---
def menu_money_rank():
    while True:
        clear()
        banner()
        print(f"{MAGENTA}[ MONEY & RANK ]{RESET}")
        print("1. Inject Rank King (Top 1)")
        print("2. Add Money Only")
        print("3. Add Coin Only")
        print("4. Set Race Stats (Win/Loss)")
        print("0. Kembali ke Menu Utama")
        
        choice = input("\nPilih: ")
        if choice == '0': break
        
        email = get_input("Masukan Email Akun")
        password = get_input("Masukan Password Akun")
        
        if choice == '1':
            print_result(request_api('inject_rank_king', {'email': email, 'password': password}))
        elif choice == '2':
            amt = int(get_input("Jumlah Money (Max 50M)"))
            print_result(request_api('add_money_only', {'email': email, 'password': password, 'money': amt}))
        elif choice == '3':
            amt = int(get_input("Jumlah Coin (Max 500K)"))
            print_result(request_api('add_coin_only', {'email': email, 'password': password, 'coin': amt}))
        elif choice == '4':
            win = get_input("Jumlah Wins")
            lose = get_input("Jumlah Losses")
            print_result(request_api('set_race_stats', {'email': email, 'password': password, 'wins': win, 'losses': lose}))

# --- 3. UNLOCK FEATURES ---
def menu_unlocks():
    while True:
        clear()
        banner()
        print(f"{MAGENTA}[ UNLOCK FEATURES ]{RESET}")
        print("1. Unlock All Clothes")
        print("2. Unlock All Levels")
        print("3. Unlock Houses")
        print("4. Unlock W16 Car")
        print("5. Unlock Horns")
        print("6. Unlock Smoke")
        print("7. Disable Damage")
        print("8. Unlimited Fuel")
        print("9. Remove Face (Male)")
        print("10. Remove Face (Female)")
        print("0. Kembali ke Menu Utama")
        
        choice = input("\nPilih: ")
        if choice == '0': break
        
        email = get_input("Masukan Email Akun")
        password = get_input("Masukan Password Akun")
        
        action_map = {
            '1': 'unlock_all_clothes', '2': 'unlock_all_levels',
            '3': 'unlock_houses', '4': 'unlock_w16',
            '5': 'unlock_horns', '6': 'unlock_smoke',
            '7': 'disable_damage', '8': 'unlimited_fuel',
            '9': 'remove_face_male', '10': 'remove_face_female'
        }
        
        if choice in action_map:
            print_result(request_api(action_map[choice], {'email': email, 'password': password}))
        else:
            print("Pilihan salah")

# --- 4. ADVANCED TOOLS ---
def menu_advanced():
    while True:
        clear()
        banner()
        print(f"{MAGENTA}[ ADVANCED TOOLS ]{RESET}")
        print("1. Clone Single Account")
        print("2. Bulk Clone Accounts (Buat Banyak Akun)")
        print("3. Copy Plates (Tuning)")
        print("0. Kembali ke Menu Utama")
        
        choice = input("\nPilih: ")
        if choice == '0': break
        
        if choice == '1':
            # Clone Single
            print(f"{YELLOW}[SOURCE AKUN - YANG DICOPY]{RESET}")
            s_email = get_input("Email Source")
            s_pass = get_input("Password Source")
            print(f"{YELLOW}[TARGET AKUN - TUJUAN]{RESET}")
            t_email = get_input("Email Target")
            t_pass = get_input("Password Target")
            
            res = request_api('clone_single_account', {
                'emailSource': s_email, 'passwordSource': s_pass,
                'emailTarget': t_email, 'passwordTarget': t_pass
            })
            print_result(res)
            
        elif choice == '2':
            # Bulk Clone
            print(f"{YELLOW}[SOURCE AKUN]{RESET}")
            s_email = get_input("Email Source")
            s_pass = get_input("Password Source")
            count = int(get_input("Berapa banyak akun?"))
            rank = input("Inject Rank juga? (y/n): ").lower() == 'y'
            
            res = request_api('bulk_clone_accounts', {
                'sourceEmail': s_email, 'sourcePassword': s_pass,
                'count': count, 'includeRank': rank
            })
            if res.get('success'):
                accounts = res.get('accounts', [])
                print(f"{GREEN}Berhasil membuat {len(accounts)} akun!{RESET}")
                for acc in accounts:
                    print(f"{CYAN}Email: {acc['email']} | Pass: {acc['password']} | ID: {acc['localID']}{RESET}")
                # Simpan ke file
                with open('result_clone.txt', 'w') as f:
                    for acc in accounts:
                        f.write(f"{acc['email']}:{acc['password']}\n")
                print(f"{YELLOW}Data tersimpan di result_clone.txt{RESET}")
            else:
                print_result(res)
            input("Tekan Enter...")
            
        elif choice == '3':
            # Copy Plates
            print(f"{YELLOW}[SOURCE AKUN - PEMILIK PLATES]{RESET}")
            s_email = get_input("Email Source")
            s_pass = get_input("Password Source")
            print(f"{YELLOW}[TARGET AKUN - YANG DITERIMA]{RESET}")
            t_email = get_input("Email Target")
            t_pass = get_input("Password Target")
            
            print(f"{YELLOW}Info: Jika pilih ID kosong, akan copy semua plates.{RESET}")
            plates = input("Masukan ID Plate (Pisahkan koma, atau kosongkan untuk semua): ")
            plate_list = plates.split(',') if plates else []
            
            res = request_api('copy_plates', {
                'emailSource': s_email, 'passwordSource': s_pass,
                'emailTarget': t_email, 'passwordTarget': t_pass,
                'selectedPlateIds': json.dumps(plate_list)
            })
            print_result(res)

# --- 5. VIP & INFO ---
def menu_vip():
    while True:
        clear()
        banner()
        print(f"{MAGENTA}[ VIP & STATUS ]{RESET}")
        
        # Cek status dulu
        info = request_api('get_user_info')
        if info.get('success'):
            data = info.get('data', {})
            bal = data.get('balance', 0)
            is_vip = data.get('is_vip', False)
            exp = data.get('vip_expires_at', 'None')
            print(f"Saldo: Rp {bal}")
            print(f"Status VIP: {'AKTIF' if is_vip else 'TIDAK'}")
            print(f"Exp VIP: {exp}\n")
        else:
            print("Gagal mengambil info user.\n")

        print("1. Beli Paket VIP")
        print("2. Riwayat Transaksi")
        print("0. Kembali ke Menu Utama")
        
        choice = input("\nPilih: ")
        if choice == '0': break
        
        if choice == '1':
            print("Daftar Paket:")
            print("1. Promo (2 Hari) - Rp 25.000")
            print("2. Paket 1 (4 Hari) - Rp 50.000")
            print("3. Paket 2 (7 Hari) - Rp 80.000")
            print("4. Paket 3 (1 Bulan) - Rp 350.000")
            print("5. Paket 4 (1 Tahun) - Rp 1.500.000")
            p_code = input("Masukan kode paket (promo/paket1/paket2/paket3/paket4): ")
            print_result(request_api('buy_vip_package', {'package_code': p_code}))
            
        elif choice == '2':
            res = request_api('get_transactions')
            if res.get('success'):
                hist = res.get('data', [])
                print(f"{CYAN}--- 20 TRANSAKSI TERAKHIR ---{RESET}")
                for h in hist:
                    print(f"{h['type']} | Rp {h['amount']} | {h['description']} | {h['created_at']}")
            else:
                print("Gagal mengambil riwayat.")
            input("Tekan Enter...")

# ================= MAIN LOGIN & LOOP =================
def login():
    global API_KEY
    clear()
    print(f"{CYAN}Silakan masukkan API Key Anda.{RESET}")
    print("Jika belum punya, silakan beli/daftar di website terkait.\n")
    key = input("API KEY: ")
    if key:
        API_KEY = key
        # Validasi Key
        res = request_api('get_user_info')
        if res.get('success'):
            print(f"{GREEN}Login Berhasil! Selamat datang.{RESET}")
            time.sleep(1.5)
            return True
        else:
            print(f"{RED}API Key Invalid!{RESET}")
            time.sleep(2)
    return False

def main_menu():
    while True:
        clear()
        banner()
        print(f"{MAGENTA}[ MAIN MENU ]{RESET}")
        print("1. Account Manager (Check, Edit, Bugfix)")
        print("2. Money & Rank (Inject, Stats)")
        print("3. Unlock Features (Cars, Clothes, Houses)")
        print("4. Advanced Tools (Clone, Copy Plates)")
        print("5. VIP & Balance Status")
        print("0. Keluar")
        
        choice = input(f"\n{WHITE}Pilih Menu: {RESET}")
        
        if choice == '1': menu_account()
        elif choice == '2': menu_money_rank()
        elif choice == '3': menu_unlocks()
        elif choice == '4': menu_advanced()
        elif choice == '5': menu_vip()
        elif choice == '0':
            print(f"{YELLOW}Terima kasih!{RESET}")
            sys.exit()
        else:
            print(f"{RED}Pilihan tidak tersedia.{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    if login():
        main_menu()
    else:
        sys.exit()
