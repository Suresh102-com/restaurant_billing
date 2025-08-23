import io
import pandas as pd
import streamlit as st
from utils.calculator import calc_order_total, order_to_df
from utils.db_utils import save_order
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Hide Streamlit Deploy, hamburger menu, and footer 
hide_streamlit_style = """ 
    <style> 
        #MainMenu {visibility: hidden;} /* hide hamburger menu */
        header {visibility: hidden;} /* hide Streamlit header (Deploy button lives here) */ 
        footer {visibility: hidden;} /* hide footer */
    </style> 
""" 
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- Default menu ---
DEFAULT_MENU = pd.DataFrame(
    {
        "item": ["Masala Dosa", "Paneer Tikka", "Veg Biryani", "Idli Sambhar", "Chai"],
        "price": [120.0, 220.0, 180.0, 80.0, 25.0],
    }
)

def money(x: float) -> str:
    return f"₹{x:,.2f}"

def run_ui():
    st.set_page_config(page_title="Restaurant_Billing", page_icon="🍽️", layout="wide")

    # Initialize session
    if "menu_df" not in st.session_state:
        st.session_state.menu_df = DEFAULT_MENU.copy()
    if "order" not in st.session_state:
        st.session_state.order = {}
    if "mode" not in st.session_state:
        st.session_state.mode = "Dine-In"
    if "meta" not in st.session_state:
        st.session_state.meta = {"table_no": "", "customer_name": ""}
    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Page navigation
    if st.session_state.page == "home":
        show_home()
    elif st.session_state.page == "payment":
        show_payment()

def go_to(page: str):
    st.session_state.page = page
    st.rerun()

# --- Home Page ---
def show_home():
    st.title("🍽️ Restaurant Billing")

    # Sidebar menu
    with st.sidebar:
        st.subheader("Current Menu")
        st.dataframe(st.session_state.menu_df, use_container_width=True, hide_index=True)

    left, right = st.columns([1, 1])

    with left:
        st.subheader("Order Mode")
        st.session_state.mode = st.radio("Select:", ["Dine-In", "Takeaway"], horizontal=True)
        if st.session_state.mode == "Dine-In":
            st.session_state.meta["table_no"] = st.text_input("Table No.", value=st.session_state.meta.get("table_no",""))
        else:
            st.session_state.meta["customer_name"] = st.text_input("Customer Name", value=st.session_state.meta.get("customer_name",""))

        st.subheader("Add Items")
        menu_df = st.session_state.menu_df
        if not menu_df.empty:
            item_names = menu_df["item"].tolist()
            selected_item = st.selectbox("Item", options=item_names)
            selected_price = float(menu_df.loc[menu_df["item"] == selected_item, "price"].iloc[0])
            qty = st.number_input("Quantity", min_value=1, max_value=20, value=1)
            if st.button("➕ Add to Order"):
                if selected_item in st.session_state.order:
                    st.session_state.order[selected_item]["qty"] += qty
                else:
                    st.session_state.order[selected_item] = {"price": selected_price, "qty": qty}
                st.toast(f"Added {qty} × {selected_item}", icon="🍽️")

    with right:
        st.subheader("Current Order")
        df = order_to_df(st.session_state.order)
        if df.empty:
            st.info("No items added yet.")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)
            total = calc_order_total(st.session_state.order)
            st.subheader(f"Running Total: {money(total)}")

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🧹 Clear Order"):
                    st.session_state.order = {}
                    st.rerun()
            with c2:
                st.download_button("🧾 Download Bill (CSV)", df.to_csv(index=False), file_name="bill.csv")
            with c3:
                if st.button("✅ Confirm Your Order"):
                    go_to("payment")

# --- Payment Page ---
def show_payment():
    # Back button on top-left 
    back_col, _, _ = st.columns([1,4,1])
    with back_col:
        if st.button("⬅️ Back", use_container_width=True):
            go_to("home")
    st.title("💳 Payment Page")
    method = st.radio("Payment Method", ["Cash", "Card", "UPI"], horizontal=True)
    if st.button("✅ Complete Payment", use_container_width=True):
        total = calc_order_total(st.session_state.order)
        save_order(
            st.session_state.mode,
            st.session_state.meta.get("customer_name"),
            st.session_state.meta.get("table_no"),
            str(st.session_state.order),
            total,
            method
        )

        

        st.success(f"Payment successful via {method} | Total: {money(total)}")
        st.session_state.order = {}
        go_to("home")
