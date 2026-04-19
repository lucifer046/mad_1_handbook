# MAD-I Handbook

> **Modern Web App Development I** — A premium, interactive learning experience designed for high-performance curriculum exploration.

![MAD-I Handbook Logo](book/logo.png)

## Features

- **Exclusive Accordion Navigation**: A fluid, "liquid-flow" Table of Contents that keeps you focused by automatically collapsing non-active sections.
- **Cyber-Minimalist Design**: A state-of-the-art UI with a sophisticated color palette, premium typography (Inter & Fira Code), and smooth micro-animations.
- **Multilingual Syntax Highlighting**: Native support for **Python**, **SQL**, and **Bash** powered by PrismJS, featuring an custom "X-Ray" tooltip system for variable analysis.
- **Mathematical Precision**: Full integration with **MathJax** for beautiful, LaTeX-style formula rendering.
- **Command Palette (Ctrl + K)**: Lightning-fast navigation and searching across the entire handbook.
- **Locked Aesthetics**: Hard-locked against dark mode extensions to ensure the premium design remains exactly as intended.
- **Dynamic Build System**: A Python-based automation script that builds the curriculum metadata directly from your folder structure.

---

## Getting Started

### 1. Installation
Clone the repository to your local machine:
```bash
git clone <repository-url>
cd MAD_1_handbook
```

### 2. Update Curriculum Data
The handbook automatically discovers new experiments and theory sections. If you add new files, run the build script to update the metadata:
```bash
python book/build_data.py
```

### 3. Running Locally
Simply open `index.html` in any modern web browser or use a Live Server extension in your IDE for the best experience.

---

## Project Structure

- `book/`: Core application logic, styling, and the automated build system.
  - `app.js`: Interactive UI logic and curriculum rendering.
  - `style.css`: The Cyber-Minimalist design system.
  - `build_data.py`: The curriculum discovery script.
- `Practical_Experiments/`: Hands-on coding modules.
- `Theory_Sections/`: Comprehensive theoretical documentation.
- `index.html`: The main entry point of the handbook.

---

## Technology Stack

- **Frontend**: Vanilla JavaScript, HTML5, CSS3.
- **Typography**: [Inter](https://fonts.google.com/specimen/Inter) & [Fira Code](https://fonts.google.com/specimen/Fira+Code).
- **Libraries**:
  - [PrismJS](https://prismjs.com/): Advanced code highlighting.
  - [Lucide](https://lucide.dev/): Crisp, modern iconography.
  - [MathJax](https://www.mathjax.org/): LaTeX formula rendering.

---

## License
This project is designed for educational purposes as part of the Modern Web App Development curriculum.

---
*Created with passion for Modern Web App Development.*
