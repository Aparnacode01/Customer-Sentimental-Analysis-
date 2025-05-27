from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load customer data
data_path = "customer_segmentation_and_clv_final.xlsx"
df1 = pd.read_excel(data_path, sheet_name="Customer Data 1")
df2 = pd.read_excel(data_path, sheet_name="Customer Data 2")

# Merge datasets if necessary (assuming an ID column for merging)
df = pd.merge(df1, df2, on="Name", how="inner")

# Aggregate data (modify based on actual column names)
customer_stats = df.groupby("Name").agg({
    "Total Purchases": "sum",
    "Amount Spent": "sum",
    "Customer Since": "first",
    "Age": "first",
    "Gender": "first"
}).reset_index()

@app.route('/')
def index():
    return render_template('index.html', customers=customer_stats.to_dict(orient="records"))

if __name__ == '__main__':
    app.run(debug=True)
