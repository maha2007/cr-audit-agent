# FCR Audit AI Agent - Quick Start Guide

## Setup (One-Time)

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

2. **Configure API Key**:
   - Create `.env` file in project root
   - Add: `ANTHROPIC_API_KEY=your_api_key_here`
   - Get key from: https://console.anthropic.com/

## Running the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Quick Workflow

1. **Upload PDFs** → Select credit proposal PDFs
2. **Enter Info** → Obligor name and outstanding limit (sidebar)
3. **Configure** → Choose model and thinking level (sidebar)
4. **Run Analysis** → Click "Start Audit Analysis"
5. **View Results** → See scores, justifications, and findings
6. **Export** → Download JSON results

## Features

✅ Multi-PDF upload and processing  
✅ AI-powered audit analysis (Claude Sonnet 4.5 API)  
✅ 5 Pillars × 16 Questions evaluation  
✅ Interactive results table with expandable details  
✅ Weighted scoring system  
✅ Issue identification and findings  
✅ JSON export  

## Troubleshooting

- **API Key Error**: Check `.env` file has `ANTHROPIC_API_KEY`
- **Import Errors**: Run `pip install -r requirements.txt`
- **PDF Errors**: Ensure PDFs have selectable text (not just scanned)

