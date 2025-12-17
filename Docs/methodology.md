# SCIENTIFIC METHODOLOGY

## 1. Experimental Design
- **Type**: Within-subjects repeated measures
- **Independent Variable**: Light color (3 levels: Red, Green, Blue)
- **Dependent Variable**: Distance estimation accuracy (cm)
- **Controls**: Fixed lighting, consistent participant position

## 2. Hardware Setup
- **Microcontroller**: Arduino Uno
- **Distance Sensor**: HC-SR04 Ultrasonic (2-400cm range)
- **Visual Stimuli**: RGB LED with calibrated colors
- **Data Collection**: Serial communication at 115200 baud

## 3. Experimental Protocol
1. System calibration and testing
2. Participant briefing (informed consent)
3. Random color sequence generation
4. 10-second exposure per color
5. Continuous distance measurement (200ms intervals)
6. Data logging with timestamps

## 4. Statistical Analysis
- **Software**: Python 3.9+
- **Packages**: Pandas, NumPy, SciPy, Pingouin
- **Tests**: ANOVA, Tukey HSD, Effect sizes
- **Visualization**: Matplotlib, Seaborn

## 5. Ethical Considerations
- Informed consent obtained
- Participant anonymity maintained
- No physical or psychological risks
- Data used only for research purposes
