import streamlit as st

# Cấu hình giao diện trang web
st.set_page_config(
    page_title="Etostavich Screening Model", page_icon="⚠️", layout="centered"
)


def calculate_et(N, molar_mass, V, t, s):
  # Tính hệ số tỉ khối so với không khí (d_MA / 29)
  specific_gravity = molar_mass / 29.0
  # Công thức hằng số et
  et = (N * specific_gravity) / (V * t * s)
  return et, specific_gravity


def evaluate_risk(et_value):
  # Hệ thống ngưỡng chuẩn hóa (Calibration Thresholds)
  if et_value > 1e22:
    return (
        "VÙNG TỬ ĐỊA CẤP TÍNH (Đỏ)",
        "Tổn thương hô hấp cực nặng, tử vong tức thì trong vài giây đầu.",
    )
  elif et_value > 1e20:
    return (
        "VÙNG NGUY HIỂM CỰC ĐỘ (Cam)",
        "Gây co thắt thanh quản, phù phổi cấp, cần sơ tán khẩn cấp.",
    )
  elif et_value > 1e18:
    return (
        "VÙNG KÍCH ỨNG MẠNH (Vàng)",
        "Gây cay mắt, ho sặc sụa, kích ứng đường thở rõ rệt.",
    )
  else:
    return (
        "VÙNG AN TOÀN / DƯỚI NGƯỠNG (Xanh)",
        "Nồng độ thấp, không gây nguy hiểm cấp tính.",
    )


# Giao diện ứng dụng
st.title("🚨 Mô hình Sàng lọc Xung lực Thảm họa Etostavich")
st.markdown(
    "Công cụ đánh giá rủi ro nhanh tại mốc xung lực **t = 1 giây** cho sự cố"
    " phát thải khí độc / công nghiệp."
)
st.divider()

# Khu vực nhập liệu
col1, col2 = st.columns(2)

with col1:
  N = st.number_input(
      "Tổng số hạt phát thải (N)", value=1.2044e24, format="%e"
  )
  molar_mass = st.number_input(
      "Khối lượng mol chất (g/mol)",
      value=71.0,
      help="Ví dụ: Cl2 = 71, CO = 28",
  )

with col2:
  V = st.number_input(
      "Thể tích buồng/không gian (m³)", value=30.0, format="%.2f"
  )
  s = st.number_input(
      "Khoảng cách từ tâm chấn (m)",
      value=1.0,
      min_value=0.1,
      format="%.2f",
  )

# Mốc thời gian cố định cho kịch bản tồi tệ nhất
t = 1.0

st.markdown("<br>", unsafe_allow_html=True)

# Nút thực thi tính toán
if st.button("Chạy mô phỏng tính toán et", type="primary", use_container_width=True):
  et_res, sg = calculate_et(N, molar_mass, V, t, s)
  zone, description = evaluate_risk(et_res)

  st.divider()
  st.subheader("📊 Kết quả phân tích mô hình")

  col_res1, col_res2 = st.columns(2)
  with col_res1:
    st.metric(label="Hằng số xung lực et", value=f"{et_res:.2e}")
  with col_res2:
    st.metric(label="Hệ số tỉ khối (d/29)", value=f"{sg:.3f}")

  # Hiển thị cảnh báo trực quan theo cấp độ màu
  if "Đỏ" in zone:
    st.error(f"**CẢNH BÁO: {zone}**\n\n{description}")
  elif "Cam" in zone:
    st.warning(f"**CẢNH BÁO: {zone}**\n\n{description}")
  elif "Vàng" in zone:
    st.info(f"**LƯU Ý: {zone}**\n\n{description}")
  else:
    st.success(f"**THÔNG BÁO: {zone}**\n\n{description}")
