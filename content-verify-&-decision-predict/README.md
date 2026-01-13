# Venture Content Guard 🛡️

**Welcome!** This project is an intelligent "Content Guard" for business platforms. It uses Artificial Intelligence (AI) to automatically check user posts before they go live.

### What does it do?
Imagine you have a professional social network for startups. You want to make sure:
1.  **It's Professional:** No rants, no politics, no spam.
2.  **It's Relevant:** A "Healthcare" company should post about health, not real estate.

This tool does exactly that. It approves good content and rejects the rest with a clear reason.

---

## 🚀 Quick Start Guide

Follow these steps to get the project running on your computer.

### Prerequisites
You need **Python** installed on your computer. If you don't have it, download it from [python.org](https://www.python.org/).

### Step 1: Install Dependencies
Open your terminal (Command Prompt or PowerShell) in this folder and run:
```bash
pip install -r requirements.txt
```
*This installs the necessary tools (FastAPI, Google Gemini AI, etc.)*

### Step 2: Set up your API Key
This project uses Google's AI. You need a free key to use it.
1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and click "Get API Key".
2.  Open the file named `.env` in this folder.
3.  Paste your key like this:
    ```env
    GEMINI_API_KEY=AIzaSyB... (your actual key)
    ```

### Step 3: Run the Server
In your terminal, run:
```bash
uvicorn app.main:app --reload
```
You should see a message saying `Uvicorn running on http://127.0.0.1:8000`.

---

## 🧪 How to Test It

You don't need to write code to test it. We have built-in easy ways!

### Option A: Use the Website (Easiest)
1.  While the server is running, open this link in your browser:
    👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
2.  Click on the green `POST /analyze` bar.
3.  Click **Try it out** button (top right).
4.  Copy one of the "Test Cases" below into the "Request body" box.
5.  Click the big blue **Execute** button and check the "Server response" below.

### Option B: Run the Test Script
Open a new terminal window and run:
```bash
python test_api.py
```
This will automatically run a few checks and show you the results.

---

## 📚 Copy-Paste Test Cases

Here are examples you can copy into the website (`/docs`) to see how the AI reacts.

### ✅ Examples that will be APPROVED
**1. Healthcare Domain**
```json
{
  "User_Text": "Our new telemedicine app allows patients to consult doctors remotely via secure video calls.",
  "Registered_Domain": "Healthcare"
}
```

**2. FinTech Domain**
```json
{
  "User_Text": "We just launched a new credit card with 0% fees for international transactions.",
  "Registered_Domain": "FinTech"
}
```

**3. EduTech Domain**
```json
{
  "User_Text": "Enroll in our new AI certification course to boost your career in machine learning.",
  "Registered_Domain": "EduTech"
}
```

**4. E-Commerce Domain**
```json
{
  "User_Text": "Our biggest summer sale starts tomorrow! Get up to 50% off on electronics.",
  "Registered_Domain": "E-Commerce"
}
```

**5. Real Estate Domain**
```json
{
  "User_Text": "Luxurious 3-bedroom apartment available for rent in the city center. Book a viewing today.",
  "Registered_Domain": "Real Estate"
}
```

**6. Marketing Domain**
```json
{
  "User_Text": "Learn the top 5 SEO strategies to drive organic traffic to your website in 2024.",
  "Registered_Domain": "Marketing"
}
```

**7. Logistics Domain**
```json
{
  "User_Text": "We have optimized our supply chain to ensure 24-hour delivery across the country.",
  "Registered_Domain": "Logistics"
}
```

**8. Sustainability Domain**
```json
{
  "User_Text": "Join our initiative to plant 10,000 trees this year and reduce our carbon footprint.",
  "Registered_Domain": "Sustainability"
}
```

**9. Cybersecurity Domain**
```json
{
  "User_Text": "Our new firewall solution protects your business from advanced ransomware attacks.",
  "Registered_Domain": "Cybersecurity"
}
```

**10. AI/Tech Domain**
```json
{
  "User_Text": "Introducing our latest language model that understands context better than ever before.",
  "Registered_Domain": "Technology"
}
```

### ❌ Examples that will be REJECTED (Off-Topic/Unprofessional)
**1. Personal Rant**
```json
{
  "User_Text": "I hate traffic! It took me 2 hours to get to work today. So annoyed.",
  "Registered_Domain": "Marketing"
}
```

**2. Political Talk**
```json
{
  "User_Text": "Everyone must vote for this candidate! The other side is destroying the country.",
  "Registered_Domain": "EduTech"
}
```

**3. Spam/Clickbait**
```json
{
  "User_Text": "You won a free iPhone! Click this link now to claim your prize instantly!",
  "Registered_Domain": "FinTech"
}
```

**4. Offensive Content**
```json
{
  "User_Text": "This other company is absolute trash and their CEO is an idiot.",
  "Registered_Domain": "Technology"
}
```

**5. Personal Blog/Diary**
```json
{
  "User_Text": "Had a great hamburger for lunch today. Feeling sleepy now.",
  "Registered_Domain": "Healthcare"
}
```

**6. Irrelevant Joke/Meme**
```json
{
  "User_Text": "Why did the chicken cross the road? To get to the other side! LOL.",
  "Registered_Domain": "Logistics"
}
```

**7. Soliciting/Follow-for-Follow**
```json
{
  "User_Text": "Please follow my personal Instagram account! I need 100 more followers.",
  "Registered_Domain": "E-Commerce"
}
```

**8. Conspiracy Theory**
```json
{
  "User_Text": "The moon landing was faked! Wake up sheeple!",
  "Registered_Domain": "Science"
}
```

**9. Sports Fan Commentary**
```json
{
  "User_Text": "Did you see that game last night? The referee was totally biased.",
  "Registered_Domain": "Real Estate"
}
```

**10. Religious Preaching**
```json
{
  "User_Text": "You must repent for your sins immediately to be saved.",
  "Registered_Domain": "Cybersecurity"
}
```

### ⚠️ Examples that will be REJECTED (Wrong Domain)
**1. Mismatch (Healthcare posting about Real Estate)**
```json
{
  "User_Text": "Check out this amazing 3-bedroom apartment for sale in downtown!",
  "Registered_Domain": "Healthcare"
}
```

**2. Mismatch (FinTech posting Medical Advice)**
```json
{
  "User_Text": "If you have a headache, take two aspirins and get some rest.",
  "Registered_Domain": "FinTech"
}
```

**3. Mismatch (EduTech posting Crypto Tips)**
```json
{
  "User_Text": "Buy Dogecoin now! It's going to the moon! 🚀",
  "Registered_Domain": "EduTech"
}
```

**4. Mismatch (Real Estate posting Coding Tutorials)**
```json
{
  "User_Text": "Here is how you center a div in CSS using Flexbox.",
  "Registered_Domain": "Real Estate"
}
```

**5. Mismatch (Marketing posting Prescription Drugs)**
```json
{
  "User_Text": "Buy cheap antibiotics online without a prescription.",
  "Registered_Domain": "Marketing"
}
```

**6. Mismatch (E-Commerce posting Political Opinions)**
```json
{
  "User_Text": "We believe the government's new tax policy is a disaster.",
  "Registered_Domain": "E-Commerce"
}
```

**7. Mismatch (Cybersecurity posting Fashion Trends)**
```json
{
  "User_Text": "Floral prints are totally in for this spring season!",
  "Registered_Domain": "Cybersecurity"
}
```

**8. Mismatch (Logistics posting Movie Reviews)**
```json
{
  "User_Text": "The new superhero movie was disappointing. The plot made no sense.",
  "Registered_Domain": "Logistics"
}
```

**9. Mismatch (Legal Services posting DIY Plumbing)**
```json
{
  "User_Text": "Fix your leaky sink with this simple wrench trick!",
  "Registered_Domain": "Legal Services"
}
```

**10. Mismatch (Sustainability posting Fast Food Promos)**
```json
{
  "User_Text": "Get a double cheeseburger for only $1 at the new burger joint!",
  "Registered_Domain": "Sustainability"
}
```

---

## ❓ Troubleshooting

-   **Error: "Gemini API Key is missing"**:
    -   Make sure you edited the `.env` file and saved it.
-   **Error: "Quota exceeded"**:
    -   You might be making too many requests too fast. Wait a minute and try again.