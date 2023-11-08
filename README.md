# INVENTORY TRACKER
![Static Badge](https://img.shields.io/badge/app_version-v1.0.0-gree)

Browser based dashboard to track inventory.
Built in Python using Dash.
---
## Screenshots

![Screenshot 1](/screenshots/mvp-screenshot.PNG)

---
# Features

### v01 

![Static Badge](https://img.shields.io/badge/status-completed-gree)
- Stock predictor based on historical sales
- Main indicators for supplier
- Export data to excel
- Custom UI

### v02

![Static Badge](https://img.shields.io/badge/status-work_in_progress-yellow)
- Overview page
- Product page
- Historical stock levels
- Custom date picker
- Improved UI

### v03

![Static Badge](https://img.shields.io/badge/status-future_work-red)
- Machine learning stock predictions
- Alerts system

---
## Installation

To install this project, you can use the following steps:

1. Clone the repository
2. Install pyinstaller if you don't have it already
3. Install ODBC driver
4. From the project run:
```
pyinstaller --onefile.spec app.py
```
This will create an executable file on \dist folder that you can run
Sample data is already included.

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](/LICENSE.txt)

