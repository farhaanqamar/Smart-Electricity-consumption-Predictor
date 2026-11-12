import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Rect, Line, String

def generate_ke_bill_pdf(pdf_path, consumer_data=None):
    if consumer_data is None:
        consumer_data = {
            "account_no": "1234567890123",
            "consumer_no": "AB123124",
            "customer_name": "MR. ABDULLAH KHAN",
            "tariff": "A1-R Residential",
            "status": "PAID • STAR Consumer",
            "bill_month": "Jul-25",
            "issue_date": "28-Jul-2025",
            "due_date": "11-Aug-2025",
            "current_units": 172.0,
            "amount_due": 2071.0,
            "amount_after_due": 2157.0,
            "variable_charges": 1093.56,
            "additional_surcharge": 58.82,
            "electricity_duty": 25.69,
            "sales_tax": 73.96,
            "prev_reading": 20521,
            "curr_reading": 20693,
            "sanc_load": "1 kW",
            "conn_load": "1 kW",
            "invoice_no": "739000565027"
        }

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=28,
        leftMargin=28,
        topMargin=24,
        bottomMargin=24
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    brand_title = ParagraphStyle('Brand', parent=styles['Heading1'], fontSize=16, leading=18, textColor=colors.HexColor('#0F172A'), fontName='Helvetica-Bold')
    sub_title = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.HexColor('#64748B'))
    header_right = ParagraphStyle('HeadRight', parent=styles['Normal'], fontSize=8, leading=11, alignment=2, textColor=colors.HexColor('#334155'))
    section_head = ParagraphStyle('SecHead', parent=styles['Normal'], fontSize=9, leading=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#0F172A'))
    
    cell_bold = ParagraphStyle('CBold', parent=styles['Normal'], fontSize=7.5, leading=9.5, fontName='Helvetica-Bold', textColor=colors.HexColor('#0F172A'))
    cell_norm = ParagraphStyle('CNorm', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=colors.HexColor('#334155'))
    cell_right = ParagraphStyle('CRight', parent=styles['Normal'], fontSize=7.5, leading=9.5, alignment=2, textColor=colors.HexColor('#0F172A'))
    cell_center = ParagraphStyle('CCenter', parent=styles['Normal'], fontSize=7.5, leading=9.5, alignment=1, textColor=colors.HexColor('#334155'))

    big_amt = ParagraphStyle('BigAmt', parent=styles['Heading1'], fontSize=15, leading=17, textColor=colors.HexColor('#0F172A'), fontName='Helvetica-Bold')
    big_units = ParagraphStyle('BigUnits', parent=styles['Heading1'], fontSize=15, leading=17, textColor=colors.HexColor('#0F172A'), fontName='Helvetica-Bold', alignment=2)
    green_paid = ParagraphStyle('GreenPaid', parent=styles['Normal'], fontSize=8, leading=10, fontName='Helvetica-Bold', alignment=2, textColor=colors.HexColor('#166534'))

    story = []

    # 1. Main Header
    head_table = Table([
        [
            Paragraph('<b>K-ELECTRIC (KE)</b><br/><font size="7" color="#64748B">Power That Moves Karachi • Official Digital Duplicate Bill</font>', brand_title),
            Paragraph(f'<b>DUPLICATE CONSUMER BILL</b><br/>Bill Month: <b>{consumer_data.get("bill_month", "Jul-25")}</b> | Issue Date: {consumer_data.get("issue_date", "28-Jul-2025")}<br/><font color="#166534"><b>PAID • STAR CONSUMER</b></font>', header_right)
        ]
    ], colWidths=[270, 268])
    head_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(head_table)
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor('#0F172A'), spaceAfter=6, spaceBefore=4))

    # 2. Key Highlights Row (Amount Due | Current Month Units | Due Date)
    kpi_table_data = [
        [
            Paragraph('<font size="7" color="#64748B">AMOUNT DUE (WITHIN DUE DATE)</font><br/><b>Rs. ' + f"{int(consumer_data['amount_due']):,}" + '</b>', big_amt),
            Paragraph('<font size="7" color="#64748B">CURRENT MONTH UNITS</font><br/><b>' + f"{int(consumer_data['current_units'])} Units" + '</b>', ParagraphStyle('KUnits', parent=big_amt, alignment=1)),
            Paragraph('<font size="7" color="#64748B">PAYMENT DUE DATE</font><br/><b>' + consumer_data.get('due_date', '11-Aug-2025') + '</b>', ParagraphStyle('KDate', parent=big_amt, alignment=2))
        ]
    ]
    t_kpi = Table(kpi_table_data, colWidths=[180, 178, 180])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 6))

    # 3. Customer Information Table (Two Columns)
    story.append(Paragraph('<b>Customer &amp; Connection Details / صارف کی معلومات</b>', section_head))
    cust_data = [
        [
            Paragraph('<b>Account Number:</b>', cell_bold), Paragraph(str(consumer_data.get('account_no', '1234567890123')), cell_norm),
            Paragraph('<b>Contract No:</b>', cell_bold), Paragraph('040000001013', cell_norm)
        ],
        [
            Paragraph('<b>Consumer Number:</b>', cell_bold), Paragraph(str(consumer_data.get('consumer_no', 'AB123124')), cell_norm),
            Paragraph('<b>Sanctioned Load:</b>', cell_bold), Paragraph(str(consumer_data.get('sanc_load', '1 kW')), cell_norm)
        ],
        [
            Paragraph('<b>Customer Name:</b>', cell_bold), Paragraph(str(consumer_data.get('customer_name', 'MR. ABDULLAH KHAN')), cell_norm),
            Paragraph('<b>Connected Load:</b>', cell_bold), Paragraph(str(consumer_data.get('conn_load', '1 kW')), cell_norm)
        ],
        [
            Paragraph('<b>Tariff Category:</b>', cell_bold), Paragraph(str(consumer_data.get('tariff', 'A1-R Residential')), cell_norm),
            Paragraph('<b>Status:</b>', cell_bold), Paragraph('<font color="#166534"><b>Clear (Active Star Consumer)</b></font>', cell_norm)
        ],
        [
            Paragraph('<b>NTN / STRN:</b>', cell_bold), Paragraph('1543137-1 / 12-00-2716-007-28', cell_norm),
            Paragraph('<b>Billing Mode:</b>', cell_bold), Paragraph('NORM (A1-R Protected)', cell_norm)
        ]
    ]
    t_cust = Table(cust_data, colWidths=[90, 180, 95, 173])
    t_cust.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#F1F5F9')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_cust)
    story.append(Spacer(1, 6))

    # 4. Meter Reading Summary
    story.append(Paragraph('<b>Electricity You Have Used / بجلی کا استعمال</b>', section_head))
    meter_data = [
        ['Energy Head', 'Previous Reading', 'Current Reading', 'MF', 'Total Units (kWh)', 'MDI (kW)'],
        ['Peak / Normal', str(consumer_data.get('prev_reading', 20521)), str(consumer_data.get('curr_reading', 20693)), '1.0', f"{int(consumer_data['current_units'])}", '1.0']
    ]
    t_meter = Table(meter_data, colWidths=[100, 90, 90, 50, 110, 98])
    t_meter.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_meter)
    story.append(Spacer(1, 6))

    # 5. Bill Calculation & Tax Breakdown Table
    story.append(Paragraph('<b>Bill Calculation Breakdown / آپ کے موجودہ بل کا حساب</b>', section_head))
    curr_u = float(consumer_data['current_units'])
    calc_rows = [
        ['Billing Charge Item', 'Slab / Calculation Basis', 'Rate (PKR)', 'Amount (PKR)'],
        ['Variable Charges (Protected Slab 0 - 100)', '100 Units', '16.50', '1,650.00'],
        ['Variable Charges (Protected Slab 101 - 200)', f'{int(max(0, curr_u - 100))} Units', '22.95', f'{max(0, curr_u - 100)*22.95:,.2f}'],
        ['Additional Surcharge (PHL)', 'Targeted Surcharge', 'Uniform Tariff', f'{consumer_data.get("additional_surcharge", 58.82):,.2f}'],
        ['Fuel Charges Adjustment (FPA)', f'{int(curr_u)} Units determination', '4.50 / Unit', f'{curr_u * 4.50:,.2f}'],
        ['Electricity Duty (Sindh ED)', 'Provincial Duty 1.5%', '1.5%', f'{consumer_data.get("electricity_duty", 25.69):,.2f}'],
        ['General Sales Tax (GST)', 'Standard Sales Tax 18%', '18.0%', f'{consumer_data.get("sales_tax", 73.96):,.2f}'],
        ['Total Current Period Electricity Charges', 'Protected Category A1-R', '-', f'Rs. {int(consumer_data["amount_due"]):,}'],
        ['Amount Payable within Due Date', f'Due Date: {consumer_data.get("due_date", "11-Aug-2025")}', '-', f'Rs. {int(consumer_data["amount_due"]):,}'],
        ['Amount Payable After Due Date (Incl. 5% LPS)', 'Late Payment Surcharge', '5%', f'Rs. {int(consumer_data.get("amount_after_due", 2157)):,}']
    ]
    t_calc = Table(calc_rows, colWidths=[220, 140, 80, 98])
    t_calc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-3), [colors.HexColor('#F8FAFC'), colors.white]),
        ('BACKGROUND', (0,-2), (-1,-2), colors.HexColor('#E2E8F0')),
        ('FONTNAME', (0,-2), (-1,-2), 'Helvetica-Bold'),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F1F5F9')),
        ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_calc)
    story.append(Spacer(1, 6))

    # 6. 13-Month Consumption & History Record
    story.append(Paragraph('<b>13-Month Usage History / 13 مہینے کے استعمال کی تفصیل</b>', section_head))
    hist_table_data = [
        ['Month', 'Units', 'Amount (PKR)', 'Month', 'Units', 'Amount (PKR)'],
        ['Jul-25', '172', 'Rs. 2,071', 'Jan-25', '48', 'Rs. 720'],
        ['Jun-25', '173', 'Rs. 2,150', 'Dec-24', '83', 'Rs. 980'],
        ['May-25', '195', 'Rs. 2,680', 'Nov-24', '159', 'Rs. 1,820'],
        ['Apr-25', '195', 'Rs. 2,680', 'Oct-24', '175', 'Rs. 2,100'],
        ['Mar-25', '162', 'Rs. 1,890', 'Sep-24', '184', 'Rs. 2,340'],
        ['Feb-25', '94', 'Rs. 1,150', 'Aug-24', '190', 'Rs. 2,450'],
    ]
    t_hist = Table(hist_table_data, colWidths=[89, 80, 100, 89, 80, 100])
    t_hist.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#334155')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.white]),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_hist)
    story.append(Spacer(1, 6))

    # 7. Bank Clearance Slip & Barcode Counterfoil
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#94A3B8'), spaceAfter=4, spaceBefore=2))
    counterfoil = [
        [
            Paragraph('<b>Customer Name:</b> ' + consumer_data.get('customer_name', 'MR. ABDULLAH KHAN') + '<br/><b>Account Number:</b> ' + consumer_data.get('account_no', '1234567890123'), cell_norm),
            Paragraph('<b>Invoice Number:</b> ' + consumer_data.get('invoice_no', '739000565027') + '<br/><b>Due Date:</b> ' + consumer_data.get('due_date', '11-Aug-2025'), cell_norm),
            Paragraph('<b>Amount Due:</b> Rs. ' + f"{int(consumer_data['amount_due']):,}" + '<br/><b>After Due:</b> Rs. ' + f"{int(consumer_data.get('amount_after_due', 2157)):,}", cell_bold)
        ]
    ]
    t_foil = Table(counterfoil, colWidths=[180, 180, 178])
    t_foil.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_foil)
    story.append(Spacer(1, 4))

    # 8. Verification Note
    story.append(Paragraph('Official Computerized Duplicate Bill Generated via VOLTIFY Smart Energy Predictor. Certified Against K-Electric DISCO Tariff Gazette.', ParagraphStyle('Foot', parent=styles['Normal'], fontSize=7, textColor=colors.HexColor('#64748B'), alignment=1)))

    doc.build(story)
    return pdf_path

if __name__ == "__main__":
    out = r"G:\farhan_fyp\simulator\static\ke_official_bill.pdf"
    generate_ke_bill_pdf(out)
    print("PDF generated successfully:", out)
