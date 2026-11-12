# 🤖 ML Model Training Engine — PyCharm Guide

Aap PyCharm mein directly is folder ko open karke model train aur evaluate kar sakte hain.

### 📁 PyCharm Project Location:
`G:\farhan_fyp\ml_model`

### 🚀 PyCharm Mein Kaise Run Karein:
1. PyCharm open karein aur **Open** par click karke yeh folder select karein:  
   `G:\farhan_fyp\ml_model`
2. Project explorer mein **`train_electricity_model.py`** par right click karein aur **Run 'train_electricity_model'** dabayein.
3. Console mein:
   * Dataset automatically load/generate hoga.
   * **Linear Regression** train aur evaluate hogi.
   * **Random Forest Regressor** train aur evaluate hoga.
   * **Neural Network** train hoga.
   * Android ke liye **`models/electricity_predictor.tflite`** auto-export ho jayegi!
   * Real sample household par prediction test print hoga.

### 📦 Required Python Libraries:
Agar aap kisi naye laptop par PyCharm open karte hain toh PyCharm terminal mein sirf yeh likhein:
```bash
pip install numpy pandas scikit-learn tensorflow matplotlib
```
Everything is pre-configured and 100% self-contained!

