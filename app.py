import streamlit as st

st.set_page_config(page_title="PCA投与量計算ツール", layout="centered")

st.title("PCA投与量計算ツール")
st.caption("ダブルチェック用（希釈後濃度ベース）")

st.header("入力")

col1, col2 = st.columns(2)

with col1:
    ampoule_mg = st.number_input("アンプル量 (mg)", min_value=0.0, step=1.0)
    ampoule_ml = st.number_input("アンプル容量 (mL)", min_value=0.0, step=0.1)
    ampoules = st.number_input("使用本数", min_value=0.0, step=1.0)

with col2:
    saline_ml = st.number_input("生理食塩水 (mL)", min_value=0.0, step=1.0)
    rate_ml_h = st.number_input("投与速度 (mL/h)", min_value=0.0, step=0.01)

st.divider()

st.subheader("追加機能（PCA確認）")
dose_mg = st.number_input("1回ドーズ量 (mg)", min_value=0.0, step=0.1)
freq_per_day = st.number_input("1日使用回数（回/日）", min_value=0.0, step=1.0)

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

if mg_per_h > 0 and dose_mg > 0:
    duration_h = dose_mg / mg_per_h
else:
    duration_h = 0

if freq_per_day > 0:
    interval_h = 24 / freq_per_day
else:
    interval_h = 0

st.header("結果")

st.write(f"**Total量:** {total_ml:.2f} mL")
st.write(f"**濃度:** {concentration:.4f} mg/mL")
st.write(f"**1時間投与量:** {mg_per_h:.4f} mg/h")
st.write(f"**1日投与量:** {mg_per_day:.4f} mg/day")

st.divider()

st.subheader("PCA確認")
st.write(f"**1回投与持続時間:** {duration_h:.2f} 時間")
st.write(f"**使用間隔（理論）:** {interval_h:.2f} 時間")

if duration_h > 0 and interval_h > 0:
    coverage = duration_h / interval_h
    st.write(f"**カバー率（目安）:** {coverage:.2f}")

    if coverage < 1:
        st.warning("投与間隔より効果持続が短い可能性があります")
    else:
        st.success("持続時間は使用間隔をカバーしています")

st.caption("※本ツールはダブルチェック補助目的です。最終判断は医療プロトコルに従ってください")