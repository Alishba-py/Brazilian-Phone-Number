import streamlit as st
import random
import pandas as pd
from io import BytesIO
from fpdf import FPDF

# Function to generate Brazilian phone numbers
def generate_brazilian_phone_numbers(quantity):
    phone_numbers = []
    for _ in range(quantity):
        area_code = random.randint(11, 99)
        prefix = random.choice(["9", ""])
        if prefix == "9":
            number = f"{prefix}{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        else:
            number = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        phone_numbers.append(f"({area_code}) {number}")
    return phone_numbers

# Function to create a PDF
def create_pdf(phone_numbers):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Brazilian Phone Numbers", ln=True, align="C")
    pdf.ln(10)
    for number in phone_numbers:
        pdf.cell(0, 10, txt=number, ln=True)
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    return pdf_output.getvalue()

# Streamlit app
st.title("Brazilian Phone Number Generator")

quantity = st.number_input("Enter the number of phone numbers to generate:", min_value=1, max_value=100000, value=10)

if st.button("Generate"):
    st.write("Generating phone numbers...")
    numbers = generate_brazilian_phone_numbers(quantity)
    st.success("Phone numbers generated successfully!")
    st.write(numbers)
    
    # Convert to DataFrame for CSV/Excel
    df = pd.DataFrame({"Phone Numbers": numbers})
    
    # TXT Download
    file_content_txt = "\n".join(numbers)
    st.download_button(
        label="Download as TXT",
        data=file_content_txt,
        file_name="brazilian_phone_numbers.txt",
        mime="text/plain",
    )
    
    # CSV Download
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download as CSV",
        data=csv_data,
        file_name="brazilian_phone_numbers.csv",
        mime="text/csv",
    )
    
    # Excel Download
    excel_data = BytesIO()
    with pd.ExcelWriter(excel_data, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Phone Numbers")
    excel_data.seek(0)
    st.download_button(
        label="Download as Excel",
        data=excel_data,
        file_name="brazilian_phone_numbers.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    
    # PDF Download
    pdf_data = create_pdf(numbers)
    st.download_button(
        label="Download as PDF",
        data=pdf_data,
        file_name="brazilian_phone_numbers.pdf",
        mime="application/pdf",
    )
