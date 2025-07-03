from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from copy_logic import copy_file_to_all_subdirs

class CopyToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件批量复制工具")
        self.root.geometry("550x280")

        self.src_file: Path | None = None
        self.target_dir: Path | None = None

        # 拖拽提示
        drag_tip = tk.Label(root, text="你也可以将文件/文件夹直接拖拽到下面", fg="gray")
        drag_tip.pack(pady=5)

        # 拖拽源文件框
        self.src_entry = tk.Entry(root, width=70)
        self.src_entry.pack(pady=5)
        self.src_entry.insert(0, "拖入源文件 或 点击按钮选择")
        self.src_entry.drop_target_register(DND_FILES)
        self.src_entry.dnd_bind('<<Drop>>', self.handle_src_drop)

        self.src_btn = tk.Button(root, text="选择源文件", command=self.select_source_file)
        self.src_btn.pack(pady=5)

        # 拖拽目标目录框
        self.target_entry = tk.Entry(root, width=70)
        self.target_entry.pack(pady=5)
        self.target_entry.insert(0, "拖入目标文件夹 或 点击按钮选择")
        self.target_entry.drop_target_register(DND_FILES)
        self.target_entry.dnd_bind('<<Drop>>', self.handle_target_drop)

        self.target_btn = tk.Button(root, text="选择目标目录", command=self.select_target_dir)
        self.target_btn.pack(pady=5)

        # 执行复制按钮
        self.copy_btn = tk.Button(root, text="复制并打开", command=self.do_copy, width=20, bg="green", fg="white")
        self.copy_btn.pack(pady=15)

        self.copy_only_btn = tk.Button(root, text="仅复制", command=self.do_copy_only, width=20, bg="gray", fg="white")
        self.copy_only_btn.pack(pady=5)

    def handle_src_drop(self, event):
        path = Path(event.data.strip("{}"))  # 处理空格或带大括号的路径
        if path.is_file():
            self.src_file = path
            self.src_entry.delete(0, tk.END)
            self.src_entry.insert(0, str(path))
        else:
            messagebox.showerror("错误", "请拖入一个文件作为源文件")

    def handle_target_drop(self, event):
        path = Path(event.data.strip("{}"))
        if path.is_dir():
            self.target_dir = path
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, str(path))
        else:
            messagebox.showerror("错误", "请拖入一个文件夹作为目标目录")

    def select_source_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.src_file = Path(file_path)
            self.src_entry.delete(0, tk.END)
            self.src_entry.insert(0, str(self.src_file))

    def select_target_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.target_dir = Path(dir_path)
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, str(self.target_dir))

    def do_copy(self):
        try:
            if not self.src_file or not self.src_file.exists():
                raise FileNotFoundError("请选择一个有效的源文件")
            if not self.target_dir or not self.target_dir.exists():
                raise NotADirectoryError("请选择一个有效的目标目录")

            count = copy_file_to_all_subdirs(self.src_file, self.target_dir)
            messagebox.showinfo("复制完成", f"已将文件复制到 {count} 个子目录中（如有同名文件已覆盖）。")

        except Exception as e:
            messagebox.showerror("错误", str(e))

    def do_copy_only(self):
        try:
            if not self.src_file or not self.src_file.exists():
                raise FileNotFoundError("请选择一个有效的源文件")
            if not self.target_dir or not self.target_dir.exists():
                raise NotADirectoryError("请选择一个有效的目标目录")

            count = copy_file_to_all_subdirs(self.src_file, self.target_dir, open_after_copy=False)
            messagebox.showinfo("复制完成", f"已将文件复制到 {count} 个子目录中（未打开文件）。")

        except Exception as e:
            messagebox.showerror("错误", str(e))


if __name__ == "__main__":
    root = TkinterDnD.Tk()  # 用 tkinterdnd2 启动窗口
    app = CopyToolApp(root)
    root.mainloop()
