# 🛡️ AI-Powered Network Threat Classification System

**Intel Unnati Industrial Training 2025**  
**Problem Statement 1: Network Security**  
**Team Name: Execthron**


---

## 🎥 Demo

▶️ [Watch Demo Video](https://drive.google.com/file/d/1SIK_kruyaB2uLdFsY7iY5bJJZ7SaKgWz/view?usp=drivesdk)

---

## 📌 Project Overview

The **AI-Powered Traffic Classification Model** is a real-time intelligent system designed to detect and classify network traffic as **malicious** or **safe** using flow-level features.

Built with a **Random Forest machine learning model**, the system is deployed via a simple and efficient **Flask web interface**. It supports `.csv` file uploads, analyzes the data, and visualizes the results instantly.

---

## 💡 Key Features

* 🔍 Real-time classification of uploaded `.csv` traffic logs
* 🧠 AI-powered Random Forest model trained on UNSW-NB15
* 📈 Visualization with **Chart.js** (pie chart: malicious vs. safe)
* 🌐 Flask-based web interface for ease of use
* 🧾 Display of predicted traffic labels with protocol and classification only (e.g., Safe/Malicious)

---

## 📚 Dataset Used

**UNSW-NB15** – A labeled dataset containing both normal and malicious network traffic.

Includes:

* DoS
* Exploits (including SQL Injection, XSS, Buffer Overflow, Shellcode, etc.)
* Fuzzers
* Reconnaissance
* Analysis
* Backdoors

> 📌 Provided by: Australian Centre for Cyber Security (ACCS)

---

## 🧰 Tech Stack

| Layer        | Technologies                        |
| ------------ | ----------------------------------- |
| Language     | Python                              |
| Backend      | Flask, Flask-CORS                   |
| ML Libraries | Scikit-learn, Joblib, Pandas, NumPy |
| Frontend     | HTML, CSS, JavaScript, Chart.js     |

---


## ✅ Outcomes

* Achieved **accurate classification** of malicious vs. safe traffic using a Random Forest model.
* Designed a **user-friendly interface** for uploading and analyzing `.csv` network logs.
* Successfully integrated **real-time visualization** of predictions using Chart.js.
* Demonstrated the practicality of ML models in supporting **automated network threat detection** in a lightweight environment.

---

## ⚠️ Limitations

* The model is trained only on **offline flow data** and does not process **live packet capture**.
* Limited to `.csv` files with specific feature formatting; **data preprocessing must match training setup**.
* Accuracy and generalization may reduce on **real-world enterprise networks** due to differences from training data.
* Does not show full metadata like source/destination IP, time, etc., which can help with deeper threat investigation.

---

## 🚀 Future Scope

* Extend the system to support **real-time packet sniffing** using tools like `PyShark` or `Scapy`.
* Add **detailed analytics** with IP/port-level information and interactive dashboards.
* Integrate **alerting systems** (e.g., email, Telegram) for critical threat detections.
* Experiment with **deep learning models** (e.g., LSTM, CNN) for improved accuracy on complex patterns.
* Provide **cloud deployment** for scalability and integration with existing SIEM tools.

---


## ⚙️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Vasu-uu/Network-Threat-Analyzer.git
cd Network-Threat-Analyzer
```

### 2️⃣ Install Python Packages

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
python app.py
```

### 4️⃣ Open the App

Visit in your browser:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

---

## 👥 Contributors

* **Steny Thankkam Raju**
* **Vasudev V**
* **Jalphy Reji**

> ✅ *Submitted as part of Intel Unnati Industrial Training 2025 – Team Execthron*

---

---

## 🙏 Acknowledgements

* Intel Unnati Industrial Training Team
* Australian Centre for Cyber Security – UNSW-NB15 Dataset

---
