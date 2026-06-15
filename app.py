import streamlit as st
import json
import time
import base64
import os
from PIL import Image
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# ========================================================
# BULLETPROOF CLEANER (The antidote for Error 404)
# ========================================================
raw_endpoint = os.getenv("AZURE_ENDPOINT", "").strip()
clean_endpoint = raw_endpoint.split("/openai")[0].split("/models")[0].split("/v1")[0].split("/chat")[0]

client = AzureOpenAI(
    api_key=os.getenv("AZURE_API_KEY", "").strip(),  
    api_version="2024-12-01-preview", 
    azure_endpoint=clean_endpoint
)

st.set_page_config(page_title="Nox. Premium Headwear", page_icon="🎩", layout="wide")

# ==========================================
# Function to load local photos
# ==========================================
def get_img_b64(img_path):
    if str(img_path).startswith("http"):
        return img_path 
    try:
        with open(img_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            ext = img_path.split('.')[-1].lower()
            mime = "image/png" if ext == "png" else "image/jpeg"
            return f"data:{mime};base64,{encoded}"
    except Exception:
        return "https://placehold.co/400x400/111111/ffffff?text=PHOTO+NOT+FOUND"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&family=Space+Grotesk:wght@400;600;700&display=swap');

    .stApp {
        background-color: #050505;
        color: #f0f0f0;
        font-family: 'Space Grotesk', sans-serif;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E");
    }
    
    .st-emotion-cache-1wmy9hl, .st-emotion-cache-1r6slb0, .css-1n76uvr { background-color: transparent !important; }
    
    .product-card {
        background-color: #111111;
        border: 1px solid #222222;
        padding: 1rem;
        margin-bottom: 1.5rem;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .product-card:hover {
        transform: translateY(-5px);
        border-color: #ffffff;
    }
    .product-img { width: 100%; height: 250px; object-fit: cover; border-bottom: 1px solid #222222; margin-bottom: 1rem; }
    .product-brand { font-family: 'Montserrat', sans-serif; font-size: 0.8rem; color: #888888; letter-spacing: 2px; }
    .product-name { font-weight: 700; font-size: 1.1rem; margin: 0.5rem 0; color: #ffffff; }
    .product-price { font-weight: 400; font-size: 1.2rem; color: #f0f0f0; margin-bottom: 1rem; }

    .nox-logo {
        font-family: 'Montserrat', sans-serif; font-weight: 900; font-size: 4rem; letter-spacing: -2px;
        margin-bottom: 0; padding-bottom: 0; color: transparent; -webkit-text-stroke: 1px #ffffff;
        text-transform: uppercase; line-height: 1.1; text-align: center;
    }
    .nox-logo:hover { color: #ffffff; text-shadow: 0 0 40px rgba(255, 255, 255, 0.15); }
    
    .subtitle { color: #888888; font-size: 1rem; font-weight: 600; letter-spacing: 3px; text-align: center; margin-bottom: 30px; }

    h1, h2, h3 { font-family: 'Montserrat', sans-serif; font-weight: 900; text-transform: uppercase; color: #ffffff; }
    p, span { font-family: 'Space Grotesk', sans-serif; }
    
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 40px; border-bottom: 1px solid #222222; margin-bottom: 2rem; }
    .stTabs [data-baseweb="tab"] { height: 60px; background-color: transparent; color: #888888; font-family: 'Montserrat', sans-serif; font-weight: 900; letter-spacing: 2px; font-size: 1.1rem; }
    .stTabs [aria-selected="true"] { color: #ffffff; border-bottom: 3px solid #ffffff; }
    
    .stButton>button {
        background-color: #ffffff; color: #050505; border: 1px solid #ffffff; border-radius: 0px;
        padding: 0.5rem 1rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; width: 100%; transition: all 0.3s;
    }
    .stButton>button:hover { background-color: #050505; color: #ffffff; }
    
    .ticker-wrap { width: 100%; overflow: hidden; background-color: #111111; border-top: 1px solid #222222; border-bottom: 1px solid #222222; padding: 10px 0; margin-bottom: 30px; }
    .ticker { display: inline-block; white-space: nowrap; padding-right: 100%; animation: ticker 25s linear infinite; font-weight: 700; letter-spacing: 3px; color: #888888; }
    @keyframes ticker { 0% { transform: translate3d(0, 0, 0); } 100% { transform: translate3d(-100%, 0, 0); } }
    </style>
""", unsafe_allow_html=True)

# Ticker and Header
st.markdown('<div class="ticker-wrap"><div class="ticker">Nox. URBAN BOUTIQUE ✦ ALPINESTARS ✦ OAKLEY ✦ FOX RACING ✦ Nox. URBAN BOUTIQUE ✦ ALPINESTARS ✦ OAKLEY Nox. URBAN BOUTIQUE ✦ ALPINESTARS ✦ OAKLEY ✦ FOX RACING ✦ Nox. URBAN BOUTIQUE ✦ ALPINESTARS ✦ OAKLEY </div></div>', unsafe_allow_html=True)
st.markdown('<p class="nox-logo">Nox.</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">PREMIUM HEADWEAR SHOP</p>', unsafe_allow_html=True)

# Load Catalog
@st.cache_data
def load_catalog():
    with open('catalog.json', 'r', encoding='utf-8') as f:
        return json.load(f)

catalog = load_catalog()
catalog_owned = catalog[:min(3, len(catalog))]

# Tabs
tab_shop, tab_concierge, tab_vault = st.tabs(["✦ SHOP (CATALOG)", "✦ AI CONCIERGE", "✦ MY VAULT"])

# ==========================================
# TAB 1: SHOP (Real E-commerce)
# ==========================================
with tab_shop:
    st.markdown("<h3 style='text-align:center; margin-bottom: 2rem;'>NEW ARRIVALS</h3>", unsafe_allow_html=True)
    cols = st.columns(5)
    for index, item in enumerate(catalog):
        with cols[index % 5]:
            img_src = get_img_b64(item.get('image', ''))
            st.markdown(f"""
                <div class="product-card">
                    <img src="{img_src}" class="product-img">
                    <p class="product-brand">{item['brand'].upper()}</p>
                    <p class="product-name">{item['name']}</p>
                    <p class="product-price">{item.get('price', '$100.00')}</p>
                </div>
            """, unsafe_allow_html=True)
            st.button("VIEW DETAILS", key=f"btn_shop_{item['id']}")

# ==========================================
# REAL AI ENGINE (Azure Foundry - o4-mini)
# ==========================================
def analyze_outfit_and_recommend(images, catalog_to_search, mode="boutique"):
    st.info("Connecting to Microsoft Foundry IQ [Vision Model: o4-mini]...")
    
    try:
        catalog_clean = [{"id": c["id"], "brand": c["brand"], "name": c["name"], "color": c["color"]} for c in catalog_to_search]
        catalog_text = json.dumps(catalog_clean)
        
        contexto = "You act as a fashion curator for the Nox. boutique." if mode == "boutique" else "You act as a personal stylist scanning the user's vault."
        
        prompt = f"""
        You are the 'Nox. Visual Concierge'. {contexto}
        1. Analyze ALL garments sent in the attached images (e.g. top, bottom, footwear). Identify their colors, textures, and vibe.
        2. Review this catalog of available hats: {catalog_text}
        3. Choose the ID of the hat that acts as the perfect 'visual anchor' to unify the entire outfit using color theory (harmony or contrast) and style.
        
        You must return a JSON object structured exactly like this:
        {{
            "selected_id": "ID_HERE",
            "justification": "Write a deep, fashion-expert paragraph explaining how this hat specifically connects with the multiple garments in the photos."
        }}
        """
        
        content_array = [{"type": "text", "text": prompt}]
        
        for img in images:
            bytes_data = img.getvalue()
            base64_image = base64.b64encode(bytes_data).decode('utf-8')
            content_array.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})
        
        response = client.chat.completions.create(
            model="o4-mini", 
            messages=[
                {
                    "role": "user",
                    "content": content_array
                }
            ],
            response_format={ "type": "json_object" }
        )
        
        raw_response = response.choices[0].message.content.strip()
        ia_data = json.loads(raw_response)
        
        recommended_item = next((item for item in catalog_to_search if item["id"] == ia_data.get("selected_id")), catalog_to_search[0])
        return recommended_item, ia_data.get("justification", "Selection based on the chromatic profile of the entire outfit.")
        
    except json.JSONDecodeError:
        st.error(f"Error parsing AI response. Ensure the model returns only JSON.")
        return catalog_to_search[0], "Technical format error."
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return catalog_to_search[0], "Technical connection error."

def display_recommendation(rec, just):
    st.markdown("---")
    st.markdown("### THE Nox. RECOMMENDATION")
    rc1, rc2 = st.columns([1, 2])
    with rc1:
        img_src = get_img_b64(rec.get('image', ''))
        st.markdown(f"""
            <div style="background-color:#111; border:1px solid #222; padding:1rem; text-align:center;">
                <img src="{img_src}" style="width:100%; height:250px; object-fit:cover; border-bottom:1px solid #222; margin-bottom:1rem;">
                <span style="font-family:'Montserrat', sans-serif; font-weight:900; color:#fff;">{rec['brand'].upper()}</span>
            </div>
        """, unsafe_allow_html=True)
    with rc2:
        st.markdown(f"**PIECE:** <span style='color:#ffffff; font-weight:600;'>{rec['name']}</span>", unsafe_allow_html=True)
        st.markdown(f"**PROFILE:** <span style='color:#888888;'>{', '.join(rec.get('style_tags', [])).upper()}</span>", unsafe_allow_html=True)
        st.markdown(f"**PRICE:** <span style='color:#ffffff;'>{rec.get('price', '$100.00')}</span>", unsafe_allow_html=True)
        st.markdown(f"**JUSTIFICATION:** <span style='color:#888888;'>{just}</span>", unsafe_allow_html=True)
        if st.button("ADD TO CART", key=f"add_cart_{rec['id']}"):
            st.success("Successfully added to cart.")

# ==========================================
# TAB 2: AI CONCIERGE
# ==========================================
with tab_concierge:
    st.markdown("<p style='text-align:center; color:#888;'>Upload your outfit. Our AI will scan our catalog and select the perfect hat for your style.</p>", unsafe_allow_html=True)
    up_concierge = st.file_uploader("Select images (Max 3)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, key="up_c")
    if up_concierge:
        cols = st.columns(len(up_concierge[:3]))
        for idx, file in enumerate(up_concierge[:3]):
            cols[idx].image(Image.open(file), use_container_width=True)
        if st.button("REQUEST VISUAL CURATION", key="btn_c"):
            with st.spinner("Processing request in Microsoft Foundry IQ..."):
                rec, just = analyze_outfit_and_recommend(up_concierge, catalog, mode="boutique")
                display_recommendation(rec, just)

# ==========================================
# TAB 3: MY VAULT
# ==========================================
with tab_vault:
    st.markdown(f"<p style='text-align:center; color:#888;'>You have <span style='color:#fff; font-weight:bold;'>{len(catalog_owned)} pieces</span> in your collection. What will you wear today?</p>", unsafe_allow_html=True)
    
    cols_v = st.columns(len(catalog_owned))
    for i, item in enumerate(catalog_owned):
        with cols_v[i]:
            img_src = get_img_b64(item.get('image', ''))
            st.markdown(f"<div style='border:1px solid #222; padding:10px; text-align:center;'><img src='{img_src}' style='width:100%; height:150px; object-fit:cover;'><br><span style='font-size:0.8rem; color:#888;'>{item['name']}</span></div>", unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    up_vault = st.file_uploader("Upload today's outfit", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True, key="up_v")
    if up_vault:
        st.write("### TODAY'S OUTFIT:")
        cols = st.columns(len(up_vault[:3]))
        for idx, file in enumerate(up_vault[:3]):
            cols[idx].image(Image.open(file), use_container_width=True)
        if st.button("ASSIGN ITEM OF THE DAY", key="btn_v"):
            with st.spinner("Scanning Personal Vault..."):
                rec, just = analyze_outfit_and_recommend(up_vault, catalog_owned, mode="coleccion")
                display_recommendation(rec, just)