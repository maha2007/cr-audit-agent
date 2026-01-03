# Deployment Guide - FCR Audit AI Agent

This guide walks you through deploying the FCR Audit AI Agent to Streamlit Cloud, making it publicly accessible while keeping your API keys secure.

## Prerequisites

Before deploying, ensure you have:

1. **GitHub Account**: Free account at https://github.com
2. **Streamlit Cloud Account**: Free account at https://share.streamlit.io (sign in with GitHub)
3. **Anthropic API Key**: Get from https://console.anthropic.com/
4. **Code Repository**: Your code pushed to a GitHub repository

## Important Security & Cost Considerations

### API Key Security
- ✅ **NEVER** hardcode API keys in code or commit them to Git
- ✅ Use Streamlit Secrets for deployment (secure, encrypted)
- ✅ Keep `.env` for local development (already in `.gitignore`)
- ✅ The code automatically checks Streamlit secrets first, then falls back to environment variables

### Cost Implications
- ⚠️ **Public deployment means anyone can use your API key and generate costs**
- Each audit uses Claude API (costs per token)
- Monitor your API usage in the Anthropic console
- Consider adding rate limiting or authentication if costs are a concern (see Optional Enhancements below)

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Ensure your code is committed and pushed to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Verify `.gitignore` excludes sensitive files:**
   - `.env` should be ignored
   - `.streamlit/secrets.toml` should be ignored (if you create it locally)
   - Any log files should be ignored

### Step 2: Connect to Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Create a New App:**
   - Click "New app" button
   - Select your GitHub repository
   - Choose the branch (usually `main` or `master`)
   - Set the main file path to: `app.py`
   - Click "Deploy"

### Step 3: Configure API Key Secret

1. **In Streamlit Cloud Dashboard:**
   - Go to your app's settings (click the three dots menu → "Settings")
   - Navigate to "Secrets" section

2. **Add Your API Key:**
   - Click "Edit secrets"
   - Add the following:
   ```toml
   ANTHROPIC_API_KEY = "your_actual_api_key_here"
   ```
   - Replace `your_actual_api_key_here` with your actual Anthropic API key
   - Click "Save"

3. **Verify Secret is Set:**
   - The secret should appear in the secrets editor
   - It will be encrypted and only visible to you

### Step 4: Deploy and Test

1. **Deploy the App:**
   - If not already deployed, click "Deploy" in the Streamlit Cloud dashboard
   - Wait for the build to complete (usually 1-2 minutes)

2. **Test the Application:**
   - Open the app URL (provided by Streamlit Cloud)
   - Try uploading a PDF and running an analysis
   - Verify that the API key is working correctly

3. **Check Logs:**
   - If there are errors, check the logs in Streamlit Cloud dashboard
   - Common issues:
     - Missing API key → Check secrets configuration
     - Import errors → Check `requirements.txt` has all dependencies
     - API errors → Check API key validity and quota

### Step 5: Share Your App

1. **Get the Public URL:**
   - Your app URL will be: `https://your-app-name.streamlit.app`
   - Or: `https://share.streamlit.io/your-username/your-repo-name`

2. **Share with Users:**
   - Anyone with the URL can access your app
   - No authentication required (unless you add it)

## Updating Your App

After making code changes:

1. **Push changes to GitHub:**
   ```bash
   git add .
   git commit -m "Update description"
   git push origin main
   ```

2. **Streamlit Cloud will automatically redeploy:**
   - Go to your app dashboard
   - Click "Reboot app" if needed
   - Changes are usually live within 1-2 minutes

## Troubleshooting

### App Won't Deploy

**Issue:** Build fails or app won't start

**Solutions:**
- Check that `requirements.txt` includes all dependencies
- Verify `app.py` is in the root directory
- Check logs in Streamlit Cloud dashboard for specific errors
- Ensure Python version is compatible (Streamlit Cloud uses Python 3.9+)

### API Key Not Working

**Issue:** "ANTHROPIC_API_KEY not found" error

**Solutions:**
- Verify secret is set in Streamlit Cloud (Settings → Secrets)
- Check secret name matches exactly: `ANTHROPIC_API_KEY`
- Ensure no extra spaces or quotes in the secret value
- Try redeploying the app after setting the secret

### Import Errors

**Issue:** Module not found errors

**Solutions:**
- Verify all dependencies are in `requirements.txt`
- Check that package names are correct
- Some packages may need specific versions (e.g., `anthropic>=0.40.0`)
- Rebuild the app after updating `requirements.txt`

### High API Costs

**Issue:** Unexpected API usage/costs

**Solutions:**
- Monitor usage in Anthropic console: https://console.anthropic.com/
- Set up usage alerts/limits in Anthropic dashboard
- Consider adding authentication (see Optional Enhancements)
- Consider adding rate limiting per user/session

## Optional Enhancements

### Add Authentication

To protect your app from unauthorized use:

1. **Simple Password Protection:**
   - Add a password check at the start of `app.py`
   - Use Streamlit secrets to store the password
   - Only allow access after password verification

2. **OAuth/SSO:**
   - Integrate with Google/Microsoft OAuth
   - Use Streamlit's authentication components
   - Restrict access to specific email domains

### Add Rate Limiting

To prevent API abuse:

1. **Session-based Rate Limiting:**
   - Track requests per session
   - Limit number of audits per session
   - Show warning when limit reached

2. **IP-based Rate Limiting:**
   - Track requests per IP address
   - Use Streamlit session state or external service
   - Block excessive requests

### Add Usage Monitoring

1. **Log API Calls:**
   - Track token usage per request
   - Store usage statistics
   - Display usage dashboard

2. **Set Usage Quotas:**
   - Limit total API calls per day
   - Alert when approaching limits
   - Automatically disable app if quota exceeded

## Local Development vs. Deployment

### Local Development
- Uses `.env` file for API key
- Run with: `streamlit run app.py`
- Access at: `http://localhost:8501`

### Streamlit Cloud Deployment
- Uses Streamlit Secrets for API key
- Automatically deployed from GitHub
- Public URL provided by Streamlit Cloud

The code automatically detects which environment it's running in and uses the appropriate method to load the API key.

## Support

For issues or questions:
- Check Streamlit Cloud documentation: https://docs.streamlit.io/streamlit-cloud
- Review Anthropic API documentation: https://docs.anthropic.com/
- Check application logs in Streamlit Cloud dashboard

## Security Best Practices

1. ✅ **Never commit API keys to Git**
2. ✅ **Use Streamlit Secrets for deployment**
3. ✅ **Monitor API usage regularly**
4. ✅ **Set up usage alerts/limits**
5. ✅ **Consider authentication for production use**
6. ✅ **Keep dependencies up to date**
7. ✅ **Review logs for suspicious activity**

