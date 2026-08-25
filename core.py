import os
import sys
import time
import logging
import subprocess
import random
import ctypes
import traceback
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    CREATE_NO_WINDOW = 0x08000000
else:
    CREATE_NO_WINDOW = 0


class OfficeCore:
    """Ядро программы: работа с файлами, процессами, удаление."""

    def __init__(self):
        self.logger = self._setup_logging()
        self.is_admin = self._check_admin()

    def _setup_logging(self):
        log_dir = Path(os.environ.get('TEMP', '.')) / 'OfficeLockCleaner_Logs'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f'unlock_office_{datetime.now().strftime("%Y%m%d")}.log'
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def _check_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def kill_office_processes(self):
        """Завершает процессы офисных пакетов."""
        office_masks = ['r7*', 'winword*', 'excel*', 'powerpnt*', 'soffice*']
        try:
            found_any = False
            for mask in office_masks:
                cmd_check = ['tasklist', '/fi', f'imagename eq {mask}', '/fo', 'csv']
                result = subprocess.run(
                    cmd_check,
                    capture_output=True,
                    text=True,
                    timeout=5,
                    creationflags=CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                base_name = mask.rstrip('*')
                if base_name.lower() in result.stdout.lower():
                    found_any = True
                    break

            if not found_any:
                self.logger.info("Процессы офисных пакетов не найдены")
                return True

            self.logger.info("Обнаружены процессы офисных пакетов, завершаем...")
            for attempt in range(3):
                for mask in office_masks:
                    subprocess.run(
                        ['taskkill', '/f', '/im', mask],
                        capture_output=True,
                        timeout=5,
                        creationflags=CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                    )
                time.sleep(1)

                still_running = False
                for mask in office_masks:
                    check = subprocess.run(
                        ['tasklist', '/fi', f'imagename eq {mask}', '/fo', 'csv'],
                        capture_output=True,
                        text=True,
                        timeout=5,
                        creationflags=CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                    )
                    base_name = mask.rstrip('*')
                    if base_name.lower() in check.stdout.lower():
                        still_running = True
                        break

                if not still_running:
                    self.logger.info("Все процессы офисных пакетов завершены")
                    return True
                self.logger.warning(f"Попытка {attempt+1}: процессы ещё есть")

            self.logger.warning("Не удалось завершить все процессы, продолжаем удаление")
            return False
        except Exception as e:
            self.logger.error(f"Ошибка при завершении процессов: {e}")
            return False

    def find_lock_files(self, file_path):
        """Находит все lock-файлы для данного файла."""
        try:
            folder = os.path.dirname(file_path)
            if not folder or not os.path.exists(folder):
                return []
            base = os.path.basename(file_path)
            name, ext = os.path.splitext(base)

            lock_files = set()
            for pat in [f".~lock.{base}#", f".~lock.{base}", f"~${base}"]:
                p = os.path.join(folder, pat)
                if os.path.isfile(p):
                    lock_files.add(p)

            for entry in os.listdir(folder):
                full = os.path.join(folder, entry)
                if not os.path.isfile(full):
                    continue
                entry_lower = entry.lower()
                if entry_lower.startswith('~$') or entry_lower.startswith('.~lock.'):
                    test_name = entry
                    for prefix in ['~$', '.~lock.']:
                        if test_name.startswith(prefix):
                            test_name = test_name[len(prefix):]
                    if test_name.endswith('#'):
                        test_name = test_name[:-1]
                    test_base, _ = os.path.splitext(test_name)
                    if test_base and (test_base in name or name in test_base):
                        lock_files.add(full)
            return list(lock_files)
        except Exception as e:
            self.logger.error(f"Ошибка в find_lock_files для {file_path}: {e}")
            return []

    def force_delete_file(self, filepath):
        """Удаляет файл несколькими способами, возвращает (успех, сообщение)."""
        if not os.path.exists(filepath):
            return True, "Уже удалён"

        # 1. Python
        try:
            os.chmod(filepath, 0o777)
            os.remove(filepath)
            if not os.path.exists(filepath):
                return True, "os.remove"
        except:
            pass

        # 2. PowerShell
        try:
            ps_cmd = [
                'powershell', '-Command',
                f'Remove-Item -LiteralPath "{filepath}" -Force -ErrorAction Stop'
            ]
            subprocess.run(
                ps_cmd,
                capture_output=True,
                timeout=10,
                check=True,
                creationflags=CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            if not os.path.exists(filepath):
                return True, "PowerShell"
        except:
            pass

        # 3. Переименование
        try:
            temp_dir = os.path.dirname(filepath) or os.getcwd()
            temp_name = os.path.join(temp_dir, f'~del_{random.randint(10000,99999)}.tmp')
            os.rename(filepath, temp_name)
            os.remove(temp_name)
            if not os.path.exists(filepath):
                return True, "переименование"
        except:
            pass

        # 4. cmd
        try:
            cmd = ['cmd', '/c', 'del', '/f', '/q', filepath]
            subprocess.run(
                cmd,
                capture_output=True,
                timeout=5,
                check=True,
                creationflags=CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            if not os.path.exists(filepath):
                return True, "cmd"
        except:
            pass

        return False, "не удалось удалить"

    def scan_folder_for_locks(self, folder):
        """Рекурсивно сканирует папку на наличие lock-файлов."""
        lock_files = []
        try:
            for root, dirs, files in os.walk(folder):
                for f in files:
                    if f.startswith('~$') or f.startswith('.~lock.'):
                        full = os.path.join(root, f)
                        if os.path.isfile(full):
                            lock_files.append(full)
        except Exception as e:
            self.logger.error(f"Ошибка сканирования {folder}: {e}")
            raise
        return lock_files