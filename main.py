import argparse
import sys
import tkinter as tk
from vfs import VFS
from shell import Shell
from gui import ConsoleGUI

def main():
    parser = argparse.ArgumentParser(description="Standalone GUI Shell Emulator")
    parser.add_argument("--vfs", type=str, help="Путь к CSV файлу VFS", default=None)
    parser.add_argument("--script", type=str, help="Путь к стартовому скрипту", default=None)

    args = parser.parse_args()

    # 1. Инициализация файловой системы
    vfs = VFS()
    if args.vfs:
        try:
            vfs.load_from_csv(args.vfs)
        except Exception as e:
            print(f"Критическая ошибка загрузки VFS: {e}")
            sys.exit(1)
    else:
        vfs.mkdir("/home")
        vfs.mkdir("/home/user")

    # 2. Создание окна консоли(Tkinter)
    root = tk.Tk()

    # Заглушка для вывода (сразу заменится на GUI-функцию внутри ConsoleGUI)
    shell = Shell(vfs_instance=vfs, output_callback=print)

    # Инициализация GUI
    app = ConsoleGUI(root, shell)

    # 3. Если передан скрипт — выполняем его внутри GUI
    if args.script:
        app.print_to_console(f"Автозапуск: {args.script}\n", "yellow")
        shell.run_script(args.script)
        app.update_prompt()

    # Запуск главного цикла окна
    root.mainloop()


if __name__ == "__main__":
    main()
