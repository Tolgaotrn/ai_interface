from datetime import datetime
import streamlit as st
from PIL import Image
import os
import base64
from io import BytesIO
import io
import re
import requests
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as ReportLabImage, Table, TableStyle
import time
from datetime import datetime

# ======================
# DATA SETUP
# ======================

patient_cases = {
    "Case 1": {
        "Oral Health Status": "Green",
        "present": {
            "maxilla": [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28],
            "mandible": [38, 37, 36, 35, 34, 33, 32, 31, 41, 42, 43, 44, 45, 46, 47, 48],
        },
        "missing": {"maxilla": [], "mandible": []},
        "filling": {"maxilla": [17, 16, 26, 27, 28], "mandible": [38, 37, 36, 35, 46, 47, 48]},
        "root_canal": {"maxilla": [16, 26], "mandible": []},
        "crown": {"maxilla": [26], "mandible": []},
        "bridge": {"maxilla": [], "mandible": []},
        "implant": {"maxilla": [], "mandible": []},
        "impacted": {"maxilla": [], "mandible": []},
        "teeth_green":{
            "maxilla":{18,15,14,13,12,11,21,22,23,24,25},
            "mandible":{34,33,32,31,41,42,43,44,45},
        },
        "teeth_yellow":{
            "maxilla":{17,16,26,27,28},
            "mandible":{38,37,36,35,46}
        },
        "teeth_red":{
            "maxilla":{},
            "mandible":{}
        },
    },
    "Case 2": {
        "Oral Health Status": "Yellow",
        "present": {
            "maxilla": [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27],
            "mandible": [38, 37, 35, 34, 33, 32, 31, 41, 42, 43, 44, 46, 47, 48],
        },
        "missing": {"maxilla": [28], "mandible": [36, 45]},
        "filling": {"maxilla": [17, 16, 11, 21, 25, 26, 27], "mandible": [37, 35, 46, 47]},
        "root_canal": {"maxilla": [16, 11, 21], "mandible": [47]},
        "crown": {"maxilla": [], "mandible": []},
        "bridge": {"maxilla": [], "mandible": []},
        "implant": {"maxilla": [], "mandible": [36]},
        "impacted": {"maxilla": [], "mandible": []},
        "teeth_green":{
            "maxilla":{18,15,14,13,12,22,23,24,28},
            "mandible":{38,34,33,32,31,41,42,43,44,45,48},
        },
        "teeth_yellow":{
            "maxilla":{17,16,11,21,25,26,27},
            "mandible":{37,35,46,47}
        },
        "teeth_red":{
            "maxilla":{},
            "mandible":{36}
        },

    },
    "Case 3": {
        "Oral Health Status": "Red",
        "present": {
            "maxilla": [17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26],
            "mandible": [38, 36, 35, 34, 33, 32, 31, 41, 42, 43, 44, 46, 47],
        },
        "missing": {"maxilla": [18, 27, 28], "mandible": [37, 45, 48]},
        "filling": {"maxilla": [17, 16], "mandible": [38, 47]},
        "root_canal": {"maxilla": [14, 13], "mandible": [34, 33]},
        "crown": {"maxilla": [14, 26], "mandible": [36]},
        "bridge": {"maxilla": [], "mandible": [44, 45, 46]},
        "implant": {"maxilla": [], "mandible": []},
        "impacted": {"maxilla": [], "mandible": []},
        "teeth_green":{
            "maxilla":{18,15,12,11,21,22,23,24,25,28},
            "mandible":{37,35,34,33,32,31,41,42,43,48},
        },
        "teeth_yellow":{
            "maxilla":{17,16,14,13,26},
            "mandible":{38,36,44,45,46,47}
        },
        "teeth_red":{
            "maxilla":{27},
            "mandible":{}
        },
    },
    "Case 4": {
        "Oral Health Status": "Yellow",
        "present": {
            "maxilla": [17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27],
            "mandible": [38, 37, 35, 34, 33, 32, 31, 41, 42, 43, 44, 45, 47, 48],
        },
        "missing": {"maxilla": [18, 28], "mandible": [36, 46]},
        "filling": {"maxilla": [17, 15, 14, 12, 22, 23, 24, 26, 27], "mandible": [38, 47, 48]},
        "root_canal": {"maxilla": [], "mandible": [37, 35, 47]},
        "crown": {"maxilla": [25], "mandible": []},
        "bridge": {"maxilla": [], "mandible": [37, 36, 35]},
        "implant": {"maxilla": [], "mandible": []},
        "impacted": {"maxilla": [], "mandible": []},
        "teeth_green":{
            "maxilla":{18,16,13,11,21,28},
            "mandible":{34,33,32,31,41,42,43,44,45,46},
        },
        "teeth_yellow":{
            "maxilla":{17,15,14,12,22,23,24,25,26,27},
            "mandible":{38,37,36,35,47,48}
        },
        "teeth_red":{
            "maxilla":{},
            "mandible":{}
        },
    },
    "Case 5": {
        "Oral Health Status": "Yellow",
        "present": {
            "maxilla": [17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28],
            "mandible": [38, 37, 36, 35, 34, 33, 32, 31, 41, 42, 43, 44, 45, 46, 47, 48],
        },
        "missing": {"maxilla": [18], "mandible": []},
        "filling": {"maxilla": [17, 16, 27, 28], "mandible": [38, 37, 36, 46, 48]},
        "root_canal": {"maxilla": [], "mandible": [46]},
        "crown": {"maxilla": [21], "mandible": []},
        "bridge": {"maxilla": [], "mandible": []},
        "implant": {"maxilla": [], "mandible": []},
        "impacted": {"maxilla": [], "mandible": []},
        "teeth_green":{
            "maxilla":{18,15,14,13,12,11,22,23,24,25,26},
            "mandible":{35,34,33,32,31,41,42,43,44,45,47},
        },
        "teeth_yellow":{
            "maxilla":{17,16,21,27,28},
            "mandible":{38,37,36,35,46,48}
        },
        "teeth_red":{
            "maxilla":{},
            "mandible":{}
        },
    },
}

# ======================
# HELPER FUNCTIONS  
# ======================

def reset_application():
    """Reset the application to its initial state"""
    st.session_state.update({
        'selected_tooth': None,
        'show_popup': False,
        'current_case': None,
        'treatment_type': "Crown",
        'affected_teeth': [],
        'notes': "",
        'file_uploaded': False,
        'popup_image': None,
        'viewing_mode': "normal",  # Can be "normal" or "tooth_detail"
        'show_ai_analysis': False,  # New state for AI analysis
        'ai_diagnosis': None,       # Store AI diagnosis results
    })
    st.rerun()

def get_tooth_image_path(tooth_num, treatment_type=None, case_number=None, is_popup=False):
    """Return the appropriate image path for a tooth based on its condition"""
    base_path = "UCLL_dataset_24"
    
    # Popup için sadece case klasöründeki görseli kullan
    if is_popup and case_number:
        case_img_path = os.path.join(base_path, "Trial_cases", f"case_{case_number}", f"{tooth_num}.jpg")
        if os.path.exists(case_img_path):
            return case_img_path
    
    # Önce case klasörüne bak
    if case_number:
        case_img_path = os.path.join(base_path, "Trial_cases", f"case_{case_number}", f"{tooth_num}.jpg")
        if os.path.exists(case_img_path):
            return case_img_path
    
    # Tedavi tipine göre icon klasöründen al
    icon_folders = {
        "implant": "Icon_implant",
        "filling": "Icon_df",
        "crown": "Icon_crown_tooth",
        "root_canal": "Icon_crown_rcf",
        "bridge": "Icon_bridge_tooth",
        "impacted": "Icon_impacted",
        "missing": "Icon_missing_teeth"
    }
    
    if treatment_type in icon_folders:
        icon_path = os.path.join(base_path, "Icons", icon_folders[treatment_type], f"{tooth_num}.png")
        if os.path.exists(icon_path):
            return icon_path
    
    # Hiçbiri yoksa normal diş görselini kullan
    normal_path = os.path.join(base_path, "Icons", "Icon_normal_teeth", f"{tooth_num}.png")
    if os.path.exists(normal_path):
        return normal_path
    
    return None

def extract_case_number(filename):
    """Extract case number from filename"""
    pattern = r'case[\s_]?(\d+)'
    match = re.search(pattern, filename.lower())
    return f"Case {match.group(1)}" if match else None

def generate_pdf_report(case_data, notes=None):
    """Generate a PDF report for the dental case"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Add custom style for colored text
    red_style = ParagraphStyle('RedStyle', parent=styles['Normal'], textColor=colors.red)
    yellow_style = ParagraphStyle('YellowStyle', parent=styles['Normal'], textColor=colors.orange)
    
    # Get patient info from session state
    patient_info = {
        'profile_number': st.session_state.get('profile_number', 'N/A'),
        'family_name': st.session_state.get('family_name', 'N/A'),
        'first_name': st.session_state.get('first_name', 'N/A'),
        'gender': st.session_state.get('gender', 'N/A').replace("👨 ", "").replace("👩 ", ""),
        'age': st.session_state.get('age', 'N/A'),
        'date_of_birth': st.session_state.get('date_of_birth'),
        'scan_date': st.session_state.get('scan_date')
    }

    # Format dates if they exist
    if patient_info['date_of_birth'] is not None:
        patient_info['date_of_birth'] = patient_info['date_of_birth'].strftime("%d/%m/%Y")
    else:
        patient_info['date_of_birth'] = 'N/A'
        
    if patient_info['scan_date'] is not None:
        patient_info['scan_date'] = patient_info['scan_date'].strftime("%d/%m/%Y")
    else:
        patient_info['scan_date'] = datetime.now().strftime("%d/%m/%Y")  # Default to current date if not set

    # PDF elements
    elements = []
    
    # Title
    elements.append(Paragraph("Radiology Report", styles["Title"]))
    elements.append(Spacer(1, 20))
    
    # Enhanced patient info table with dates
    patient_table = Table([
        ["Patient ID", ":", patient_info['profile_number']],
        ["Name", ":", f"{patient_info['first_name']} {patient_info['family_name']}"],
        ["Date of Birth", ":", patient_info['date_of_birth']],
        ["Age", ":", f"{patient_info['age']} years"],
        ["Gender", ":", patient_info['gender']],
        ["Scan date", ":", patient_info['scan_date']],
    ], colWidths=[80, 10, 200], hAlign='LEFT')
        
    patient_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(patient_table)
    elements.append(Spacer(1, 16))
    
    # X-ray image - use regular case image instead of segmented
    case_number = st.session_state.current_case.split()[1] if st.session_state.current_case else None
    if case_number:
        # Use regular case image instead of segmented
        case_img_path = os.path.join("UCLL_dataset_24", "Trial_cases", f"case_{case_number}", f"case_{case_number}.jpeg")
        
        # Process the case X-ray image
        if os.path.exists(case_img_path):
            try:
                case_img = Image.open(case_img_path)
                img_buffer = BytesIO()
                case_img.save(img_buffer, format="PNG")
                xray_img = ReportLabImage(io.BytesIO(img_buffer.getvalue()), 
                           width=400,  # Full width for the x-ray image
                           height=int(case_img.height * (400 / case_img.width)))
                
                # Add the X-ray image centered
                xray_table = Table([[xray_img]], colWidths=[450])
                xray_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                    ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
                ]))
                elements.append(xray_table)
                elements.append(Spacer(1, 10))  # Space after X-ray
            except Exception as e:
                elements.append(Paragraph(f"Error loading X-ray image: {str(e)}", styles["Normal"]))
        
        # Create dental chart with icons
        try:
            # Create tables for upper and lower jaws with tooth icons
            upper_data = []
            lower_data = []
            
            # Create header row with proper FDI tooth numbers
            upper_teeth_nums = [str(i) for i in range(18, 10, -1)] + [str(i) for i in range(21, 29)]
            upper_header = upper_teeth_nums
            upper_data.append(upper_header)
            
            # Create row with tooth icons
            upper_icons = []
            
            # Function to get tooth icon
            def get_tooth_icon(tooth_num, jaw_key):
                icon_path = None
                is_missing = tooth_num in case_data["missing"][jaw_key] or tooth_num not in case_data["present"][jaw_key]
                is_filling = tooth_num in case_data["filling"][jaw_key]
                is_root_canal = tooth_num in case_data["root_canal"][jaw_key]
                is_crown = tooth_num in case_data["crown"][jaw_key]
                is_bridge = tooth_num in case_data["bridge"][jaw_key]
                is_implant = tooth_num in case_data["implant"][jaw_key]
                
                if is_missing:
                    icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_missing_teeth", f"{tooth_num}.png")
                elif is_bridge:
                    if is_root_canal:
                        icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_bridge_tooth_rcf", f"{tooth_num}.png")
                    elif is_implant:
                        icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_bridge_implant", f"{tooth_num}.png")
                    else:
                        icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_bridge_tooth", f"{tooth_num}.png")
                elif is_crown:
                    if is_root_canal:
                        icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_crown_rcf", f"{tooth_num}.png")
                    elif is_implant:
                        icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_crown_implant", f"{tooth_num}.png")
                    else:
                        icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_crown_tooth", f"{tooth_num}.png")
                elif is_root_canal:
                    if is_filling:
                        icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_df_rcf", f"{tooth_num}.png")
                    else:
                        icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_df_rcf", f"{tooth_num}.png")
                elif is_filling:
                    icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_df", f"{tooth_num}.png")
                else:
                    icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_normal_teeth", f"{tooth_num}.png")
                
                if icon_path and os.path.exists(icon_path):
                    img = Image.open(icon_path)
                    img_buffer = BytesIO()
                    img.save(img_buffer, format="PNG")
                    return ReportLabImage(io.BytesIO(img_buffer.getvalue()), width=18, height=18)
                return None

            # Upper jaw icons
            for tooth_num in range(18, 10, -1):
                icon = get_tooth_icon(tooth_num, "maxilla")
                upper_icons.append(icon if icon else "")
            
            for tooth_num in range(21, 29):
                icon = get_tooth_icon(tooth_num, "maxilla")
                upper_icons.append(icon if icon else "")
            
            upper_data.append(upper_icons)
            
            # Lower jaw icons and numbers
            lower_icons = []
            
            for tooth_num in range(38, 30, -1):
                icon = get_tooth_icon(tooth_num, "mandible")
                lower_icons.append(icon if icon else "")
            
            for tooth_num in range(41, 49):
                icon = get_tooth_icon(tooth_num, "mandible")
                lower_icons.append(icon if icon else "")
            
            lower_data.append(lower_icons)
            
            # Add FDI tooth numbers for lower jaw
            lower_teeth_nums = [str(i) for i in range(38, 30, -1)] + [str(i) for i in range(41, 49)]
            lower_data.append(lower_teeth_nums)
            
            # Create tables with proper styling - larger tooth icons
            upper_table = Table(upper_data, colWidths=[20] * len(upper_header))
            lower_table = Table(lower_data, colWidths=[20] * len(lower_teeth_nums))
            
            for table in [upper_table, lower_table]:
                table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTSIZE', (0, 0), (-1, 0), 6),  # Font for tooth numbers
                    ('FONTSIZE', (0, 1), (-1, 1), 6),  # Font for tooth numbers
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),  # No padding
                    ('RIGHTPADDING', (0, 0), (-1, -1), 0),  # No padding
                ]))
            
            # Create a parent table to hold all dental elements with proper spacing
            dental_chart = Table([
                [upper_table],
                [Spacer(1, 5)],  # Space between upper and lower
                [lower_table]
            ])
            
            dental_chart.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            # Add the dental chart centered below the X-ray
            chart_table = Table([[dental_chart]], colWidths=[450])
            chart_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
            ]))
            elements.append(chart_table)
            elements.append(Spacer(1, 15))  # Space after chart
            
        except Exception as e:
            # If there's an error creating the teeth diagram, add a placeholder
            elements.append(Paragraph(f"Error creating teeth diagram: {str(e)}", styles["Normal"]))
    
    # Count total teeth present
    total_teeth = len(case_data['present']['maxilla']) + len(case_data['present']['mandible'])
    
    # Teeth findings section
    elements.append(Paragraph(f"The panoramic radiograph reveals {total_teeth} teeth are present. The following teeth are present:", styles["Normal"]))
    elements.append(Paragraph(f"Maxilla: {', '.join(map(str, case_data['present']['maxilla']))}", styles["Normal"]))
    elements.append(Paragraph(f"Mandible: {', '.join(map(str, case_data['present']['mandible']))}", styles["Normal"]))
    elements.append(Spacer(1, 10))
    
    elements.append(Paragraph("The following teeth are missing:", styles["Normal"]))
    missing_maxilla = ', '.join(map(str, case_data['missing']['maxilla'])) if case_data['missing']['maxilla'] else "-"
    missing_mandible = ', '.join(map(str, case_data['missing']['mandible'])) if case_data['missing']['mandible'] else "-"
    elements.append(Paragraph(f"Maxilla: {missing_maxilla}", styles["Normal"]))
    elements.append(Paragraph(f"Mandible: {missing_mandible}", styles["Normal"]))
    elements.append(Spacer(1, 10))
    
    # Detailed findings for each condition
    dental_findings = [
        ("Dental fillings are detected in", "filling"),
        ("Root canal fillings are detected in", "root_canal"),
        ("Crowns are detected in", "crown"),
        ("Bridges are detected in", "bridge"),
        ("Implants are detected in", "implant"),
        ("Impacted teeth are detected in", "impacted")
    ]
    
    for label, key in dental_findings:
        teeth = case_data[key]["maxilla"] + case_data[key]["mandible"]
        teeth_text = ', '.join(map(str, teeth)) if teeth else "-"
        elements.append(Paragraph(f"{label} {teeth_text}", styles["Normal"]))
    
    elements.append(Spacer(1, 20))
    
    # Add a line separator
    elements.append(Paragraph("_" * 70, styles["Normal"]))
    elements.append(Spacer(1, 10))
    
    # Add color-coded warnings
    red_warnings = []
    yellow_warnings = []
    
    # Check for teeth that need immediate attention (based on root canal without crown)
    for tooth in case_data["root_canal"]["maxilla"] + case_data["root_canal"]["mandible"]:
        if (tooth in case_data["root_canal"]["maxilla"] and tooth not in case_data["crown"]["maxilla"]) or \
           (tooth in case_data["root_canal"]["mandible"] and tooth not in case_data["crown"]["mandible"]):
            red_warnings.append(tooth)
    
    # Check for teeth that need close observation (based on deep fillings)
    for tooth in case_data["filling"]["maxilla"] + case_data["filling"]["mandible"]:
        if tooth not in red_warnings:
            yellow_warnings.append(tooth)
    
    # Add red warnings with tooth icons
    for tooth in red_warnings:
        # Get tooth image path if available
        tooth_img_path = get_tooth_image_path(tooth, treatment_type=None, case_number=case_number)
        
        # Add table with red circle and tooth image
        if tooth_img_path and os.path.exists(tooth_img_path):
            try:
                tooth_img = Image.open(tooth_img_path)
                tooth_buffer = BytesIO()
                tooth_img.save(tooth_buffer, format="PNG")
                tooth_image = ReportLabImage(io.BytesIO(tooth_buffer.getvalue()), width=60, height=60)
                
                # Create a table with a red circle indicator and the text
                data = [[None, tooth_image, f"{tooth}: Immediate check up"]]
                t = Table(data, colWidths=[20, 70, 300])
                t.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                elements.append(t)
            except Exception as e:
                elements.append(Paragraph(f"{tooth}: Immediate check up", red_style))
        else:
            elements.append(Paragraph(f"{tooth}: Immediate check up", red_style))
    
    elements.append(Spacer(1, 10))
    
    # Add yellow warnings with tooth icons
    for tooth in yellow_warnings:
        # Get tooth image path if available
        tooth_img_path = get_tooth_image_path(tooth, treatment_type=None, case_number=case_number)
        
        # Add table with yellow circle and tooth image
        if tooth_img_path and os.path.exists(tooth_img_path):
            try:
                tooth_img = Image.open(tooth_img_path)
                tooth_buffer = BytesIO()
                tooth_img.save(tooth_buffer, format="PNG")
                tooth_image = ReportLabImage(io.BytesIO(tooth_buffer.getvalue()), width=60, height=60)
                
                # Create a table with a yellow circle indicator and the text
                data = [[None, tooth_image, f"{tooth}: Close observation"]]
                t = Table(data, colWidths=[20, 70, 300])
                t.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                elements.append(t)
            except Exception as e:
                elements.append(Paragraph(f"{tooth}: Close observation", yellow_style))
        else:
            elements.append(Paragraph(f"{tooth}: Close observation", yellow_style))
    
    # Notes
    if notes:
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("Additional Notes:", styles["Heading2"]))
        elements.append(Paragraph(notes, styles["Normal"]))
    
    doc.build(elements)
    return buffer
    
# New function for AI analysis
def get_ai_diagnosis(clinical_data, radiographic_data, image_base64=None):
    """Get AI diagnosis using Replicate API"""
    try:
        # Create structured prompt
        prompt = f"""
        i will give all the information of dental patients that you can find below  like the race of the patient, age of the patient etc.,  i will also upload the x-ray images of each one of the patient`s teeth. I want you to analyze these both information and x-ray image and generate a diagnosis for each one of the cases.


        Clinical features:
        - Sex: {clinical_data['sex']}
        - Race: {clinical_data['race']}
        - Age: {clinical_data['age']}
        - Pain/paresthesia: {clinical_data['pain']}

        Radiographic features:
        - Jaw location: {radiographic_data['jaw']}
        - Region: {radiographic_data['region']}
        - Relationship to teeth: {radiographic_data['teeth_relation']}
        - Number of lesions: {radiographic_data['lesion_count']}
        - Maximum lesion size: {radiographic_data['lesion_size']}
        - Origin of lesion: {radiographic_data['lesion_origin']}
        - Borders: {radiographic_data['borders']}
        - Loculation: {radiographic_data['loculation']}
        - Contents: {radiographic_data['contents']}
        - Contains teeth: {radiographic_data['contains_teeth']}
        - Expands cortex: {radiographic_data['expands_cortex']}
        - Root resorption: {radiographic_data['root_resorption']}
        - Tooth displacement/impaction: {radiographic_data['tooth_displacement']}

        Please give me only the diagnose name nothing more it could be like 2 most possible diagnoses with probability of each one of them. If you are certain about the diagnose name the give it only one.
        """
        
        # Replicate API configuration
        api_token = "r8_3kgRNUIn1RdbjIugQ8EOFg8lZQiE9by0EgLOH"
        headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json",
        }
        
        # Using Replicate's Llama 2 model
        data = {
            "version": "2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
            "input": {
                "prompt": prompt,
                "system_prompt": "You are a dental radiology expert specialized in diagnosis.",
                "max_new_tokens": 1000,
                "temperature": 0.2,
                "top_p": 0.9,
                "presence_penalty": 0
            }
        }
        
        # Create prediction
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 201:
            prediction = response.json()
            
            # Poll for completion
            while True:
                # Get prediction status
                status_response = requests.get(
                    f"https://api.replicate.com/v1/predictions/{prediction['id']}",
                    headers=headers
                )
                status_data = status_response.json()
                
                if status_data['status'] == 'succeeded':
                    diagnosis = ''.join(status_data['output'])
                    return {"success": True, "diagnosis": diagnosis}
                elif status_data['status'] == 'failed':
                    return {"success": False, "error": "Prediction failed"}
                
                time.sleep(1)  # Wait before polling again
        else:
            return {"success": False, "error": f"API Error: {response.status_code} - {response.text}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

# ======================
# STREAMLIT UI SETUP
# ======================

st.set_page_config(page_title="Dental Chart Interface", layout="wide")

# CSS styling
st.markdown("""
<style>
    .popup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9998;
    }
    .popup {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        position: relative;
        max-width: 90%;
        max-height: 90vh;
        overflow: auto;
        text-align: center;
        box-shadow: 0 4px 32px rgba(0,0,0,0.25);
    }
    .popup img {
        max-width: 100%;
        max-height: 70vh;
        object-fit: contain;
        margin-bottom: 15px;
    }
    .popup-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    }
    .close-button {
        background-color: #ff4b4b;
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        border: none;
        margin-top: 10px;
        font-size: 16px;
        transition: background-color 0.3s;
    }
    .close-button:hover {
        background-color: #ff3333;
    }
    .tooth-button {
        cursor: pointer;
        transition: transform 0.2s;
        display: inline-block;
    }
    .tooth-button:hover {
        transform: scale(1.1);
    }
    .tooth-button img {
        width: 60px;
        height: 60px;
        object-fit: contain;
    }
    /* Hide the default Streamlit button styling */
    .stButton button {
        opacity: 0;
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        margin: 0;
        padding: 0;
    }
    /* Style the close button */
    .stButton>button[kind="secondary"] {
        display: inline-block;
        opacity: 1;
        position: relative;
        margin-top: 10px;
    }
    .missing-tooth { 
        background-color: #f0f0f0; border: 1px dashed #cc0000; 
        width: 60px; height: 60px; display: flex; 
        align-items: center; justify-content: center; border-radius: 5px; 
    }
    .missing-tooth-symbol { color: #cc0000; font-size: 24px; }
    .download-btn {
        background-color: #4CAF50; color: white; padding: 10px 20px;
        text-align: center; text-decoration: none; display: inline-block;
        font-size: 16px; margin: 10px 0; cursor: pointer; border-radius: 5px;
    }
    .popup-close {
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 28px;
        font-weight: bold;
        color: #888;
        cursor: pointer;
        background: none;
        border: none;
        z-index: 10000;
        transition: color 0.2s;
    }
    .popup-close:hover {
        color: #ff3333;
    }
    /* Modal style (Flask-like) */
    .modal-overlay {
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.7);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .modal-content {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        max-width: 80%;
        max-height: 80vh;
        overflow: auto;
        position: relative;
    }
    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #eee;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }
    .modal-title {
        font-size: 20px;
        font-weight: bold;
        margin: 0;
    }
    .modal-close {
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 24px;
        background: none;
        border: none;
        cursor: pointer;
        color: #666;
        transition: color 0.2s;
    }
    .modal-close:hover {
        color: #ff3333;
    }
    .modal-body {
        text-align: center;
    }
    .modal-body img {
        max-width: 100%;
        max-height: 60vh;
        object-fit: contain;
    }
    .modal-footer {
        border-top: 1px solid #eee;
        padding-top: 15px;
        margin-top: 15px;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'profile_number' not in st.session_state:
    st.session_state.update({
        'profile_number': "0000",
        'family_name': "Wick",
        'first_name': "John",
        'gender': "👨 Male",
        'age': 30,
        'date_of_birth': None,
        'scan_date': None,
        'selected_tooth': None,
        'show_popup': False,
        'current_case': None,
        'treatment_type': "Crown",
        'affected_teeth': [],
        'notes': "",
        'file_uploaded': False,
        'popup_image': None,
        'viewing_mode': "normal",  # Can be "normal" or "tooth_detail"
        'show_ai_analysis': False, # New state for AI analysis
        'ai_diagnosis': None,      # Store AI diagnosis results
    })

# Ensure all session state variables exist
for key in ['profile_number', 'family_name', 'first_name', 'gender', 'age', 
            'selected_tooth', 'show_popup', 'current_case', 'treatment_type', 
            'affected_teeth', 'notes', 'file_uploaded', 'popup_image', 
            'viewing_mode', 'show_ai_analysis', 'ai_diagnosis']:
    if key not in st.session_state:
        if key in ['profile_number']:
            st.session_state[key] = "0000"
        elif key in ['family_name']:
            st.session_state[key] = "Wick"
        elif key in ['first_name']:
            st.session_state[key] = "John"
        elif key in ['gender']:
            st.session_state[key] = "👨 Male"
        elif key in ['age']:
            st.session_state[key] = 30
        elif key in ['treatment_type']:
            st.session_state[key] = "Crown"
        elif key in ['affected_teeth']:
            st.session_state[key] = []
        elif key in ['notes']:
            st.session_state[key] = ""
        elif key in ['viewing_mode']:
            st.session_state[key] = "normal"
        else:
            st.session_state[key] = False if key.startswith('show_') or key == 'editing_mode' else None

# ======================
# SIDEBAR
# ======================

with st.sidebar:
    st.markdown("## 🧾 Patient Profile")
    st.session_state.profile_number = st.text_input("Profile number", value=st.session_state.profile_number)
    st.session_state.family_name = st.text_input("Family name", value=st.session_state.family_name)
    st.session_state.first_name = st.text_input("First name", value=st.session_state.first_name)
    
    # Add date of birth field
    dob = st.date_input(
        "Date of Birth",
        value=st.session_state.date_of_birth if st.session_state.date_of_birth else None,
        format="DD/MM/YYYY",
        min_value=datetime(1900, 1, 1),
        max_value=datetime.now()
    )
    if dob:
        st.session_state.date_of_birth = dob
        # Calculate age automatically
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        st.session_state.age = age
    
    st.session_state.gender = st.radio("Gender", ["👨 Male", "👩 Female"], 
                                     index=0 if st.session_state.gender == "👨 Male" else 1,
                                     horizontal=True)
    
    # Display age (now calculated from DOB)
    st.markdown(f"**Age:** {st.session_state.age} years")
    
    # Add scan date field
    scan_date = st.date_input(
        "Scan Date",
        value=st.session_state.scan_date if st.session_state.scan_date else datetime.now(),
        format="DD/MM/YYYY",
        min_value=datetime(1900, 1, 1),
        max_value=datetime.now()
    )
    if scan_date:
        st.session_state.scan_date = scan_date

    st.markdown("### 📤 Upload X-ray")
    
    # Use a session state flag to track upload status
    if 'file_uploaded' not in st.session_state:
        st.session_state.file_uploaded = False
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Drag and drop file here\nLimit 200MB per file • JPG, JPEG, PNG",
        type=["jpg", "jpeg", "png"],
        key="file_uploader",
        on_change=lambda: st.session_state.update({'file_uploaded': True})
    )
    
    # Handle when user clicks the X button
    if st.session_state.file_uploaded and uploaded_file is None:
        reset_application()
    
    # Process the uploaded file
    if uploaded_file:
        try:
            xray_image = Image.open(uploaded_file)
            case_id = extract_case_number(uploaded_file.name)
            st.session_state.current_case = case_id if case_id in patient_cases else "Case 1"
            st.success(f"Loaded {st.session_state.current_case}")
        except Exception as e:
            st.error(f"Error loading image: {e}")
            reset_application()

# ======================
# MAIN INTERFACE
# ======================

# If we're in tooth detail view, show only that
if st.session_state.get('viewing_mode') == "tooth_detail" and st.session_state.popup_image:
    # Create a container for the tooth detail view with minimal spacing
    tooth_detail_container = st.container()
    
    with tooth_detail_container:
        # More compact layout with back button, title, and a prominent close button
        col1, col2, col3 = st.columns([6, 3, 1])
        
        with col1:
            # Smaller title inline with back button
            st.markdown(f"#### Tooth {st.session_state.selected_tooth} Detail")
        
        with col2:
            # Back button aligned right
            if st.button("← Return to Main View", key="back_button", type="primary"):
                st.session_state.viewing_mode = "normal"
                st.session_state.show_popup = False
                st.session_state.popup_image = None
                st.rerun()
                
        with col3:
            # Prominent close button
            if st.button("✕ Close", key="close_button", type="secondary"):
                st.session_state.viewing_mode = "normal"
                st.session_state.show_popup = False
                st.session_state.popup_image = None
                st.rerun()
        
        # Horizontal line to separate header from content
        st.markdown("---")
        
        # Two columns for content: image on left, analysis on right
        img_col, info_col = st.columns([1, 1], gap="small")
        
        with img_col:
            try:
                img = Image.open(st.session_state.popup_image)
                # Display image with a fixed height to ensure it fits on screen
                st.image(img, width=350)
                
                # Add FDI tooth numbering system explanation
                tooth_num = st.session_state.selected_tooth
                quadrant = (tooth_num // 10)
                position = tooth_num % 10
                
                if quadrant == 1:
                    quadrant_name = "Upper Right (Maxilla)"
                elif quadrant == 2:
                    quadrant_name = "Upper Left (Maxilla)"
                elif quadrant == 3:
                    quadrant_name = "Lower Left (Mandible)"
                else:  # quadrant == 4
                    quadrant_name = "Lower Right (Mandible)"
                
                tooth_type = ""
                if position == 1:
                    tooth_type = "Central Incisor"
                elif position == 2:
                    tooth_type = "Lateral Incisor"
                elif position == 3:
                    tooth_type = "Canine"
                elif position == 4:
                    tooth_type = "First Premolar"
                elif position == 5:
                    tooth_type = "Second Premolar"
                elif position == 6:
                    tooth_type = "First Molar"
                elif position == 7:
                    tooth_type = "Second Molar"
                elif position == 8:
                    tooth_type = "Third Molar (Wisdom Tooth)"
                
                st.markdown(f"**Tooth ID:** {tooth_num}")
                st.markdown(f"**Location:** {quadrant_name}")
                st.markdown(f"**Type:** {tooth_type}")
                
            except Exception as e:
                st.error(f"Error loading tooth image: {e}")
                st.session_state.viewing_mode = "normal"
                st.rerun()
        
        with info_col:
            # Analysis section next to the image
            st.markdown("##### Dental Status")
            
            # Determine tooth condition based on case data
            if st.session_state.current_case and st.session_state.selected_tooth:
                case_data = patient_cases[st.session_state.current_case]
                tooth_num = st.session_state.selected_tooth
                
                # Check which jaw the tooth belongs to
                jaw_key = "maxilla" if tooth_num < 29 else "mandible"
                
                # First check if the tooth is present or missing
                if tooth_num in case_data["missing"][jaw_key]:
                    st.markdown("**⚠️ This tooth is missing**")
                elif tooth_num not in case_data["present"][jaw_key]:
                    st.markdown("**⚠️ This tooth is not present**")
                else:
                    st.markdown("**✓ This tooth is present**")
                
                # Always check and show tooth status
                if tooth_num in case_data["teeth_green"][jaw_key]:
                    st.success("🟢 Healthy - Regular Checkup")
                elif tooth_num in case_data["teeth_yellow"][jaw_key]:
                    st.warning("🟠 Close Observation")
                elif tooth_num in case_data["teeth_red"][jaw_key]:
                    st.error("🔴 Immediate Treatment Required")
                
                # Create an expander for detailed conditions
                with st.expander("**Detailed Conditions**", expanded=True):
                    # Check and display all possible conditions
                    if tooth_num in case_data["filling"][jaw_key]:
                        st.markdown("✓ **Filling:** This tooth has a dental filling")
                    
                        
                    if tooth_num in case_data["root_canal"][jaw_key]:
                        st.markdown("✓ **Root Canal:** This tooth has had root canal treatment")
                    
                        
                    if tooth_num in case_data["crown"][jaw_key]:
                        st.markdown("✓ **Crown:** This tooth has a dental crown")
                    
                        
                    if tooth_num in case_data["bridge"][jaw_key]:
                        st.markdown("✓ **Bridge:** This tooth is part of a dental bridge")
                    
                        
                    if tooth_num in case_data["implant"][jaw_key]:
                        st.markdown("✓ **Implant:** This tooth has a dental implant")
                    
                        
                    if tooth_num in case_data["impacted"][jaw_key]:
                        st.markdown("✓ **Impacted:** This tooth is impacted")
                   
                
                # Treatment recommendation expander
                with st.expander("**Treatment Recommendations**", expanded=True):
                    if tooth_num in case_data["filling"][jaw_key] and tooth_num in case_data["root_canal"][jaw_key]:
                        st.markdown("• Consider crown placement for better protection")
                    elif tooth_num in case_data["filling"][jaw_key]:
                        st.markdown("• Monitor filling condition at next checkup")
                    elif tooth_num in case_data["root_canal"][jaw_key]:
                        st.markdown("• Recommend crown placement to prevent fracture")
                    elif tooth_num in case_data["missing"][jaw_key]:
                        st.markdown("• Consider dental implant or bridge")
                    else:
                        st.markdown("• Continue regular dental hygiene")
                        st.markdown("• No specific treatment needed at this time")
                    
                    # Display current treatment type if affecting this tooth
                    if st.session_state.treatment_type and tooth_num in st.session_state.affected_teeth:
                        st.markdown(f"**Current Treatment Plan:** {st.session_state.treatment_type}")
                
                # Risk factors expander
                with st.expander("**Risk Assessment**", expanded=False):
                    risk_level = "Low"
                    if tooth_num in case_data["filling"][jaw_key] and tooth_num in case_data["root_canal"][jaw_key]:
                        risk_level = "Moderate"
                    elif tooth_num in case_data["root_canal"][jaw_key]:
                        risk_level = "Moderate"
                    
                    st.markdown(f"**Risk Level:** {risk_level}")
                    st.markdown("**Factors to consider:**")
                    if risk_level == "Moderate":
                        st.markdown("• Previous dental work increases risk of complications")
                    else:
                        st.markdown("• No significant risk factors identified")
            else:
                st.write("No tooth data available")
         
        # Footer with additional navigation
        st.markdown("---")
        if st.button("Return to Main View", key="back_button_bottom"):
            st.session_state.viewing_mode = "normal"
            st.session_state.show_popup = False
            st.session_state.popup_image = None
            st.rerun()
            
else:
    # Normal view with 3 columns
    col1, col2, col3 = st.columns([2.5, 0.1, 1.4])

    # Left Column - X-ray and Teeth Chart
    with col1:
        st.markdown("## 🦷 Dental Panaromic View")
        if uploaded_file:
            # Try to load the segmented case image
            case_number = st.session_state.current_case.split()[1] if st.session_state.current_case else None
            if case_number:
                segmented_img_path = os.path.join("UCLL_dataset_24", "Trial_cases", f"case_{case_number}", f"segmented_case_{case_number}.jpg")
                if os.path.exists(segmented_img_path):
                    segmented_img = Image.open(segmented_img_path)
                    st.image(segmented_img, use_container_width=True)
                else:
                    # Fallback to original image if segmented image not found
                    st.image(xray_image, use_container_width=True)
                    st.warning("Segmented case image not found")
            else:
                st.info("Please upload a dental X-ray image")

        if st.session_state.current_case:
            case_data = patient_cases[st.session_state.current_case]
            
            st.markdown("### 🧩 Tooth Selection")
            
            def display_teeth_row(jaw_type, teeth_list):
                # st.markdown(f"#### 🦷 {jaw_type} Jaw")
                jaw_key = "maxilla" if jaw_type == "Upper" else "mandible"
                all_teeth = list(range(18, 10, -1)) + list(range(21, 29)) if jaw_type == "Upper" else list(range(48, 40, -1)) + list(range(31, 39))
                missing_teeth = case_data["missing"][jaw_key]
                
                # For lower jaw, show buttons first
                if jaw_type == "Lower":
                    # Create columns for buttons
                    button_cols = st.columns(len(all_teeth))
                    for idx, tooth_num in enumerate(all_teeth):
                        with button_cols[idx]:
                            is_missing = tooth_num in missing_teeth or tooth_num not in case_data["present"][jaw_key]
                            is_implant = tooth_num in case_data["implant"][jaw_key]
                            is_bridge = tooth_num in case_data["bridge"][jaw_key]
                            
                            # Add button if tooth is present or is an implant or is a bridge
                            if not is_missing or is_implant or is_bridge:
                                # Add an invisible button over the icon
                                if st.button("", key=f"tooth_{tooth_num}_clicked", type="secondary"):
                                    case_number = st.session_state.current_case.split()[1] if st.session_state.current_case else None
                                    case_img_path = os.path.join("UCLL_dataset_24", "Trial_cases", f"case_{case_number}", f"{tooth_num}.jpg")
                                    if os.path.exists(case_img_path):
                                        st.session_state.selected_tooth = tooth_num
                                        st.session_state.popup_image = case_img_path
                                        # Do NOT set viewing_mode or show_popup
                                        st.rerun()
                
                # Create columns for icons
                icon_cols = st.columns(len(all_teeth))
                for idx, tooth_num in enumerate(all_teeth):
                    with icon_cols[idx]:
                        is_missing = tooth_num in missing_teeth or tooth_num not in case_data["present"][jaw_key]
                        is_implant = tooth_num in case_data["implant"][jaw_key]
                        
                        # Determine tooth condition and corresponding icon path
                        icon_path = None
                        
                        # Check various conditions
                        is_bridge = tooth_num in case_data["bridge"][jaw_key]
                        is_root_canal = tooth_num in case_data["root_canal"][jaw_key]
                        is_crown = tooth_num in case_data["crown"][jaw_key]
                        is_filling = tooth_num in case_data["filling"][jaw_key]
                        is_impacted = tooth_num in case_data["impacted"][jaw_key]
                        
                        # Handle special cases for missing teeth
                        if is_missing:
                            if is_bridge:
                                icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_bridge_pontic", f"{tooth_num}.png")
                            elif is_implant:
                                icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_implant", f"{tooth_num}.png")
                            else:
                                icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_missing_teeth", f"{tooth_num}.png")
                        else:
                            # Check conditions in order of priority
                            if is_bridge:
                                if is_root_canal:
                                    icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_bridge_tooth_rcf", f"{tooth_num}.png")
                                elif is_implant:
                                    icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_bridge_implant", f"{tooth_num}.png")
                                else:
                                    icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_bridge_tooth", f"{tooth_num}.png")
                            elif is_crown:
                                if is_root_canal:
                                    icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_crown_rcf", f"{tooth_num}.png")
                                elif is_implant:
                                    icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_crown_implant", f"{tooth_num}.png")
                                else:
                                    icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_crown_tooth", f"{tooth_num}.png")
                            elif is_root_canal:
                                if is_filling:
                                    icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_df_rcf", f"{tooth_num}.png")
                                else:
                                    icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_df_rcf", f"{tooth_num}.png")
                            elif is_filling:
                                icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_df", f"{tooth_num}.png")
                            elif is_impacted:
                                icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_impacted", f"{tooth_num}.png")
                            elif is_implant:
                                icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_implant", f"{tooth_num}.png")
                            else:
                                icon_path = os.path.join("UCLL_dataset_24", "Icons", "Icon_normal_teeth", f"{tooth_num}.png")

                        # Display the icon
                        if icon_path and os.path.exists(icon_path):
                            try:
                                img = Image.open(icon_path)
                                buffered = BytesIO()
                                img.save(buffered, format="PNG")
                                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                                
                                st.markdown(f"""
                                    <div style="text-align:center">
                                        <div class="tooth-button">
                                            <img src="data:image/png;base64,{img_base64}"/>
                                            <div class="tooth-number">{tooth_num}</div>
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Error loading icon: {e}")
                        else:
                            # Fallback to default display if icon not found
                            if is_missing:
                                st.markdown(f"""
                                    <div style="text-align:center">
                                        <div class="missing-tooth">
                                            <span class="missing-tooth-symbol">✕</span>
                                        </div>
                                        <div class="tooth-number">{tooth_num}</div>
                                    </div>
                                """, unsafe_allow_html=True)
                
                # For upper jaw, show buttons after icons
                if jaw_type == "Upper":
                    # Create columns for buttons
                    button_cols = st.columns(len(all_teeth))
                    for idx, tooth_num in enumerate(all_teeth):
                        with button_cols[idx]:
                            is_missing = tooth_num in missing_teeth or tooth_num not in case_data["present"][jaw_key]
                            is_implant = tooth_num in case_data["implant"][jaw_key]
                            is_bridge = tooth_num in case_data["bridge"][jaw_key]
                            
                            # Add button if tooth is present or is an implant or is a bridge
                            if not is_missing or is_implant or is_bridge:
                                # Add an invisible button over the icon
                                if st.button("", key=f"tooth_{tooth_num}_clicked", type="secondary"):
                                    case_number = st.session_state.current_case.split()[1] if st.session_state.current_case else None
                                    case_img_path = os.path.join("UCLL_dataset_24", "Trial_cases", f"case_{case_number}", f"{tooth_num}.jpg")
                                    if os.path.exists(case_img_path):
                                        st.session_state.selected_tooth = tooth_num
                                        st.session_state.popup_image = case_img_path
                                        # Do NOT set viewing_mode or show_popup
                                        st.rerun()
                
            display_teeth_row("Upper", case_data["present"]["maxilla"])
            display_teeth_row("Lower", case_data["present"]["mandible"])

    # Right Column - Treatment Info
    with col3:
        st.markdown("## 🩺 Oral Health Summary")
        
        if st.session_state.current_case:
            case_data = patient_cases[st.session_state.current_case]
            
            # Count teeth by status
            green_count = len(case_data["teeth_green"]["maxilla"]) + len(case_data["teeth_green"]["mandible"])
            yellow_count = len(case_data["teeth_yellow"]["maxilla"]) + len(case_data["teeth_yellow"]["mandible"])
            red_count = len(case_data["teeth_red"]["maxilla"]) + len(case_data["teeth_red"]["mandible"])
            
            st.markdown("### Tooth Status Summary")
            st.markdown(f"🟢 **Healthy - Regular Checkup:** {green_count}")
            st.markdown(f"🟠 **Close Observation:** {yellow_count}")
            st.markdown(f"🔴 **Immediate Treatment Required:** {red_count}")
                
        with st.expander("Oral radiographic report"):
            if st.session_state.current_case:
                pdf_buffer = generate_pdf_report(
                    case_data,
                    st.session_state.notes
                )
                pdf_bytes = pdf_buffer.getvalue()

                st.download_button(
                    label="Generate PDF Report",
                    data=pdf_bytes,
                    file_name=f"{st.session_state.family_name}_{st.session_state.first_name}_dental_report.pdf",
                    mime="application/pdf",

                )
            else:
                st.info("Please upload an X-ray to load a case before downloading a report.")

                
                
        with st.expander("Treated teeth and their treated conditions"):

            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button("Crown", use_container_width=True):
                    st.session_state.treatment_type = "Crown"
            with col2:
                if st.button("Dental filling", use_container_width=True):
                    st.session_state.treatment_type = "Filling"
            with col3:
                if st.button("Root canal treatment", use_container_width=True):
                    st.session_state.treatment_type = "Root Canal"
            
            if st.session_state.current_case:
                treatment_map = {
                    "Crown": "crown",
                    "Filling": "filling",
                    "Root Canal": "root_canal"
                }
                treatment_key = treatment_map[st.session_state.treatment_type]
                st.session_state.affected_teeth = (
                    case_data[treatment_key]["maxilla"] + 
                    case_data[treatment_key]["mandible"]
                )
                
                treatment_images = {
                    "Crown": "crown.jpg",
                    "Filling": "dental_fillings.jpg", 
                    "Root Canal": "root_canal_treatment.jpg"
                }
                
                img_name = treatment_images.get(st.session_state.treatment_type)
                if img_name:
                    img_path = None
                    if case_number := (st.session_state.current_case.split()[1] if st.session_state.current_case else None):
                        case_img_path = os.path.join("UCLL_dataset_24", "Trial_cases", f"case_{case_number}", img_name)
                        if os.path.exists(case_img_path):
                            img_path = case_img_path
                    
                    if not img_path and os.path.exists(img_name):
                        img_path = img_name
                    
                    if img_path:
                        try:
                            st.image(Image.open(img_path), use_container_width=True)
                        except Exception as e:
                            st.error(f"Error loading image: {e}")
                    else:
                        st.info("Treatment image not found")

                
                st.markdown("#### 🦷 Affected Teeth:")
                if st.session_state.affected_teeth:
                    st.markdown(", ".join([f"Tooth {t}" for t in st.session_state.affected_teeth]))
                else:
                    st.info(f"No teeth affected by {st.session_state.treatment_type}")
                
                

        # AI Analysis section
        with st.expander("AI Analysis"):
            st.markdown("### 🤖 AI Diagnostic Analysis")
            
            # Create tabs for different sections of the form
            tab1, tab2, tab3 = st.tabs(["Clinical Data", "Radiographic Data", "Results"])
            
            with tab1:
                st.markdown("#### Clinical Features")
                col1, col2 = st.columns(2)
                
                clinical_data = {}
                with col1:
                    clinical_data['sex'] = st.radio("Sex", ["Male", "Female"])
                    clinical_data['age'] = st.number_input("Age", min_value=1, max_value=120, value=42)
                
                with col2:
                    clinical_data['race'] = st.selectbox("Race", ["Non black", "Black"], index=0)
                    clinical_data['pain'] = st.radio("Pain or paresthesia", ["Yes", "No"], index=1)
                
                # Show X-ray preview in clinical tab
                if uploaded_file:
                    try:
                        image = Image.open(uploaded_file)
                        st.image(image, caption="Uploaded X-ray", width=300)
                    except Exception as e:
                        st.warning("Failed to display X-ray preview")
            
            with tab2:
                st.markdown("#### Radiographic Features")
                
                col1, col2 = st.columns(2)
                
                radiographic_data = {}
                with col1:
                    st.markdown("##### Location and Size")
                    radiographic_data['jaw'] = st.radio("Jaw containing the lesion", ["Maxilla", "Mandible"])
                    radiographic_data['region'] = st.selectbox("Region", ["Molar region", "Ramus region", "Anterior region", "Premolar region"])
                    radiographic_data['teeth_relation'] = st.selectbox("Relationship to teeth", ["Crown associated", "Root associated", "Not tooth associated"])
                    radiographic_data['lesion_count'] = st.selectbox("Number of lesions", ["1", "2", "3", "Multiple"])
                    radiographic_data['lesion_size'] = st.selectbox("Maximum lesion size", ["<1 cm", "1-2 cm", "2-3 cm", ">3 cm"])
                    radiographic_data['lesion_origin'] = st.selectbox("Origin of lesion", ["Central", "Peripheral"], index=0)
                    radiographic_data['borders'] = st.selectbox("Borders of the lesion", ["Corticated", "Defined but not corticated", "Ill-defined"])
                
                with col2:
                    st.markdown("##### Characteristics and Effects")
                    radiographic_data['loculation'] = st.radio("Loculation", ["Unilocular", "Multilocular"])
                    radiographic_data['contents'] = st.radio("Contents of lesions", ["Radiolucent", "Mixed", "Radiopaque"])
                    radiographic_data['contains_teeth'] = st.radio("Contains teeth?", ["Yes", "No"])
                    radiographic_data['expands_cortex'] = st.radio("Expands bony cortex?", ["Yes", "No"])
                    radiographic_data['root_resorption'] = st.radio("Causes root resorption?", ["Yes", "No", "Unselected"])
                    radiographic_data['tooth_displacement'] = st.radio("Causes tooth displacement/impaction?", ["Yes", "No", "Unselected"])
            
            with tab3:
                st.markdown("#### Analysis Results")
                
                # Get X-ray image if available
                image_base64 = None
                if uploaded_file:
                    image_bytes = uploaded_file.getvalue()
                    image_base64 = base64.b64encode(image_bytes).decode()
                
                # Run analysis button
                if st.button("Run AI Analysis", use_container_width=True):
                    with st.spinner("Analyzing..."):
                        result = get_ai_diagnosis(clinical_data, radiographic_data, image_base64)
                        
                        if result["success"]:
                            st.success("Analysis complete!")
                            
                            # Create styled box for diagnosis with darker background
                            st.markdown("""
                            <style>
                            .diagnosis-box {
                                background-color: #1E1E1E;
                                border-left: 4px solid #00FF00;
                                padding: 20px;
                                border-radius: 4px;
                                margin: 10px 0;
                                color: #FFFFFF;
                                font-size: 16px;
                                font-weight: 500;
                                line-height: 1.5;
                            }
                            </style>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"""
                            <div class="diagnosis-box">
                            {result["diagnosis"]}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Add to notes button
                            if st.button("Add to Notes"):
                                if st.session_state.notes:
                                    st.session_state.notes += f"\n\n--- AI DIAGNOSIS ---\n{result['diagnosis']}"
                                else:
                                    st.session_state.notes = f"--- AI DIAGNOSIS ---\n{result['diagnosis']}"
                                st.success("Added to notes!")
                        else:
                            st.error(f"Analysis failed: {result['error']}")
                else:
                    st.info("Click 'Run AI Analysis' to get diagnostic assessment")
        
        st.markdown("### 📝 Notes")
        st.session_state.notes = st.text_area(
            "Write any additional notes here...",
            value=st.session_state.notes,
            height=100,
            key='notes_area'
        )
            

    # Tooth Popup
    if st.session_state.show_popup and st.session_state.selected_tooth:
        tooth_num = st.session_state.selected_tooth
        case_data = patient_cases.get(st.session_state.current_case, {})
        
        # Determine treatment
        treatment_type = next(
            (t for t in ["crown", "filling", "root_canal", "bridge", "implant"]
            if tooth_num in case_data.get(t, {}).get("maxilla", []) + case_data.get(t, {}).get("mandible", [])),
            None
        )
        
        # Find image
        img_path = None
        if case_number := (st.session_state.current_case.split()[1] if st.session_state.current_case else None):
            case_img_path = os.path.join("UCLL_dataset_24", "Trial_cases", f"case_{case_number}", f"{tooth_num}.jpg")
            if os.path.exists(case_img_path):
                img_path = case_img_path
        
        if not img_path:
            tooth_3d_path = os.path.join("tooth_3d", f"{tooth_num}.png")
            if os.path.exists(tooth_3d_path):
                img_path = tooth_3d_path
        
        if not img_path and treatment_type:
            treatment_img_path = f"{treatment_type}.jpg"
            if os.path.exists(treatment_img_path):
                img_path = treatment_img_path
        
        if img_path:
            try:
                img = Image.open(img_path)
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                st.markdown(f"""
                    <div class="popup-overlay">
                        <div class="popup">
                            <h4>Tooth {tooth_num}{f" - {treatment_type.title()}" if treatment_type else ""}</h4>
                            <img src="data:image/png;base64,{img_base64}"/>
                            <button onclick="document.querySelector('#close_popup').click();">Close</button>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading image: {e}")
        else:
            st.warning(f"No image found for Tooth {tooth_num}")

        if st.button("Close", key="close_popup"):
            st.session_state.show_popup = False
            st.rerun()

if st.session_state.selected_tooth and st.session_state.popup_image:
    tooth_num = st.session_state.selected_tooth
    img_path = st.session_state.popup_image
    case_data = patient_cases[st.session_state.current_case]
    jaw_key = "maxilla" if tooth_num < 29 else "mandible"

    st.markdown("---")
    st.markdown(f"## 🦷 Tooth {tooth_num} Detail")
    cols = st.columns([1, 2])
    with cols[0]:
        if img_path and os.path.exists(img_path):
            st.image(Image.open(img_path), width=200)
        quadrant = (tooth_num // 10)
        position = tooth_num % 10
        quadrant_name = ["Upper Right (Maxilla)", "Upper Left (Maxilla)", "Lower Left (Mandible)", "Lower Right (Mandible)"][quadrant-1]
        tooth_types = ["", "Central Incisor", "Lateral Incisor", "Canine", "First Premolar", "Second Premolar", "First Molar", "Second Molar", "Third Molar (Wisdom Tooth)"]
        tooth_type = tooth_types[position] if position < len(tooth_types) else ""
        st.markdown(f"**Tooth ID:** {tooth_num}")
        st.markdown(f"**Location:** {quadrant_name}")
        st.markdown(f"**Type:** {tooth_type}")

    with cols[1]:
        st.markdown("### Dental Status")
        if tooth_num in case_data["missing"][jaw_key]:
            st.markdown("**⚠️ This tooth is missing**")
        elif tooth_num not in case_data["present"][jaw_key]:
            st.markdown("**⚠️ This tooth is not present**")
        else:
            st.markdown("**✓ This tooth is present**")
        if tooth_num in case_data["teeth_green"][jaw_key]:
            st.success("🟢 Healthy - Regular Checkup")
        elif tooth_num in case_data["teeth_yellow"][jaw_key]:
            st.warning("🟠 Close Observation")
        elif tooth_num in case_data["teeth_red"][jaw_key]:
            st.error("🔴 Immediate Treatment Required")

        st.markdown("**Detailed Conditions**")
        if tooth_num in case_data["filling"][jaw_key]:
            st.markdown("✓ **Filling:** This tooth has a dental filling")
        if tooth_num in case_data["root_canal"][jaw_key]:
            st.markdown("✓ **Root Canal:** This tooth has had root canal treatment")
        if tooth_num in case_data["crown"][jaw_key]:
            st.markdown("✓ **Crown:** This tooth has a dental crown")
        if tooth_num in case_data["bridge"][jaw_key]:
            st.markdown("✓ **Bridge:** This tooth is part of a dental bridge")
        if tooth_num in case_data["implant"][jaw_key]:
            st.markdown("✓ **Implant:** This tooth has a dental implant")
        if tooth_num in case_data["impacted"][jaw_key]:
            st.markdown("✓ **Impacted:** This tooth is impacted")

        st.markdown("**Treatment Recommendations**")
        if tooth_num in case_data["filling"][jaw_key] and tooth_num in case_data["root_canal"][jaw_key]:
            st.markdown("• Consider crown placement for better protection")
        elif tooth_num in case_data["filling"][jaw_key]:
            st.markdown("• Monitor filling condition at next checkup")
        elif tooth_num in case_data["root_canal"][jaw_key]:
            st.markdown("• Recommend crown placement to prevent fracture")
        elif tooth_num in case_data["missing"][jaw_key]:
            st.markdown("• Consider dental implant or bridge")
        else:
            st.markdown("• Continue regular dental hygiene")
            st.markdown("• No specific treatment needed at this time")
        if st.session_state.treatment_type and tooth_num in st.session_state.affected_teeth:
            st.markdown(f"**Current Treatment Plan:** {st.session_state.treatment_type}")

        st.markdown("**Risk Assessment**")
        risk_level = "Low"
        if tooth_num in case_data["filling"][jaw_key] and tooth_num in case_data["root_canal"][jaw_key]:
            risk_level = "Moderate"
        elif tooth_num in case_data["root_canal"][jaw_key]:
            risk_level = "Moderate"
        st.markdown(f"**Risk Level:** {risk_level}")
        st.markdown("**Factors to consider:**")
        if risk_level == "Moderate":
            st.markdown("• Previous dental work increases risk of complications")
        else:
            st.markdown("• No significant risk factors identified")

    # Add a close button to clear the selection
    if st.button("Close Tooth Detail"):
        st.session_state.selected_tooth = None
        st.session_state.popup_image = None
        st.rerun()