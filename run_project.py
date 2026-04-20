"""
run_project.py
==============
Reads SAP O2C data and generates:
  - charts/chart1_monthly_revenue.png
  - charts/chart2_top_customers.png
  - charts/chart3_order_status.png
  - charts/chart4_regional_revenue.png
  - charts/chart5_product_revenue.png
  - charts/chart6_quarterly.png
  - charts/dashboard_overview.png

Author : Priyanshu Rajhans | Roll: 23051769
Program: SAP Data Analytics & Engineering — KIIT, Bhubaneswar
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
import os

os.makedirs("charts", exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────────────
so = pd.read_csv("data/sap_sales_orders.csv")
inv = pd.read_csv("data/sap_inventory.csv")

so["SO_Date"]  = pd.to_datetime(so["SO_Date"],  dayfirst=True)
so["Month"]    = so["SO_Date"].dt.to_period("M")
so["Quarter"]  = so["SO_Date"].dt.to_period("Q")
so["MonthStr"] = so["SO_Date"].dt.strftime("%b %Y")

# ── Palette ───────────────────────────────────────────────────────────────────
BLUE       = "#1F4E79"
MED_BLUE   = "#2E75B6"
LT_BLUE    = "#9DC3E6"
TEAL       = "#00B4D8"
ORANGE     = "#E05C00"
GREEN      = "#2E7D32"
PURPLE     = "#6A1B9A"
GOLD       = "#F9A825"
COLORS6    = [BLUE, MED_BLUE, TEAL, GREEN, PURPLE, GOLD]
PIE_COLORS = ["#1F4E79","#2E75B6","#9DC3E6","#4CAF50","#FFC107","#F44336","#9C27B0","#00BCD4"]

plt.rcParams.update({
    "font.family":     "DejaVu Sans",
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.grid":          True,
    "grid.alpha":         0.25,
    "grid.linestyle":     "--",
})

def fmt_cr(val):
    """Format value in Crores INR"""
    return f"₹{val/1e7:.2f}Cr"

def save(name):
    plt.tight_layout()
    plt.savefig(f"charts/{name}", dpi=150, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close()
    print(f"  [OK] {name}")

# ═════════════════════════════════════════════════════════════════════════════
# CHART 1 — Monthly Revenue Trend
# ═════════════════════════════════════════════════════════════════════════════
monthly = (so.groupby("Month")["Total_Invoice_Value"]
             .sum()
             .reset_index()
             .sort_values("Month"))
monthly["Label"] = monthly["Month"].dt.strftime("%b %y")
monthly["RevCr"] = monthly["Total_Invoice_Value"] / 1e7

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(range(len(monthly)), monthly["RevCr"], alpha=0.18, color=MED_BLUE)
ax.plot(range(len(monthly)), monthly["RevCr"], marker="o", color=MED_BLUE,
        linewidth=2.5, markersize=7, markerfacecolor=BLUE, markeredgecolor="white", markeredgewidth=1.5)

for i, (_, row) in enumerate(monthly.iterrows()):
    ax.annotate(f"₹{row['RevCr']:.1f}Cr", (i, row["RevCr"]),
                textcoords="offset points", xytext=(0, 10),
                ha="center", fontsize=7.5, color=BLUE, fontweight="bold")

ax.set_xticks(range(len(monthly)))
ax.set_xticklabels(monthly["Label"], rotation=45, ha="right", fontsize=9)
ax.set_ylabel("Revenue (₹ Crores)", fontsize=11)
ax.set_title("Monthly Revenue Trend — Reliance Retail Ltd.\nFY 2024-25 | SAP O2C Analysis",
             fontsize=13, fontweight="bold", color=BLUE, pad=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₹{x:.1f}Cr"))
ax.set_facecolor("#F8FBFF")
fig.patch.set_facecolor("white")

# Add trend line
z = np.polyfit(range(len(monthly)), monthly["RevCr"], 1)
p = np.poly1d(z)
ax.plot(range(len(monthly)), p(range(len(monthly))), "--", color=ORANGE,
        alpha=0.7, linewidth=1.5, label="Trend")
ax.legend(fontsize=9)
save("chart1_monthly_revenue.png")

# ═════════════════════════════════════════════════════════════════════════════
# CHART 2 — Top 10 Customers by Revenue
# ═════════════════════════════════════════════════════════════════════════════
top_cust = (so.groupby(["Customer_Code","Customer_Name"])["Total_Invoice_Value"]
              .sum()
              .reset_index()
              .sort_values("Total_Invoice_Value", ascending=True))
top_cust["RevCr"] = top_cust["Total_Invoice_Value"] / 1e7
top_cust["ShortName"] = top_cust["Customer_Name"].str.replace(r"\s*(Pvt\.?\s*Ltd\.?|Trading\s*Co\.?|Wholesale\s*Mart|Consumer\s*Goods|Retail\s*Hub|Superstore|Distributors|Traders|Tech\s*Solutions|Brothers)", "", regex=True).str.strip()

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.barh(top_cust["ShortName"], top_cust["RevCr"],
               color=[plt.cm.Blues(0.4 + 0.06*i) for i in range(len(top_cust))],
               edgecolor="white", linewidth=0.5, height=0.65)

for bar, val in zip(bars, top_cust["RevCr"]):
    ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
            f"₹{val:.2f}Cr", va="center", fontsize=9, color=BLUE, fontweight="bold")

ax.set_xlabel("Total Revenue (₹ Crores)", fontsize=11)
ax.set_title("Top Customers by Revenue — FY 2024-25\nReliance Retail Ltd. | SAP SD Analysis",
             fontsize=13, fontweight="bold", color=BLUE, pad=12)
ax.set_facecolor("#F8FBFF")
ax.set_xlim(0, top_cust["RevCr"].max() * 1.22)
save("chart2_top_customers.png")

# ═════════════════════════════════════════════════════════════════════════════
# CHART 3 — Order Status Distribution (Donut)
# ═════════════════════════════════════════════════════════════════════════════
status_cnt = so["Order_Status"].value_counts()
fig, ax = plt.subplots(figsize=(9, 7))
wedges, texts, autotexts = ax.pie(
    status_cnt.values,
    labels=None,
    autopct="%1.1f%%",
    startangle=140,
    colors=PIE_COLORS[:len(status_cnt)],
    pctdistance=0.82,
    wedgeprops={"width": 0.55, "edgecolor": "white", "linewidth": 2},
)
for at in autotexts:
    at.set_fontsize(9)
    at.set_fontweight("bold")
    at.set_color("white")

ax.legend(wedges, [f"{k} ({v})" for k, v in status_cnt.items()],
          loc="lower center", bbox_to_anchor=(0.5, -0.08),
          ncol=3, fontsize=9, framealpha=0)

# Centre text
ax.text(0, 0.08, str(so.shape[0]), ha="center", va="center",
        fontsize=28, fontweight="bold", color=BLUE)
ax.text(0, -0.18, "Total Orders", ha="center", va="center",
        fontsize=10, color="grey")

ax.set_title("Order Status Distribution — SAP O2C\nFY 2024-25 | Reliance Retail Ltd.",
             fontsize=13, fontweight="bold", color=BLUE, pad=12)
save("chart3_order_status.png")

# ═════════════════════════════════════════════════════════════════════════════
# CHART 4 — Revenue by Region (State)
# ═════════════════════════════════════════════════════════════════════════════
region = (so.groupby("State")["Total_Invoice_Value"]
            .sum()
            .reset_index()
            .sort_values("Total_Invoice_Value", ascending=False))
region["RevCr"] = region["Total_Invoice_Value"] / 1e7

fig, ax = plt.subplots(figsize=(11, 5.5))
bar_colors = [COLORS6[i % len(COLORS6)] for i in range(len(region))]
bars = ax.bar(region["State"], region["RevCr"], color=bar_colors,
              edgecolor="white", linewidth=0.8, width=0.65)

for bar, val in zip(bars, region["RevCr"]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
            f"₹{val:.1f}Cr", ha="center", va="bottom", fontsize=8.5,
            color=BLUE, fontweight="bold")

ax.set_ylabel("Revenue (₹ Crores)", fontsize=11)
ax.set_xlabel("State / Region", fontsize=11)
ax.set_xticklabels(region["State"], rotation=30, ha="right", fontsize=9)
ax.set_title("Revenue by Region (State) — FY 2024-25\nReliance Retail Ltd. | SAP SD Geographic Analysis",
             fontsize=13, fontweight="bold", color=BLUE, pad=12)
ax.set_facecolor("#F8FBFF")
save("chart4_regional_revenue.png")

# ═════════════════════════════════════════════════════════════════════════════
# CHART 5 — Revenue by Product Category (Horizontal + Pie)
# ═════════════════════════════════════════════════════════════════════════════
# Map category
cat_map = {
    "MAT-TV": "Televisions", "MAT-AC": "Air Conditioners",
    "MAT-RF": "Refrigerators", "MAT-WM": "Washing Machines",
    "MAT-MO": "Mobiles", "MAT-LT": "Laptops",
    "MAT-TB": "Tablets", "MAT-HP": "Headphones", "MAT-CC": "Cameras"
}
so["Category"] = so["Material_Code"].apply(
    lambda x: next((v for k, v in cat_map.items() if x.startswith(k)), "Other"))

prod_rev = (so.groupby("Category")["Total_Invoice_Value"]
              .sum()
              .reset_index()
              .sort_values("Total_Invoice_Value", ascending=False))
prod_rev["RevCr"] = prod_rev["Total_Invoice_Value"] / 1e7

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Bar
bars = ax1.barh(prod_rev["Category"][::-1], prod_rev["RevCr"][::-1],
                color=[plt.cm.Blues(0.35 + 0.07*i) for i in range(len(prod_rev))],
                edgecolor="white", height=0.6)
for bar, val in zip(bars, prod_rev["RevCr"][::-1]):
    ax1.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
             f"₹{val:.1f}Cr", va="center", fontsize=8.5, color=BLUE, fontweight="bold")
ax1.set_xlabel("Revenue (₹ Crores)", fontsize=10)
ax1.set_title("Revenue by Product Category", fontsize=11, fontweight="bold", color=BLUE)
ax1.set_xlim(0, prod_rev["RevCr"].max() * 1.25)
ax1.set_facecolor("#F8FBFF")

# Pie
wedges, _, autotexts = ax2.pie(
    prod_rev["RevCr"],
    labels=None,
    autopct="%1.1f%%",
    startangle=90,
    colors=[plt.cm.Blues(0.3 + 0.08*i) for i in range(len(prod_rev))],
    pctdistance=0.75,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5}
)
for at in autotexts:
    at.set_fontsize(8)
    at.set_fontweight("bold")
ax2.legend(wedges, prod_rev["Category"], loc="lower center",
           bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=8, framealpha=0)
ax2.set_title("Category Revenue Share", fontsize=11, fontweight="bold", color=BLUE)

fig.suptitle("Product Revenue Analysis — FY 2024-25 | Reliance Retail Ltd.",
             fontsize=13, fontweight="bold", color=BLUE, y=1.01)
save("chart5_product_revenue.png")

# ═════════════════════════════════════════════════════════════════════════════
# CHART 6 — Quarterly Revenue & Orders (Combined)
# ═════════════════════════════════════════════════════════════════════════════
quarterly = so.groupby("Quarter").agg(
    Revenue=("Total_Invoice_Value","sum"),
    Orders=("SO_Number","count"),
    AvgOrderVal=("Total_Invoice_Value","mean")
).reset_index().sort_values("Quarter")
quarterly["RevCr"] = quarterly["Revenue"] / 1e7
quarterly["Label"] = quarterly["Quarter"].astype(str)

fig, ax1 = plt.subplots(figsize=(10, 5.5))
ax2 = ax1.twinx()

x = np.arange(len(quarterly))
w = 0.4
bars = ax1.bar(x - w/2, quarterly["RevCr"], width=w, color=MED_BLUE,
               alpha=0.85, label="Revenue (₹Cr)", edgecolor="white")
line = ax2.plot(x + w/2, quarterly["Orders"], marker="s", color=ORANGE,
                linewidth=2.5, markersize=9, label="No. of Orders",
                markerfacecolor=ORANGE, markeredgecolor="white", markeredgewidth=1.5)

for bar, val in zip(bars, quarterly["RevCr"]):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f"₹{val:.1f}Cr", ha="center", va="bottom", fontsize=8.5,
             color=BLUE, fontweight="bold")
for xi, yi in zip(x + w/2, quarterly["Orders"]):
    ax2.annotate(str(int(yi)), (xi, yi), textcoords="offset points",
                 xytext=(0, 8), ha="center", fontsize=8.5, color=ORANGE, fontweight="bold")

ax1.set_xticks(x)
ax1.set_xticklabels(quarterly["Label"], fontsize=10)
ax1.set_ylabel("Revenue (₹ Crores)", fontsize=11, color=BLUE)
ax2.set_ylabel("Number of Orders", fontsize=11, color=ORANGE)
ax1.tick_params(axis="y", colors=BLUE)
ax2.tick_params(axis="y", colors=ORANGE)
ax1.set_facecolor("#F8FBFF")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)

plt.title("Quarterly Revenue & Order Volume — FY 2024-25\nReliance Retail Ltd. | SAP O2C Analytics",
          fontsize=13, fontweight="bold", color=BLUE, pad=12)
save("chart6_quarterly.png")

# ═════════════════════════════════════════════════════════════════════════════
# DASHBOARD OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(20, 14))
fig.patch.set_facecolor("#EBF3FB")

gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.48, wspace=0.32,
                       left=0.05, right=0.97, top=0.90, bottom=0.06)

# ── KPI Cards (top row, 3 cols as merged) ─────────────────────────────────
ax_kpi = fig.add_subplot(gs[0, :])
ax_kpi.set_xlim(0, 10)
ax_kpi.set_ylim(0, 1)
ax_kpi.axis("off")

total_rev  = so["Total_Invoice_Value"].sum()
total_ord  = len(so)
total_cust = so["Customer_Code"].nunique()
avg_ord    = so["Total_Invoice_Value"].mean()
comp_pct   = (so["Order_Status"]=="Completed").mean()*100
total_gst  = so["GST_Amount"].sum()

kpis = [
    ("Total Revenue",     fmt_cr(total_rev),      BLUE),
    ("Total Orders",      f"{total_ord}",           MED_BLUE),
    ("Customers",         f"{total_cust}",           TEAL),
    ("Avg Order Value",   fmt_cr(avg_ord),           GREEN),
    ("Completion Rate",   f"{comp_pct:.1f}%",        PURPLE),
    ("Total GST Paid",    fmt_cr(total_gst),         GOLD),
]

for i, (label, val, col) in enumerate(kpis):
    x0 = i * 1.67 + 0.05
    rect = mpatches.FancyBboxPatch((x0, 0.05), 1.5, 0.88,
                                    boxstyle="round,pad=0.03",
                                    facecolor=col, edgecolor="white", linewidth=2)
    ax_kpi.add_patch(rect)
    ax_kpi.text(x0+0.75, 0.65, val,    ha="center", va="center", fontsize=17,
                fontweight="bold", color="white")
    ax_kpi.text(x0+0.75, 0.25, label,  ha="center", va="center", fontsize=9,
                color="white", alpha=0.9)

# ── Monthly Revenue (mid-left) ─────────────────────────────────────────────
ax1 = fig.add_subplot(gs[1, :2])
ax1.fill_between(range(len(monthly)), monthly["RevCr"], alpha=0.18, color=MED_BLUE)
ax1.plot(range(len(monthly)), monthly["RevCr"], marker="o", color=MED_BLUE,
         linewidth=2, markersize=5, markerfacecolor=BLUE, markeredgecolor="white")
ax1.set_xticks(range(len(monthly)))
ax1.set_xticklabels(monthly["Label"], rotation=45, ha="right", fontsize=7)
ax1.set_title("Monthly Revenue Trend (₹ Crores)", fontsize=10, fontweight="bold", color=BLUE)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₹{x:.1f}Cr"))
ax1.set_facecolor("white")
ax1.tick_params(labelsize=7)

# ── Order Status Donut (mid-right) ─────────────────────────────────────────
ax2 = fig.add_subplot(gs[1, 2])
wedges2, _, at2 = ax2.pie(
    status_cnt.values, autopct="%1.0f%%", startangle=90,
    colors=PIE_COLORS[:len(status_cnt)],
    pctdistance=0.75, wedgeprops={"width":0.55,"edgecolor":"white","linewidth":1.5}
)
for a in at2: a.set_fontsize(7); a.set_color("white"); a.set_fontweight("bold")
ax2.set_title("Order Status", fontsize=10, fontweight="bold", color=BLUE)
ax2.legend(wedges2, status_cnt.index, loc="lower center",
           bbox_to_anchor=(0.5,-0.12), ncol=2, fontsize=6.5, framealpha=0)

# ── Regional Revenue (bottom-left) ────────────────────────────────────────
ax3 = fig.add_subplot(gs[2, 0])
ax3.barh(region["State"][:6], region["RevCr"][:6],
         color=[plt.cm.Blues(0.4+0.08*i) for i in range(6)],
         edgecolor="white", height=0.6)
ax3.set_title("Revenue by State (Top 6)", fontsize=9, fontweight="bold", color=BLUE)
ax3.tick_params(labelsize=7.5)
ax3.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₹{x:.0f}Cr"))
ax3.set_facecolor("white")

# ── Product Revenue (bottom-mid) ──────────────────────────────────────────
ax4 = fig.add_subplot(gs[2, 1])
ax4.barh(prod_rev["Category"][::-1][:7], prod_rev["RevCr"][::-1][:7],
         color=[plt.cm.Blues(0.3+0.07*i) for i in range(7)],
         edgecolor="white", height=0.6)
ax4.set_title("Revenue by Product Category", fontsize=9, fontweight="bold", color=BLUE)
ax4.tick_params(labelsize=7.5)
ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₹{x:.0f}Cr"))
ax4.set_facecolor("white")

# ── Quarterly (bottom-right) ──────────────────────────────────────────────
ax5 = fig.add_subplot(gs[2, 2])
ax5b = ax5.twinx()
xq = np.arange(len(quarterly))
ax5.bar(xq, quarterly["RevCr"], color=MED_BLUE, alpha=0.75, width=0.5, edgecolor="white")
ax5b.plot(xq, quarterly["Orders"], marker="o", color=ORANGE,
          linewidth=2, markersize=6, markerfacecolor=ORANGE, markeredgecolor="white")
ax5.set_xticks(xq)
ax5.set_xticklabels(quarterly["Label"], rotation=15, fontsize=7)
ax5.tick_params(axis="y", labelsize=7, colors=BLUE)
ax5b.tick_params(axis="y", labelsize=7, colors=ORANGE)
ax5.set_title("Quarterly Revenue & Orders", fontsize=9, fontweight="bold", color=BLUE)
ax5.set_facecolor("white")

# Title
fig.text(0.5, 0.955, "SAP O2C Analytics Dashboard — Reliance Retail Ltd.",
         ha="center", fontsize=17, fontweight="bold", color=BLUE)
fig.text(0.5, 0.935, "FY 2024-25  |  Priyanshu Rajhans (23051769)  |  SAP Data Analytics & Engineering — KIIT",
         ha="center", fontsize=10, color="grey")

plt.savefig("charts/dashboard_overview.png", dpi=150, bbox_inches="tight",
            facecolor="#EBF3FB", edgecolor="none")
plt.close()
print("  [OK] dashboard_overview.png")

print("\nAll charts generated successfully in /charts folder.")
print(f"  Sales Orders : {len(so)} records")
print(f"  Total Revenue: {fmt_cr(total_rev)}")
print(f"  Total Orders : {total_ord}")
