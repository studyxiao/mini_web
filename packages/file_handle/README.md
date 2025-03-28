# 比较 `os.scandir` 与 `os.listdir`

- `os.scandir` 是一个迭代器，返回 `os.DirEntry` 对象，包含文件的元数据
  - name: 文件名，对应 `os.listdir` 的返回值
  - path: 文件路径，对应 `os.path.join(scandir_path, entry.name)` 的返回值
  - is_file: 是否是文件，缓存在 `os.DirEntry` 对象中，不需要系统调用
  - is_dir: 是否是目录，缓存在 `os.DirEntry` 对象中
  - is_symlink: 是否是符号链接，缓存在 `os.DirEntry` 对象中
  - stat: 文件的元数据，调用 `stat()` 系统调用获取，会缓存
  - inode: 文件的 inode 号，会缓存
- `os.listdir` 是一个列表，返回文件名的字符串
- 影响 `os.walk` 速度

> Windows 和 Linux 下部分特性可能不同

## 主要优化形式

- 系统调用优化
  - os.listdir: 1 次系统调用，仅返回文件名。需要更多信息时，需要使用 os.stat 等触发系统调用
  - os.scandir: 1 次系统调用，会返回更多信息
- 内存优化
  - os.listdir: 返回一个列表，内存占用大
  - os.scandir: 返回一个迭代器，内存占用小
- 缓存优化
  - os.scandir: 缓存文件的元数据，避免多次系统调用

## 推荐使用方式

- 仅需要文件名时，两者皆可。
- 需要文件的元数据时，推荐使用 `os.scandir`，尤其在有大量文件时
  - 如文件大小、修改时间、创建时间等、文件类型、是否是目录、是否是符号链接等

## 学习

- [os.scandir](https://docs.python.org/3/library/os.html#os.scandir)
- [PEP 471](https://peps.python.org/pep-0471/)
