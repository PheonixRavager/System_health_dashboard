## **System Health Monitoring Dashboard**⚙️💻

A real-time dashboard to monitor CPU, Memory, Disk, and Network usage using Python and Streamlit.
The app collects system performance metrics every few seconds and displays interactive visualizations,
recent logs, and summary insights.
```
System_health_dashboard/
├── app.py                    # Streamlit dashboard application
├── utils/
│   └── system_stats.py       # Functions for collecting system metrics (CPU, RAM, Disk, Network)
├── data/
│   └── system_log.csv        # (Auto-generated) System logs stored with timestamps
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation (this file)

```
## **Description** ##

**Goal**:
To create a real-time system monitoring dashboard that provides insights into system performance using live data collected from psutil.

 ### **✅Features:** 

 #### Real-time tracking of: 

* CPU usage (%)

* Memory usage (%)

* Disk usage (%)

* Network activity (Sent/Received MB)

#### Interactive controls 

* Choose metrics to display

* Select refresh interval

* Time range filtering (1 min, 5 min, 15 min, all records)

####  Visualizations

* Line charts for performance over time

* Recent system statistics table

#### Data Logging

* Automatically logs all readings to system_log.csv

* Downloadable logs directly from the app

#### Dashboard Statistics

* Total records collected

* Last updated timestamp

* Dashboard uptime

**A clean, minimal design with a dark modern UI theme.**

### **✅Getting Started**
**1. Clone this repository**
 ``` 
git clone <your-repo-url>
cd System_health_dashboard
 ``` 

**2. Install dependencies**

(Optional) Create & activate a virtual environment:
 ``` 
python -m venv .venv
 ``` 

Windows:
 ``` 
.venv\Scripts\activate
 ``` 

Linux/Mac:
 ``` 
source .venv/bin/activate
 ``` 
**Install packages:**
 ``` 
pip install -r requirements.txt
 ``` 
**3. Launch the Dashboard**
streamlit run app.py


The app will open automatically at:

http://localhost:8501

### **Dashboard Features**
#### 📊 Filters & Controls

* Choose refresh interval (1s–10s)

* Checkbox metric selection:

* CPU

* Memory

* Disk

* Network Sent

* Network Received

* Time-range filters
(1 min • 5 min • 15 min • all data)

#### 📈 Visualizations

* Line charts with live updates:

* CPU Usage Trend

* Memory Usage Trend

* Disk Usage Trend

* Network Sent/Received Trend

#### 📋 Data Table

* Always shows the latest 20 records

* Uses real timestamps

#### 📥 CSV Download

Download the cleaned and filtered system log from dashboard:

**system_health_log.csv**

Notes

system_log.csv grows over time — you can delete or archive it as needed.

Metrics depend on device hardware and workload.

For extended monitoring, you can deploy the app on Streamlit Cloud.

#### Future Enhancements

Here are optional features you may add later:

* Pause/Resume tracking
* Alerts for high CPU/Memory
* Light/Dark theme toggle
* Email/SMS notification triggers


#### Author 

Developed by **Ansal P Mathew**

LinkedIn:[Profile](https://www.linkedin.com/in/ansalmathew)