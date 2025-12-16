import streamlit as st
import qrcode
from io import BytesIO
import uuid

# ---- QR generation function ----
def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# ---- Streamlit UI ----
st.set_page_config(page_title="Metro Ticket Booking")
st.title("🚇 Metro Ticket Booking System")

stations = ["Ameerpet", "KPHB", "JNTU", "Balanagar", "Jubilee Hills"]

name = st.text_input("Passenger Name")
source = st.selectbox("Source Station", stations)
destination = st.selectbox("Destination Station", stations)
no_tickets = st.number_input("Number of Tickets", min_value=1, value=1)

price_per_ticket = 30
total_amount = no_tickets * price_per_ticket
st.info(f"Total Amount: ₹{total_amount}")

# ---- Booking Button ----
if st.button("Book Ticket"):
    if name.strip() == "":
        st.error("Please enter passenger name")
    elif source == destination:
        st.error("Source and destination cannot be the same")
    else:
        booking_id = str(uuid.uuid4())[:8]

        qr_data = (
            f"Booking ID: {booking_id}\n"
            f"Name: {name}\n"
            f"From: {source}\n"
            f"To: {destination}\n"
            f"Tickets: {no_tickets}\n"
            f"Amount: ₹{total_amount}"
        )

        qr_img = generate_qr(qr_data)
        buf = BytesIO()
        qr_img.save(buf, format="PNG")

        st.success("✅ Ticket booked successfully!")
        st.write(f"**Booking ID:** {booking_id}")
        st.write(f"**Passenger Name:** {name}")
        st.write(f"**From:** {source}")
        st.write(f"**To:** {destination}")
        st.write(f"**Tickets:** {no_tickets}")
        st.write(f"**Amount Paid:** ₹{total_amount}")
        st.image(buf.getvalue(), width=250, caption="Metro Ticket QR")

