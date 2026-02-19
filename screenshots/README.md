# 🎬 TARS CLI Demo & Screenshots

## 📸 Screenshots Captured

All command outputs saved in `screenshots/` directory:

- `oncall.txt` - On-call dashboard
- `health.txt` - Cluster health check
- `top.txt` - Resource usage

## 🎥 Recording Instructions

### For Reddit Post - Use asciinema:

```bash
# 1. Start recording
asciinema rec tars-demo.cast

# 2. Run these commands (manually for best effect):
clear
echo "# TARS CLI Demo - AI-Powered Kubernetes Monitoring"
echo ""
sleep 2

echo "# 1. On-Call Dashboard"
tars oncall
sleep 3

echo ""
echo "# 2. Health Check"
tars health
sleep 3

echo ""
echo "# 3. Top Resource Consumers"
tars top
sleep 3

# 3. Stop recording (Ctrl+D)

# 4. Upload
asciinema upload tars-demo.cast
```

### Alternative - Quick GIF:

```bash
# Install terminalizer
npm install -g terminalizer

# Record
terminalizer record tars-demo -c terminalizer.yml

# Render
terminalizer render tars-demo
```

## 📤 Upload Locations

1. **Asciinema:** https://asciinema.org (best for terminal)
2. **Imgur:** https://imgur.com/upload (for GIFs)
3. **GitHub:** Add to repo as `demo.gif`

## 🎯 For Reddit Post

Add this to your post:

```markdown
## 🎥 Demo

[![asciicast](https://asciinema.org/a/YOUR_ID.svg)](https://asciinema.org/a/YOUR_ID)

Or watch the demo: [Link to your recording]
```

## 📱 Manual Screenshots (macOS)

If you prefer manual screenshots:

1. Open terminal (make it big: 120x30)
2. Run: `tars oncall`
3. Press: `Cmd + Shift + 4` (select area)
4. Repeat for other commands
5. Upload to Imgur

## ✅ Ready to Record?

Run this command to start:

```bash
asciinema rec tars-demo.cast
```

Then manually type and run:
- `tars oncall`
- `tars health`
- `tars top`

Press `Ctrl+D` when done, then upload!
