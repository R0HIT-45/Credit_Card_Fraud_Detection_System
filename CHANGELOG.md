# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-06-29

### Added
- **FraudSense AI v1.0 Production Release**.
- Developed a highly polished, single-column SaaS-style web interface.
- Built a Rule-based **Explainable AI** module mapping contextual banking variables (Amount, Device, VPN, Location, etc.) to the dual-model ML output.
- Interactive transaction preset cards (UPI, ATM, International, Shopping) for seamless ML demonstrations.
- Advanced Model Configuration section allowing technical users to safely edit hidden PCA features.
- Dual-Model prediction panel showcasing both Random Forest and XGBoost outputs side-by-side with risk thresholds.
- Premium UI aesthetics including custom dark mode, large typography, SVG branding, and smooth CSS transitions.
- Comprehensive repository documentation (World-class `README.md`, `.gitignore`, `PROJECT_STRUCTURE.md`).

### Changed
- Replaced the multi-page/cluttered dashboard concept with a clean, focused single-page analyzer.
- Overhauled CSS to decouple monolithic classes and implement modular CSS variables (`style.css`).
- Rewrote the client-side controller (`app.js`) to streamline API request compilation and cleanly handle dynamic UI updates without duplicate logic.

### Removed
- Cleaned up root directory by deleting obsolete planning docs (`COMPLETION_REPORT.md`, `INDEX.md`, etc.).
- Removed unnecessary UI elements (sidebars, timeline feeds) that did not directly support the ML feature presentation.
- Removed unused and duplicate CSS/JS logic.
