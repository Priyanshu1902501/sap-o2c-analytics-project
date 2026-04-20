"""
generate_data.py
================
Generates realistic SAP O2C sample datasets for Reliance Retail Ltd.
Produces:
  - data/sap_sales_orders.csv
  - data/sap_inventory.csv

Author : Priyanshu Rajhans | Roll: 23051769
Program: SAP Data Analytics & Engineering — KIIT, Bhubaneswar
"""

import csv
import random
import os
from datetime import date, timedelta

random.seed(42)
os.makedirs("data", exist_ok=True)

# ── Reference data ────────────────────────────────────────────────────────────
CUSTOMERS = [
    ("CUST-1001", "Sharma Electronics Pvt. Ltd.",    "Pune",       "Maharashtra"),
    ("CUST-1002", "Mehta Traders",                   "Ahmedabad",  "Gujarat"),
    ("CUST-1003", "Sundar Tech Solutions",            "Chennai",    "Tamil Nadu"),
    ("CUST-1004", "Kapoor Distributors",              "Delhi",      "Delhi"),
    ("CUST-1005", "Reddy Electronics",                "Hyderabad",  "Telangana"),
    ("CUST-1006", "Bansal Retail Hub",                "Jaipur",     "Rajasthan"),
    ("CUST-1007", "Nair Consumer Goods",              "Kochi",      "Kerala"),
    ("CUST-1008", "Singh Wholesale Mart",             "Chandigarh", "Punjab"),
    ("CUST-1009", "Das Brothers Trading Co.",         "Kolkata",    "West Bengal"),
    ("CUST-1010", "Iyer Superstore",                  "Bengaluru",  "Karnataka"),
]

PRODUCTS = [
    ("MAT-TV-5501", "Smart LED TV 55 Inch 4K UHD",     "85287300", 45000, "Electronics"),
    ("MAT-TV-4301", "Smart LED TV 43 Inch FHD",         "85287300", 28000, "Electronics"),
    ("MAT-AC-1501", "Split AC 1.5 Ton 5-Star Inverter", "84151010", 38000, "Appliances"),
    ("MAT-RF-3001", "Double Door Refrigerator 300L",    "84181000", 32000, "Appliances"),
    ("MAT-WM-0801", "Front Load Washing Machine 8KG",   "84501100", 29500, "Appliances"),
    ("MAT-MO-6401", "Smartphone 64MP 128GB",            "85171200", 22000, "Mobile"),
    ("MAT-LT-1501", "Laptop 15.6 Inch Core i5 16GB",   "84713010", 58000, "Computing"),
    ("MAT-TB-1001", "Tablet 10 Inch 256GB WiFi",        "84713020", 18500, "Computing"),
    ("MAT-HP-2001", "Wireless Headphones Noise Cancel", "85183000", 4500,  "Accessories"),
    ("MAT-CC-0501", "DSLR Camera Kit 24MP",             "90065910", 52000, "Electronics"),
]

SALES_REPS = ["Arjun Verma", "Priya Nair", "Rohit Sharma", "Sneha Patel", "Vikram Das"]
PAYMENT_TERMS = ["Z030", "Z045", "Z060", "Z015"]
ORDER_STATUS  = ["Completed", "Completed", "Completed", "Delivered", "Delivered",
                 "Billed", "In Transit", "Processing", "Cancelled"]

def rand_date(start_y=2024, end_y=2025):
    start = date(start_y, 4, 1)
    end   = date(end_y, 3, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def gst_type(supplier_state, customer_state):
    return "CGST+SGST" if supplier_state == customer_state else "IGST"

def gst_rate(material_code):
    cat = material_code.split("-")[1]
    return 18  # All electronics/appliances 18% GST

# ── 1. Sales Orders CSV ───────────────────────────────────────────────────────
so_headers = [
    "SO_Number","SO_Date","Customer_Code","Customer_Name","City","State",
    "Material_Code","Material_Description","HSN_Code","Quantity","Unit_Price_INR",
    "Discount_Pct","Net_Taxable_Value","GST_Type","GST_Rate_Pct","GST_Amount",
    "Total_Invoice_Value","Payment_Terms","Sales_Rep","Order_Status",
    "Delivery_Date","Payment_Due_Date","Payment_Received","Outstanding_INR"
]

so_rows = []
for i in range(120):
    so_num  = f"SO-{10000+i}"
    so_date = rand_date()
    cust    = random.choice(CUSTOMERS)
    prod    = random.choice(PRODUCTS)
    qty     = random.randint(5, 200)
    disc    = random.choice([0, 3, 5, 7, 10])
    base    = prod[3] * qty
    net     = round(base * (1 - disc/100), 2)
    gtype   = gst_type("Maharashtra", cust[3])
    grate   = 18
    gtax    = round(net * grate / 100, 2)
    total   = round(net + gtax, 2)
    pt      = random.choice(PAYMENT_TERMS)
    days    = int(pt[1:])
    due     = so_date + timedelta(days=days+30)
    status  = random.choice(ORDER_STATUS)
    paid    = total if status == "Completed" else (0 if status in ["Processing","Cancelled"] else round(total * random.uniform(0.5,1), 2))
    outstanding = round(total - paid, 2)
    del_date = so_date + timedelta(days=random.randint(3, 15))

    so_rows.append([
        so_num, so_date.strftime("%d-%m-%Y"),
        cust[0], cust[1], cust[2], cust[3],
        prod[0], prod[1], prod[2],
        qty, prod[3], disc, net,
        gtype, grate, gtax, total,
        pt, random.choice(SALES_REPS), status,
        del_date.strftime("%d-%m-%Y"),
        due.strftime("%d-%m-%Y"),
        round(paid, 2), outstanding
    ])

with open("data/sap_sales_orders.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(so_headers)
    w.writerows(so_rows)

print(f"[OK] sap_sales_orders.csv — {len(so_rows)} records")

# ── 2. Inventory CSV ──────────────────────────────────────────────────────────
inv_headers = [
    "Material_Code","Material_Description","HSN_Code","Category",
    "Plant","Storage_Location","Unrestricted_Stock","Reserved_Stock",
    "Available_Stock","Reorder_Level","Max_Stock_Level",
    "Unit_Cost_INR","Total_Stock_Value_INR","Last_GR_Date","Last_GI_Date",
    "Shelf_Life_Days","Batch_Number","Valuation_Class"
]

plants = [("MH01","WH01","Mumbai"),("DL01","WH01","Delhi"),
          ("KA01","WH01","Bengaluru"),("TN01","WH01","Chennai")]

inv_rows = []
for prod in PRODUCTS:
    for plant, sl, city in plants:
        unres  = random.randint(50, 500)
        res    = random.randint(10, min(100, unres))
        avail  = unres - res
        reord  = random.randint(30, 80)
        maxstk = random.randint(400, 600)
        ucost  = round(prod[3] * 0.62, 2)
        tval   = round(unres * ucost, 2)
        lgr    = rand_date(2024, 2025)
        lgi    = lgr + timedelta(days=random.randint(1, 20))
        batch  = f"BT{random.randint(10000,99999)}"
        inv_rows.append([
            prod[0], prod[1], prod[2], prod[4],
            plant, sl, unres, res, avail,
            reord, maxstk, ucost, tval,
            lgr.strftime("%d-%m-%Y"), lgi.strftime("%d-%m-%Y"),
            730, batch, "7920"
        ])

with open("data/sap_inventory.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(inv_headers)
    w.writerows(inv_rows)

print(f"[OK] sap_inventory.csv    — {len(inv_rows)} records")
print("\nData generation complete. Files saved in /data folder.")
