# Data Tracking Plan Dashboard

A comprehensive Flask-based dashboard for analyzing and visualizing tracking implementations across **Amplitude**, **Insider**, and **Google Tag Manager (GTM)**.

## 🎯 Project Overview

This project provides a unified view of your data tracking plan across multiple platforms, enabling you to:

- **Amplitude**: Analyze events, properties, and schema validation status
- **Insider**: Review event definitions, parameters, and PII compliance  
- **GTM**: Examine tags, variables, triggers, and data destinations for both server-side and client-side containers

## 📊 Key Features

### **Platform Analytics**
- **Events Count**: Total events per platform
- **Parameters Analysis**: Properties and parameter types distribution
- **Schema Validation**: Tracking schema status and compliance
- **Data Destinations**: Where your tracking data is being sent

### **GTM Specific Features**
- **Container Comparison**: Server-side vs Client-side analysis
- **Tag Management**: Active/paused tags with destination mapping
- **Data Flow Analysis**: Trigger relationships and dependencies
- **Destination Tracking**: Complete view of where data flows

### **Cross-Platform Insights**
- **Unified Dashboard**: Summary metrics across all platforms
- **Data Quality Reports**: Inconsistencies and validation issues
- **Export Capabilities**: Data export for further analysis

## 🏗️ Project Structure

```
DataTrackingPlan/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── parsers/                        # Data parsing modules
│   ├── amplitude_parser.py         # Amplitude CSV parser
│   ├── insider_parser.py           # Insider JSON parser
│   └── gtm_parser.py              # GTM JSON parser
│
├── models/                         # Data models and schemas
├── services/                       # Business logic services
│
├── static/                         # Static files (CSS, JS, images)
│   ├── css/dashboard.css
│   └── js/charts.js
│
├── templates/                      # HTML templates
│   ├── base.html                   # Base template
│   ├── dashboard.html              # Main dashboard
│   └── error.html                  # Error handling
│
└── sources/                        # Your data files
    ├── amplitude/
    │   └── Kavak - PROD_events_2025-07-17T12_55_21.764+00_00.csv
    ├── insider/
    │   └── insider.json
    └── gtm/
        ├── GTM-P32K5GT_workspace486.json    # Server-side
        └── GTM-NRGXLJ_workspace1002673.json # Client-side
```

## 🚀 Getting Started

### **Prerequisites**
- Python 3.8+
- Flask 2.3+
- Pandas for data processing
- Modern web browser

### **Installation**

1. **Clone or set up the project directory**
```bash
cd DataTrackingPlan
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify your data sources are in place**
```
sources/
├── amplitude/*.csv
├── insider/*.json  
└── gtm/*.json
```

4. **Run the application**
```bash
python app.py
```

5. **Access the dashboard**
```
http://localhost:5000
```

## 📈 Platform Metrics

### **Amplitude Analysis**
- **Total Events**: Complete count of tracked events
- **Properties**: Unique event properties and their types
- **Schema Status**: Validation and approval status
- **Activity Status**: Active vs. deleted events
- **Volume Metrics**: 180-day event volume and query counts

### **Insider Analysis** 
- **Events & Parameters**: Total counts and unique parameters
- **Parameter Types**: String, number, boolean, array distribution
- **PII Compliance**: Events and parameters with PII data
- **Segmentation**: Parameters enabled for segmentation
- **Parameter Reuse**: Cross-event parameter usage analysis

### **GTM Analysis**
- **Tags**: Total, active, and paused tag counts
- **Variables**: Custom and built-in variables by type
- **Triggers**: Firing conditions and trigger types
- **Destinations**: Where your data is being sent (GA4, Facebook, Amplitude, etc.)
- **Container Types**: Separate analysis for server-side vs client-side

## 🎨 Dashboard Views

### **Main Dashboard**
- Overview cards for each platform
- Summary statistics across all platforms  
- Quick navigation to detailed views

### **Platform Detail Pages**
- **Amplitude**: Events list, properties breakdown, schema status
- **Insider**: Events with parameters, PII analysis, usage patterns
- **GTM**: Tags management, destination analysis, data flow visualization

### **API Endpoints**
- `/api/amplitude/events` - Amplitude events data
- `/api/insider/events` - Insider events data  
- `/api/gtm/<container_type>/tags` - GTM tags data

## 🔧 Configuration

Edit `config.py` to customize:

```python
class Config:
    # Data sources paths
    AMPLITUDE_CSV = 'path/to/amplitude/export.csv'
    INSIDER_JSON = 'path/to/insider/events.json'
    GTM_SERVER_JSON = 'path/to/gtm/server-container.json'
    GTM_CLIENT_JSON = 'path/to/gtm/client-container.json'
```

## 🧪 Testing the Parsers

You can test individual parsers before running the full application:

```python
# Test Amplitude parser
from parsers.amplitude_parser import AmplitudeParser
amplitude = AmplitudeParser('sources/amplitude/your-file.csv')
print(amplitude.get_platform_overview())

# Test Insider parser  
from parsers.insider_parser import InsiderParser
insider = InsiderParser('sources/insider/insider.json')
print(insider.get_events_summary())

# Test GTM parser
from parsers.gtm_parser import GTMParser
gtm = GTMParser('sources/gtm/your-container.json')
print(gtm.get_container_info())
```

## 📋 Data Requirements

### **Amplitude CSV Export**
- Must include columns: `Object Type`, `Object Name`, `Event Property Name`, etc.
- Export from Amplitude's Data section

### **Insider JSON Export** 
- Event definitions with parameters
- Must include `key`, `display_name`, `params` structure

### **GTM JSON Export**
- Workspace export from GTM
- Both server-side and client-side containers supported
- Includes tags, variables, triggers, and container metadata

## 🚦 Status Indicators

- ✅ **Green**: Active/Available data
- ⚠️ **Yellow**: Warnings or pending items
- ❌ **Red**: Errors or deleted items
- ℹ️ **Blue**: Informational metrics

## 🔮 Next Steps

The current implementation focuses on data extraction and basic visualization. Potential enhancements:

1. **Data Validation**: Cross-platform event name consistency checks
2. **Advanced Analytics**: Trending analysis and usage patterns
3. **Export Features**: PDF reports and data exports
4. **Real-time Updates**: Automated data refresh from APIs
5. **Comparison Tools**: Before/after implementation analysis

## 📝 Notes

- The dashboard is read-only and doesn't modify your source data
- Large datasets are paginated for performance
- All data processing happens locally
- No external API calls required for basic functionality

---

**Built for analyzing Kavak's data tracking implementation across Amplitude, Insider, and Google Tag Manager.** 