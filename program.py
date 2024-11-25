import tkinter as tk
from tkinter import ttk
import winreg
import ctypes
import os
import subprocess
from tkinter import messagebox
import json
import sys

class WindowsTweaker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WinArc")
        self.root.geometry("450x510")
        
        # Применяем современный стиль
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настраиваем цвета
        self.root.configure(bg='#f0f0f0')
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TButton', padding=6, background='#0078d7', foreground='white')
        
        # Создаем вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Вкладка Кастомизация
        self.customization_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.customization_frame, text='Кастомизация')
        
        # Вкладка Система
        self.system_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.system_frame, text='Система')
        
        self.create_customization_tweaks()
        self.create_system_tweaks()

        # Скрываем консоль
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        current_window = kernel32.GetConsoleWindow()
        user32.ShowWindow(current_window, 0)


    def create_customization_tweaks(self):
        # Настройки кастомизации
        tweaks = [
            ("Тёмная тема", self.toggle_dark_theme),
            ("Отключить прозрачность", self.toggle_transparency),
            ("Скрыть значки рабочего стола", self.toggle_desktop_icons),
            ("Изменить цвет акцента", self.change_accent_color),
            ("Скрыть панель поиска", self.toggle_search_bar)
        ]
        
        for i, (text, command) in enumerate(tweaks):
            btn = ttk.Button(self.customization_frame, text=text, command=command)
            btn.pack(pady=5, padx=20, fill='x')

    def create_system_tweaks(self):
        # Системные настройки
        tweaks = [
            ("Отключить Windows Defender", self.toggle_defender),
            ("Оптимизация производительности", self.optimize_performance),
            ("Отключить телеметрию", self.disable_telemetry),
            ("Очистка диска", self.clean_disk),
            ("Отключить обновления", self.toggle_updates)
        ]
        
        for i, (text, command) in enumerate(tweaks):
            btn = ttk.Button(self.system_frame, text=text, command=command)
            btn.pack(pady=5, padx=20, fill='x')

    def toggle_dark_theme(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                               0, winreg.KEY_ALL_ACCESS)
            current_value = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 1 if current_value == 0 else 0)
            messagebox.showinfo("Успех", "Настройка темы изменена. Перезагрузите систему.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить тему: {str(e)}")

    def toggle_transparency(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                               0, winreg.KEY_ALL_ACCESS)
            current_value = winreg.QueryValueEx(key, "EnableTransparency")[0]
            winreg.SetValueEx(key, "EnableTransparency", 0, winreg.REG_DWORD, 1 if current_value == 0 else 0)
            messagebox.showinfo("Успех", "Прозрачность изменена")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить прозрачность: {str(e)}")

    def toggle_desktop_icons(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                               0, winreg.KEY_ALL_ACCESS)
            current_value = winreg.QueryValueEx(key, "HideIcons")[0]
            winreg.SetValueEx(key, "HideIcons", 0, winreg.REG_DWORD, 1 if current_value == 0 else 0)
            self.refresh_explorer()
            messagebox.showinfo("Успех", "Настройка значков изменена")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить отображение значков: {str(e)}")

    def change_accent_color(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\DWM",
                               0, winreg.KEY_ALL_ACCESS)
            current_value = winreg.QueryValueEx(key, "AccentColor")[0]
            # Переключаем между несколькими предустановленными цветами
            colors = [0xFF0000, 0x00FF00, 0x0000FF]
            current_index = colors.index(current_value) if current_value in colors else -1
            new_color = colors[(current_index + 1) % len(colors)]
            winreg.SetValueEx(key, "AccentColor", 0, winreg.REG_DWORD, new_color)
            messagebox.showinfo("Успех", "Цвет акцента изменен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить цвет акцента: {str(e)}")

    def toggle_search_bar(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Search",
                               0, winreg.KEY_ALL_ACCESS)
            current_value = winreg.QueryValueEx(key, "SearchboxTaskbarMode")[0]
            winreg.SetValueEx(key, "SearchboxTaskbarMode", 0, winreg.REG_DWORD, 0 if current_value == 1 else 1)
            self.refresh_explorer()
            messagebox.showinfo("Успех", "Отображение поиска изменено")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить отображение поиска: {str(e)}")

    def toggle_defender(self):
        try:
            if ctypes.windll.shell32.IsUserAnAdmin():
                subprocess.run(['powershell', 'Set-MpPreference -DisableRealtimeMonitoring $true'], 
                             capture_output=True)
                messagebox.showinfo("Успех", "Windows Defender временно отключен")
            else:
                messagebox.showerror("Ошибка", "Требуются права администратора")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отключить Windows Defender: {str(e)}")

    def optimize_performance(self):
        try:
            # Отключаем визуальные эффекты
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                               0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
            
            # Очищаем временные файлы
            subprocess.run(['powershell', 'Clear-RecycleBin -Force'], capture_output=True)
            os.system('del /s /q %temp%\\*')
            
            messagebox.showinfo("Успех", "Оптимизация выполнена")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить оптимизацию: {str(e)}")

    def disable_telemetry(self):
        try:
            if ctypes.windll.shell32.IsUserAnAdmin():
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                   r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                                   0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(key, "AllowTelemetry", 0, winreg.REG_DWORD, 0)
                messagebox.showinfo("Успех", "Телеметрия отключена")
            else:
                messagebox.showerror("Ошибка", "Требуются права администратора")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отключить телеметрию: {str(e)}")

    def clean_disk(self):
        try:
            subprocess.run(['cleanmgr', '/sagerun:1'], capture_output=True)
            messagebox.showinfo("Успех", "Запущена очистка диска")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить очистку диска: {str(e)}")

    def toggle_updates(self):
        try:
            if ctypes.windll.shell32.IsUserAnAdmin():
                service_name = "wuauserv"
                subprocess.run(['sc', 'config', service_name, 'start=disabled'], capture_output=True)
                subprocess.run(['net', 'stop', service_name], capture_output=True)
                messagebox.showinfo("Успех", "Служба обновлений отключена")
            else:
                messagebox.showerror("Ошибка", "Требуются права администратора")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отключить обновления: {str(e)}")

    def refresh_explorer(self):
        try:
            subprocess.run(['taskkill', '/f', '/im', 'explorer.exe'], capture_output=True)
            subprocess.Popen('explorer.exe')
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось перезапустить проводник: {str(e)}")

if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        app = WindowsTweaker()
        app.root.mainloop()
