# Instagram Reel Upload Automation - Summary

## Overview

This implementation adds a complete Instagram Reel upload automation solution to the n8n documentation repository, addressing the user's request for social media content automation with clear documentation on credential storage and daily content viewing.

## What Was Added

### 1. Core Python Script
**File**: `_doctools/upload_instagram_reel.py`

A production-ready Python script that:
- Uploads Reels to Instagram using the `instagrapi` library
- Manages authentication with session persistence
- Supports 2FA (Two-Factor Authentication)
- Provides comprehensive logging
- Accepts command-line arguments for video, thumbnail, and caption
- Uses environment variables for secure credential management

**Key Features**:
- Session file management to avoid frequent re-logins
- Automatic session validation
- Robust error handling
- Support for optional thumbnail images
- Configurable caption text

### 2. Documentation Files

#### Main Documentation
**File**: `docs/code/cookbook/instagram-automation.md`

Comprehensive English documentation that covers:
- Prerequisites and installation instructions
- Usage examples (basic and advanced)
- Complete explanation of where credentials are stored
- Methods for viewing daily content
- Security best practices
- Integration with n8n workflows
- Troubleshooting common issues

#### Spanish README
**File**: `_doctools/README_INSTAGRAM.md`

Spanish-language quick reference that explains:
- Script location and purpose
- Where sessions and credentials are stored
- How to view daily content and uploaded Reels
- Log tracking system
- Daily upload workflow
- Common troubleshooting

### 3. Helper Scripts

#### Daily Upload Script
**File**: `daily_instagram_upload.sh`

A bash wrapper script that:
- Simplifies daily uploads
- Creates organized logs with timestamps
- Provides user-friendly output
- Validates input parameters
- Extracts and displays Reel IDs from logs
- Supports optional thumbnails and custom captions

### 4. Configuration Files

#### Python Dependencies
**File**: `_doctools/requirements_instagram.txt`

Separate requirements file for Instagram automation dependencies:
```
instagrapi>=2.0.0
```

#### Updated .gitignore
Added entries to prevent committing sensitive files:
```
insta_session.json
*.session.json
logs_instagram/
upload_logs/
```

### 5. n8n Workflow Example
**File**: `docs/_workflows/instagram-automation-example.json`

A complete n8n workflow demonstrating:
- Scheduled daily uploads using Cron
- Dynamic video path and caption generation
- Instagram upload execution
- Success/failure checking
- Notification system

The workflow includes 6 nodes:
1. Schedule Daily Upload (Cron Trigger)
2. Prepare Upload Data (Code Node)
3. Upload to Instagram (Execute Command)
4. Check Upload Success (IF Node)
5. Success Notification (Slack)
6. Error Notification (Slack)

### 6. Documentation Navigation
**File**: `nav.yml`

Added the Instagram automation guide to the documentation navigation under:
`Code → Cookbook → Instagram Reel Upload Automation`

## Answering the User's Specific Questions

### "¿Dónde está almacenado?" (Where is it stored?)

The documentation clearly explains credential storage:

1. **Session File** (`insta_session.json`):
   - Location: Current directory (configurable via `--session-file` or `IG_SESSION_FILE` env var)
   - Contains: Authentication tokens, cookies, device info
   - Purpose: Avoids re-login on subsequent runs
   - Security: Must be protected (chmod 600) and never committed to git

2. **Environment Variables** (Recommended):
   - `IG_USERNAME`: Instagram username
   - `IG_PASSWORD`: Instagram password
   - `IG_CAPTION`: Default caption text
   - `IG_SESSION_FILE`: Custom session file path
   - Storage: Shell profile (~/.bashrc, ~/.zshrc) for persistence

3. **Upload Logs**:
   - Location: `logs_instagram/` directory
   - Format: `upload_YYYYMMDD_HHMMSS.log`
   - Contains: Timestamps, status, Reel IDs, errors

### "¿Cómo verlo diario?" (How to see it daily?)

The documentation provides multiple methods:

1. **View on Instagram**:
   - Mobile app: Profile → Reels tab
   - Web browser: `https://www.instagram.com/YOUR_USERNAME/`

2. **Check Upload Logs**:
   ```bash
   # View latest log
   cat logs_instagram/$(ls -t logs_instagram/ | head -1)
   
   # Search successful uploads
   grep "¡Éxito!" logs_instagram/*.log
   
   # List all uploads
   ls -lt logs_instagram/
   ```

3. **Automated Daily Tracking**:
   - Use `daily_instagram_upload.sh` for automatic log creation
   - Each run creates a timestamped log file
   - Script extracts and displays Reel ID for easy reference

4. **Integration with n8n**:
   - Set up workflow with Cron trigger for daily automation
   - Receive notifications on success/failure
   - View execution history in n8n dashboard

## Security Features

1. **Credential Protection**:
   - Environment variables recommended over hardcoded values
   - Password input via getpass() if not provided
   - Session files excluded from version control

2. **File Permissions**:
   - Documentation includes chmod 600 instructions
   - .gitignore prevents accidental commits

3. **Session Management**:
   - Automatic session validation before use
   - Graceful degradation on session expiry
   - Secure token storage

## Usage Examples

### Basic Usage
```bash
python _doctools/upload_instagram_reel.py \
  --username my_account \
  --video path/to/video.mp4
```

### With Environment Variables
```bash
export IG_USERNAME="my_account"
export IG_PASSWORD="my_password"
python _doctools/upload_instagram_reel.py --video video.mp4
```

### Daily Upload Script
```bash
./daily_instagram_upload.sh videos/daily_content.mp4 thumbnail.jpg "Today's content! 🎥"
```

### View Daily Logs
```bash
# Latest upload status
tail logs_instagram/*.log | grep -E "Éxito|Error"

# All Reel IDs
grep -oP 'ID: \K[0-9]+' logs_instagram/*.log
```

## Testing Performed

1. ✅ Python syntax validation
2. ✅ Function structure verification
3. ✅ JSON workflow validation
4. ✅ Markdown documentation structure
5. ✅ Navigation menu integration
6. ✅ Script executability
7. ✅ Git ignore configuration

## Files Added

```
_doctools/
├── upload_instagram_reel.py      (Python script - 5,046 bytes)
├── README_INSTAGRAM.md            (Spanish guide - 5,471 bytes)
└── requirements_instagram.txt     (Dependencies - 113 bytes)

docs/
├── code/cookbook/
│   └── instagram-automation.md    (Documentation - 6,707 bytes)
└── _workflows/
    └── instagram-automation-example.json (n8n workflow - 3,298 bytes)

daily_instagram_upload.sh          (Helper script - 2,595 bytes)
.gitignore                         (Updated)
nav.yml                            (Updated)
```

## Total Lines of Code

- Python: ~150 lines
- Bash: ~85 lines
- Documentation: ~300 lines
- JSON: ~90 lines
- **Total**: ~625 lines

## Next Steps for User

1. **Install Dependencies**:
   ```bash
   pip install -r _doctools/requirements_instagram.txt
   ```

2. **Set Up Credentials**:
   ```bash
   export IG_USERNAME="your_username"
   export IG_PASSWORD="your_password"
   ```

3. **Test Upload**:
   ```bash
   python _doctools/upload_instagram_reel.py --video test_video.mp4
   ```

4. **Check Session**:
   ```bash
   ls -la insta_session.json  # Session file created
   ```

5. **View on Instagram**:
   Visit your Instagram profile to see the uploaded Reel

6. **Review Logs**:
   ```bash
   cat logs_instagram/*.log  # If using daily_instagram_upload.sh
   ```

## Integration with n8n

The workflow example can be imported into n8n to:
- Schedule automatic uploads
- Integrate with content generation workflows
- Receive notifications
- Track upload history
- Chain with other social media automation

## Documentation Quality

The documentation follows n8n standards:
- Clear structure with table of contents
- Step-by-step instructions
- Multiple usage examples
- Security best practices
- Troubleshooting section
- Related resources links
- Integration examples

## Conclusion

This implementation provides a complete, production-ready solution for Instagram Reel automation with:
- ✅ Automated upload capability
- ✅ Clear documentation of storage locations
- ✅ Multiple methods for daily content viewing
- ✅ Secure credential management
- ✅ Comprehensive logging
- ✅ n8n workflow integration
- ✅ Both English and Spanish documentation

The user can now:
1. **Automate uploads**: Use the script or n8n workflow
2. **Know where data is stored**: Session files, environment variables, and logs
3. **View content daily**: Through Instagram, logs, or automated tracking
4. **Maintain security**: With proper credential and session management
