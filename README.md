# Scraper.ai 🕸️
🚀 Live App: https://scraper-ai.onrender.com

Scraper.ai is a full-stack web scraper + AI formatter powered by Google Gemini API.  
You give it a URL and a natural language prompt, it scrapes the content (using requests or Selenium), then formats/summarizes it using AI.

## 🚀 Features
- **Web Scraping**: Supports both BeautifulSoup for static pages and Selenium for dynamic, JavaScript-heavy sites.  
- **AI Processing**: Uses Google Gemini API to format, summarize, or transform scraped content.  
- **Frontend**: Streamlit interface for a clean and interactive user experience.  
- **Backend**: Flask API that manages scraping, AI calls, and response handling.  
- **Deployment**: Structured for easy hosting on Render with separate frontend and backend services.  

---



## Local Setup
1️⃣ Clone the repository

- git clone https://github.com/aniruddramesh/Scraper.ai.git
- cd scraper-ai

2️⃣ Backend setup

- cd backend
- pip install -r requirements.txt

3️⃣ Set environment variables
- Create a .env file inside the backend folder:

- GEMINI_API_KEY=your_api_key_here
- Or set it directly in your terminal:

- export GEMINI_API_KEY=your_api_key_here  # Mac/Linux
- set GEMINI_API_KEY=your_api_key_here     # Windows

5️⃣ Run the backend
- cd backend
- python app.py
- The backend will start at http://127.0.0.1:5000.

6️⃣ Run the frontend
- In another terminal:
- cd frontend
- streamlit run app.py
- Frontend will run on http://localhost:8501
