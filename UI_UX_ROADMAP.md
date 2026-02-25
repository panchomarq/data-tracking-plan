# UI/UX Remediation Roadmap

Based on the automated audit performed on Jan 13, 2026, we have identified the following areas for improvement.

## Phase 1: Standardization (Low Effort, High Impact)

**Objective**: Eliminate inconsistencies in color usage and remove inline styles.

### 1.1 Fix Hardcoded Colors
- **Issue**: Found hardcoded colors in `static/css/dashboard.css` (e.g., `#FFFFFF`, `#F3F4F6`).
- **Action**: Replace instances with their corresponding CSS variables (e.g., `var(--light-bg)`).
- **Target Files**: `static/css/dashboard.css`

### 1.2 Remove Inline Styles
- **Issue**: Found 24 instances of inline styles, primarily `style="font-size: 0.7rem;"` in dashboard cards.
- **Action**: 
    - Create a utility class `.text-xs` or similar in `dashboard.css`.
    - Replace `style="..."` attributes with this class.
- **Target Files**: `templates/dashboard.html`, `templates/gtm.html`, etc.

## Phase 2: Component Architecture (Medium Effort)

**Objective**: Reduce code duplication by extracting repeated UI patterns into Jinja macros.

### 2.1 Metric Cards
- **Observation**: The "Metric Card" pattern (Value + Label + Icon) is repeated across `dashboard.html` and platform detail pages.
- **Action**: Create `templates/components/metrics.html` with a `metric_card` macro.

### 2.2 Platform Cards
- **Observation**: The platform summary cards in `dashboard.html` share identical structure but have different content.
- **Action**: Create `templates/components/cards.html` with a `platform_card` macro.

## Phase 3: Accessibility & Polish (Ongoing)

**Objective**: Ensure the application is usable by everyone.

### 3.1 Review Semantic HTML
- Ensure headers (`h1`-`h6`) follow a logical hierarchy.
- Verify table headers have `scope="col"`.

### 3.2 Focus States
- Ensure all interactive elements (buttons, links, inputs) have visible focus states (audited via `dashboard.css`).

## Phase 4: Enhancements (Future)

- Implement DataTables.js for sorting/filtering large event lists.
- Add "Copy to Clipboard" functionality for event properties.

