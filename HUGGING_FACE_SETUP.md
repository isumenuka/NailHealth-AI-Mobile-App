# 🔐 Hugging Face Authentication Setup Guide

## Problem

The MedSigLIP model is a **gated model** on Hugging Face Hub. This means you need authentication to access it.

### Error Message
```
Error loading model: You are trying to access a gated repo.
Make sure to have access to it at https://huggingface.co/google/medsigLIP-448.
401 Client Error. Cannot access gated repo.
```

---

## ✅ Solution

### Step 1: Create a Hugging Face Account
1. Go to [huggingface.co](https://huggingface.co)
2. Click **Sign Up** and create an account
3. Verify your email

### Step 2: Request Access to MedSigLIP
1. Visit the model page: [google/MedSigLIP-2B](https://huggingface.co/google/MedSigLIP-2B)
2. Click **"Access repository"** button
3. Accept the terms and conditions
4. Wait for approval (usually instant)

### Step 3: Generate Access Token
1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **"New token"**
3. Select **"Read"** permission
4. Give it a name like "MedSigLIP-Colab"
5. Click **"Create token"**
6. Copy the token (keep it secret!)

### Step 4: Run the Authentication Cell

The first cell in the notebook (`🔐 Hugging Face Login`) will prompt you for your token:

```python
from huggingface_hub import login

# This will prompt for your token
login(token=None, add_to_git_credential=True)
```

When prompted, paste your token and press Enter.

---

## 🔑 Alternative: Use Environment Variable

You can also set the token as an environment variable:

```bash
export HF_TOKEN="your_token_here"
```

Or in the notebook:

```python
import os
os.environ["HF_TOKEN"] = "your_token_here"

from huggingface_hub import login
login()
```

---

## 🚀 Google Colab Setup

### Option A: Interactive Login (Recommended)

Run the first cell in the notebook. It will:
1. Display instructions
2. Prompt for your token
3. Save it for the session

### Option B: Manual Token Setup

1. Create a secret in Colab:
   - Click **🔑 Secrets** in the left sidebar
   - Add a new secret: `HF_TOKEN` = your_token
   - Mark it as "Notebook access"

2. Access it in code:
   ```python
   from google.colab import userdata
   hf_token = userdata.get('HF_TOKEN')
   
   from huggingface_hub import login
   login(token=hf_token)
   ```

---

## ⚠️ Security Best Practices

✅ **DO:**
- Use **Read-only** tokens
- Regenerate tokens after each project
- Store tokens in environment variables or secrets
- Set token expiration dates

❌ **DON'T:**
- Share tokens in GitHub commits
- Use the same token for multiple projects
- Use full-access tokens unnecessarily
- Leave tokens in notebook code

---

## 🐛 Troubleshooting

### Token Not Working
- Verify you have access to the model page
- Check token hasn't expired
- Regenerate a new token

### Still Getting Access Error
- Make sure you clicked "Access repository" on the model page
- Wait a few minutes after requesting access
- Try logging out and logging in again

### "gated_repo_url" Error
- This means the token is not being passed correctly
- Ensure you ran the login cell before loading the model
- Check there are no typos in your token

---

## 📖 More Information

- [Hugging Face Hub Documentation](https://huggingface.co/docs/hub/security-tokens)
- [MedSigLIP Model Card](https://huggingface.co/google/MedSigLIP-2B)
- [Gated Models Guide](https://huggingface.co/docs/hub/models-gated)

---

## 🎯 Next Steps

Once authenticated:
1. ✅ Run the second cell: "Setup & Installation"
2. ✅ Check GPU availability
3. ✅ Load your nail disease dataset
4. ✅ Start fine-tuning!

---

**Happy training! 🚀**
