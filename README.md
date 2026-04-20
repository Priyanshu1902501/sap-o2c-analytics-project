# SAP Capstone Project — Order-to-Cash (O2C)
## Complete Sales Cycle Implementation in SAP SD

**Student:** Priyanshu Rajhans | **Roll No:** 23051769  
**Branch:** Computer Science & Engineering (CSE)  
**Program:** SAP - Data Analytics & Engineering  
**Institution:** Kalinga Institute of Industrial Technology, Bhubaneswar  
**Academic Year:** 2025-2026 | **Submission:** April 21, 2026

---

## Project Overview

End-to-end **Order-to-Cash (O2C)** implementation in SAP SD for **Reliance Retail Ltd.** — a fictitious B2B electronics distributor supplying Smart LED TVs to regional distributors across India. Includes Python-based data analytics layer with 6 BI charts and a KPI dashboard.

---

## Folder Structure

```
SAP_O2C_Project_Priyanshu_Rajhans/
├── README.md
├── generate_data.py                              ← Generates SAP CSV datasets
├── run_project.py                                ← Generates all charts & dashboard
├── generate_pdf.py                               ← Generates Project_Documentation.pdf
├── generate_docx.js                              ← Generates project report DOCX
│
├── data/
│   ├── sap_sales_orders.csv                      ← 120 SAP O2C sales order records
│   └── sap_inventory.csv                         ← 40 inventory records (4 plants × 10 products)
│
├── charts/
│   ├── dashboard_overview.png                    ← Full KPI dashboard
│   ├── chart1_monthly_revenue.png                ← Monthly revenue trend
│   ├── chart2_top_customers.png                  ← Top customers by revenue
│   ├── chart3_order_status.png                   ← Order status donut chart
│   ├── chart4_regional_revenue.png               ← Revenue by state/region
│   ├── chart5_product_revenue.png                ← Revenue by product category
│   └── chart6_quarterly.png                      ← Quarterly revenue & order volume
│
├── Project_Documentation.pdf                     ← 5-page PDF documentation (submit this)
└── sap_project_priyanshu_rajhans_23051769.docx   ← Full project report with charts
```

---

## O2C Process Steps

| # | Step | T-Code | SAP Document |
|---|------|--------|-------------|
| 01 | Pre-Sales Inquiry | VA11 | Inquiry (IN) |
| 02 | Quotation Creation | VA21 | Quotation (QT) |
| 03 | Sales Order | VA01 | Sales Order (OR) |
| 04 | Credit Check & Release | FD32 / VKM3 | Credit Master |
| 05 | Outbound Delivery | VL01N | Delivery (LF) |
| 06 | Picking & Packing | VL02N / LT0A | Transfer Order |
| 07 | Post Goods Issue | VL02N (PGI) | Material Document |
| 08 | Billing / Tax Invoice | VF01 | Billing Doc F2 |
| 09 | Incoming Payment | F-28 | Payment Doc DZ |

---

## How to Run

```bash
# Step 1: Generate CSV data
python generate_data.py

# Step 2: Generate charts & dashboard
python run_project.py

# Step 3: Generate PDF documentation
python generate_pdf.py

# Step 4: Generate DOCX report (requires Node.js)
node generate_docx.js
```

**Requirements:** `pip install pandas matplotlib seaborn numpy reportlab` | `npm install -g docx`

---

## Business Scenario

| Field | Value |
|-------|-------|
| Company | Reliance Retail Ltd. (IN10) |
| Customer | Sharma Electronics Pvt. Ltd., Pune, MH |
| Product | Smart LED TV 55 Inch 4K (MAT-TV-5501) |
| Quantity | 100 units |
| Invoice Value | INR 50,44,500 (incl. CGST 9% + SGST 9%) |
| Dataset Revenue | ~INR 44.88 Crores (FY 2024-25, 120 orders) |
