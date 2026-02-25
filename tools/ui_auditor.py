import os
import re
import json
from collections import defaultdict
from typing import Dict, List, Any
import sys
import os
from pathlib import Path

# Add script directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from tools.constants import (
        PROJECT_ROOT, TEMPLATES_DIR, CSS_DIR, OUTPUT_JSON, OUTPUT_MD,
        CSS_VARS, HEX_COLOR_PATTERN, INLINE_STYLE_PATTERN, 
        IMG_TAG_PATTERN, A_TAG_PATTERN
    )
except ImportError:
    try:
        from constants import (
            PROJECT_ROOT, TEMPLATES_DIR, CSS_DIR, OUTPUT_JSON, OUTPUT_MD,
            CSS_VARS, HEX_COLOR_PATTERN, INLINE_STYLE_PATTERN, 
            IMG_TAG_PATTERN, A_TAG_PATTERN
        )
    except ImportError:
        # Fallback if both fail (unlikely if path is correct)
        raise

class UIAuditor:
    def __init__(self):
        self.report: Dict[str, Any] = {
            "design_tokens": [],
            "inline_styles": [],
            "accessibility": [],
            "structure": [],
            "consistency": []
        }

    def scan_files(self):
        print("Starting UI/UX Audit...")
        self._scan_css()
        self._scan_templates()
        self._generate_report()
        print("Audit complete. Reports generated.")

    def _scan_css(self):
        """Scan CSS files for hardcoded colors instead of variables."""
        for css_file in CSS_DIR.glob("*.css"):
            relative_path = css_file.relative_to(PROJECT_ROOT)
            content = css_file.read_text(encoding="utf-8")
            
            # Find hex colors
            matches = re.finditer(HEX_COLOR_PATTERN, content)
            for match in matches:
                original_hex = match.group(0)
                hex_color = original_hex.upper()
                line_no = content[:match.start()].count('\n') + 1
                
                # Check if it's a definition of a variable (skip)
                line_content = content.splitlines()[line_no-1]
                if line_content.strip().startswith("--"):
                    continue
                    
                if hex_color in CSS_VARS:
                    self.report["design_tokens"].append({
                        "file": str(relative_path),
                        "line": line_no,
                        "issue": f"Hardcoded color {original_hex}",
                        "token": original_hex,
                        "suggestion": f"Use var({CSS_VARS[hex_color]})"
                    })

    def _scan_templates(self):
        """Scan HTML templates for inline styles, accessibility, and consistency."""
        for html_file in TEMPLATES_DIR.glob("*.html"):
            relative_path = html_file.relative_to(PROJECT_ROOT)
            content = html_file.read_text(encoding="utf-8")
            lines = content.splitlines()

            for i, line in enumerate(lines):
                line_no = i + 1
                
                # 1. Inline Styles
                if 'style="' in line:
                    self.report["inline_styles"].append({
                        "file": str(relative_path),
                        "line": line_no,
                        "issue": "Inline style detected",
                        "content": line.strip()
                    })

                # 2. Hardcoded Colors in HTML
                hex_matches = re.finditer(HEX_COLOR_PATTERN, line)
                for match in hex_matches:
                    original_hex = match.group(0)
                    hex_color = original_hex.upper()
                    if hex_color in CSS_VARS:
                         self.report["design_tokens"].append({
                            "file": str(relative_path),
                            "line": line_no,
                            "issue": f"Hardcoded color {original_hex} in HTML",
                            "token": original_hex,
                            "suggestion": f"Use var({CSS_VARS[hex_color]}) in CSS class"
                        })

                # 3. Accessibility - Images
                img_matches = re.finditer(IMG_TAG_PATTERN, line)
                for _ in img_matches:
                    if 'alt="' not in line:
                        self.report["accessibility"].append({
                            "file": str(relative_path),
                            "line": line_no,
                            "issue": "Image missing alt attribute"
                        })

                # 4. Accessibility - Empty Links
                a_matches = re.finditer(A_TAG_PATTERN, line)
                for _ in a_matches:
                    if 'href=""' in line or 'href="#"' in line:
                        self.report["accessibility"].append({
                            "file": str(relative_path),
                            "line": line_no,
                            "issue": "Empty or placeholder link"
                        })

    def _generate_report(self):
        # Save JSON
        with open(OUTPUT_JSON, 'w') as f:
            json.dump(self.report, f, indent=2)

        # Save Markdown Summary
        with open(OUTPUT_MD, 'w') as f:
            f.write("# UI/UX Audit Summary\n\n")
            f.write(f"Generated on: {os.popen('date').read().strip()}\n\n")
            
            f.write("## 1. Design Tokens Issues\n")
            f.write(f"Found {len(self.report['design_tokens'])} instances of hardcoded colors.\n")
            for item in self.report['design_tokens'][:5]: # Show first 5
                f.write(f"- `{item['file']}:{item['line']}`: {item['issue']} -> **{item['suggestion']}**\n")
            if len(self.report['design_tokens']) > 5:
                f.write(f"- ... and {len(self.report['design_tokens']) - 5} more.\n")
            
            f.write("\n## 2. Inline Styles\n")
            f.write(f"Found {len(self.report['inline_styles'])} instances of inline styles.\n")
            for item in self.report['inline_styles'][:5]:
                f.write(f"- `{item['file']}:{item['line']}`: `{item['content']}`\n")
            
            f.write("\n## 3. Accessibility\n")
            f.write(f"Found {len(self.report['accessibility'])} accessibility issues.\n")
            for item in self.report['accessibility']:
                f.write(f"- `{item['file']}:{item['line']}`: {item['issue']}\n")

if __name__ == "__main__":
    auditor = UIAuditor()
    auditor.scan_files()

