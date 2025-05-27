import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

st.set_page_config(page_title="Customer Analytics Dashboard", layout="wide")
st.title("📊 Customer Analytics & Segmentation")

# Load the Excel file
excel_path = "customer_segmentation_and_clv_final.xlsx"
df1 = pd.read_excel(excel_path, sheet_name="Customer Data 1")
df2 = pd.read_excel(excel_path, sheet_name="Customer Data 2")

# Normalize column names in df2
df2 = df2.rename(columns={
    'Customer Name': 'Name',
    'Customer Email': 'Email',
    'Sex': 'Gender',
    'Purchases Count': 'Total Purchases',
    'Amount Spent': 'Total Spent'
})

# Merge both datasets
df = pd.merge(df1, df2, on=['Name', 'Email', 'Gender'], how='outer')
df['Total Purchases'] = df['Total Purchases_x'].fillna(df['Total Purchases_y'])
df['Total Spent'] = df['Total Spent_x'].fillna(df['Total Spent_y'])
df.drop(columns=['Total Purchases_x', 'Total Purchases_y', 'Total Spent_x', 'Total Spent_y', 'Age Group'], inplace=True, errors='ignore')

df.dropna(subset=['Total Purchases', 'Total Spent'], inplace=True)

# Customer Segmentation (KMeans Clustering)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[['Total Purchases', 'Total Spent']])

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Visualization of Clusters
st.subheader("Customer Segmentation (K-Means Clusters)")
fig, ax = plt.subplots(figsize=(8,6))
sns.scatterplot(x=df['Total Purchases'], y=df['Total Spent'], hue=df['Cluster'], palette='viridis', ax=ax)
ax.set_title('Customer Segmentation')
st.pyplot(fig)

# Decision Tree Classifier
X = df[['Age', 'Total Purchases', 'Gender']]
X = pd.get_dummies(X, columns=['Gender'], drop_first=True)  # Convert categorical variable
y = df['Cluster']  # Using clusters as classification labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

dt_classifier = DecisionTreeClassifier(max_depth=5, random_state=42)
dt_classifier.fit(X_train, y_train)

y_pred_dt = dt_classifier.predict(X_test)

# Model Evaluation
st.subheader("Decision Tree Classification Report")
st.text(classification_report(y_test, y_pred_dt))
st.write(f"**Decision Tree Accuracy:** {accuracy_score(y_test, y_pred_dt):.2f}")

# Confusion Matrix
st.subheader("Confusion Matrix")
fig, ax = plt.subplots()
sns.heatmap(confusion_matrix(y_test, y_pred_dt), annot=True, fmt='d', cmap='Blues', ax=ax)
st.pyplot(fig)

# Decision Tree Visualization
st.subheader("Decision Tree Visualization")
fig, ax = plt.subplots(figsize=(12, 8))
plot_tree(dt_classifier, feature_names=X.columns, class_names=['Cluster 0', 'Cluster 1', 'Cluster 2'], filled=True)
st.pyplot(fig)

# Customer Lookup Feature
st.subheader("🔍 Customer Info Lookup")
customer_name = st.text_input("Enter Customer Name to search:")

if customer_name:
    filtered = df[df['Name'].str.lower() == customer_name.strip().lower()]
    if not filtered.empty:
        st.subheader("Customer Details")
        st.write("Name:", filtered.iloc[0]['Name'])
        st.write("Email:", filtered.iloc[0]['Email'])
        st.write("Gender:", filtered.iloc[0]['Gender'])
        st.write("Age:", filtered.iloc[0]['Age'])
        st.write("Customer Since:", filtered.iloc[0].get('Customer Since', 'N/A'))
        st.write("Total Purchases:", int(filtered.iloc[0]['Total Purchases']))
        st.write("Total Spent:", f"₹{filtered.iloc[0]['Total Spent']:.2f}")
        st.write("Cluster:", filtered.iloc[0]['Cluster'])
    else:
        st.warning("No matching customer found. Please check the name and try again.")
