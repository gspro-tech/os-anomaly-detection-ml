# OS Anomaly Detection System

An Operating System anomaly detection system built using **Machine Learning (Isolation Forest)** to identify abnormal behavior based on system resource usage. The system analyzes **CPU utilization, memory usage, disk usage, and process-level metrics**, and displays results using a **Flask-based web dashboard**.

This project was developed during a **hackathon** and successfully **qualified for Round 2**.

---

## 🚀 Features
- Unsupervised anomaly detection using **Isolation Forest**
- Monitoring of OS-level metrics (CPU, memory, disk usage)
- Process-level behavior analysis
- **CSV-based data storage** for model training and learning
- Web-based visualization using **Flask**
- Real-time anomaly detection output in browser (Chrome)

---

## 🛠️ Tech Stack
- **Language:** Python  
- **Machine Learning:** Isolation Forest (scikit-learn)  
- **Web Framework:** Flask  
- **Data Handling:** Pandas, NumPy, CSV  
- **System Monitoring:** psutil  

---

## 📊 How It Works
1. System metrics such as CPU, memory, disk usage, and process data are collected.
2. Collected data is stored in **CSV files** for historical learning.
3. The **Isolation Forest** model is trained on normal system behavior.
4. Incoming real-time data is analyzed to detect anomalies.
5. Results are displayed through a **Flask web interface**.
---
Note on AI Assistance

This project was developed with the assistance of AI tools (e.g., ChatGPT) for code generation and optimization. The overall system design, integration, and understanding were carried out by the author.
