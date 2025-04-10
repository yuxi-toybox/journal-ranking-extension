
# Journal Ranking Extension Tutorial

This repository contains the code and tutorial for building a journal ranking extension, which queries journal rankings from SJR and Fenqubiao and displays them directly in a browser extension.

## 📝 Overview

This project consists of two major components:

1. **Backend (Flask-based API)**: A Flask server that scrapes the SJR website and returns journal rankings.
2. **Frontend (Chrome Extension)**: A Chrome extension that allows users to query journal rankings directly from the browser.

### Features:
- Query journal rankings using SJR
- View journal rankings in a simple and easy-to-use Chrome extension popup
- Track last query results and save them for future reference

---

## ⚙️ Setup and Installation

### Backend Setup

The backend uses Flask to serve the API that provides journal ranking data.

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Journal-Ranking-Extension.git
   cd Journal-Ranking-Extension
   ```

2. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   python app.py
   ```

5. Your backend API will be available at `http://127.0.0.1:5050`.

---

### Frontend Setup

The frontend is a Chrome extension that interacts with the Flask backend API.

1. Open Google Chrome and navigate to `chrome://extensions/`.

2. Enable **Developer Mode** by toggling the switch in the top-right corner.

3. Click on **Load Unpacked** and select the `frontend` directory.

4. The extension will now be available in your browser.

---

## 🛠️ Running the Application

1. Once the backend server is running, you can query journal rankings from the extension popup.
2. The extension will show the results and keep them stored for future use.
3. If you need to make changes, simply update the code in `frontend/` or `backend/` and reload the extension.

---

## 💡 Features to Add

- Integration with other journal ranking APIs
- Support for more journal data points
- Background processing for continuous journal tracking
- User authentication for accessing personalized rankings

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Feel free to fork this repository, make improvements, and create pull requests. For large contributions, open an issue to discuss the changes before proceeding.

---

## 🔗 Resources

- [SJR website](https://www.scimagojr.com/)
- [Flask documentation](https://flask.palletsprojects.com/)
- [Chrome Extension Developer Guide](https://developer.chrome.com/docs/extensions/mv3/getstarted/)
