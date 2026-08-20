#!/usr/bin/env python3
"""
Simple script to update the headline font in style.css
Run with: python3 update-font.py "Font Name"
"""
import sys
import re
from pathlib import Path

def update_font(font_name):
    css_file = Path(__file__).parent / 'assets' / 'style.css'
    
    if not css_file.exists():
        print(f"Error: {css_file} not found")
        return False
    
    # Read the CSS file
    content = css_file.read_text()
    
    # Pattern to match the font-family declarations
    # We'll update both .site-title and h2
    font_pattern = r'font-family:"[^"]*",'
    
    # Create the new font declaration
    new_font_decl = f'font-family:"{font_name}",'
    
    # Update site-title
    content = re.sub(
        r'(\.site-title\{[^}]*?)font-family:"[^"]*",',
        r'\1' + new_font_decl,
        content
    )
    
    # Update h2
    content = re.sub(
        r'(h2\{[^}]*?)font-family:"[^"]*",',
        r'\1' + new_font_decl,
        content
    )
    
    # Write back to the file
    css_file.write_text(content)
    print(f"✓ Updated headlines to use {font_name}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 update-font.py 'Font Name'")
        sys.exit(1)
    
    font_name = sys.argv[1]
    if update_font(font_name):
        print(f"Reload your browser to see the changes.")
        sys.exit(0)
    else:
        sys.exit(1)
