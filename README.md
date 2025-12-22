# 🌈 Luminous-Behavior Study: Effects of Color on Distance Perception

**Authors**: Fernando Augusto & Daniel Sora
**Country**: Mozambique  
**Fields**: Aerospace Engineering & Data Science  
**Year**: 2024

---

## 🎯 Project Overview

An interdisciplinary scientific investigation into how **different colored lighting affects human distance perception accuracy**. This research combines hardware engineering, statistical analysis, and experimental psychology to provide insights for aviation display design and human-machine interface optimization.

## 🔬 Scientific Question

**Does the color of ambient lighting significantly affect distance estimation accuracy in humans?**

## 📊 Key Findings

- **Red lighting** → Most accurate distance perception (±2.1cm error)
- **Blue lighting** → Systematic overestimation (+3.8cm average)
- **Green lighting** → Intermediate performance
- **Statistical significance**: p < 0.05 (ANOVA, F=8.42)
- **Effect size**: Medium (Cohen's d = 0.65)

## 🛠️ Technical Implementation

### Hardware System
- **Microcontroller**: Arduino Uno
- **Distance Sensor**: HC-SR04 Ultrasonic (2-400cm range)
- **Visual Stimuli**: RGB LED with controlled color output
- **Ambient Sensing**: IR luminosity sensor
- **Data Output**: Serial communication to computer

### Software Pipeline
- **Data Collection**: Custom Arduino firmware with randomized protocol
- **Analysis**: Python statistical pipeline (ANOVA, effect sizes, visualization)
- **Visualization**: Publication-ready charts and graphs

## 🏗️ Project Structure

```
Luminous-Behavior-Study/
├── README.md          # This file (English)
├── README_PT.md       # Portuguese version
├── LICENSE           # MIT License
├── .gitignore        # Git ignore rules
├── hardware/         # Arduino code & schematics
├── analysis/         # Python scripts & sample data
├── docs/            # Scientific documentation
└── images/          # Photos & diagrams
```

## 🚀 Getting Started

### 1. Hardware Setup
```bash
# Assemble circuit following hardware/schematic
# Upload hardware/circuit.ino to Arduino
```

### 2. Software Installation
```bash
# Install Python dependencies
pip install -r analysis/requirements.txt
```

### 3. Run Analysis
```bash
python analysis/analysis.py
```

## 📈 Sample Analysis Output

```
=== LUMINOUS BEHAVIOR STUDY RESULTS ===

Total measurements: 450
ANOVA: F(2,6) = 8.42, p = 0.018*
Effect size: Cohen's d = 0.65 (medium)

Color Performance:
- RED:   45.2 ± 2.1 cm (most accurate)
- GREEN: 43.8 ± 2.9 cm
- BLUE:  46.5 ± 3.3 cm (overestimation)
```

## 🎓 Academic Value

This project demonstrates:
- ✅ **Experimental design** skills
- ✅ **Hardware-software integration**
- ✅ **Statistical analysis** proficiency
- ✅ **Scientific writing** and documentation
- ✅ **Interdisciplinary collaboration**

## 🌍 Context & Impact

### For Mozambique:
- **Local innovation** with accessible components
- **STEM education** advancement
- **Research capacity** building
- **Global contribution** from African students

### For Aerospace Engineering:
- **Cockpit display** optimization
- **Aviation safety** improvements
- **Human factors** considerations
- **Training protocol** enhancements

## 👥 Authors & Contributions

### Fernando Augusto- Hardware & Aerospace Applications
- Circuit design and assembly
- Embedded systems programming
- Experimental setup
- Aerospace relevance analysis

### Daniel Sora- Data Science & Statistics
- Statistical methodology
- Python analysis pipeline
- Data visualization
- Hypothesis testing

## 📚 Documentation

- [Scientific Abstract](docs/abstract.md)
- [Methodology](docs/methodology.md)
- [Results Summary](docs/results_summary.md)
- [Components List](hardware/components.txt)

## 📞 Contact
 
**Location**: Mozambique  
**GitHub**: https://github.com/meme5y

---

*"Advancing scientific inquiry through interdisciplinary collaboration in Mozambique."*
