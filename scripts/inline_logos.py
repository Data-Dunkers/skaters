import base64
import re
from pathlib import Path

html_path = Path(r'c:\Users\miste\Documents\GitHub\skaters\docs\card-creator\card-creator.html')
content = html_path.read_text(encoding='utf-8')

logos = ['dell-logo.png', 'lotus-8-esports-logo.png', 'mfnerc-logo.png', 'ps43-foundation-logo.png']
base_dir = Path(r'c:\Users\miste\Documents\GitHub\skaters\docs\card-creator')

for logo in logos:
    logo_path = base_dir / logo
    if logo_path.exists():
        encoded = base64.b64encode(logo_path.read_bytes()).decode('utf-8')
        data_uri = f'data:image/png;base64,{encoded}'
        # Replace <img src="logo"> with <img src="data_uri">
        content = content.replace(f'src="{logo}"', f'src="{data_uri}"')

html_path.write_text(content, encoding='utf-8')
print('Logos inlined successfully!')
