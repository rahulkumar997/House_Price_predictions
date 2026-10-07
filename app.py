import pandas as pd
import streamlit as st

from house_price_prediction import load_model, predict_house_value


st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide",
)


@st.cache_resource
def get_model():
    return load_model()


model = get_model()


def render_theme_css():
    dark_mode = st.session_state.get("dark_mode", False)
    background = "#0f172a" if dark_mode else "#edf2ff"
    surface = "rgba(15, 23, 42, 0.72)" if dark_mode else "rgba(255, 255, 255, 0.75)"
    panel = "#111827" if dark_mode else "#ffffff"
    text = "#e5eefc" if dark_mode else "#1f2937"
    muted = "#c7d2fe" if dark_mode else "#64748b"
    primary = "#8ea8ff" if dark_mode else "#2563eb"
    primary_hover = "#a7baff" if dark_mode else "#1d4ed8"
    border = "rgba(148, 163, 184, 0.28)" if dark_mode else "rgba(148, 163, 184, 0.2)"
    shadow = "rgba(15, 23, 42, 0.32)" if dark_mode else "rgba(37, 99, 235, 0.12)"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, rgba(15,23,42,0.18), rgba(15,23,42,0.06)), {background};
            color: {text};
        }}
        .main .block-container {{
            padding-top: 1.25rem;
            padding-bottom: 2rem;
        }}
        .app-shell {{
            max-width: 1250px;
            margin: 0 auto;
            padding: 0.4rem 0.2rem 0.6rem;
        }}
        .hero-card {{
            background: {surface};
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid {border};
            border-radius: 28px;
            box-shadow: 0 28px 40px {shadow};
            padding: 1rem;
        }}
        .form-panel {{
            background: {panel};
            border: 1px solid {border};
            border-radius: 20px;
            padding: 1.1rem 1rem 0.8rem;
            box-shadow: 0 14px 30px {shadow};
        }}
        .hero-image {{
            border-radius: 18px;
            overflow: hidden;
            height: 100%;
            min-height: 520px;
            border: 1px solid {border};
            background: #d7e2ff;
        }}
        .hero-image img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 18px;
            display: block;
        }}
        .rating-badge {{
            display: inline-block;
            background: rgba(37, 99, 235, 0.14);
            border: 1px solid {border};
            color: {muted};
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            border-radius: 999px;
            padding: 0.38rem 0.7rem;
            margin-bottom: 0.7rem;
        }}
        .title {{
            font-size: clamp(1.8rem, 2vw, 2.6rem);
            font-weight: 800;
            line-height: 1.08;
            margin: 0 0 0.4rem;
            color: {text};
        }}
        .subtitle {{
            color: {muted};
            font-size: 1rem;
            margin-bottom: 1rem;
        }}
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > div {{
            background: {panel};
            color: {text};
            border: 1px solid {border};
            border-radius: 12px;
            box-shadow: none;
        }}
        .stButton > button {{
            width: 100%;
            border: none;
            border-radius: 12px;
            background: linear-gradient(135deg, {primary}, {primary_hover});
            color: white;
            font-weight: 700;
            padding: 0.8rem 1rem;
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.2);
        }}
        .stButton > button:hover {{
            background: linear-gradient(135deg, {primary_hover}, {primary});
        }}
        .result-box {{
            margin-top: 1rem;
            background: linear-gradient(135deg, rgba(37,99,235,0.13), rgba(52,211,153,0.10));
            border: 1px solid {border};
            border-radius: 16px;
            padding: 1rem 1.1rem;
        }}
        .result-label {{
            font-size: 0.76rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: {muted};
        }}
        .result-value {{
            font-size: 2.1rem;
            font-weight: 800;
            color: {text};
            margin-top: 0.3rem;
        }}
        .theme-toggle {{
            padding: 0.35rem 0.9rem;
            border-radius: 999px;
            border: 1px solid {border};
            background: {surface};
            width: fit-content;
            margin-left: auto;
            margin-bottom: 0.7rem;
        }}
        .theme-toggle label {{
            color: {text};
            font-weight: 600;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


render_theme_css()


dark_mode = st.toggle("Dark mode", value=st.session_state.get("dark_mode", False), key="dark_mode")
if dark_mode:
    render_theme_css()

left_col, right_col = st.columns([1.18, 0.9], gap="large")

with left_col:
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    st.image("housebg.jpeg", use_container_width=True, output_format="auto")
    st.markdown('</div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="form-panel">', unsafe_allow_html=True)
    st.markdown('<div class="rating-badge">Property Advisor</div>', unsafe_allow_html=True)
    st.markdown('<div class="title">Smart home pricing</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predict the likely value of a home from verified property features.</div>', unsafe_allow_html=True)

    with st.form("house_prediction_form"):
        longitude = st.number_input("Longitude", min_value=-125.0, max_value=-114.0, value=-122.23, step=0.01)
        latitude = st.number_input("Latitude", min_value=32.0, max_value=42.0, value=37.88, step=0.01)
        housing_median_age = st.number_input("House median age", min_value=1, max_value=52, value=41)
        total_rooms = st.number_input("Total rooms", min_value=1, max_value=20000, value=880)
        total_bedrooms = st.number_input("Total bedrooms", min_value=1, max_value=15000, value=129)
        population = st.number_input("Population", min_value=1, max_value=30000, value=322)
        households = st.number_input("Households", min_value=1, max_value=20000, value=126)
        median_income = st.number_input("Median income", min_value=0.0, max_value=30.0, value=8.3252, step=0.01)
        ocean_proximity = st.selectbox(
            "Ocean proximity",
            ["NEAR BAY", "<1H OCEAN", "INLAND", "NEAR OCEAN", "ISLAND"],
        )
        submitted = st.form_submit_button("Estimate Price")

    if submitted:
        input_data = pd.DataFrame(
            [{
                "longitude": longitude,
                "latitude": latitude,
                "housing_median_age": housing_median_age,
                "total_rooms": total_rooms,
                "total_bedrooms": total_bedrooms,
                "population": population,
                "households": households,
                "median_income": median_income,
                "ocean_proximity": ocean_proximity,
            }]
        )
        prediction = predict_house_value(input_data, model=model).iloc[0]
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-label">Estimated house value</div>
                <div class="result-value">${prediction:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)
