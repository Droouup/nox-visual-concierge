# Nox. Smart Vision Stylist Agent 🎩

> **Scanning your style. Curating your perfect Nox. match.**

🎥 Demo Video   
See the multimodal AI stylist in action:

👉 https://youtu.be/XCbwfmtgCu8 👈


**Nox. Visual Concierge** is an innovative, multimodal AI-powered styling assistant and multi-brand luxury curator built exclusively for the **Agents League Hackathon (2026)**.

---

### 🏆 Hackathon Details
- **Track:** Reasoning Agents
- **AI Intelligence Layer:** Microsoft Foundry IQ
- **Core Model:** o4-mini

---

## 📖 The Vision
In fashion e-commerce, customers often struggle to visualize how an accessory will fit into their existing wardrobe. Traditional recommendation systems rely on basic text searches or generic tags. 

**Nox.** transforms this experience. Moving beyond standard chatbots, it acts as an exclusive visual concierge for high-end headwear (featuring premium brands like Fox, Alpinestars, and Oakley). It bridges the gap between a customer's daily wardrobe and our digital storefront using advanced visual reasoning.

## 🧠 Core Architecture (Multi-Step Reasoning)
Our agent doesn't just "see" an image; it understands fashion aesthetics through a multi-step logical pipeline:

1. **👀 Vision Analysis:** Extracts dominant color palettes, textures, and lifestyle aesthetics (e.g., urban, racing, minimalist) from user-uploaded outfit photos.
2. **🔐 Secure Knowledge Retrieval:** Leverages **Microsoft Foundry IQ** to query our verified enterprise catalog (`catalog.json`) without exposing raw data.
3. **🎯 Curated Recommendation:** Cross-references the visual semantics with the grounded catalog data to return a highly personalized, logically sound recommendation based on complementary color theory.

## ✨ Key Features
- **Zero-Hallucination Curation:** Grounded strictly in the available catalog via Foundry IQ.
- **Multimodal Understanding:** Powered by `o4-mini` to seamlessly process complex visual context.
- **Premium Dark UI:** A sleek, minimalist interface built with Streamlit, honoring the Nox. brandbook guidelines (Space Grotesk & Montserrat fonts, noise textures).

## 🛠️ Tech Stack
- **Frontend / UI:** Streamlit (Python)
- **Backend / Reasoning:** Python 3.x
- **AI / LLM:** Microsoft Foundry IQ (Powered by o4-mini)
- **Data Structure:** JSON

---

## 🚀 Quick Start (Run Locally)

Want to see the concierge in action? Follow these steps:

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd nox-hackathon
```

**2. Set up a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install streamlit pillow
```

4. Add your API Keys
(Create a .env file in the root directory and add your Microsoft Foundry credentials securely).

5. Run the application
```bash
streamlit run app.py
```


📜 Disclaimer
This project is submitted for the Agents League Hackathon. No confidential, sensitive, or proprietary user information is included in this repository.