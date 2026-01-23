---
title: Instagram Reel Upload Automation
description: Automate Instagram Reel uploads using Python and instagrapi
contentType: tutorial
priority: medium
---

# Instagram Reel Upload Automation

This guide shows you how to automate Instagram Reel uploads using Python and the instagrapi library. This is useful for content creators who want to schedule and automate their social media posts.

## Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher installed
- An Instagram account
- pip package manager

## Installation

Install the required Python package:

```bash
pip install instagrapi
```

## Usage

### Basic Usage

The automation script is located at `_doctools/upload_instagram_reel.py`. You can run it with:

```bash
python _doctools/upload_instagram_reel.py --username YOUR_USERNAME --video path/to/video.mp4
```

### Using Environment Variables (Recommended)

For better security, use environment variables instead of passing credentials directly:

```bash
# Set environment variables
export IG_USERNAME="your_instagram_username"
export IG_PASSWORD="your_instagram_password"
export IG_CAPTION="¡Contenido creado con mi IA! 🚀 #IA #Automation #ContentCreation"

# Run the script
python _doctools/upload_instagram_reel.py --video path/to/video.mp4
```

### Command Line Options

- `--username` or `-u`: Instagram username (or use `IG_USERNAME` environment variable)
- `--password` or `-p`: Instagram password (or use `IG_PASSWORD` environment variable)
- `--video` or `-v`: Path to video file (.mp4) - **Required**
- `--thumbnail` or `-t`: Path to thumbnail image (.jpg/.png) - Optional
- `--caption` or `-c`: Caption text for the Reel (or use `IG_CAPTION` environment variable)
- `--session-file` or `-s`: Path to session file (default: `insta_session.json`)

### Complete Example

```bash
python _doctools/upload_instagram_reel.py \
  --username my_account \
  --video videos/my_reel.mp4 \
  --thumbnail images/cover.jpg \
  --caption "Check out my new content! 🎥 #NewReel #ContentCreator"
```

## Where Credentials Are Stored

### Session File

After the first successful login, the script creates a session file (default: `insta_session.json`) in the current directory. This file contains:

- Authentication tokens
- Cookie data
- Device information

**Important Security Notes:**

- The session file contains sensitive authentication data
- Keep it secure and never commit it to version control
- Add `insta_session.json` to your `.gitignore` file
- The session file allows the script to avoid re-login on subsequent runs

### Environment Variables

Credentials can be stored as environment variables:

- `IG_USERNAME`: Your Instagram username
- `IG_PASSWORD`: Your Instagram password
- `IG_CAPTION`: Default caption for your posts
- `IG_SESSION_FILE`: Custom path for the session file

To persist environment variables across sessions, add them to your shell profile:

**For Bash (.bashrc or .bash_profile):**
```bash
export IG_USERNAME="your_username"
export IG_PASSWORD="your_password"
```

**For Zsh (.zshrc):**
```zsh
export IG_USERNAME="your_username"
export IG_PASSWORD="your_password"
```

## Viewing Your Daily Content

### Check Uploaded Content Status

After uploading, the script logs the Reel ID. You can view your content:

1. **Via Instagram App**: Open Instagram and go to your profile to see the uploaded Reel
2. **Via Web Browser**: Visit `https://www.instagram.com/YOUR_USERNAME/` to view your profile
3. **Check Upload Log**: The script logs each successful upload with a timestamp

### Log File Example

The script outputs logs in the following format:

```
2026-01-23 10:30:15 INFO: Sesión cargada desde insta_session.json
2026-01-23 10:30:16 INFO: Sesión válida para my_account
2026-01-23 10:30:16 INFO: Subiendo Reel... (esto puede tardar dependiendo del tamaño)
2026-01-23 10:32:45 INFO: ¡Éxito! Reel publicado. ID: 1234567890123456789
```

You can redirect logs to a file for daily review:

```bash
python _doctools/upload_instagram_reel.py --video my_video.mp4 2>&1 | tee upload_log_$(date +%Y%m%d).txt
```

### Create a Daily Content Tracking Script

Create a simple bash script to track your daily uploads:

```bash
#!/bin/bash
# daily_upload.sh

DATE=$(date +%Y-%m-%d)
LOG_DIR="./upload_logs"
mkdir -p $LOG_DIR

python _doctools/upload_instagram_reel.py \
  --video "$1" \
  --caption "Daily content for $DATE 🚀 #DailyContent" \
  2>&1 | tee "$LOG_DIR/upload_$DATE.log"

echo "Upload completed. Log saved to $LOG_DIR/upload_$DATE.log"
```

Make it executable and use it:

```bash
chmod +x daily_upload.sh
./daily_upload.sh path/to/video.mp4
```

## Two-Factor Authentication (2FA)

If your Instagram account has 2FA enabled:

1. Run the script normally
2. When prompted, enter the 2FA code from your authenticator app or SMS
3. The session will be saved for future use

```
Introduce el código 2FA recibido: 123456
```

## Troubleshooting

### Common Issues

**"Bad Password" Error:**
- Verify your username and password are correct
- Check if you need to approve the login from the Instagram app

**"Challenge Required" Error:**
- Instagram may require additional verification
- Try logging in via the Instagram app first
- Complete any pending security checks

**Session Expired:**
- Delete the session file and run the script again
- The script will create a new session

### Security Best Practices

1. **Never hardcode credentials** in your scripts
2. **Use environment variables** or secure credential managers
3. **Protect your session file** with appropriate file permissions:
   ```bash
   chmod 600 insta_session.json
   ```
4. **Rotate your passwords** regularly
5. **Add session files to `.gitignore`**:
   ```
   insta_session.json
   *.session.json
   ```

## Integration with n8n Workflows

You can integrate this script with n8n workflows by:

1. Using the **Execute Command** node to run the Python script
2. Passing video paths and captions from previous workflow steps
3. Storing credentials in n8n's credential system
4. Scheduling uploads using n8n's Cron node

Example n8n workflow structure:
```
Cron Node → Generate Video → Execute Command (upload_instagram_reel.py) → Notification
```

## Further Reading

- [Instagram API Best Practices](https://developers.facebook.com/docs/instagram-api/)
- [n8n Execute Command Documentation](/integrations/builtin/core-nodes/n8n-nodes-base.executecommand/)
- [n8n Credential Storage](/credentials/)
- [n8n Workflow Automation](/workflows/)

## Related Resources

- [Facebook Trigger Node](/integrations/builtin/trigger-nodes/n8n-nodes-base.facebooktrigger/)
- [Instagram Object Documentation](/integrations/builtin/trigger-nodes/n8n-nodes-base.facebooktrigger/instagram.md)
