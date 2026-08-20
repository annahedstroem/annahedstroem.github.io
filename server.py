#!/usr/bin/env python3
"""Simple server to serve the site and handle font updates"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class FontUpdateHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve static files normally
        super().do_GET()
    
    def do_POST(self):
        if self.path == '/update-font':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)
            font_name = data.get('font', 'Roboto Mono')
            
            # Update CSS file
            css_path = Path('/Users/annahedstrom/Projects/annahedstroem.github.io/assets/style.css')
            css_content = css_path.read_text()
            
            # Import the new font if not already there
            if font_name not in css_content:
                if '@import' in css_content:
                    # Add font to imports
                    import_line = f"family={font_name.replace(' ', '+')}"
                    if import_line not in css_content:
                        css_content = css_content.replace(
                            '@import url(',
                            f"@import url('https://fonts.googleapis.com/css2?{import_line}&display=swap');\n@import url("
                        )
            
            # Update .site-title and h2 font-family
            old_title_pattern = '.site-title{font-size:28px;margin:0;font-family:"'
            old_h2_pattern = 'h2{font-size:22px;margin:48px 0 14px;font-family:"'
            
            # Find and replace title font
            if old_title_pattern in css_content:
                start = css_content.find(old_title_pattern)
                end = css_content.find('",', start)
                if start != -1 and end != -1:
                    css_content = css_content[:start + len(old_title_pattern)] + font_name + css_content[end:]
            
            # Find and replace h2 font
            if old_h2_pattern in css_content:
                start = css_content.find(old_h2_pattern)
                end = css_content.find('",', start)
                if start != -1 and end != -1:
                    css_content = css_content[:start + len(old_h2_pattern)] + font_name + css_content[end:]
            
            css_path.write_text(css_content)
            
            # Return success response
            response = json.dumps({'success': True, 'font': font_name}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(response))
            self.end_headers()
            self.wfile.write(response)
        else:
            self.send_error(404)

if __name__ == '__main__':
    os.chdir('/Users/annahedstrom/Projects/annahedstroem.github.io')
    server = HTTPServer(('localhost', 8000), FontUpdateHandler)
    print('Server running on http://localhost:8000')
    print('Font options at http://localhost:8000/font-options-retro.html')
    server.serve_forever()
