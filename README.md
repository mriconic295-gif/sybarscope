# 🛡️ CyberScope - Cybersecurity Analysis & Reconnaissance Tool

**CyberScope** is a comprehensive, open-source cybersecurity reconnaissance and intelligence-gathering application built with Python and CustomTkinter. It allows security analysts, penetration testers, and web administrators to perform complete domain, network, and vulnerability assessments from an intuitive graphical user interface (GUI).

---

## ✨ Features & Capabilities

* **🌐 Domain & IP Intelligence**
  * **URL & Domain Validation:** Ensures input strings are properly structured before execution.
  * **DNS Records Lookup:** Resolves `A`, `AAAA`, `MX`, `NS`, `TXT`, `CNAME`, and `SOA` records.
  * **IP & ASN Lookup:** Extracts server IPv4/IPv6 details, Autonomous System Numbers (ASN), and ISP details.
  * **GeoIP Tracking:** Identifies hosting server location (Country, Region, City, Latitude/Longitude).
  * **WHOIS Reconnaissance:** Gathers domain registrar information, creation/expiration dates, and contact emails.

* **🔒 SSL/TLS & Web Security**
  * **SSL Certificate Analysis:** Validates SSL validity, issuer details, protocol versions, and expiration dates.
  * **HTTP Security Headers Inspection:** Detects presence and misconfigurations of critical security headers (`CSP`, `HSTS`, `X-Frame-Options`, `X-Content-Type-Options`, etc.).

* **🔎 Infrastructure & Technology Fingerprinting**
  * **Technology Stack Detection:** Identifies CMS, web servers (Nginx, Apache, IIS), frameworks, and analytics tags.
  * **Open Port Scanning:** Scans common network ports (`21`, `22`, `80`, `443`, `3306`, `8080`, etc.) for exposed services.
  * **CDN & Origin IP Exposure Check:** Identifies whether a domain is behind Cloudflare/WAF and attempts to detect potential origin IP leaks.

* **📸 Automated Web Reconnaissance**
  * **Automated Screenshots:** Captures live homepage rendering using headless Selenium Chrome Driver with HTTP Render fallback support.

* **🤖 AI-Powered Risk Assessment**
  * **Rule-Based Vulnerability Scoring:** Automatically evaluates network and SSL misconfigurations to produce an accurate Risk Score (`0-100`).
  * **Smart Threat Summaries:** Generates concise security findings and actionable remediation steps.

---

## 🚀 Installation & Usage Guide

Follow the steps below according to your operating system to set up and run **CyberScope**.

---

### 🐧 Option 1: Linux / macOS Setup

#### Step 1: Clone the Repository
Open your terminal and clone the CyberScope project:
```bash
git clone [https://github.com/your-username/cyberscope.git](https://github.com/your-username/cyberscope.git)
cd cyberscope
Step 2: Create a Virtual Environment (myenv)
It is recommended to use an isolated environment for Python packages:

Bash
python3 -m venv myenv
Step 3: Activate the Virtual Environment
Bash
source myenv/bin/activate
(Once activated, you will see (myenv) prefixed to your shell prompt).

Step 4: Install Required Packages
Install all necessary dependencies listed in requirements.txt:

Bash
pip install -r requirements.txt
Step 5: Launch CyberScope
Start the main application GUI:

Bash
python3 main.py

🪟 Option 2: Windows Setup
Step 1: Open Command Prompt & Clone Repository
Open Command Prompt (cmd) or PowerShell and run:

DOS
git clone https://github.com/mriconic295-gif/sybarscope.git
cd cyberscope
Step 2: Create a Virtual Environment (myenv)
DOS
python -m venv myenv
Step 3: Activate the Virtual Environment
DOS
myenv\Scripts\activate
(You should now see (myenv) at the beginning of your command prompt line).

Step 4: Install Required Packages
DOS
pip install -r requirements.txt
Step 5: Run the Tool
DOS
python main.py
📌 Usage Workflow
Launch CyberScope using python main.py.

Enter the target URL or domain name (e.g., example.com or https://example.com) in the top search bar.

Click the Scan / Analyze button.

View real-time results categorized into tabs:

Dashboard / Risk Score

DNS & WHOIS

SSL & Security Headers

Tech Stack & Open Ports

Web Screenshot

🛠️ Requirements & Prerequisites
Python: Version 3.8 or higher.

Google Chrome: Required for headless screenshot generation.

Pip Packages:

customtkinter (GUI Interface)

requests (HTTP requests & API interaction)

selenium & webdriver-manager (Automated screenshots)

python-whois (WHOIS resolution)

dnspython (DNS record querying)

Pillow (Image handling)

⚠️ Disclaimer
CyberScope is developed for educational, security research, and authorized defensive auditing purposes only. Performing unauthorized scans against targets without prior permission may violate applicable cyber laws. Always ensure you have permission before scanning any infrastructure.
