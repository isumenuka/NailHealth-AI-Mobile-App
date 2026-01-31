# 🧰 Tools & Resources Used

Comprehensive list of all tools, frameworks, models, and resources used in NailHealth AI project.

---

## 🤖 AI Models (Google HAI-DEF)

### MedSigLIP
- **Full Name**: Medical SigLIP (Sigmoid Loss for Language-Image Pre-training)
- **Source**: Google Health AI Developer Foundations
- **Model ID**: `google/medsiglip-448`
- **Purpose**: Medical image classification
- **Parameters**: ~400M
- **Input**: 448x448 RGB images
- **Training Data**: Dermatology images (PAD-UFES-20, SCIN datasets)
- **License**: Apache 2.0
- **Documentation**: [HAI-DEF MedSigLIP](https://developers.google.com/health-ai-developer-foundations)
- **Use Case**: Nail sign classification (white nails, clubbing, etc.)

### MedGemma 4B
- **Full Name**: Medical Gemma 4 Billion Parameters
- **Source**: Google Health AI Developer Foundations
- **Model ID**: `google/medgemma-4b-it` (instruction-tuned)
- **Purpose**: Medical text generation and reasoning
- **Parameters**: 4B
- **Architecture**: Transformer-based language model
- **Training Data**: Medical literature, clinical notes (de-identified)
- **License**: Apache 2.0
- **Documentation**: [HAI-DEF MedGemma](https://developers.google.com/health-ai-developer-foundations/medgemma)
- **Use Case**: Clinical explanation generation, disease prediction

---

## 📱 Mobile Development

### React Native
- **Version**: 0.73.0
- **Purpose**: Cross-platform mobile framework
- **Website**: [reactnative.dev](https://reactnative.dev)
- **Why**: Single codebase for iOS + Android
- **License**: MIT

### Expo
- **Version**: ~50.0.0
- **Purpose**: React Native development framework
- **Website**: [expo.dev](https://expo.dev)
- **Features Used**:
  - Expo Go (instant testing)
  - Expo Camera
  - Expo Image Picker
  - EAS Build (production builds)
- **Why**: Simplifies development, testing, and deployment
- **License**: MIT

### Expo Camera
- **Version**: ~14.0.0
- **Purpose**: Camera access for photo capture
- **Documentation**: [docs.expo.dev/camera](https://docs.expo.dev/versions/latest/sdk/camera/)

### Expo Image Picker
- **Version**: ~14.7.0
- **Purpose**: Photo selection from gallery
- **Documentation**: [docs.expo.dev/image-picker](https://docs.expo.dev/versions/latest/sdk/imagepicker/)

### Axios
- **Version**: 1.6.0
- **Purpose**: HTTP client for API requests
- **Website**: [axios-http.com](https://axios-http.com)
- **Why**: Promise-based, better error handling than fetch

---

## 🔧 Backend Development

### Python
- **Version**: 3.10
- **Purpose**: Backend programming language
- **Website**: [python.org](https://python.org)
- **Why**: Excellent ML/AI library ecosystem

### Flask
- **Version**: 3.0.0
- **Purpose**: Lightweight web framework
- **Website**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
- **Why**: Simple REST API development
- **License**: BSD-3-Clause

### Flask-CORS
- **Version**: 4.0.0
- **Purpose**: Handle Cross-Origin Resource Sharing
- **Why**: Enable mobile app to call API

### Gunicorn
- **Version**: 21.2.0
- **Purpose**: Production WSGI server
- **Website**: [gunicorn.org](https://gunicorn.org)
- **Configuration**: 1 worker, 2 threads, 120s timeout
- **Why**: Production-ready Python web server

---

## 🧠 Machine Learning

### PyTorch
- **Version**: 2.1.0
- **Purpose**: Deep learning framework
- **Website**: [pytorch.org](https://pytorch.org)
- **Why**: Required by Transformers library
- **License**: BSD-style

### Transformers (Hugging Face)
- **Version**: 4.36.0
- **Purpose**: Model loading and inference
- **Website**: [huggingface.co/transformers](https://huggingface.co/docs/transformers)
- **Why**: Easy access to pre-trained models
- **License**: Apache 2.0

### Pillow (PIL)
- **Version**: 10.1.0
- **Purpose**: Image processing
- **Website**: [pillow.readthedocs.io](https://pillow.readthedocs.io)
- **Why**: Image decoding, resizing, preprocessing

### NumPy
- **Version**: 1.24.3
- **Purpose**: Numerical operations
- **Website**: [numpy.org](https://numpy.org)
- **Why**: Array operations for image data

---

## ☁️ Cloud Infrastructure

### Google Cloud Run
- **Purpose**: Serverless container hosting
- **Website**: [cloud.google.com/run](https://cloud.google.com/run)
- **Features Used**:
  - Auto-scaling
  - HTTPS endpoints
  - Pay-per-use pricing
- **Why**: No server management, auto-scales, free tier
- **Region**: us-central1
- **Configuration**: 4GB memory, 2 vCPU

### Google Cloud Storage
- **Purpose**: Model file storage
- **Website**: [cloud.google.com/storage](https://cloud.google.com/storage)
- **Why**: Reliable, scalable object storage

### Google Cloud Build
- **Purpose**: Container image building
- **Website**: [cloud.google.com/build](https://cloud.google.com/build)
- **Why**: Automated Docker builds

### Google Container Registry
- **Purpose**: Docker image hosting
- **Why**: Integrates with Cloud Run

---

## 🐳 Containerization

### Docker
- **Purpose**: Application containerization
- **Website**: [docker.com](https://docker.com)
- **Base Image**: `python:3.10-slim`
- **Why**: Consistent environments, easy deployment

---

## 📊 Training Infrastructure

### Kaggle
- **Purpose**: Model training platform
- **Website**: [kaggle.com](https://kaggle.com)
- **GPU**: Tesla T4 (16GB)
- **Why**: Free GPU access, Jupyter notebooks
- **Notebooks**:
  - MedSigLIP fine-tuning
  - MedGemma 4B fine-tuning

### Jupyter Notebook
- **Purpose**: Interactive development environment
- **Why**: Ideal for ML experimentation

---

## 🛠️ Development Tools

### Node.js
- **Version**: 18+
- **Purpose**: JavaScript runtime for React Native
- **Website**: [nodejs.org](https://nodejs.org)

### npm
- **Purpose**: Package manager for JavaScript
- **Bundled with**: Node.js

### Git
- **Purpose**: Version control
- **Website**: [git-scm.com](https://git-scm.com)

### GitHub
- **Purpose**: Code hosting and collaboration
- **Repository**: [github.com/isumenuka/NailHealth-AI-Mobile-App](https://github.com/isumenuka/NailHealth-AI-Mobile-App)

### VS Code (Recommended)
- **Purpose**: Code editor
- **Website**: [code.visualstudio.com](https://code.visualstudio.com)
- **Extensions Used**:
  - React Native Tools
  - Python
  - Docker
  - GitLens

---

## 📚 Documentation Tools

### Markdown
- **Purpose**: Documentation format
- **Why**: Simple, readable, version-controllable

---

## 📖 Datasets

### Custom Nail Disease Dataset
- **Size**: 700+ images
- **Categories**: 7 nail conditions
- **Sources**:
  - DermIS.net (dermatology images)
  - Wikimedia Commons medical images
  - Clinical photography from textbooks
  - Custom collected data
- **Format**: JPEG, PNG
- **Resolution**: Various (resized to 448x448)

### Clinical Text Dataset
- **Size**: 250+ text pairs
- **Format**: JSON
- **Structure**: Instruction-response pairs
- **Sources**:
  - Clinical textbooks (UpToDate, Harrison's)
  - PubMed abstracts
  - Synthetic clinical vignettes

---

## 📜 Medical Resources

### Clinical References
- **UpToDate**: Clinical decision support
- **Harrison's Principles of Internal Medicine**: Medical textbook
- **PubMed**: Medical research database
- **Disease Ontology (DO)**: Disease classification
- **UMLS**: Medical terminology system

---

## 🔒 Security & Privacy

### HTTPS
- **Provider**: Google Cloud (automatic SSL)
- **Why**: Encrypt data in transit

### CORS
- **Implementation**: Flask-CORS
- **Why**: Secure cross-origin requests

---

## 💰 Cost Breakdown

| Service | Free Tier | Paid Tier | Current Usage |
|---------|-----------|-----------|---------------|
| Google Cloud Run | 2M requests/month | $0.000024/request | FREE |
| Cloud Storage | 5GB | $0.02/GB/month | FREE |
| Cloud Build | 120 min/day | $0.003/min | FREE |
| Kaggle GPU | Unlimited | N/A | FREE |
| Expo | Unlimited | N/A | FREE |
| GitHub | Unlimited public repos | $4/month private | FREE |

**Total Monthly Cost**: $0 (using free tiers)

---

## 📎 Quick Links

### Official Documentation
- [Google HAI-DEF](https://developers.google.com/health-ai-developer-foundations)
- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [Expo Documentation](https://docs.expo.dev)
- [Flask Documentation](https://flask.palletsprojects.com)
- [Google Cloud Run](https://cloud.google.com/run/docs)

### Community Resources
- [Hugging Face Forums](https://discuss.huggingface.co)
- [React Native Community](https://reactnative.dev/community/overview)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/react-native)

### Learning Resources
- [React Native Tutorial](https://reactnative.dev/docs/tutorial)
- [Expo Tutorial](https://docs.expo.dev/tutorial/introduction/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)

---

## 🎓 Skills Required

### For Mobile Development
- JavaScript / TypeScript
- React / React Native
- REST API integration
- Async programming
- Mobile UI/UX design

### For Backend Development
- Python programming
- Flask web framework
- RESTful API design
- Docker containerization
- Cloud deployment

### For ML/AI
- PyTorch basics
- Transformers library
- Model fine-tuning
- Transfer learning
- Image preprocessing

### For DevOps
- Git version control
- Docker basics
- Google Cloud Platform
- CI/CD concepts

---

## ❤️ Acknowledgments

- **Google Health AI Team**: For HAI-DEF models
- **Hugging Face**: For Transformers library
- **Expo Team**: For amazing mobile framework
- **Kaggle**: For free GPU resources
- **Medical Community**: For datasets and research
- **Open Source Community**: For all the tools

---

## 📞 Contact

**Project Maintainer**: K.G.I Enuka  
**GitHub**: [@isumenuka](https://github.com/isumenuka)  
**Repository**: [NailHealth-AI-Mobile-App](https://github.com/isumenuka/NailHealth-AI-Mobile-App)

---

**Last Updated**: January 31, 2026  
**Document Version**: 1.0
