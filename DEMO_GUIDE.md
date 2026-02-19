# Creating Demo Content for Reddit

## 🎥 Option 1: Terminal Recording (Recommended)

### Using asciinema (Best for terminal demos):

```bash
# Install
brew install asciinema

# Record demo
asciinema rec tars-demo.cast

# Run commands manually or use demo script:
./demo.sh

# Stop recording: Ctrl+D

# Convert to GIF
npm install -g asciicast2gif
asciicast2gif tars-demo.cast tars-demo.gif
```

### Using terminalizer:

```bash
# Install
npm install -g terminalizer

# Record
terminalizer record tars-demo

# Render to GIF
terminalizer render tars-demo
```

## 📸 Option 2: Screenshots

### Take screenshots of:

1. **tars oncall** - On-call dashboard
2. **tars health** - Health check with status
3. **tars triage** - Issue detection
4. **tars watch** - Live monitoring
5. **tars diagnose <pod>** - Pod diagnostics

### Tools:
- macOS: Cmd+Shift+4 (select area)
- Use iTerm2 for better colors
- Set terminal to 120x30 for good size

## 🎬 Option 3: Quick Video (30-60 seconds)

### Using QuickTime:
1. Open QuickTime Player
2. File > New Screen Recording
3. Select terminal area
4. Run: `./demo.sh`
5. Export as MP4

### Upload to:
- **Imgur** (for GIFs/images)
- **Streamable** (for videos)
- **YouTube** (unlisted, for longer demos)

## 📝 What to Show:

### 30-Second Demo Flow:
```
1. tars oncall       (5s) - "Here's your on-call dashboard"
2. tars health       (5s) - "Quick health check"
3. tars triage       (5s) - "Detect issues"
4. tars diagnose pod (5s) - "Deep dive with AI"
5. tars top          (5s) - "Resource usage"
6. Show GitHub link  (5s)
```

## 🎨 Make it Look Good:

### Terminal Setup:
```bash
# Use a nice theme
# iTerm2 > Preferences > Profiles > Colors
# Recommended: "Solarized Dark" or "Dracula"

# Set font size for recording
# iTerm2 > Preferences > Profiles > Text
# Font: Monaco 14pt or Menlo 14pt

# Set window size
# iTerm2 > Preferences > Profiles > Window
# Columns: 120, Rows: 30
```

## 📤 Upload & Share:

1. **Upload GIF to Imgur:**
   ```bash
   # Upload at: https://imgur.com/upload
   # Get direct link
   ```

2. **Add to Reddit post:**
   ```markdown
   ![TARS Demo](https://i.imgur.com/YOUR_IMAGE.gif)
   ```

3. **Add to README:**
   ```markdown
   ## Demo
   ![Demo](https://i.imgur.com/YOUR_IMAGE.gif)
   ```

## ⚡ Quick Start (Fastest):

```bash
# 1. Record with asciinema
brew install asciinema
asciinema rec tars-demo.cast
./demo.sh
# Press Ctrl+D when done

# 2. Upload to asciinema.org
asciinema upload tars-demo.cast
# Get shareable link

# 3. Add to Reddit post
```

## 🎯 Pro Tips:

- ✅ Clear terminal before recording: `clear`
- ✅ Use a clean cluster (not too many pods)
- ✅ Show colorful output (TARS has great colors!)
- ✅ Keep it under 60 seconds
- ✅ Add captions/text overlay if making video
- ✅ Test recording first

Ready to record? Run:
```bash
./demo.sh
```
