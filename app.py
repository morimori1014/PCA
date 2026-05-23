import streamlit as st

st.set_page_config(page_title="PCA投与量計算ツール", layout="centered")

st.title("PCA投与量計算ツール")
st.caption("ダブルチェック用（希釈後濃度ベース）")

st.header("入力")

col1, col2 = st.columns(2)

with col1:
    ampoule_mg = st.number_input("アンプル量 (mg)", min_value=0, step=1, value=20)
    ampoule_ml = st.number_input("アンプル容量 (mL)", min_value=0, step=1, value=2)
    ampoules = st.number_input("使用本数", min_value=0, step=1, value=1)

with col2:
    saline_ml = st.number_input("生理食塩水 (mL)", min_value=0, step=1, value=48)
    rate_ml_h = st.number_input("投与速度 (mL/h)", min_value=0.0, step=0.01, value=0.10)

st.divider()

st.subheader("追加機能（PCA確認）")
bolus_equiv_h = st.number_input("1回ドーズ量（何時間分か）", min_value=0, step=0.5)
freq_per_day = st.number_input("1日平均使用回数（回/日）", min_value=0, step=1)

st.divider()

# --- 計算 ---
total_mg = ampoule_mg * ampoules
total_ml = ampoule_ml * ampoules + saline_ml

if total_ml > 0:
    concentration = total_mg / total_ml
else:
    concentration = 0

mg_per_h = concentration * rate_ml_h
mg_per_day = mg_per_h * 24

# --- PCA bolus model ---
# bolus = basal mg/h × bolus_equiv_h
# average bolus rate = bolus × freq/24
# total consumption = basal + bolus contribution
if mg_per_h > 0:
    consumption_rate = mg_per_h * (1 + (bolus_equiv_h * freq_per_day / 24))
else:
    consumption_rate = 0

if consumption_rate > 0:
    time_to_empty = total_mg / consumption_rate
else:
    time_to_empty = 0

st.header("結果")

st.write(f"**Total量:** {total_ml:.0f} mL")
st.write(f"**濃度:** {concentration:.2f} mg/mL")
st.write(f"**1時間投与量:** {mg_per_h:.2f} mg/h")
st.write(f"**1日投与量:** {mg_per_day:.2f} mg/day")

st.divider()

st.subheader("PCA評価")
st.write(f"**想定枯渇時間:** {time_to_empty:.1f} 時間")

if bolus_equiv_h > 0 and freq_per_day > 0:
    st.write(f"**ボーラス負荷係数:** {1 + (bolus_equiv_h * freq_per_day / 24):.2f} 倍")

    if (1 + (bolus_equiv_h * freq_per_day / 24)) > 1.5:
        st.warning("ボーラス使用により消費が大きく増加する可能性があります")

st.caption("※本ツールはダブルチェック補助目的です。最終判断は医療プロトコルに従ってください")
