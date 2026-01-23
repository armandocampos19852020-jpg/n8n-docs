# Quick Start: Instagram Reel Automation

This guide will get you started with Instagram Reel automation in 5 minutes.

## Prerequisites

- Python 3.8+
- Instagram account
- Video file (.mp4)

## Step 1: Install Dependencies

```bash
cd /path/to/n8n-docs
pip install -r _doctools/requirements_instagram.txt
```

## Step 2: Set Up Credentials

**Option A: Environment Variables (Recommended)**
```bash
export IG_USERNAME="your_instagram_username"
export IG_PASSWORD="your_instagram_password"
```

**Option B: Interactive (Prompted for password)**
```bash
# Password will be requested when you run the script
```

## Step 3: Upload Your First Reel

### Simple Upload
```bash
python _doctools/upload_instagram_reel.py --video path/to/your/video.mp4
```

### With Caption and Thumbnail
```bash
python _doctools/upload_instagram_reel.py \
  --video path/to/video.mp4 \
  --thumbnail path/to/cover.jpg \
  --caption "Check out my content! 🎥 #ContentCreator"
```

### Using the Helper Script
```bash
./daily_instagram_upload.sh path/to/video.mp4
```

## Step 4: Check Your Upload

1. **On Instagram**: Open the Instagram app → Your profile → Reels tab
2. **Check Logs**: Look for success message with Reel ID
   ```bash
   # If you used daily_instagram_upload.sh
   cat logs_instagram/*.log
   ```

## Where Things Are Stored

### Session File
- **Location**: `insta_session.json` (in the directory where you run the script)
- **Purpose**: Stores login session to avoid re-authenticating
- **Security**: This file is automatically excluded from git (in .gitignore)

### Logs (if using daily script)
- **Location**: `logs_instagram/upload_TIMESTAMP.log`
- **Contains**: Upload status, timestamps, Reel IDs, any errors

### Environment Variables
- Stored in your shell profile (~/.bashrc or ~/.zshrc) if you add them there
- More secure than hardcoding credentials

## Daily Usage

To upload content daily:

```bash
# Method 1: Direct script
python _doctools/upload_instagram_reel.py --video today_video.mp4

# Method 2: Helper script with automatic logging
./daily_instagram_upload.sh today_video.mp4 thumbnail.jpg "Daily content!"
```

## View All Your Uploads

```bash
# List all upload logs
ls -lt logs_instagram/

# View most recent log
cat logs_instagram/$(ls -t logs_instagram/ | head -1)

# Find all successful uploads
grep "¡Éxito!" logs_instagram/*.log

# Get all Reel IDs
grep -oP 'ID: \K[0-9]+' logs_instagram/*.log
```

## Troubleshooting

### "Module not found: instagrapi"
```bash
pip install instagrapi
```

### "Bad Password" Error
1. Verify your username and password
2. Try logging in via Instagram app first
3. Check for pending security verifications

### 2FA Code Requested
1. Check your authenticator app or SMS
2. Enter the 6-digit code when prompted
3. Session will be saved for future use

### Session Expired
```bash
# Delete old session and start fresh
rm insta_session.json
python _doctools/upload_instagram_reel.py --video video.mp4
```

## Integration with n8n

To automate with n8n:

1. Import the workflow: `docs/_workflows/instagram-automation-example.json`
2. Configure the Execute Command node with your video path
3. Set up credentials in n8n
4. Use Cron node to schedule daily uploads

## Documentation

- **Full Documentation**: `docs/code/cookbook/instagram-automation.md`
- **Spanish Guide**: `_doctools/README_INSTAGRAM.md`
- **Implementation Details**: `INSTAGRAM_IMPLEMENTATION_SUMMARY.md`

## Support

For more help with n8n workflows:
- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)

## Security Reminder

⚠️ **Important**:
- Never commit `insta_session.json` to git (already in .gitignore)
- Use environment variables for credentials
- Protect session files: `chmod 600 insta_session.json`
- Don't share your session file or logs containing credentials

---

**Ready to automate!** 🚀

Your Instagram credentials are stored in:
- ✅ Environment variables (if set)
- ✅ Session file: `insta_session.json`
- ✅ Upload logs: `logs_instagram/` (if using helper script)

View your daily content:
- 📱 Instagram app
- 🌐 https://www.instagram.com/YOUR_USERNAME/
- 📋 Log files in `logs_instagram/`
