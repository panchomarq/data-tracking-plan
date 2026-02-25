import json
import re
from pathlib import Path
from typing import Dict, Any
import sys
import os
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Also add tools dir to path for direct execution
tools_dir = str(Path(__file__).parent)
if tools_dir not in sys.path:
    sys.path.append(tools_dir)

try:
    from tools.constants import PROJECT_ROOT, AUDIT_REPORT_PATH, CSS_VARS
except ImportError:
    try:
        from constants import PROJECT_ROOT, AUDIT_REPORT_PATH, CSS_VARS
    except ImportError:
        # Last resort: try importing as if we are in the tools dir
        import constants
        PROJECT_ROOT = constants.PROJECT_ROOT
        AUDIT_REPORT_PATH = constants.AUDIT_REPORT_PATH
        CSS_VARS = constants.CSS_VARS

class UIFixerAgent:
    def __init__(self):
        self.report = self._load_report()

    def _load_report(self) -> Dict[str, Any]:
        if not AUDIT_REPORT_PATH.exists():
            print("No audit report found. Please run ui_auditor.py first.")
            return {}
        with open(AUDIT_REPORT_PATH, 'r') as f:
            return json.load(f)

    def fix_design_tokens(self, auto_apply=False):
        """Replaces hardcoded colors with CSS variables."""
        print("\n--- Fixing Design Tokens ---")
        issues = self.report.get("design_tokens", [])
        if not issues:
            print("No design token issues to fix.")
            return

        for issue in issues:
            file_path = PROJECT_ROOT / issue["file"]
            line_no = issue["line"]
            
            # Use specific token if available, else extract from issue text (fallback)
            target_token = issue.get("token")
            if not target_token:
                 match = re.search(r"#(?:[0-9a-fA-F]{3}){1,2}", issue["issue"])
                 if match:
                     target_token = match.group(0)
            
            if not target_token:
                continue

            # Look up using uppercase, but replace exact token
            hex_upper = target_token.upper()
            if hex_upper not in CSS_VARS:
                continue

            replacement = f"var({CSS_VARS[hex_upper]})"
            
            print(f"File: {issue['file']}:{line_no}")
            print(f"  Replace {target_token} -> {replacement}")
            
            if auto_apply:
                self._apply_replacement(file_path, line_no, target_token, replacement)
            else:
                confirm = input("  Apply this fix? (y/n): ")
                if confirm.lower() == 'y':
                    self._apply_replacement(file_path, line_no, target_token, replacement)

    def _apply_replacement(self, file_path: Path, line_no: int, old: str, new: str):
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
            if 0 <= line_no - 1 < len(lines):
                lines[line_no - 1] = lines[line_no - 1].replace(old, new)
                file_path.write_text("\n".join(lines), encoding="utf-8")
                print("  [Fixed]")
            else:
                print("  [Error] Line number out of range.")
        except Exception as e:
            print(f"  [Error] Could not write file: {e}")

    def suggest_macros(self):
        """Analyzes the report for structural repetition and suggests macros."""
        # This is a placeholder for future logic to identify repetitive blocks
        pass

    def run_interactive(self):
        print("Welcome to UI Fixer Agent")
        print("1. Fix Design Tokens (Colors)")
        print("2. Fix Inline Styles (Coming Soon)")
        print("3. Extract Macros (Coming Soon)")
        print("q. Quit")
        
        while True:
            choice = input("\nSelect an action: ")
            if choice == '1':
                self.fix_design_tokens()
            elif choice == 'q':
                break
            else:
                print("Invalid option or feature not implemented yet.")

if __name__ == "__main__":
    agent = UIFixerAgent()
    agent.run_interactive()

