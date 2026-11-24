"""读取 practice/sample-data.csv，生成 reports/周报.xlsx。"""

import csv
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.styles import Font, PatternFill

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "practice" / "sample-data.csv"
OUT_PATH = ROOT / "reports" / "周报.xlsx"

GREEN = PatternFill(fill_type="solid", start_color="C6EFCE", end_color="C6EFCE")
BOLD = Font(bold=True)


# 第 1 步：读取 CSV
def read_rows():
    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["日期"] = date.fromisoformat(r["日期"])
        for col in ("播放量", "点赞", "涨粉"):
            r[col] = int(r[col])
    return rows


# 第 2 步：按日期算出每行属于第几周（以最早日期所在的那周周一为第 1 周）
def add_week(rows):
    first_monday = min(r["日期"] for r in rows)
    first_monday = date.fromordinal(first_monday.toordinal() - first_monday.weekday())
    for r in rows:
        r["周次"] = f"第{(r['日期'] - first_monday).days // 7 + 1}周"
    return sorted({r["周次"] for r in rows}, key=lambda w: int(w[1:-1]))


# 第 3 步：写「明细」表，播放量前 3 名整行标绿
def write_detail(ws, rows):
    headers = ["日期", "周次", "视频标题", "平台", "播放量", "点赞", "涨粉"]
    ws.append(headers)
    for c in ws[1]:
        c.font = BOLD

    top3 = sorted(rows, key=lambda r: r["播放量"], reverse=True)[:3]
    for r in rows:
        ws.append([r[h] for h in headers])
        if r in top3:
            for c in ws[ws.max_row]:
                c.fill = GREEN
        ws.cell(ws.max_row, 1).number_format = "yyyy-mm-dd"

    for col, width in zip("ABCDEFG", (12, 8, 30, 8, 10, 8, 8)):
        ws.column_dimensions[col].width = width


# 第 4 步：写「每周汇总」表，合计全部用 SUMIFS 公式从明细表算
def write_summary(ws, weeks, n_rows):
    ws.append(["周次", "播放量合计", "点赞合计", "涨粉合计"])
    for c in ws[1]:
        c.font = BOLD

    last = n_rows + 1  # 明细表最后一行（第 1 行是表头）
    week_range = f"明细!$B$2:$B${last}"
    for i, week in enumerate(weeks, start=2):
        ws.append([
            week,
            f"=SUMIFS(明细!$E$2:$E${last},{week_range},A{i})",
            f"=SUMIFS(明细!$F$2:$F${last},{week_range},A{i})",
            f"=SUMIFS(明细!$G$2:$G${last},{week_range},A{i})",
        ])

    for col in "ABCD":
        ws.column_dimensions[col].width = 12
    return len(weeks) + 1  # 汇总表最后一行


# 第 5 步：在汇总表旁边加「每周播放量」折线图
def add_chart(ws, last_row):
    chart = LineChart()
    chart.title = "每周播放量"
    chart.y_axis.title = "播放量"
    chart.x_axis.title = "周次"
    chart.legend = None
    data = Reference(ws, min_col=2, min_row=1, max_row=last_row)
    cats = Reference(ws, min_col=1, min_row=2, max_row=last_row)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    ws.add_chart(chart, "F2")


# 第 6 步：保存到 reports/周报.xlsx
def main():
    rows = read_rows()
    weeks = add_week(rows)

    wb = Workbook()
    summary = wb.active
    summary.title = "每周汇总"
    detail = wb.create_sheet("明细")

    write_detail(detail, rows)
    last_row = write_summary(summary, weeks, len(rows))
    add_chart(summary, last_row)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT_PATH)
    print(f"已生成：{OUT_PATH}")


if __name__ == "__main__":
    main()
