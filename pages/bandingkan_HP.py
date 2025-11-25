import streamlit as st

# ==========================
# DATA HP (TANPA API)
# ==========================
phones = [
    {
        "phoneDetails": {
            "customId": 103001,
            "yearValue": "2022",
            "brandValue": "Samsung",
            "modelValue": "Galaxy S22 Ultra 5G"
        },
        "gsmPlatformDetails": {
            "platformChipset": "Qualcomm Snapdragon 8 Gen 1"
        },
        "gsmMemoryDetails": {
            "memoryInternal": "12GB RAM, 256GB storage"
        },
        "gsmMainCameraDetails": {
            "mainCameraQuad": "108 MP (wide), 10 MP (periscope), 10 MP (telephoto), 12 MP (ultrawide)"
        },
        "gsmBatteryDetails": {
            "batteryType": "Li-Ion 5000 mAh"
        }
    },
    {
        "phoneDetails": {
            "customId": 103002,
            "yearValue": "2021",
            "brandValue": "Apple",
            "modelValue": "iPhone 13 Pro Max"
        },
        "gsmPlatformDetails": {
            "platformChipset": "Apple A15 Bionic"
        },
        "gsmMemoryDetails": {
            "memoryInternal": "6GB RAM, 256GB storage"
        },
        "gsmMainCameraDetails": {
            "mainCameraQuad": "12 MP (wide), 12 MP (telephoto), 12 MP (ultrawide)"
        },
        "gsmBatteryDetails": {
            "batteryType": "Li-Ion 4352 mAh"
        }
    },
    {
        "phoneDetails": {
            "customId": 103003,
            "yearValue": "2021",
            "brandValue": "Xiaomi",
            "modelValue": "Mi 11 Ultra"
        },
        "gsmPlatformDetails": {
            "platformChipset": "Qualcomm Snapdragon 888"
        },
        "gsmMemoryDetails": {
            "memoryInternal": "12GB RAM, 256GB storage"
        },
        "gsmMainCameraDetails": {
            "mainCameraQuad": "50 MP (wide), 48 MP (periscope), 48 MP (ultrawide)"
        },
        "gsmBatteryDetails": {
            "batteryType": "Li-Ion 5000 mAh"
        }
    }
]


# ==========================
# UTILITY FUNCTIONS
# ==========================
def get_phone_by_name(name):
    """Cari HP berdasarkan modelValue"""
    for hp in phones:
        if hp["phoneDetails"].get("modelValue") == name:
            return hp
    return None


def format_phone_for_display(hp):
    """Format dict HP jadi data readable"""
    details = hp.get("phoneDetails", {})
    data = {
        "Phone Name": details.get("modelValue", "N/A"),
        "Brand": details.get("brandValue", "N/A"),
        "Year": details.get("yearValue", "N/A")
    }

    for category, values in hp.items():
        if category == "phoneDetails":
            continue
        if isinstance(values, dict):
            for key, value in values.items():
                label = f"{category} - {key}"
                data[label] = value
    return data


def generate_simple_analysis(hp1, hp2):
    d1 = hp1["phoneDetails"]
    d2 = hp2["phoneDetails"]

    chipset1 = hp1["gsmPlatformDetails"].get("platformChipset", "N/A")
    chipset2 = hp2["gsmPlatformDetails"].get("platformChipset", "N/A")

    ram1 = hp1["gsmMemoryDetails"].get("memoryInternal", "N/A")
    ram2 = hp2["gsmMemoryDetails"].get("memoryInternal", "N/A")

    cam1 = hp1["gsmMainCameraDetails"].get("mainCameraQuad", "N/A")
    cam2 = hp2["gsmMainCameraDetails"].get("mainCameraQuad", "N/A")

    bat1 = hp1["gsmBatteryDetails"].get("batteryType", "N/A")
    bat2 = hp2["gsmBatteryDetails"].get("batteryType", "N/A")

    return f"""
## 📊 Analisis Singkat

### {d1['modelValue']} vs {d2['modelValue']}

| Fitur | {d1['modelValue']} | {d2['modelValue']} |
|-------|----------------------|----------------------|
| Tahun Rilis | {d1['yearValue']} | {d2['yearValue']} |
| Chipset | {chipset1} | {chipset2} |
| RAM/Storage | {ram1} | {ram2} |
| Kamera | {cam1} | {cam2} |
| Baterai | {bat1} | {bat2} |
"""


# ==========================
# STREAMLIT UI
# ==========================
st.title("📱 Bandingkan Dua HP (Offline / No API)")
st.markdown("---")

hp_names = [hp["phoneDetails"]["modelValue"] for hp in phones]

# Dropdown Select
col1, col2 = st.columns(2)
with col1:
    hp1_name = st.selectbox("Pilih HP Pertama", hp_names)

with col2:
    hp2_name = st.selectbox("Pilih HP Kedua", [n for n in hp_names if n != hp1_name])

# Button
if st.button("🔍 Bandingkan", type="primary"):
    hp1 = get_phone_by_name(hp1_name)
    hp2 = get_phone_by_name(hp2_name)

    colA, colB = st.columns(2)

    with colA:
        st.markdown(f"### {hp1_name}")
        st.json(format_phone_for_display(hp1))

    with colB:
        st.markdown(f"### {hp2_name}")
        st.json(format_phone_for_display(hp2))

    st.markdown("---")
    st.markdown(generate_simple_analysis(hp1, hp2))
