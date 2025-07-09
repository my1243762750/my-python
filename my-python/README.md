# Python 前端转型入门实战指南

## 1. 环境准备

### 1.1 安装 Python
- 推荐使用 [Python 官网](https://www.python.org/downloads/) 下载最新版 Python（建议 3.10 及以上）。
- 安装时勾选 "Add Python to PATH"。
- macOS 用户可用 Homebrew 安装：
  ```bash
  brew install python
  ```

### 1.2 推荐 IDE
- [PyCharm Community](https://www.jetbrains.com/pycharm/download/)
- [VSCode](https://code.visualstudio.com/) + Python 插件

### 1.3 验证安装
安装完成后，在终端验证：
```bash
# macOS 用户（推荐）
python3 --version
pip3 --version

# 或者设置别名后使用
python --version
pip --version
```

### 1.4 安装依赖包
- 推荐使用 pip 管理依赖。
- 本实战例子会用到：requests、beautifulsoup4、openpyxl。
- 安装命令：
  ```bash
  pip install requests beautifulsoup4 openpyxl
  ```
- 验证安装：
  ```bash
  python -c "import requests, bs4, openpyxl; print('所有依赖包安装成功！')"
  ```

## 2. 推荐学习资料
- [廖雪峰的 Python 教程](https://www.liaoxuefeng.com/wiki/1016959663602400)
- [Python官方文档](https://docs.python.org/zh-cn/3/)
- [菜鸟教程 Python3](https://www.runoob.com/python3/python3-tutorial.html)

## 3. 实战项目：爬取豆瓣电影 Top 250 并保存为 Excel

### 3.1 项目目标
- 爬取豆瓣电影 Top 250 的电影名称、评分、链接。
- 保存为 Excel 文件。

### 3.2 快速启动（推荐）

#### 方法一：一键启动（最简单）
```bash
# 直接运行启动脚本
./start.sh
```

#### 方法二：使用自动化脚本
```bash
# 1. 运行初始化脚本
python3 setup.py

# 2. 激活虚拟环境
# Windows:
# venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 运行爬虫
python3 douban_top250.py
```

#### 方法二：手动设置
```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
# Windows:
# venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 安装依赖
pip3 install -r requirements.txt

# 4. 验证安装
python3 -c "import requests, bs4, openpyxl; print('所有依赖包安装成功！')"

# 5. 运行爬虫
python3 douban_top250.py
```

#### 步骤 3：编写爬虫代码
- 用 requests 获取网页内容。
- 用 BeautifulSoup 解析 HTML。
- 提取电影信息。
- 用 openpyxl 写入 Excel。

#### 步骤 4：运行脚本
- 在终端运行：
  ```bash
  python douban_top250.py
  ```
- 生成 `douban_top250.xlsx` 文件。

### 3.3 项目文件说明

- `setup.py` - 自动化初始化脚本，一键设置项目环境
- `requirements.txt` - 项目依赖包列表
- `douban_top250.py` - 完整的爬虫代码，包含错误处理和进度显示
- `README.md` - 项目说明文档

### 3.4 运行结果

运行成功后，你将看到：
1. 控制台显示爬取进度
2. 生成 `douban_top250.xlsx` 文件
3. Excel 文件包含：排名、电影名称、评分、链接、导演/年份信息

### 3.5 代码特点

- ✅ 完整的错误处理
- ✅ 进度显示
- ✅ 请求延迟（避免被封）
- ✅ 详细的注释说明
- ✅ 符合 Python 编码规范

---

## 4. 进阶建议
- 学习 Python 基础语法后，尝试用 Flask/Django 写 Web 后端。
- 结合前端技能，做全栈小项目。

---

如有问题，欢迎随时提问！ 