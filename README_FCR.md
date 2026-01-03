# FCR Audit AI Agent - Web Application

A web-based tool for automated Fundamental Credit Review (FCR) audits using AI-powered analysis.

## Features

- **Multi-PDF Processing**: Upload and analyze multiple credit proposal PDFs simultaneously
- **AI-Powered Analysis**: Uses Anthropic Claude Sonnet 4.5 API for intelligent audit analysis
- **Five Pillar Framework**: Evaluates credit proposals across 5 pillars with 16 specific questions
- **Interactive Results**: View detailed scores, justifications, and findings in an interactive table
- **Export Capabilities**: Download audit results as JSON

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```
   - Get your API key from: https://console.anthropic.com/

3. Download spaCy language model (if not already done):
```bash
python -m spacy download en_core_web_sm
```

## Usage

### Running the Web Application

Start the Streamlit application:
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Application

1. **Upload PDFs**: 
   - Go to the "Upload & Process" tab
   - Click "Choose PDF files" and select one or more credit proposal PDFs
   - Enter obligor name and outstanding limit (optional)

2. **Configure Settings** (Sidebar):
   - Model: claude-sonnet-4-5-20250929 (automatically selected)
   - Choose thinking level (high/medium/low) - kept for compatibility
   - Enter obligor information

3. **Run Analysis**:
   - Click "Start Audit Analysis"
   - Wait for processing to complete (extraction → prompt preparation → AI analysis → results)

4. **View Results**:
   - Go to "Results" tab to see:
     - Overall summary
     - Pillar scores (weighted and unweighted)
     - Detailed question analysis with scores, justifications, and citations
     - Issues raised (questions with scores ≤ 2)

5. **Export Results**:
   - Go to "Export" tab
   - Download results in JSON, Excel, or PDF format
   - All formats match the web visualization layout

## Five Pillar Analysis

The audit evaluates credit proposals across:

1. **Bank Guidelines** (30% weight)
2. **Proposal Quality** (35% weight)
3. **Financial Analysis** (20% weight)
4. **Rating Veracity** (10% weight)
5. **Early Warning & Collateral** (5% weight)

## Scoring System

- **Score 1**: Critical deficiency - Information completely missing
- **Score 2**: Significant deficiency - Information present but not adequately addressed
- **Score 3**: Adequate - Information present and reasonably addressed
- **Score 4**: Excellent - Information comprehensive and well-articulated

Scores ≤ 2 generate findings that must be addressed.

## Output Format

Results can be exported in three formats (JSON, Excel, PDF), all containing:
- Obligor information
- Individual question scores (1-16) with justifications
- Pillar scores (weighted and unweighted)
- Issues raised

Excel and PDF formats match the web visualization layout with formatted tables, color-coded scores, and organized sections.

## Troubleshooting

### API Key Issues
- Ensure `ANTHROPIC_API_KEY` is set in `.env` file
- Verify the API key is valid and has access to Claude models

### PDF Extraction Errors
- Ensure PDFs are not password-protected
- Check that PDFs contain selectable text (not just scanned images)
- For scanned PDFs, OCR may be required

### Processing Errors
- Check that all dependencies are installed
- Verify internet connection for API calls
- Review error messages in the application for specific issues

## Deployment

### Quick Deployment to Streamlit Cloud

1. **Push code to GitHub** (if not already done)
2. **Go to Streamlit Cloud**: https://share.streamlit.io/
3. **Sign in with GitHub** and click "New app"
4. **Select your repository** and set main file to `app.py`
5. **Set API Key Secret**:
   - Go to Settings → Secrets
   - Add: `ANTHROPIC_API_KEY = "your_key_here"`
6. **Deploy** and share the public URL

### Detailed Deployment Guide

For complete step-by-step instructions, security considerations, and troubleshooting, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Security Notes

- ✅ API keys are stored securely in Streamlit Secrets (encrypted)
- ✅ Never commit API keys to Git
- ⚠️ Public deployment means anyone can use your API key (monitor costs)
- 💡 Consider adding authentication for production use

## Architecture

- **PDF Extraction**: Claude 4.5 Sonnet Visual API for PDF-to-Markdown conversion
- **AI Analysis**: Anthropic Claude Sonnet 4.5 API (claude-sonnet-4-5-20250929)
- **Web Interface**: Streamlit
- **Data Processing**: Custom modules for prompt generation, result processing, and scoring

## License

This project is provided as-is for FCR audit purposes.

