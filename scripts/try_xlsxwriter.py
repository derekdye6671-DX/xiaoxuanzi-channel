"""试用 XlsxWriter：读取 practice/sample-data.csv，生成 reports/周报-xlsxwriter版.xlsx。

只有一张「每周汇总」表 + 每周播放量折线图。
"""

import csv
from datetime import date, datetime
from pathlib import Path

import xlsxwriter

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "practice" / "sample-data.csv"
OUT_PATH = ROOT / "reports" / "周报-xlsxwriter版.xlsx"


# 第 1 步：读取 CSV（日期格式是 2026/10/26 这种斜杠写法）
def read_rows():
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["日期"] = datetime.strptime(r["日期"], "%Y/%m/%d").date()
        for col in ("播放量", "点赞", "涨粉"):
            r[col] = int(r[col])
    return rows


# 第 2 步：按周汇总（以最早日期所在那周的周一为第 1 周）
def summarize(rows):
    first = min(r["日期"] for r in rows)
    first_monday = date.fromordinal(first.toordinal() - first.weekday())
    totals = {}
    for r in rows:
        n = (r["日期"] - first_monday).days // 7 + 1
        t = totals.setdefault(n, [0, 0, 0])
        t[0] += r["播放量"]
        t[1] += r["点赞"]
        t[2] += r["涨粉"]
    return [(f"第{n}周", *totals[n]) for n in sorted(totals)]


# 第 3 步：写「每周汇总」表，再在旁边插入折线图
def main():
    summary = summarize(read_rows())

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # in_memory=True：整个文件在内存里拼好再写出，不在系统临时目录留中间文件
    wb = xlsxwriter.Workbook(str(OUT_PATH), {"in_memory": True})
    ws = wb.add_worksheet("每周汇总")
    bold = wb.add_format({"bold": True})

    ws.write_row(0, 0, ["周次", "播放量合计", "点赞合计", "涨粉合计"], bold)
    for i, row in enumerate(summary, start=1):
        ws.write_row(i, 0, row)
    ws.set_column(0, 3, 12)

    last = len(summary)  # 最后一行数据的行号（从 0 数）
    chart = wb.add_chart({"type": "line"})
    chart.add_series({
        "name": "播放量",
        "categories": ["每周汇总", 1, 0, last, 0],  # A 列：第1周～第4周
        "values": ["每周汇总", 1, 1, last, 1],      # B 列：播放量合计
        "marker": {"type": "circle"},
    })
    chart.set_title({"name": "每周播放量"})
    chart.set_x_axis({"name": "周次"})
    chart.set_y_axis({"name": "播放量", "major_gridlines": {"visible": True}})
    chart.set_legend({"none": True})
    ws.insert_chart("F2", chart)

    wb.close()
    print(f"已生成：{OUT_PATH}")


if __name__ == "__main__":
    main()
