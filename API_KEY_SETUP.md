# 🔐 API Key Setup Guide

## Generated Secure API Key

```
zWWRlxZJPHauLozPAz9tqMiR174qt0OWk4yelnx8RyU
```

**IMPORTANT: Keep this key secret! Do not commit to version control.**

---

## 📝 Setup Instructions

### 1. Update Mobile App

Edit `mobile-app/App.js` line 21:

```javascript
const API_KEY = 'zWWRlxZJPHauLozPAz9tqMiR174qt0OWk4yelnx8RyU';
```

### 2. Deploy API to Cloud Run

```bash
cd api-server

# Deploy with API key as environment variable
gcloud run deploy nailhealth-api \
  --source . \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --timeout 300 \
  --set-env-vars API_KEY=zWWRlxZJPHauLozPAz9tqMiR174qt0OWk4yelnx8RyU
```

### 3. Test API Authentication

**Without API Key (should fail):**
```bash
curl -X POST https://nailhealth-api-ig7c2nupna-uc.a.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "test"}'
# Expected: 401 Unauthorized
```

**With API Key (should work):**
```bash
curl -X POST https://nailhealth-api-ig7c2nupna-uc.a.run.app/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: zWWRlxZJPHauLozPAz9tqMiR174qt0OWk4yelnx8RyU" \
  -d '{"image": "test"}'
# Expected: Response (may fail on invalid image, but auth passes)
```

**Health Check (no auth required):**
```bash
curl https://nailhealth-api-ig7c2nupna-uc.a.run.app/health
# Expected: 200 OK
```

---

## 🔄 Rotating API Keys

To generate a new API key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Then update:
1. Mobile app configuration
2. Cloud Run environment variables
3. Any other API consumers

---

## 🔒 Security Best Practices

- ✅ **Never commit API keys to Git**
- ✅ Use environment variables for production
- ✅ Rotate keys periodically (every 3-6 months)
- ✅ Use different keys for dev/staging/production
- ✅ Monitor Cloud Run logs for unauthorized access attempts
- ❌ Don't share keys via email or chat
- ❌ Don't hardcode keys in public repositories

---

## 📱 Mobile App Security

For production apps, consider:
- Using React Native secure storage libraries
- Implementing OAuth/JWT instead of static keys
- Using environment-specific builds
- Enabling certificate pinning

---

## 🚨 If Key is Compromised

1. Generate new key immediately
2. Update Cloud Run deployment
3. Update mobile app and redeploy
4. Monitor logs for suspicious activity
5. Consider implementing rate limiting
