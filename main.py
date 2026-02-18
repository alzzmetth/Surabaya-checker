#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import sys
from datetime import datetime
from pathlib import Path

# Install colorama dulu: pip install colorama
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print("Install colorama dulu: pip install colorama")
    sys.exit(1)

# ASCII ART SURABAYA - VERSION MOBILE (lebih kecil)
ASCII_ART = f"""
{Fore.RED}██╗░░░██╗██████╗░
{Fore.BLUE}╚██╗░██╔╝╚════██╗
{Fore.RED}░╚████╔╝░░░███╔═╝
{Fore.BLUE}░░╚██╔╝░░██╔══╝░░
{Fore.RED}░░░██║░░░███████╗
{Fore.BLUE}░░░╚═╝░░░╚══════╝{Style.RESET_ALL}
{Fore.RED}S U R A B A Y A{Style.RESET_ALL}
"""

class SurabayaNIKChecker:
    def __init__(self):
        self.base_path = Path(__file__).parent.absolute()
        self.kecamatan_file = self.base_path / 'kecamatan' / 'surabaya_kecamatan.json'
        self.kelurahan_file1 = self.base_path / 'kelurahan' / 'surabaya_kelurahan.json'
        self.kelurahan_file2 = self.base_path / 'kelurahan' / 'surabaya_kelurahan2.json'
        self.db_kec = None
        self.db_kel = None
        self.load_databases()
    
    def print_header(self):
        """Print header with ASCII art"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(ASCII_ART)
        print(f"{Fore.BLUE}╔════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.BLUE}║{Fore.RED}  NIK CHECKER SURABAYA  {Fore.BLUE}║{Style.RESET_ALL}")
        print(f"{Fore.BLUE}║{Fore.RED}  by: alzzdevmaret      {Fore.BLUE}║{Style.RESET_ALL}")
        print(f"{Fore.BLUE}╚════════════════════════╝{Style.RESET_ALL}\n")
    
    def print_menu(self):
        """Print main menu - mobile optimized"""
        print(f"{Fore.RED}┌──────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE}       MENU           {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}├──────────────────────┤{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} [1]{Fore.RED} ▶{Fore.BLUE} CEK NIK    {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} [2]{Fore.RED} ▶{Fore.BLUE} DATABASE   {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} [3]{Fore.RED} ▶{Fore.BLUE} TENTANG    {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} [0]{Fore.RED} ▶{Fore.BLUE} KELUAR     {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}└──────────────────────┘{Style.RESET_ALL}")
    
    def print_info(self):
        """Print database info - mobile optimized"""
        print(f"\n{Fore.RED}┌──────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE}      DATABASE        {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}├──────────────────────┤{Style.RESET_ALL}")
        
        if self.kecamatan_file.exists():
            with open(self.kecamatan_file, 'r') as f:
                data = json.load(f)
                jml_kec = len(data.get('kecamatan', {}))
            print(f"{Fore.RED}│{Fore.GREEN} ✔{Fore.BLUE} Kec:{Fore.RED}{jml_kec}          {Fore.RED}│{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}│{Fore.RED} ✘{Fore.BLUE} Kec: -         {Fore.RED}│{Style.RESET_ALL}")
        
        total_kel = 0
        if self.kelurahan_file1.exists():
            with open(self.kelurahan_file1, 'r') as f:
                data = json.load(f)
                total_kel += len(data.get('kelurahan', {}))
        
        if self.kelurahan_file2.exists():
            with open(self.kelurahan_file2, 'r') as f:
                data = json.load(f)
                total_kel += len(data.get('kelurahan', {}))
        
        print(f"{Fore.RED}│{Fore.GREEN} ✔{Fore.BLUE} Kel:{Fore.RED}{total_kel}         {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}└──────────────────────┘{Style.RESET_ALL}\n")
    
    def load_databases(self):
        """Load all database files"""
        try:
            if self.kecamatan_file.exists():
                with open(self.kecamatan_file, 'r') as f:
                    self.db_kec = json.load(f)
            else:
                print(f"{Fore.RED}✘ File kecamatan tidak ditemukan{Style.RESET_ALL}")
                self.db_kec = {"kecamatan": {}}
            
            self.db_kel = {"kelurahan": {}}
            if self.kelurahan_file1.exists():
                with open(self.kelurahan_file1, 'r') as f:
                    kel1 = json.load(f)
                    self.db_kel['kelurahan'].update(kel1.get('kelurahan', {}))
            
            if self.kelurahan_file2.exists():
                with open(self.kelurahan_file2, 'r') as f:
                    kel2 = json.load(f)
                    self.db_kel['kelurahan'].update(kel2.get('kelurahan', {}))
                    
        except Exception as e:
            print(f"{Fore.RED}✘ Error: {str(e)[:20]}{Style.RESET_ALL}")
    
    def check_nik(self, nik):
        """Main NIK checking function"""
        if not nik.isdigit() or len(nik) != 16:
            return None, "NIK harus 16 digit angka!"
        
        kode_kota = nik[0:4]
        if kode_kota != "3578":
            return None, f"Bukan NIK Surabaya!"
        
        kode_kec = nik[0:6]
        kode_kel = nik[0:10]
        tgl = int(nik[6:8])
        bln = int(nik[8:10])
        thn = int(nik[10:12])
        nomor_urut = nik[12:16]
        
        if tgl > 40:
            tgl_asli = tgl - 40
            gender = "P"
        else:
            tgl_asli = tgl
            gender = "L"
        
        try:
            if thn > 30:
                thn_fix = 1900 + thn
            else:
                thn_fix = 2000 + thn
            
            datetime(thn_fix, bln, tgl_asli)
            valid_tgl = f"{Fore.GREEN}✓{Style.RESET_ALL}"
        except ValueError:
            valid_tgl = f"{Fore.RED}✘{Style.RESET_ALL}"
        
        kecamatan = self.db_kec['kecamatan'].get(kode_kec, "?")
        kelurahan = self.db_kel['kelurahan'].get(kode_kel, "?")
        
        # Potong nama kalo kepanjangan buat mobile
        if len(kecamatan) > 10:
            kecamatan = kecamatan[:10] + "."
        if len(kelurahan) > 10:
            kelurahan = kelurahan[:10] + "."
        
        result = {
            'nik': nik,
            'kecamatan': kecamatan,
            'kelurahan': kelurahan,
            'tgl_lahir': f"{tgl_asli:02d}-{bln:02d}-{thn_fix}",
            'gender': gender,
            'valid_tgl': valid_tgl
        }
        
        return result, None
    
    def display_result(self, result):
        """Display NIK check result - mobile optimized"""
        print(f"\n{Fore.RED}┌──────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE}        HASIL         {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}├──────────────────────┤{Style.RESET_ALL}")
        
        # Tampilkan NIK per 4 digit biar mudah dibaca di mobile
        nik_display = f"{result['nik'][:4]}-{result['nik'][4:8]}-{result['nik'][8:12]}-{result['nik'][12:]}"
        print(f"{Fore.RED}│{Fore.BLUE} NIK:{Fore.RED}{nik_display}  {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} Kec:{Fore.RED}{result['kecamatan']:<12} {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} Kel:{Fore.RED}{result['kelurahan']:<12} {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} Tgl:{Fore.RED}{result['tgl_lahir']} {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} Gender:{Fore.RED}{result['gender']}   Status:{Fore.RED}{result['valid_tgl']}   {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}└──────────────────────┘{Style.RESET_ALL}\n")
    
    def about(self):
        """Show about information - mobile optimized"""
        print(f"\n{Fore.RED}┌──────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE}       TENTANG        {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}├──────────────────────┤{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} NIK Checker Surabaya {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} v1.0 - {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} by: alzzdevmaret     {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} 31 Kecamatan         {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}│{Fore.BLUE} 159 Kelurahan        {Fore.RED}│{Style.RESET_ALL}")
        print(f"{Fore.RED}└──────────────────────┘{Style.RESET_ALL}\n")
    
    def run(self):
        """Main program loop"""
        while True:
            self.print_header()
            self.print_menu()
            
            # Prompt lebih pendek untuk mobile
            choice = input(f"{Fore.RED}▶{Fore.BLUE} Pilih: {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.print_header()
                print(f"{Fore.RED}┌──────────────────────┐{Style.RESET_ALL}")
                print(f"{Fore.RED}│{Fore.BLUE}    CEK NIK SURABAYA  {Fore.RED}│{Style.RESET_ALL}")
                print(f"{Fore.RED}└──────────────────────┘{Style.RESET_ALL}\n")
                
                nik = input(f"{Fore.RED}▶{Fore.BLUE} NIK (16 digit): {Style.RESET_ALL}").strip()
                nik = nik.replace(" ", "").replace("-", "")  # Hapus spasi atau strip kalo ada
                
                result, error = self.check_nik(nik)
                if error:
                    print(f"\n{Fore.RED}✘ {error}{Style.RESET_ALL}\n")
                else:
                    self.display_result(result)
                
                input(f"{Fore.BLUE}▶ Enter untuk lanjut...{Style.RESET_ALL}")
                
            elif choice == "2":
                self.print_header()
                self.print_info()
                input(f"{Fore.BLUE}▶ Enter untuk lanjut...{Style.RESET_ALL}")
                
            elif choice == "3":
                self.print_header()
                self.about()
                input(f"{Fore.BLUE}▶ Enter untuk lanjut...{Style.RESET_ALL}")
                
            elif choice == "0":
                print(f"\n{Fore.RED}════════════════════════{Style.RESET_ALL}")
                print(f"{Fore.BLUE}  Sampai jumpa!         ")
                print(f"{Fore.RED}  - alzzdevmaret -      ")
                print(f"{Fore.RED}════════════════════════{Style.RESET_ALL}\n")
                break

if __name__ == "__main__":
    Path("kecamatan").mkdir(exist_ok=True)
    Path("kelurahan").mkdir(exist_ok=True)
    
    app = SurabayaNIKChecker()
    app.run()
