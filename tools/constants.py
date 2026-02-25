from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
CSS_DIR = PROJECT_ROOT / "static" / "css"
OUTPUT_JSON = PROJECT_ROOT / "audit_report.json"
AUDIT_REPORT_PATH = OUTPUT_JSON  # Alias for fixer agent
OUTPUT_MD = PROJECT_ROOT / "AUDIT_SUMMARY.md"

# CSS Variables mapping (Hex -> Var)
CSS_VARS = {
    "#4F46E5": "--primary-color",
    "#4338CA": "--primary-hover", # Note: Uppercase for normalization
    "#64748B": "--secondary-color",
    "#10B981": "--success-color",
    "#F59E0B": "--warning-color",
    "#EF4444": "--danger-color",
    "#0EA5E9": "--info-color",
    "#F3F4F6": "--light-bg",
    "#1F2937": "--dark-text",
    "#6B7280": "--muted-text",
    "#E5E7EB": "--border-color",
    "#2C1863": "--amplitude-color",
    "#00BFA5": "--insider-color",
    "#4285F4": "--gtm-color",
    "#FFFFFF": "white",
    "#000000": "black",
}

# Regex Patterns
HEX_COLOR_PATTERN = r"#(?:[0-9a-fA-F]{3}){1,2}"
INLINE_STYLE_PATTERN = r'style="([^"]*)"'
IMG_TAG_PATTERN = r'<img\s+[^>]*>'
A_TAG_PATTERN = r'<a\s+[^>]*>'

