import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"
HEALTH_URL = "http://127.0.0.1:8000/health"

st.set_page_config(
    page_title="Mercedes Price Predictor",
    page_icon="🚗",
    layout="wide"
)

# ---------- SIDEBAR ---------- #

st.markdown(
    """
    <style>
    section[data-testid="stSidebar"] div.block-container {
        padding-top: 1.5rem;
        padding-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("### 🚗 Mercedes ML App")

page = st.sidebar.radio(
    "📂 Navigation",
    [
        "🏠 Home",
        "💰 Prediction",
        "🤖 Model Used"
    ]
)

# API STATUS
try:
    response = requests.get(HEALTH_URL)

    if response.status_code == 200:
        st.sidebar.success("API Running ✅")
    else:
        st.sidebar.warning("API Issue ⚠️")

except:
    st.sidebar.error("API Offline ❌")

st.sidebar.markdown(
"""
**⚙ Tech Stack**

🧠 Scikit-Learn  
⚡ FastAPI  
🎨 Streamlit
"""
)

# ---------- HOME PAGE ---------- #

if page == "🏠 Home":

    st.markdown(
        """
        <h1 style='text-align:center;'>👋 Welcome!</h1>
        <h2 style='text-align:center; color:#9aa4b2;'>
        Mercedes Car Price Prediction using Machine Learning
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.write(
        """
        This application predicts the **base price of Mercedes cars**
        using a machine learning model trained on vehicle specifications.
        """
    )

    st.write("")

    # Feature cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style='background-color:#0e1117;
                        padding:25px;
                        border-radius:15px;
                        text-align:center;
                        border:1px solid #262730'>
                <h3>🚘 Mercedes Models</h3>
                <p>A-Class, C-Class, E-Class, S-Class</p>
                <p>AMG Series, SUVs and more</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style='background-color:#0e1117;
                        padding:25px;
                        border-radius:15px;
                        text-align:center;
                        border:1px solid #262730'>
                <h3>⚙ Engine Specifications</h3>
                <p>Fuel type, horsepower</p>
                <p>Turbo configuration</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div style='background-color:#0e1117;
                        padding:20px;
                        border-radius:15px;
                        text-align:center;
                        border:1px solid #262730'>
                <h3>📊 Dataset</h3>
                <p>Real vehicle feature dataset</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style='background-color:#0e1117;
                        padding:20px;
                        border-radius:15px;
                        text-align:center;
                        border:1px solid #262730'>
                <h3>🤖 ML Model</h3>
                <p>SGDRegressor used for price prediction</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div style='background-color:#0e1117;
                        padding:20px;
                        border-radius:15px;
                        text-align:center;
                        border:1px solid #262730'>
                <h3>⚡ Instant Prediction</h3>
                <p>Fast predictions via FastAPI backend</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------- PREDICTION PAGE ---------- #

elif page == "💰 Prediction":

    # ---------- HEADER WITH MERCEDES LOGO ---------- #

    col_logo, col_title = st.columns([1,8])

    with col_logo:
        st.image("frontend/images/logo.png", width=80)

    with col_title:
        st.title("Mercedes Car Price Prediction")

    st.write("")

    # ---------- INPUT FORM ---------- #

    col1, col2 = st.columns(2)

    with col1:

        model = st.selectbox(
            "🚘 Model",
            [
                "A-Class","C-Class","E-Class","S-Class",
                "CLA","CLS","GLA","GLB","GLC",
                "GLE","GLS","G-Class",
                "AMG GT","AMG A 45","AMG C 63","AMG E 63","AMG S 63"
            ]
        )

        year = st.selectbox(
            "📅 Year",
            [2020,2021,2022,2023,2024,2025]
        )

        color = st.selectbox(
            "🎨 Color",
            [
                "Yellow","Black","Grey","White",
                "Silver","Brown","Blue","Red",
                "Green","Orange"
            ]
        )

        fuel = st.selectbox(
            "⛽ Fuel Type",
            ["Diesel","Petrol","Hybrid","Electric"]
        )

    with col2:

        horsepower = st.slider(
            "⚡ Horsepower",
            100,
            1000,
            300
        )

        turbo = st.radio(
            "🌀 Turbo",
            ["Yes","No"]
        )

    st.divider()

    # ---------- PREDICTION BUTTON ---------- #

    if st.button("🚀 Predict Price"):

        data = {
            "model": model,
            "year": year,
            "color": color,
            "fuel": fuel,
            "horsepower": horsepower,
            "turbo": turbo
        }

        try:

            with st.spinner("Predicting price..."):

                response = requests.post(API_URL, json=data)

            if response.status_code == 200:

                result = response.json()
                price = result["Predicted Car Base Price (USD)"]

                @st.dialog("💰 Prediction Result")
                def show_result():

                    st.success("Prediction Successful")

                    st.markdown(
                        f"""
                        <h2 style='text-align:center;'>Estimated Price</h2>
                        <h1 style='text-align:center;'>${price:,.2f}</h1>
                        """,
                        unsafe_allow_html=True
                    )

                show_result()

            else:

                error = response.json()

                st.error("Prediction failed.")
                st.code(error)

        except Exception as e:

            st.error("Cannot connect to FastAPI server.")
            st.code(str(e))
# ---------- MODEL PAGE ---------- #

elif page == "🤖 Model Used":

    st.title("🤖 Machine Learning Model")

    st.subheader("SGDRegressor")

    st.write(
        """
        The model used for prediction is **SGDRegressor** from Scikit-Learn.

        SGD (Stochastic Gradient Descent) is efficient for training
        linear regression models on large datasets.
        """
    )

    st.divider()

    st.subheader("Why SGDRegressor?")

    st.markdown(
        """
        - Fast training  
        - Works well for large datasets  
        - Supports incremental learning  
        - Memory efficient  
        """
    )

    st.subheader("Optimization Formula")

    st.latex(r"w = w - \eta \nabla J(w)")