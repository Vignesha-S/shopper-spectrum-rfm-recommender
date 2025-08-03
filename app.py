import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# ---------------------
# 📦 Load Data & Models
# ---------------------
df = pd.read_csv("cleaned_data.csv")
rfm = pd.read_csv("rfm.csv")
model = joblib.load("kmeans_model.pkl")
similarity_matrix = joblib.load("product_similarity.pkl")

# ---------------------
# 🎨 Streamlit Setup
# ---------------------
st.set_page_config(page_title="🛒 Shopper Spectrum", layout="wide")
st.title("🛒 Shopper Spectrum: E-Commerce Segmentation & Recommendations")

# Sidebar navigation
st.sidebar.title("🔗 Navigation")
section = st.sidebar.radio("Select Page", ["🏠 Home", "🔍 Customer Segmentation", "🎯 Product Recommendation"])

# ---------------------
# 🏠 Home Page
# ---------------------
if section == "🏠 Home":
    st.subheader("Welcome!")
    st.markdown("""
    Shopper Spectrum is an AI-powered E-Commerce analytics platform that helps businesses:
    
    - 📊 **Segment Customers** using RFM + KMeans
    - 🎯 **Recommend Products** using Item-based Collaborative Filtering
    
    Use the sidebar to explore the other modules.
    
    ---
    **Tech Stack**: Python · Pandas · Scikit-Learn · Streamlit
    """)

# ---------------------
# 🔍 Customer Segmentation
# ---------------------
elif section == "🔍 Customer Segmentation":
    st.header("🔍 Customer Segmentation")

    recency = st.number_input("Recency (in days)", min_value=0, max_value=400, value=30)
    frequency = st.number_input("Frequency (Number of Purchases)", min_value=1, max_value=250, value=5)
    monetary = st.number_input("Monetary (Total Spend)", min_value=0.0, value=1000.0)

    if st.button("Predict Cluster"):
        scaler = StandardScaler()
        scaler.fit(rfm[["Recency", "Frequency", "Monetary"]])
        input_scaled = scaler.transform([[recency, frequency, monetary]])
        cluster_label = model.predict(input_scaled)[0]

        label_map = {
            2: "High-Value",
            3: "Regular",
            0: "Occasional",
            1: "At-Risk"
        }
        segment = label_map.get(cluster_label, "Unknown")
        st.success(f"Predicted Segment: **{segment}**")

# ---------------------
# 🎯 Product Recommendation
# ---------------------
elif section == "🎯 Product Recommendation":
    st.header("🎯 Product Recommendation")

    product_list = df["Description"].dropna().unique().tolist()
    product_name = st.selectbox("Select a product", product_list)

    if st.button("Get Recommendations"):
        if product_name in similarity_matrix.index:
            similar_scores = similarity_matrix[product_name].sort_values(ascending=False)
            top_5 = similar_scores[1:6]

            st.subheader(f"Products similar to **{product_name}**:")
            for item, score in top_5.items():
                st.markdown(f"- {item} (Similarity: **{score:.2f}**)")
        else:
            st.warning("Product not found in similarity matrix.")
