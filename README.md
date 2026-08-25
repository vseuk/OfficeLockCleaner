[Русская версия](README.ru.md)

# OfficeLockCleaner

Utility for forced removal of "phantom" lock files left by office suites (Microsoft Office, R7-Office, LibreOffice, OpenOffice, etc.) after an abnormal termination (crash, freeze, power outage). Works with local and network folders, no installation required.

## Problem

Any modern office suite creates a temporary lock file when a document is opened to prevent simultaneous editing. Typically these are:

- `~$filename.extension`
- `.~lock.filename.extension#`

After an abnormal process termination (e.g., hang), these files remain. On the next attempt to open the document, the office suite reports: *"The file is already open by another user"* or *"Access denied"*. Manual deletion through File Explorer often fails due to the file being locked or insufficient permissions.

## What the program does

- Terminates all running office processes (by masks: `r7*`, `winword*`, `excel*`, `powerpnt*`, `soffice*`, etc.).
- Finds lock files corresponding to the specified file(s), including truncated name variants.
- If the lock file itself (e.g., `~$Report.xlsx`) is added to the list, it deletes it directly.
- Uses several removal methods: `os.remove`, PowerShell, renaming, `cmd del` – retrying until the file is deleted.
- All operations run silently – no command prompt windows appear.

## Usage

1. Run `OfficeLockCleaner.exe` (or `python main.py`).
2. Add files to the list:
   - **Menu File → Add Files...** – select one or more files (originals or lock files themselves).
   - **Menu File → Add Folder...** – the program will scan the selected folder and all subfolders, find all files starting with `~$` or `.~lock.`, and add them to the list.
   - **Drag and drop** files or folders directly into the window (requires `tkinterdnd2`).
   - You can also **edit the list manually** – paste paths, remove lines, modify entries.
3. Click the **Unlock** button (or `Ctrl+U`).
4. The program will terminate office processes, find and delete all associated lock files.
5. Upon completion, a report shows which files were successfully removed and which failed.

**Keyboard shortcuts:**
- `Ctrl+O` – add files
- `Ctrl+F` – add folder
- `Ctrl+U` – unlock
- `Esc` – exit

## Building from source

Requirements: Python 3.7+, tkinter (included in standard Python distribution).

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name OfficeLockCleaner --add-data "lang;lang" main.py