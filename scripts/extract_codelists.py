#!/usr/bin/env python3
"""
Extract codelists from OECD structure XML file and generate label mappings.

This script parses the OECD structure XML file to extract official code-to-label mappings
for various dimensions used in OECD datasets.
"""

import xml.etree.ElementTree as ET
import json
from pathlib import Path

def extract_codelist_from_xml(xml_file, codelist_id):
    """Extract a specific codelist from the XML structure file"""
    print(f"Extracting codelist: {codelist_id}")
    
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Define namespaces
    namespaces = {
        'structure': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
        'common': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common',
        'xml': 'http://www.w3.org/XML/1998/namespace'
    }
    
    # Find the codelist
    codelist = root.find(f'.//structure:Codelist[@id="{codelist_id}"]', namespaces)
    
    if codelist is None:
        print(f"  Codelist {codelist_id} not found")
        return {}
    
    # Extract codes and their names
    codes = {}
    for code in codelist.findall('.//structure:Code', namespaces):
        code_id = code.get('id')
        name_elem = code.find('.//common:Name[@xml:lang="en"]', namespaces)
        
        if name_elem is not None:
            codes[code_id] = name_elem.text
        else:
            codes[code_id] = code_id  # Fallback to code ID if no name found
    
    print(f"  Found {len(codes)} codes")
    return codes

def extract_all_relevant_codelists(xml_file):
    """Extract all relevant codelists for our datasets"""
    codelists = {}
    
    # Define the codelists we need based on the unlabeled variables
    codelist_mappings = {
        'CL_ADJUSTMENT': 'ADJUSTMENT',
        'CL_AREA': 'REF_AREA',  # This should already exist but let's get the official version
        'CL_SECTOR': 'SECTOR',  # This should already exist but let's get the official version
        'CL_UNIT_MEASURE': 'UNIT_MEASURE',  # This should already exist but let's get the official version
        'CL_TRANSFORMATION': 'TRANSFORMATION',
        'CL_FREQ': 'FREQ',  # This should already exist but let's get the official version
        'CL_INSTR_ASSET': 'INSTR_ASSET',
        'CL_TABLEID': 'TABLE_IDENTIFIER',
        'CL_TRANSACTION': 'TRANSACTION',  # This should already exist but let's get the official version
    }
    
    for codelist_id, mapping_name in codelist_mappings.items():
        codes = extract_codelist_from_xml(xml_file, codelist_id)
        if codes:
            codelists[mapping_name] = codes
    
    return codelists

def create_label_mappings_script(codelists):
    """Create a Python script with the extracted label mappings"""
    script_content = '''#!/usr/bin/env python3
"""
Official OECD Label Mappings extracted from structure file.

This module contains official code-to-label mappings extracted from OECD's 
structure XML file for various dimensions used in OECD datasets.
"""

def get_official_oecd_mappings():
    """Get official OECD label mappings extracted from structure file"""
    mappings = {}
    
'''
    
    for mapping_name, codes in codelists.items():
        script_content += f'    # {mapping_name} mappings (official OECD)\n'
        script_content += f'    {mapping_name.lower()}_mappings = {{\n'
        for code, label in codes.items():
            # Escape quotes in labels
            label = label.replace("'", "\\'").replace('"', '\\"')
            script_content += f"        '{code}': '{label}',\n"
        script_content += '    }\n\n'
    
    script_content += '    # Add all mappings to the main dictionary\n'
    for mapping_name in codelists.keys():
        script_content += f'    mappings["{mapping_name}"] = {mapping_name.lower()}_mappings\n\n'
    
    script_content += '    return mappings\n'
    
    return script_content

def main():
    """Main function to extract codelists and generate mappings"""
    print("=" * 60)
    print("Extracting OECD Codelists from Structure File")
    print("=" * 60)
    
    # Path to the structure file
    structure_file = Path("data/temp_structure.xml")
    
    if not structure_file.exists():
        print(f"Error: Structure file {structure_file} does not exist")
        return
    
    # Extract codelists
    codelists = extract_all_relevant_codelists(structure_file)
    
    if not codelists:
        print("No codelists found!")
        return
    
    # Print summary
    print("\n" + "=" * 60)
    print("Extracted Codelists Summary:")
    print("=" * 60)
    
    for mapping_name, codes in codelists.items():
        print(f"\n{mapping_name}:")
        print(f"  Total codes: {len(codes)}")
        print(f"  Sample codes:")
        for i, (code, label) in enumerate(list(codes.items())[:5]):
            print(f"    {code}: {label}")
        if len(codes) > 5:
            print(f"    ... and {len(codes) - 5} more")
    
    # Save to JSON for reference
    output_file = Path("results/official_oecd_mappings.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(codelists, f, indent=2)
    
    print(f"\nSaved mappings to: {output_file}")
    
    # Generate Python script
    script_content = create_label_mappings_script(codelists)
    script_file = Path("src/official_oecd_mappings.py")
    script_file.parent.mkdir(exist_ok=True)
    
    with open(script_file, 'w') as f:
        f.write(script_content)
    
    print(f"Generated Python module: {script_file}")
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Review the extracted mappings in results/official_oecd_mappings.json")
    print("2. Update label_data.py to use the official mappings from src/official_oecd_mappings.py")
    print("3. Test the updated labeling script")
    print("=" * 60)

if __name__ == "__main__":
    main() 