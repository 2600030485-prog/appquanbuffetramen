import streamlit as st
from datetime import datetime
import uuid

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Ramen Buffet",
    page_icon="🍜",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #fff8ef;
}
h1, h2, h3 {
    color: #a52a2a;
}
.stButton>button {
    background-color: #a52a2a;
    color: white;
    border-radius: 10px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("🍜 RAMEN BUFFET")
st.subheader("Nhà hàng mì Ramen tự chọn")
st.divider()

# =========================
# MENU VÀ GIÁ
# =========================
buffet = {
    "Buffet cơ bản": 129000,
    "Buffet đặc biệt": 169000,
    "Buffet cao cấp": 219000
}

toppings = [
    "Thịt Chashu",
    "Trứng lòng đào",
    "Rong biển",
    "Bắp ngọt",
    "Nấm",
    "Kim chi",
    "Phô mai"
]

mon_an = {
    "Gyoza": 30000,
    "Takoyaki": 35000,
    "Tempura": 40000,
    "Karaage": 45000
}

do_uong = {
    "Trà xanh": 15000,
    "Trà đào": 20000,
    "Nước ngọt": 15000,
    "Nước suối": 10000
}

ramen = [
    "Shoyu Ramen",
    "Miso Ramen",
    "Tonkotsu Ramen",
    "Spicy Ramen",
    "Seafood Ramen"
]

# =========================
# THÔNG TIN KHÁCH HÀNG
# =========================
st.header("1. Thông tin khách hàng")

col1, col2 = st.columns(2)

with col1:
    ten_khach = st.text_input("Tên khách hàng")

with col2:
    sdt = st.text_input("Số điện thoại")

col3, col4 = st.columns(2)

with col3:
    nguoi_lon = st.number_input(
        "Số lượng người lớn",
        min_value=0,
        value=1
    )

with col4:
    tre_em = st.number_input(
        "Số lượng trẻ em",
        min_value=0,
        value=0
    )

# =========================
# CHỌN BUFFET
# =========================
st.header("2. Chọn gói Buffet")

goi_buffet = st.selectbox(
    "Loại Buffet",
    list(buffet.keys())
)

gia_buffet = buffet[goi_buffet]

st.info(f"Giá Buffet: {gia_buffet:,} VNĐ/người")

# =========================
# CHỌN MÓN RAMEN
# =========================
st.header("3. Chọn món Ramen")

mon_ramen = st.multiselect(
    "Chọn loại mì yêu thích",
    ramen
)

do_cay = st.selectbox(
    "Mức độ cay",
    ["Không cay", "Ít cay", "Cay vừa", "Cay nhiều"]
)

nuoc_dung = st.selectbox(
    "Nước dùng",
    ["Nhẹ", "Vừa", "Đậm"]
)

# =========================
# CHỌN TOPPING MIỄN PHÍ
# =========================
st.header("4. Chọn Topping miễn phí")

chon_topping = st.multiselect(
    "Chọn các loại topping yêu thích",
    toppings
)

st.caption("Topping được phục vụ miễn phí trong gói Buffet.")

# =========================
# MÓN ĂN VÀ ĐỒ UỐNG
# =========================
st.header("5. Món ăn và đồ uống gọi thêm")

col5, col6 = st.columns(2)

with col5:
    chon_mon = st.multiselect(
        "Món ăn kèm",list(mon_an.keys())
    )

with col6:
    chon_nuoc = st.multiselect(
        "Đồ uống",
        list(do_uong.keys())
    )

st.divider()

# =========================
# TÍNH TIỀN
# =========================
st.header("6. Thanh toán")

tien_buffet = (nguoi_lon + tre_em) * gia_buffet

tien_mon = sum(mon_an[x] for x in chon_mon)
tien_nuoc = sum(do_uong[x] for x in chon_nuoc)

tam_tinh = tien_buffet + tien_mon + tien_nuoc

giam_gia = st.number_input(
    "Giảm giá (%)",
    min_value=0,
    max_value=100,
    value=0
)

vat = st.number_input(
    "VAT (%)",
    min_value=0,
    max_value=100,
    value=8
)

tien_giam = tam_tinh * giam_gia / 100
sau_giam = tam_tinh - tien_giam
tien_vat = sau_giam * vat / 100
tong_tien = sau_giam + tien_vat

st.write(f"Tiền Buffet: {tien_buffet:,.0f} VNĐ")
st.write(f"Tiền món ăn: {tien_mon:,.0f} VNĐ")
st.write(f"Tiền đồ uống: {tien_nuoc:,.0f} VNĐ")
st.write(f"Giảm giá: -{tien_giam:,.0f} VNĐ")
st.write(f"VAT: {tien_vat:,.0f} VNĐ")

st.markdown(
    f"## Tổng thanh toán: {tong_tien:,.0f} VNĐ"
)

# =========================
# THANH TOÁN
# =========================
phuong_thuc = st.selectbox(
    "Phương thức thanh toán",
    ["Tiền mặt", "Chuyển khoản"]
)

ghi_chu = st.text_area("Ghi chú đơn hàng")

if st.button("💳 THANH TOÁN"):

    if not ten_khach.strip():
        st.error("Vui lòng nhập tên khách hàng!")

    elif nguoi_lon + tre_em == 0:
        st.error("Vui lòng nhập số lượng khách!")

    else:
        ma_hd = str(uuid.uuid4())[:8].upper()
        ngay = datetime.now().strftime("%d/%m/%Y %H:%M")

        hoa_don = f"""
================================
          RAMEN BUFFET
================================

Mã hóa đơn: {ma_hd}
Ngày lập: {ngay}

THÔNG TIN KHÁCH HÀNG
Tên: {ten_khach}
Số điện thoại: {sdt}
Người lớn: {nguoi_lon}
Trẻ em: {tre_em}

GÓI BUFFET
{goi_buffet}: {gia_buffet:,} VNĐ/người

MÓN RAMEN
{', '.join(mon_ramen) or 'Không chọn'}

Độ cay: {do_cay}
Nước dùng: {nuoc_dung}

TOPPING MIỄN PHÍ
{', '.join(chon_topping) or 'Không chọn'}

MÓN ĂN KÈM
{', '.join(chon_mon) or 'Không chọn'}

ĐỒ UỐNG
{', '.join(chon_nuoc) or 'Không chọn'}

================================
CHI TIẾT THANH TOÁN

Tiền Buffet: {tien_buffet:,.0f} VNĐ
Tiền món ăn: {tien_mon:,.0f} VNĐ
Tiền đồ uống: {tien_nuoc:,.0f} VNĐ
Tạm tính: {tam_tinh:,.0f} VNĐ
Giảm giá: {tien_giam:,.0f} VNĐ
VAT: {tien_vat:,.0f} VNĐ

TỔNG THANH TOÁN:
{tong_tien:,.0f} VNĐ

Phương thức: {phuong_thuc}
Ghi chú: {ghi_chu}

================================
       CẢM ƠN QUÝ KHÁCH!
================================
"""

        st.session_state["hoa_don"] = hoa_don

        st.success("Thanh toán thành công!")

# =========================
# HIỂN THỊ VÀ XUẤT HÓA ĐƠN
# =========================
if "hoa_don" in st.session_state:

    st.header("🧾 HÓA ĐƠN THANH TOÁN")

    st.text(st.session_state["hoa_don"])

    st.download_button(
        label="📥 Tải hóa đơn",
        data=st.session_state["hoa_don"],
        file_name="hoa_don_ramen.txt",
        mime="text/plain"
    )

    if st.button("🔄 Tạo hóa đơn mới"):
        del st.session_state["hoa_don"]
        st.rerun()
