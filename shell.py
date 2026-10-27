import shlex
import getpass
import socket


class Shell:
    def __init__(self, vfs_instance, output_callback, debug=False):
        self.vfs = vfs_instance
        self.write = output_callback  # Функция для вывода текста (в GUI)
        self.debug = debug
        self.running = True
        self.username = getpass.getuser()
        try:
            self.hostname = socket.gethostname()
        except:
            self.hostname = "localhost"

    def get_prompt(self):
        return f"{self.username}@{self.hostname}:{self.vfs.get_prompt_path()}$ "

    def execute_command(self, cmd_line):
        try:
            args = shlex.split(cmd_line)
        except ValueError as e:
            self.write(f"Ошибка парсинга: {e}\n", "red")
            return

        if not args: return

        cmd, cmd_args = args[0], args[1:]

        try:
            if cmd == "exit":
                self.running = False
                self.write("Завершение работы...\n", "yellow")
            elif cmd == "ls":
                self.cmd_ls(cmd_args)
            elif cmd == "cd":
                self.cmd_cd(cmd_args)
            elif cmd == "cat":
                self.cmd_cat(cmd_args)
            elif cmd == "pwd":
                self.write(self.vfs.get_prompt_path() + "\n")
            elif cmd == "mkdir":
                if not cmd_args: raise ValueError("mkdir: пропущен операнд")
                self.vfs.mkdir(cmd_args[0])
            elif cmd == "touch":
                if not cmd_args: raise ValueError("touch: пропущен операнд")
                self.vfs.touch(cmd_args[0])
            else:
                self.write(f"{cmd}: команда не найдена\n", "red")
        except Exception as e:
            self.write(f"Ошибка: {e}\n", "red")

    def cmd_ls(self, args):
        target = args[0] if args else None
        items = self.vfs.list_dir(target)
        for item in items:
            suffix = "/" if item.is_dir else ""
            color = "blue" if item.is_dir else "white"
            self.write(f"{item.name}{suffix}\n", color)

    def cmd_cd(self, args):
        if len(args) > 1: raise ValueError("cd: слишком много аргументов")
        target = args[0] if args else "/"
        self.vfs.change_dir(target)

    def cmd_cat(self, args):
        if not args: raise ValueError("cat: пропущен операнд")
        for filepath in args:
            content = self.vfs.read_file(filepath)
            self.write(content + ("" if content.endswith("\n") else "\n"))

    def run_script(self, script_path):
        import os
        if not os.path.exists(script_path):
            self.write(f"Скрипт не найден: {script_path}\n", "red")
            return
        self.write(f"--- Выполнение скрипта: {script_path} ---\n", "yellow")
        with open(script_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"): continue
                self.write(f"{self.get_prompt()}{line}\n", "green")
                self.execute_command(line)
                if not self.running: break
        self.write("--- Скрипт завершен ---\n", "yellow")
