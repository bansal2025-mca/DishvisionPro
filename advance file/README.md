# 🍽️ Dishvision — AI Recipe Generator

Food ki photo upload karo aur turant recipe pao! Groq + Llama 4 Vision se powered.

---

## ✨ Features
- 📸 Food image se automatic dish detection
- 🧾 Complete recipe with ingredients & steps
- ▶️ YouTube video link (recipe dekhne ke liye)
- 📊 Nutrition information
- 💡 Pro chef tips
- 🌍 Any cuisine support

---

## 🚀 Setup (Step by Step)

### Step 1: Groq API Key Lo
1. https://console.groq.com pe jao
2. Free account banao
3. API Keys section mein jao → "Create API Key" karo
4. Key copy karo

### Step 2: Project Setup
```bash
# VS Code mein terminal kholo (Ctrl + `)

# Dependencies install karo
pip install -r requirements.txt

# .env file mein apni API key daalo
# .env file kholo aur likho:
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

### Step 3: App Run Karo
```bash
python app.py
```

### Step 4: Browser mein kholo
```
http://localhost:5000
```

---

## 📁 Project Structure
```
recipe-app/
├── app.py              ← Flask backend (main logic)
├── requirements.txt    ← Python dependencies
├── .env               ← API key (secret rakho!)
├── README.md          ← Ye file
└── templates/
    └── index.html     ← Frontend UI
```

---

## 🔑 API Key kahan se milegi?
- Groq: https://console.groq.com (FREE hai!)

---

## ❓ Common Errors

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` dobara chalaao |
| `Invalid API Key` | `.env` file mein sahi key daalo |
| `Port already in use` | `python app.py` ke baad `5001` try karo |

---

Made with ❤️ using Flask + Groq + Llama 4 Vision
