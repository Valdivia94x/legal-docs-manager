#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docx import Document
import sys
import os

def safe_print(text):
    """Print text safely handling encoding issues"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Replace problematic characters
        safe_text = text.encode('ascii', 'replace').decode('ascii')
        print(safe_text)

def extract_docx_format(file_path):
    try:
        doc = Document(file_path)
        
        safe_print("=== DOCUMENT STRUCTURE ===")
        structure = []
        
        for i, paragraph in enumerate(doc.paragraphs):
            if paragraph.text.strip():
                # Get style information
                style_name = paragraph.style.name if paragraph.style else 'Normal'
                alignment = str(paragraph.alignment) if paragraph.alignment else 'None'
                
                para_info = {
                    'index': i,
                    'text': paragraph.text,
                    'style': style_name,
                    'alignment': alignment,
                    'runs': []
                }
                
                # Check runs for formatting
                for j, run in enumerate(paragraph.runs):
                    if run.text.strip():
                        run_info = {
                            'text': run.text,
                            'bold': run.bold,
                            'italic': run.italic,
                            'underline': run.underline
                        }
                        para_info['runs'].append(run_info)
                
                structure.append(para_info)
                
                safe_print(f"\nParagraph {i}:")
                safe_print(f"  Style: {style_name}")
                safe_print(f"  Alignment: {alignment}")
                safe_print(f"  Text length: {len(paragraph.text)} chars")
                
                if paragraph.text.startswith('ORDEN'):
                    safe_print("  -> This is the HEADER")
                elif any(word in paragraph.text.lower() for word in ['perspectivas', 'politicas', 'economicas']):
                    safe_print("  -> This is an AGENDA ITEM")
                
        return structure
                            
    except Exception as e:
        safe_print(f"Error reading document: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    file_path = r"d:\Asus\Documents\Olea\Olea_Avances_v5\Olea\DOCUMENTOS OLEA ABOGADOS\Actas Sesiones de Consejo\OrdenDelDiaFormat.docx"
    structure = extract_docx_format(file_path)
    
    safe_print("\n=== FORMAT SUMMARY ===")
    for item in structure:
        if 'ORDEN' in item['text']:
            safe_print(f"HEADER: Style='{item['style']}', Alignment={item['alignment']}")
        else:
            safe_print(f"ITEM: Style='{item['style']}', Alignment={item['alignment']}")
