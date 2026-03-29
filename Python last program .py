import pandas as pd
import os

def load_data(path):
    df = pd.read_csv(path)
    print("Rows:", len(df))
    print(df.head())
    return df

def clean_data(df):
    df = df.dropna()
    df = df.drop_duplicates()
    # Ensure numeric types
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df = df.dropna(subset=["Price", "Quantity"])
    return df

def process_data(df):
    df["Revenue"] = df["Price"] * df["Quantity"]
    total_sales = df["Revenue"].sum()
    by_cat = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
    top_prods = df.groupby("Product_Name")["Revenue"].sum().sort_values(ascending=False).head(5)
    return total_sales, by_cat, top_prods, df

def analyse(df):
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    monthly = df.dropna(subset=["Date"]).groupby(df["Date"].dt.to_period("M"))["Revenue"].sum()
    avg_order = df["Revenue"].mean()
    return monthly, avg_order

def generate_report(total_sales, by_cat, top_prods, monthly, avg_order, out_csv="report.csv"):
    print(f"\nTotal revenue: {total_sales:.2f}")
    print("\nRevenue by category:\n", by_cat)
    print("\nTop products:\n", top_prods)
    print("\nMonthly trend:\n", monthly)
    print("\nAverage order value:", round(avg_order, 2))

    report = by_cat.reset_index()
    report.columns = ["Category", "Revenue"]
    report.to_csv(out_csv, index=False)
    print(f"\nReport saved to {out_csv}")

if __name__ == "__main__":
    # replace with your file
    path = "sales.csv"
    if not os.path.exists(path):
        print("Put a CSV with columns Order_ID, Product_Name, Category, Price, Quantity, Date")
    else:
        df = load_data(path)
        df = clean_data(df)
        total_sales, by_cat, top_prods, df = process_data(df)
        monthly, avg_order = analyse(df)
        generate_report(total_sales, by_cat, top_prods, monthly, avg_order)