#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import configparser
from pathlib import Path
from datetime import datetime

from core import OfficeCore

class OfficeGui:
    def __init__(self, root):
        self.root = root
        self.core = OfficeCore()
        self.current_lang = 'ru'
        self.lang_data = {}
        self.settings_file = Path(os.path.dirname(sys.argv[0])) / 'settings.ini'

        # Встроенные словари (fallback, если нет файлов)
        self._builtin_langs = {
            'ru': {
                'window_title': 'OfficeLockCleaner – удаление блокировок',
                'menu_file': 'Файл',
                'menu_file_add_files': 'Добавить файлы...',
                'menu_file_add_folder': 'Добавить папку...',
                'menu_file_exit': 'Выход',
                'menu_view': 'Вид',
                'menu_view_show_log': 'Показать журнал',
                'menu_view_show_status': 'Показать статусную строку',
                'menu_lang': 'Язык',
                'menu_help': 'Помощь',
                'menu_help_about': 'О программе',
                'btn_unlock': '🔓 Разблокировать',
                'btn_cancel': '⏹ Отмена',
                'btn_clear': 'Очистить',
                'tree_col_file': 'Файл',
                'tree_col_status': 'Статус',
                'status_ready': 'Готов. Добавьте файлы или папки через меню Файл.',
                'status_processing': 'Обработка...',
                'status_done': '✅ Разблокировка завершена',
                'status_partial': 'Удалено {success} файлов, ошибок {errors}',
                'status_added': 'Добавлено файлов: {count}',
                'status_found_locks': 'Найдено {count} блокировок',
                'status_cleared': 'Список очищен',
                'status_dnd': 'Добавлено через Drag&Drop: {count}',
                'status_deleting': 'Удалено {count} файлов',
                'status_processing_file': 'Обработка {idx}/{total}: {filename}',
                'status_item_pending': 'Ожидание',
                'status_item_deleted': 'Удалён',
                'status_item_error': 'Ошибка',
                'status_item_skipped': 'Пропущен',
                'log_title': 'Журнал операций',
                'list_info': 'Файлов: {count}',
                'msg_select_files': 'Выберите файлы для разблокировки',
                'msg_select_folder': 'Выберите папку для поиска блокировок',
                'msg_no_files': 'Список пуст. Добавьте файлы или папки через меню Файл.',
                'msg_no_locks': 'В папке не найдено файлов блокировки.',
                'msg_confirm_unlock': 'Будет обработано {count} записей.\n\nПрограмма завершит процессы офиса и удалит lock-файлы.\nПродолжить?',
                'msg_unlock_done': '✅ Все найденные блокировки удалены.\nОбработано: {count}',
                'msg_unlock_partial': 'Не удалось удалить:\n{errors}\n\nРекомендации:\n• Закройте офис вручную\n• Запустите от имени администратора',
                'msg_error_title': 'Ошибка',
                'msg_info_title': 'Информация',
                'msg_warning_title': 'Предупреждение',
                'msg_critical_error': 'Непредвиденная ошибка:\n{error}\n\nПодробности в логе.',
                'msg_not_admin': 'Запущено без прав администратора.\nНекоторые файлы могут не удалиться.',
                'about_text': 'OfficeLockCleaner v2.6\n\nУдаление фантомных файлов блокировки\nофисных пакетов (Word, Excel, LibreOffice, Р7-Офис).\n\nАвтор: vseuk\nЛицензия: MIT',
            },
            'en': {
                'window_title': 'OfficeLockCleaner – remove locks',
                'menu_file': 'File',
                'menu_file_add_files': 'Add Files...',
                'menu_file_add_folder': 'Add Folder...',
                'menu_file_exit': 'Exit',
                'menu_view': 'View',
                'menu_view_show_log': 'Show Log',
                'menu_view_show_status': 'Show Status Bar',
                'menu_lang': 'Language',
                'menu_help': 'Help',
                'menu_help_about': 'About',
                'btn_unlock': '🔓 Unlock',
                'btn_cancel': '⏹ Cancel',
                'btn_clear': 'Clear',
                'tree_col_file': 'File',
                'tree_col_status': 'Status',
                'status_ready': 'Ready. Add files or folders via File menu.',
                'status_processing': 'Processing...',
                'status_done': '✅ Unlock completed',
                'status_partial': 'Deleted {success} files, {errors} errors',
                'status_added': 'Added files: {count}',
                'status_found_locks': 'Found {count} lock files',
                'status_cleared': 'List cleared',
                'status_dnd': 'Added via Drag&Drop: {count}',
                'status_deleting': 'Deleted {count} files',
                'status_processing_file': 'Processing {idx}/{total}: {filename}',
                'status_item_pending': 'Pending',
                'status_item_deleted': 'Deleted',
                'status_item_error': 'Error',
                'status_item_skipped': 'Skipped',
                'log_title': 'Operation Log',
                'list_info': 'Files: {count}',
                'msg_select_files': 'Select files to unlock',
                'msg_select_folder': 'Select folder to scan for lock files',
                'msg_no_files': 'List is empty. Add files or folders via File menu.',
                'msg_no_locks': 'No lock files found in the folder.',
                'msg_confirm_unlock': 'Will process {count} entries.\n\nProgram will terminate office processes and delete lock files.\nContinue?',
                'msg_unlock_done': '✅ All found lock files deleted.\nProcessed: {count}',
                'msg_unlock_partial': 'Failed to delete:\n{errors}\n\nRecommendations:\n• Close office manually\n• Run as administrator',
                'msg_error_title': 'Error',
                'msg_info_title': 'Information',
                'msg_warning_title': 'Warning',
                'msg_critical_error': 'Unexpected error:\n{error}\n\nSee log for details.',
                'msg_not_admin': 'Running without administrator privileges.\nSome files may not be deleted.',
                'about_text': 'OfficeLockCleaner v2.6\n\nRemove phantom lock files\nfrom office suites (Word, Excel, LibreOffice, Р7-Офис).\n\nAuthor: vseuk\nLicense: MIT',
            }
        }

        self.load_language('ru')
        self.load_settings()
        self.load_language(self.current_lang)

        self.root.title(self.tr('window_title'))
        self.root.geometry("850x600")
        self.root.minsize(700, 450)

        self.processing = False
        self.cancel_requested = False
        self.log_visible = True
        self.status_visible = True

        self.build_ui()
        self.setup_hotkeys()
        self.update_ui_texts()

        if not self.core.is_admin:
            messagebox.showwarning(self.tr('msg_warning_title'), self.tr('msg_not_admin'))

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ---------- Работа с языками ----------
    def load_language(self, lang_code):
        """Загружает язык из файла lang/<lang_code>.ini, либо встроенный fallback."""
        base_path = Path(os.path.dirname(sys.argv[0]))
        lang_path = base_path / 'lang' / f'{lang_code}.ini'
        if lang_path.exists():
            try:
                config = configparser.ConfigParser()
                config.read(lang_path, encoding='utf-8')
                if 'Strings' in config:
                    self.lang_data = dict(config['Strings'])
                else:
                    self.lang_data = self._builtin_langs.get(lang_code, self._builtin_langs['ru']).copy()
            except Exception as e:
                print(f"Error loading language {lang_code}: {e}")
                self.lang_data = self._builtin_langs.get(lang_code, self._builtin_langs['ru']).copy()
        else:
            # Если файла нет, используем встроенный словарь для данного языка
            self.lang_data = self._builtin_langs.get(lang_code, self._builtin_langs['ru']).copy()
        self.current_lang = lang_code

    def get_available_langs(self):
        base_path = Path(os.path.dirname(sys.argv[0])) / 'lang'
        if not base_path.exists():
            return ['ru', 'en']  # возвращаем поддерживаемые встроенные языки
        files = base_path.glob('*.ini')
        langs = [f.stem for f in files if f.is_file()]
        # Добавляем встроенные языки, если их нет в папке
        for builtin in self._builtin_langs.keys():
            if builtin not in langs:
                langs.append(builtin)
        return sorted(langs)

    def tr(self, key, **kwargs):
        text = self.lang_data.get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except KeyError:
                pass
        return text

    # ---------- Настройки ----------
    def load_settings(self):
        if self.settings_file.exists():
            try:
                config = configparser.ConfigParser()
                config.read(self.settings_file, encoding='utf-8')
                if 'Settings' in config:
                    if 'lang' in config['Settings']:
                        lang = config['Settings']['lang']
                        if lang in self.get_available_langs():
                            self.current_lang = lang
                    if 'show_log' in config['Settings']:
                        self.log_visible = config['Settings'].getboolean('show_log')
                    if 'show_status' in config['Settings']:
                        self.status_visible = config['Settings'].getboolean('show_status')
            except:
                pass

    def save_settings(self):
        try:
            config = configparser.ConfigParser()
            config['Settings'] = {
                'lang': self.current_lang,
                'show_log': str(self.log_visible),
                'show_status': str(self.status_visible),
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                config.write(f)
        except:
            pass

    def set_language(self, lang):
        if lang != self.current_lang:
            self.current_lang = lang
            self.load_language(lang)
            self.save_settings()
            self.update_ui_texts()

    # ---------- Построение интерфейса ----------
    def build_ui(self):
        main = ttk.Frame(self.root, padding="5")
        main.pack(fill='both', expand=True)

        self.create_menu()

        # Список файлов (основная область)
        list_frame = ttk.LabelFrame(main, text=self.tr('list_info', count=0), padding="2")
        list_frame.pack(fill='both', expand=True, pady=(0, 5))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        columns = ('status',)
        self.tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', selectmode='extended')
        self.tree.heading('#0', text=self.tr('tree_col_file'))
        self.tree.heading('status', text=self.tr('tree_col_status'))
        self.tree.column('#0', width=500)
        self.tree.column('status', width=100)

        vsb = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')

        # Нижняя строка внутри рамки: счётчик + кнопка Очистить
        list_bottom = ttk.Frame(list_frame)
        list_bottom.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(2,0))
        self.list_info_var = tk.StringVar(value=self.tr('list_info', count=0))
        info_label = ttk.Label(list_bottom, textvariable=self.list_info_var, font=('Segoe UI', 8))
        info_label.pack(side='left', padx=2)

        self.btn_clear = ttk.Button(list_bottom, text=self.tr('btn_clear'), command=self.clear_list, width=10)
        self.btn_clear.pack(side='right', padx=2)

        # Центральная панель с кнопкой Разблокировать / Отмена
        action_frame = ttk.Frame(main)
        action_frame.pack(fill='x', pady=5)
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(2, weight=1)

        self.btn_unlock = tk.Button(
            action_frame,
            text=self.tr('btn_unlock'),
            command=self.unlock_all,
            font=('Segoe UI', 11, 'bold'),
            bg='#2B5797',
            fg='white',
            relief='flat',
            padx=30,
            pady=8,
            cursor='hand2'
        )
        self.btn_unlock.grid(row=0, column=1, pady=2)
        self.btn_unlock.bind('<Enter>', lambda e: self.btn_unlock.config(bg='#1E3F6F'))
        self.btn_unlock.bind('<Leave>', lambda e: self.btn_unlock.config(bg='#2B5797'))

        self.btn_cancel = tk.Button(
            action_frame,
            text=self.tr('btn_cancel'),
            command=self.cancel_unlock,
            font=('Segoe UI', 11, 'bold'),
            bg='#D32F2F',
            fg='white',
            relief='flat',
            padx=30,
            pady=8,
            cursor='hand2'
        )
        self.btn_cancel.grid(row=0, column=1, pady=2)
        self.btn_cancel.grid_remove()
        self.btn_cancel.bind('<Enter>', lambda e: self.btn_cancel.config(bg='#B71C1C'))
        self.btn_cancel.bind('<Leave>', lambda e: self.btn_cancel.config(bg='#D32F2F'))

        # Лог
        self.log_frame = ttk.LabelFrame(main, text=self.tr('log_title'), padding="2")
        self.log_frame.pack(fill='x', pady=(0, 5))

        self.log_text = scrolledtext.ScrolledText(
            self.log_frame, height=4, wrap='word', state='disabled',
            font=('Segoe UI', 8), bg='#F8F8F8'
        )
        self.log_text.pack(fill='both', expand=True)

        # Статусная строка
        self.status_frame = ttk.Frame(main)
        self.status_frame.pack(fill='x')

        self.status_var = tk.StringVar(value=self.tr('status_ready'))
        status_label = ttk.Label(self.status_frame, textvariable=self.status_var, font=('Segoe UI', 8))
        status_label.pack(side='left', fill='x', expand=True)

        self.progress = ttk.Progressbar(self.status_frame, mode='determinate', length=150)
        self.progress.pack(side='right', padx=5)
        self.progress.pack_forget()

        # Применяем сохранённые состояния видимости
        if not self.log_visible:
            self.log_frame.pack_forget()
        if not self.status_visible:
            self.status_frame.pack_forget()

    def create_menu(self):
        # Удаляем старое меню, если было
        if hasattr(self, 'menubar') and self.menubar:
            self.root.config(menu='')
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Меню "Файл"
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label=self.tr('menu_file_add_files'), command=self.add_files)
        self.file_menu.add_command(label=self.tr('menu_file_add_folder'), command=self.add_folder)
        self.file_menu.add_separator()
        self.file_menu.add_command(label=self.tr('menu_file_exit'), command=self.on_closing)
        self.menubar.add_cascade(label=self.tr('menu_file'), menu=self.file_menu)

        # Меню "Вид"
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.view_log_var = tk.BooleanVar(value=self.log_visible)
        self.view_menu.add_checkbutton(label=self.tr('menu_view_show_log'), variable=self.view_log_var,
                                       command=self.toggle_log)
        self.view_status_var = tk.BooleanVar(value=self.status_visible)
        self.view_menu.add_checkbutton(label=self.tr('menu_view_show_status'), variable=self.view_status_var,
                                       command=self.toggle_status)
        self.menubar.add_cascade(label=self.tr('menu_view'), menu=self.view_menu)

        # Меню "Язык"
        self.lang_menu = tk.Menu(self.menubar, tearoff=0)
        self.rebuild_lang_menu()
        self.menubar.add_cascade(label=self.tr('menu_lang'), menu=self.lang_menu)

        # Меню "Помощь"
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label=self.tr('menu_help_about'), command=self.show_about)
        self.menubar.add_cascade(label=self.tr('menu_help'), menu=self.help_menu)

    def rebuild_lang_menu(self):
        """Обновляет список доступных языков в меню."""
        if hasattr(self, 'lang_menu'):
            self.lang_menu.delete(0, tk.END)
        for lang in self.get_available_langs():
            label = lang.upper()
            self.lang_menu.add_command(label=label, command=lambda l=lang: self.set_language(l))

    # ---------- Обновление текстов интерфейса ----------
    def update_ui_texts(self):
        self.root.title(self.tr('window_title'))
        self.btn_unlock.config(text=self.tr('btn_unlock'))
        self.btn_cancel.config(text=self.tr('btn_cancel'))
        self.btn_clear.config(text=self.tr('btn_clear'))
        self.tree.heading('#0', text=self.tr('tree_col_file'))
        self.tree.heading('status', text=self.tr('tree_col_status'))
        self.log_frame['text'] = self.tr('log_title')
        if not self.processing:
            self.status_var.set(self.tr('status_ready'))
        self.update_list_info()

        # Обновляем всё меню пересозданием
        self.rebuild_menu()

    def rebuild_menu(self):
        """Пересоздаёт меню с актуальными переводами."""
        # Сохраняем текущие состояния переменных
        if hasattr(self, 'view_log_var'):
            log_visible = self.view_log_var.get()
            status_visible = self.view_status_var.get()
        else:
            log_visible = self.log_visible
            status_visible = self.status_visible

        # Создаём меню заново
        self.create_menu()

        # Восстанавливаем состояния чекбоксов (они уже созданы с новыми переводами)
        self.view_log_var.set(log_visible)
        self.view_status_var.set(status_visible)

    # ---------- Работа со списком файлов ----------
    def update_list_info(self):
        count = len(self.tree.get_children())
        self.list_info_var.set(self.tr('list_info', count=count))

    def add_item(self, filepath, status='pending'):
        filepath = self.normalize_path(filepath)
        for item in self.tree.get_children():
            if self.tree.item(item, 'text') == filepath:
                return
        item = self.tree.insert('', 'end', text=filepath, values=(self.tr('status_item_pending'),))
        self.tree.item(item, tags=(status,))
        self.update_list_info()
        return item

    def update_item_status(self, item, status_key, status_text=None):
        if status_text is None:
            status_text = self.tr('status_item_' + status_key)
        self.tree.set(item, 'status', status_text)
        self.tree.item(item, tags=(status_key,))
        if status_key == 'deleted':
            self.tree.tag_configure('deleted', background='#d4edda')
        elif status_key == 'error':
            self.tree.tag_configure('error', background='#f8d7da')
        elif status_key == 'skipped':
            self.tree.tag_configure('skipped', background='#fff3cd')
        self.tree.item(item, tags=(status_key,))

    def get_files_from_tree(self):
        return [self.tree.item(item, 'text') for item in self.tree.get_children()]

    def clear_list(self):
        self.tree.delete(*self.tree.get_children())
        self.update_list_info()
        self.status_var.set(self.tr('status_cleared'))
        self.core.logger.info("Список очищен")

    def add_files(self):
        filenames = filedialog.askopenfilenames(title=self.tr('msg_select_files'))
        if not filenames:
            return
        current = self.get_files_from_tree()
        added = 0
        for f in filenames:
            norm = self.normalize_path(f)
            if norm not in current:
                self.add_item(norm)
                added += 1
        if added:
            self.status_var.set(self.tr('status_added', count=added))
            self.core.logger.info(f"Добавлено {added} файлов")
            self.update_list_info()

    def add_folder(self):
        folder = filedialog.askdirectory(title=self.tr('msg_select_folder'))
        if not folder:
            return
        folder = self.normalize_path(folder)
        try:
            lock_files = self.core.scan_folder_for_locks(folder)
        except Exception as e:
            messagebox.showerror(self.tr('msg_error_title'), f"Ошибка сканирования:\n{e}")
            return
        if not lock_files:
            messagebox.showinfo(self.tr('msg_info_title'), self.tr('msg_no_locks'))
            return
        current = self.get_files_from_tree()
        added = 0
        for f in lock_files:
            if f not in current:
                self.add_item(f)
                added += 1
        if added:
            self.status_var.set(self.tr('status_found_locks', count=added))
            self.core.logger.info(f"Добавлено {added} блокировок из {folder}")
            self.update_list_info()

    def normalize_path(self, path):
        if not path:
            return path
        path = path.replace('/', '\\').strip()
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
        return path

    # ---------- Управление логом и статусной строкой ----------
    def toggle_log(self):
        self.log_visible = not self.log_visible
        if self.log_visible:
            self.log_frame.pack(fill='x', pady=(0, 5))
        else:
            self.log_frame.pack_forget()
        self.view_log_var.set(self.log_visible)
        self.save_settings()

    def toggle_status(self):
        self.status_visible = not self.status_visible
        if self.status_visible:
            self.status_frame.pack(fill='x')
        else:
            self.status_frame.pack_forget()
        self.view_status_var.set(self.status_visible)
        self.save_settings()

    def append_log(self, message):
        self.core.logger.info(message)
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()

    # ---------- Основная операция ----------
    def unlock_all(self):
        if self.processing:
            return
        file_paths = self.get_files_from_tree()
        if not file_paths:
            messagebox.showwarning(self.tr('msg_warning_title'), self.tr('msg_no_files'))
            return
        if not messagebox.askyesno(self.tr('msg_warning_title'),
                                   self.tr('msg_confirm_unlock', count=len(file_paths))):
            return

        self.processing = True
        self.cancel_requested = False

        # Меняем кнопку
        self.btn_unlock.grid_remove()
        self.btn_cancel.grid()

        self.progress.pack(side='right', padx=5)
        self.progress['value'] = 0
        self.progress['maximum'] = len(file_paths)

        for item in self.tree.get_children():
            self.update_item_status(item, 'pending')

        try:
            self.status_var.set(self.tr('status_processing'))
            self.root.update()

            self.append_log("Завершение офисных процессов...")
            self.core.kill_office_processes()

            total = len(file_paths)
            success_count = 0
            error_list = []

            for idx, path in enumerate(file_paths, 1):
                if self.cancel_requested:
                    self.append_log("Операция отменена")
                    break

                self.progress['value'] = idx - 1
                self.status_var.set(self.tr('status_processing_file',
                                            idx=idx, total=total, filename=os.path.basename(path)))
                self.root.update()

                item = None
                for it in self.tree.get_children():
                    if self.tree.item(it, 'text') == path:
                        item = it
                        break
                if not item:
                    continue

                self.core.logger.info(f"Обработка: {path}")
                try:
                    base = os.path.basename(path)
                    is_lock = base.startswith('~$') or base.startswith('.~lock.')
                    if is_lock:
                        succ, msg = self.core.force_delete_file(path)
                        if succ:
                            success_count += 1
                            self.update_item_status(item, 'deleted')
                        else:
                            error_list.append((path, msg))
                            self.update_item_status(item, 'error')
                    else:
                        locks = self.core.find_lock_files(path)
                        if not locks:
                            self.update_item_status(item, 'skipped')
                            continue
                        for lock in locks:
                            succ, msg = self.core.force_delete_file(lock)
                            if succ:
                                success_count += 1
                                self.append_log(f"Удалён: {lock}")
                            else:
                                error_list.append((lock, msg))
                            self.status_var.set(self.tr('status_deleting', count=success_count))
                            self.root.update()
                            time.sleep(0.05)
                        if any(f == path for f, _ in error_list):
                            self.update_item_status(item, 'error')
                        else:
                            self.update_item_status(item, 'deleted')
                except Exception as e:
                    self.core.logger.error(f"Критическая ошибка при обработке {path}: {e}")
                    error_list.append((path, str(e)))
                    self.update_item_status(item, 'error')

            self.progress['value'] = total

            if error_list:
                err_text = "\n".join([f"• {os.path.basename(f)}: {e}" for f, e in error_list[:10]])
                if len(error_list) > 10:
                    err_text += f"\n... и ещё {len(error_list)-10}"
                messagebox.showerror(self.tr('msg_error_title'),
                                     self.tr('msg_unlock_partial', errors=err_text))
                self.status_var.set(self.tr('status_partial', success=success_count, errors=len(error_list)))
            else:
                messagebox.showinfo(self.tr('msg_info_title'),
                                    self.tr('msg_unlock_done', count=total))
                self.status_var.set(self.tr('status_done'))

        except Exception as e:
            self.core.logger.error(f"Неожиданная ошибка: {e}")
            messagebox.showerror(self.tr('msg_error_title'),
                                 self.tr('msg_critical_error', error=e))
        finally:
            self.processing = False
            self.btn_cancel.grid_remove()
            self.btn_unlock.grid()
            self.progress.pack_forget()

    def cancel_unlock(self):
        if self.processing:
            self.cancel_requested = True
            self.append_log("Отмена запрошена...")
            self.btn_cancel.config(state='disabled')

    # ---------- Горячие клавиши ----------
    def setup_hotkeys(self):
        self.root.bind('<Control-o>', lambda e: self.add_files())
        self.root.bind('<Control-f>', lambda e: self.add_folder())
        self.root.bind('<Control-u>', lambda e: self.unlock_all())
        self.root.bind('<Escape>', lambda e: self.on_closing())

    def show_about(self):
        messagebox.showinfo(self.tr('menu_help_about'), self.tr('about_text'))

    def on_closing(self):
        self.core.logger.info("Приложение закрыто")
        self.root.destroy()