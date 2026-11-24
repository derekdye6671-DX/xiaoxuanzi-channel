# 01 · XlsxWriter：用 Python 生成带图表的 Excel

- 官方包名：`XlsxWriter`（安装时大小写都行，装好后叫 `xlsxwriter`）
- GitHub：<https://github.com/jmcnamara/XlsxWriter>
- 试用版本：3.3.4（2026-11-24 试用）
- 试用脚本：`scripts/try_xlsxwriter.py`
- 生成文件：`reports/周报-xlsxwriter版.xlsx`

## 解决什么问题

我想用脚本把频道数据（`practice/sample-data.csv`）自动做成 Excel 周报，最好连图表一起画好，不用每周手动拖表格、插图。

之前用 openpyxl 写的 `scripts/make_report.py` 能生成表和折线图，但生成的图打开后看不到坐标轴刻度。XlsxWriter 是另一个专门"写" Excel 的 Python 库，图表功能做得比较全，所以拿它来试一下：同样的数据，能不能做出一张有标题、有横纵轴名称、纵轴带刻度的折线图。

## 5 项检查结果

装之前先审核，不是看别人说安全就装。具体做法：先从 PyPI 查它的登记信息，再把安装包下载到临时文件夹解压，搜源码里有没有可疑的代码，没问题才装。

| # | 检查项 | 怎么查的 | 结果 |
|---|---|---|---|
| 1 | 包名对不对 | 查 PyPI 登记的主页、仓库、问题反馈地址 | ✅ 全部指向 `github.com/jmcnamara/XlsxWriter`，是正主，不是名字相近的假包 |
| 2 | 会不会顺带装别的东西 | 看 PyPI 上的依赖列表 | ✅ 没有任何依赖，只装它自己 |
| 3 | 会不会联网 | 在源码里搜 `socket`、`urllib`、`http`、`requests`、`ssl` | ✅ 一个都没有，不会联网 |
| 4 | 会不会偷偷运行别的命令 | 在源码里搜 `subprocess`、`os.system`、`eval`、`exec` | ✅ 一个都没有 |
| 5 | 会读写哪些文件 | 在源码里搜 `open(`、`tempfile`、`os.remove` | ✅ 只读你主动交给它的文件（图片、宏、主题）；只写你指定的输出 `.xlsx`。默认保存时会在系统临时文件夹放中间文件、用完删掉；脚本里加了 `in_memory` 选项，连临时文件都不产生 |

结论：可以装。

## 怎么装

1. 下载安装包到临时文件夹（只下载，不安装），解压后按上面 5 项检查：

   ```powershell
   .venv\Scripts\python.exe -m pip download XlsxWriter==3.3.4 --no-deps -d <临时文件夹>
   ```

2. 检查没问题，就装**刚才检查过的那个文件**，保证装的和查的是同一份：

   ```powershell
   .venv\Scripts\python.exe -m pip install --no-deps <临时文件夹>\xlsxwriter-3.3.4-py3-none-any.whl
   ```

3. 确认装好了：

   ```powershell
   .venv\Scripts\python.exe -m pip list
   ```

   能看到 `xlsxwriter 3.3.4` 就行。

4. 运行试用脚本：

   ```powershell
   .venv\Scripts\python.exe scripts\try_xlsxwriter.py
   ```

## 前后对比

| | 之前：openpyxl 版（`make_report.py`） | 之后：XlsxWriter 版（`try_xlsxwriter.py`） |
|---|---|---|
| 生成文件 | `reports/周报.xlsx` | `reports/周报-xlsxwriter版.xlsx` |
| 工作表 | 「每周汇总」+「明细」两张 | 只有「每周汇总」一张 |
| 汇总数字 | 用 SUMIFS 公式从明细表算，改明细会自动变 | Python 先算好再写进去，是死数字 |
| 折线图标题、轴名称 | 有 | 有 |
| 坐标轴刻度 | 看不到（文件里两条坐标轴都被标成"隐藏"） | 看得到，纵轴还有网格线 |
| 横轴 | — | 显示 第1周～第4周 |
| 代码行数 | 113 行 | 76 行 |

这次的汇总结果：

| 周次 | 播放量合计 | 点赞合计 | 涨粉合计 |
|---|---|---|---|
| 第1周 | 42470 | 1883 | 248 |
| 第2周 | 57160 | 2586 | 337 |
| 第3周 | 46250 | 2278 | 305 |
| 第4周 | 63080 | 2806 | 363 |

另外发现：现在 CSV 里日期是 `2026/10/26` 这种斜杠写法，`make_report.py` 只认 `2026-10-26`，直接跑会报错。新脚本按斜杠写法读，没有这个问题。

## 局限

- **只能新建，不能读、不能改。** XlsxWriter 只会从零写一个新的 Excel 文件。想打开已有的 `.xlsx` 读数据、或者在原文件上改几个格子，它做不到，还得用 openpyxl。
- **写公式不会帮你算结果。** 可以往格子里写公式，但它不会算出数值存进去，要用 Excel 打开时才算。别的程序直接读这个文件，可能读到 0 或空。所以这次汇总表用的是 Python 算好的数字，代价是不会跟着明细自动更新。
- **每次都是整份重写。** 同名文件会被直接覆盖，没有"追加一行"这种操作。
- **这次只试了折线图。** 柱状图、饼图、条件格式等功能没试。

## 结论

如果需求是"每周从数据从头生成一份新报表、图表要好看"，XlsxWriter 比 openpyxl 更合适：图表一次就出对了，坐标轴刻度正常显示。（代码行数少，主要是因为这版没做明细表，不算它的优势。）

如果要读已有的 Excel、或者在原文件上修改，还是用 openpyxl。两个可以搭配：openpyxl 负责读，XlsxWriter 负责写。
