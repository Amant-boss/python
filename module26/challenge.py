import pandas as pd
import streamlit as st
import plotly_express as px
from datetime import datetime

# 1. Load data or create a blank database template at start
try:
    receipts_df = pd.read_csv("receipts_data.csv")
    # Ensure Date column is in datetime format if it exists
    if "Date" in receipts_df.columns:
        receipts_df["Date"] = pd.to_datetime(receipts_df["Date"])
    # Handle older CSVs that used 'Year' instead of 'Date'
    if "Year" in receipts_df.columns and "Date" not in receipts_df.columns:
        receipts_df["Date"] = pd.to_datetime(receipts_df["Year"].astype(str) + "-01-01")
        receipts_df = receipts_df.drop(columns=["Year"])
except FileNotFoundError:
    columns = ["Owner", "Store", "Category", "Subtotal", "Tax", "Total Amount", "Date"]
    receipts_df = pd.DataFrame(columns=columns)

st.title("Receipt Tracker & Analyzer")
st.write("Log and analyze your shopping receipts")

# 2. Sidebar Entry Form
st.sidebar.header("Add New Receipt")
with st.sidebar.form("receipt_form"):
    new_name = st.text_input("Receipt Owner Name", placeholder="e.g., John Doe")
    new_store = st.text_input("Store / Business Name", placeholder="e.g., Walmart, Target")

    receipt_category = st.selectbox(
        "Expense Category",
        ["Groceries", "Electronics", "Clothing", "Dining Out", "Gas/Travel", "Utilities", "Other"]
    )

    st.markdown("**Enter Items & Prices** (One per line, e.g., *Milk 2.50*)")
    items_input = st.text_area(
        "Items List",
        placeholder="Apples 3.99\nBread 2.49\nCoffee 8.00",
        help="Type the item name, a space, and then the numeric price."
    )

    purchase_date = st.date_input("Purchase Date", value=datetime.today())
    tax_paid = st.number_input("Sales Tax Paid ($)", min_value=0.0, step=0.01, value=0.0)

    # INDENTED CORRECTLY INSIDE THE FORM
    submit_button = st.form_submit_button(label="Save Receipt")

# 3. Process Form Submissions (Outside the form block)
if submit_button:
    calculated_subtotal = 0.0
    parsed_items = []

    if items_input.strip():
        for line in items_input.strip().split("\n"):
            parts = line.rsplit(maxsplit=1)
            if len(parts) == 2:
                name, price_str = parts
                try:
                    price_val = float(price_str)
                    parsed_items.append({"item": name, "price": price_val})
                    calculated_subtotal += price_val
                except ValueError:
                    st.error(f"Could not parse price for line: '{line}'. Make sure the price is a number at the end.")

    final_total = calculated_subtotal + tax_paid

    new_data = {
        "Owner": [new_name],
        "Store": [new_store],
        "Category": [receipt_category],
        "Subtotal": [calculated_subtotal],
        "Tax": [tax_paid],
        "Total Amount": [final_total],
        "Date": [pd.to_datetime(purchase_date)]
    }

    # Save back to CSV file
    new_row = pd.DataFrame(new_data)
    receipts_df = pd.concat([new_row, receipts_df], ignore_index=True)
    receipts_df.to_csv("receipts_data.csv", index=False)
    st.sidebar.success("New Receipt Logged")
    st.rerun()

# 4. Summary Statistics Dashboard Section
st.subheader("Summary Statistics")
total_receipts = receipts_df.shape[0]
unique_stores = receipts_df["Store"].nunique() if total_receipts > 0 else 0
average_total = receipts_df["Total Amount"].mean() if total_receipts > 0 else 0.0
total_spent = receipts_df["Total Amount"].sum() if total_receipts > 0 else 0.0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Receipts", total_receipts)
col2.metric("Unique Stores", unique_stores)
col3.metric("Average Spent", f"${average_total:.2f}")
col4.metric("Total Spending", f"${total_spent:.2f}")

# --- MANAGE RECEIPTS SECTION (EDIT & DELETE) ---
st.subheader("Manage Receipts")
if total_receipts > 0:
    # Safely convert to date strings for clean dropdown readability
    date_display = receipts_df["Date"].dt.strftime('%Y-%m-%d')
    receipt_options = {
        idx: f"Row {idx}: {row['Owner']} at {row['Store']} on {date_display.iloc[idx]} (${row['Total Amount']:.2f})"
        for idx, row in receipts_df.iterrows()
    }

    col_manage1, col_manage2 = st.columns([3, 1])
    with col_manage1:
        selected_idx = st.selectbox("Select a receipt to Edit or Delete:", options=list(receipt_options.keys()),
                                    format_func=lambda x: receipt_options[x])

    # Nested edit layout inside expander to keep it clean
    with st.expander("✏️ Edit Selected Receipt Fields"):
        current_row = receipts_df.loc[selected_idx]

        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            edit_name = st.text_input("Edit Owner Name", value=str(current_row["Owner"]))
            edit_store = st.text_input("Edit Store / Business Name", value=str(current_row["Store"]))
            # Extract standard date object from timestamp safely
            current_date_val = current_row["Date"].date() if isinstance(current_row["Date"], pd.Timestamp) else \
            current_row["Date"]
            edit_date = st.date_input("Edit Purchase Date", value=current_date_val)
        with col_ed2:
            categories_list = ["Groceries", "Electronics", "Clothing", "Dining Out", "Gas/Travel", "Utilities", "Other"]
            default_cat_idx = categories_list.index(current_row["Category"]) if current_row[
                                                                                    "Category"] in categories_list else 0
            edit_category = st.selectbox("Edit Expense Category", options=categories_list, index=default_cat_idx)
            edit_subtotal = st.number_input("Edit Subtotal ($)", min_value=0.0, step=0.01,
                                            value=float(current_row["Subtotal"]))
            edit_tax = st.number_input("Edit Sales Tax Paid ($)", min_value=0.0, step=0.01,
                                       value=float(current_row["Tax"]))

        if st.button("💾 Save Changes", use_container_width=True):
            receipts_df.at[selected_idx, "Owner"] = edit_name
            receipts_df.at[selected_idx, "Store"] = edit_store
            receipts_df.at[selected_idx, "Category"] = edit_category
            receipts_df.at[selected_idx, "Subtotal"] = edit_subtotal
            receipts_df.at[selected_idx, "Tax"] = edit_tax
            receipts_df.at[selected_idx, "Total Amount"] = edit_subtotal + edit_tax
            receipts_df.at[selected_idx, "Date"] = pd.to_datetime(edit_date)

            receipts_df.to_csv("receipts_data.csv", index=False)
            st.success("Receipt updated successfully!")
            st.rerun()

    with col_manage2:
        st.write("")
        st.write("")
        if st.button("❌ Delete Receipt", use_container_width=True):
            receipts_df = receipts_df.drop(selected_idx).reset_index(drop=True)
            receipts_df.to_csv("receipts_data.csv", index=False)
            st.success("Receipt deleted successfully!")
            st.rerun()
else:
    st.info("No receipts available to manage.")
# --- END OF MANAGE RECEIPTS SECTION ---

st.subheader("Dataset Preview")
# Display with clean date layout formatting
preview_df = receipts_df.copy()
if total_receipts > 0:
    preview_df["Date"] = preview_df["Date"].dt.strftime('%Y-%m-%d')
st.write(preview_df.head())

st.subheader("Top Stores & Owners")
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top Stores Visited")
    if total_receipts > 0:
        top_stores = receipts_df["Store"].value_counts().head(10)
        st.bar_chart(top_stores)
    else:
        st.info("No data available yet.")

with col_right:
    st.subheader("Top Receipt Owners")
    if total_receipts > 0:
        top_owners = receipts_df["Owner"].value_counts().head(10)
        st.bar_chart(top_owners)
    else:
        st.info("No data available yet.")

st.subheader("Expense Category Distribution")
if total_receipts > 0:
    fig_pie = px.pie(
        receipts_df,
        names="Category",
        values="Total Amount",
        title="Spending Breakdown by Category",
        color="Category",
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig_pie)
else:
    st.info("No data available to build chart.")

st.subheader("Yearly Spending Trends by Category")
if total_receipts > 0:
    # Grouping by year component derived directly from the date format
    trend_df = receipts_df.copy()
    trend_df["Year"] = trend_df["Date"].dt.year
    yearly_summary = trend_df.groupby(["Year", "Category"])["Total Amount"].sum().reset_index()
    fig_bar = px.bar(
        yearly_summary,
        x="Year",
        y="Total Amount",
        color="Category",
        title="Yearly Category Expenditures",
        color_discrete_sequence=px.colors.sequential.Plasma,
        barmode="group"
    )
    st.plotly_chart(fig_bar)
else:
    st.info("No data available to build chart.")

st.subheader("Top 15 Stores by Total Spend")
if total_receipts > 0:
    top_store_spend = receipts_df.groupby("Store")["Total Amount"].sum().reset_index()
    top_store_spend = top_store_spend.sort_values(by="Total Amount", ascending=False).head(15)

    fig_horiz = px.bar(
        top_store_spend,
        x="Total Amount",
        y="Store",
        orientation="h",
        title="Highest Spend Businesses",
        labels={"Total Amount": "Total Money Spent ($)", "Store": "Store Name"},
        color="Total Amount",
        color_continuous_scale=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig_horiz)
else:
    st.info("No data available to build chart.")

st.subheader("Filter Data by Category")
if total_receipts > 0:
    category_filter = st.selectbox("Select Category to View", receipts_df["Category"].unique())
    filtered_df = receipts_df[receipts_df["Category"] == category_filter].copy()
    filtered_df["Date"] = filtered_df["Date"].dt.strftime('%Y-%m-%d')
    st.write(filtered_df)
else:
    st.info("No categories to filter yet.")
