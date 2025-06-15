import os
import shutil
from pathlib import Path
import platform
import subprocess

def open_file_cross_platform(file_path: Path):
    """跨平台打开一个文件"""
    file_path = str(file_path)
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.run(["open", file_path])
        elif system == "Windows":
            os.startfile(file_path)
        else:
            print(f"当前平台（{system}）不支持自动打开文件: {file_path}")
    except Exception as e:
        print(f"无法打开文件: {e}")

def copy_file_to_all_subdirs(src_file_path: str | Path, target_root_dir: str | Path) -> int:
    """
    将源文件复制到目标目录下的所有子目录中。
    如果目标子目录中已有同名文件，会被直接覆盖。
    复制完成后，打开每个被复制后的文件。
    返回成功复制的子目录数量。
    """
    src_path = Path(src_file_path).resolve()
    target_root = Path(target_root_dir).resolve()

    if not src_path.is_file():
        raise FileNotFoundError(f"源文件不存在: {src_path}")
    if not target_root.is_dir():
        raise NotADirectoryError(f"目标目录不存在: {target_root}")

    subdirs = [d for d in target_root.iterdir() if d.is_dir()]
    copied_count = 0

    for subdir in subdirs:
        dst_file = subdir / src_path.name
        try:
            shutil.copy2(src_path, dst_file)  # ✅ 拷贝并覆盖
            print(f"✅ 已复制到: {dst_file}")

            # ✅ 拷贝后立刻打开该目标文件
            open_file_cross_platform(dst_file)

            copied_count += 1
        except Exception as e:
            print(f"❌ 复制失败: {dst_file}，原因: {e}")

    return copied_count

if __name__ == "__main__":
    src_file = r"C:\Users\chenbin\Desktop\password.txt"
    target_dir = r"C:\Users\chenbin\Desktop\target_folder"

    try:
        count = copy_file_to_all_subdirs(src_file, target_dir)
        print(f"\n🎉 共成功复制并打开了 {count} 个子目录中的文件。")
    except Exception as e:
        print(f"发生错误: {e}")
