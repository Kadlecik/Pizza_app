# receipt_generator.py
from fpdf import FPDF
import os


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Receipt', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()


def create_receipt(pizza):
    # Ujistíme se, že složka 'receipts' existuje
    if not os.path.exists('receipts'):
        os.makedirs('receipts')

    pdf = PDF()
    pdf.add_page()

    # Title
    pdf.chapter_title('Order Receipt')

    # Order details
    details = f"""
    Order for: {pizza.name}
    Payment Method: {pizza.payment_method}
    Price: ${pizza.price:.2f}
    Paid: {'Yes' if pizza.paid else 'No'}
    Created At: {pizza.created_at.strftime('%Y-%m-%d %H:%M:%S')}
    """
    pdf.chapter_body(details)

    # Save the PDF
    receipt_filename = f"receipts/receipt_{pizza.created_at.strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(receipt_filename)
    print(f"Receipt saved as {receipt_filename}")
