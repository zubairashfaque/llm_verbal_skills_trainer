# Deployment Guide

Comprehensive deployment guide for the LLM Verbal Skills Trainer application.

## Table of Contents
- [Quick Start](#quick-start)
- [Docker Deployment](#docker-deployment)
- [Manual Deployment](#manual-deployment)
- [Environment Configuration](#environment-configuration)
- [Production Considerations](#production-considerations)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd llm_verbal_skills_trainer

# Copy environment file
cp .env.example .env

# Start services with Docker Compose
make docker-run

# Or using docker-compose directly
docker-compose up -d
```

The application will be available at `http://localhost:7860`

---

## Docker Deployment

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 8GB+ RAM (for LLM models)
- 20GB+ disk space

### Production Deployment

**1. Build the Docker image:**
```bash
make docker-build
# Or
docker build -t llm-verbal-skills-trainer:latest .
```

**2. Configure environment:**
```bash
cp .env.example .env
# Edit .env with your production settings
nano .env
```

**3. Start services:**
```bash
docker-compose up -d
```

**4. Verify deployment:**
```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f app

# Health check
curl http://localhost:7860/
```

### Development Deployment

For development with hot reload:

```bash
# Start in development mode
make docker-dev

# Or using docker-compose
docker-compose -f docker-compose.dev.yml up
```

### Docker Commands Reference

```bash
# Build
make docker-build              # Build Docker image
make docker-rebuild            # Rebuild without cache

# Run
make docker-run                # Start in production mode
make docker-dev                # Start in development mode
make docker-stop               # Stop containers

# Manage
make docker-logs               # View application logs
make docker-shell              # Open shell in container
make docker-clean              # Clean up all resources
```

### Multi-Stage Build Details

The Dockerfile uses a multi-stage build for optimization:

**Builder Stage:**
- Installs Poetry and dependencies
- Creates virtual environment
- ~800MB intermediate image

**Runtime Stage:**
- Copies only virtual environment
- Adds application code
- Final image: ~500MB

**Benefits:**
- Smaller production image
- Faster deployments
- Better security (no build tools in production)

---

## Manual Deployment

### Prerequisites
- Python 3.11
- FFmpeg
- 8GB+ RAM
- Ollama (for LLM inference)

### Installation Steps

**1. Install system dependencies:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv ffmpeg

# macOS
brew install python@3.11 ffmpeg
```

**2. Install Ollama:**
```bash
# Linux
curl https://ollama.ai/install.sh | sh

# macOS
brew install ollama

# Start Ollama
ollama serve
```

**3. Pull LLM models:**
```bash
ollama pull llama3.2:latest
```

**4. Setup application:**
```bash
# Clone repository
git clone <repository-url>
cd llm_verbal_skills_trainer

# Install Poetry
pip install poetry

# Install dependencies
poetry install

# Copy environment file
cp .env.example .env

# Edit configuration
nano .env
```

**5. Run application:**
```bash
# Using Make
make run

# Or directly
poetry run python main.py
```

---

## Environment Configuration

### Required Variables

```bash
# LLM Configuration
MODEL_NAME=llama3.2:latest
OLLAMA_SERVER_URL=http://127.0.0.1:11434/api/

# Application Settings
LOG_LEVEL=INFO
TRACKING_FILE=config/task_tracking.json
```

### Optional Variables

```bash
# Model Optimization
USE_4BIT=true
CACHE_SIZE=64
NUM_WORKERS=4
TEMPERATURE=0.7
NUM_CTX=2048
MAX_TOKENS=512

# Whisper Configuration
WHISPER_MODEL=base

# TTS Configuration
TTS_VOICE=en-us-amy
```

### Environment-Specific Configuration

**Development (.env.development):**
```bash
LOG_LEVEL=DEBUG
WHISPER_MODEL=tiny.en  # Faster for development
CACHE_SIZE=32
```

**Staging (.env.staging):**
```bash
LOG_LEVEL=INFO
WHISPER_MODEL=base
CACHE_SIZE=64
```

**Production (.env.production):**
```bash
LOG_LEVEL=WARNING
WHISPER_MODEL=medium.en
CACHE_SIZE=128
```

---

## Production Considerations

### Hardware Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Disk: 20GB SSD
- Network: 10 Mbps

**Recommended:**
- CPU: 8+ cores
- RAM: 16GB+
- Disk: 50GB+ NVMe SSD
- Network: 100 Mbps

### Performance Tuning

**1. Ollama Configuration:**
```bash
# Set number of GPU layers (if GPU available)
export OLLAMA_NUM_GPU=1

# Adjust context window
export OLLAMA_MAX_LOADED_MODELS=2
```

**2. Application Configuration:**
```bash
# Increase worker count for parallel processing
NUM_WORKERS=8

# Optimize cache size
CACHE_SIZE=256

# Adjust context length
NUM_CTX=4096
```

**3. System Optimization:**
```bash
# Increase file descriptors
ulimit -n 65536

# Optimize network settings
sysctl -w net.core.somaxconn=1024
```

### Security Checklist

- [ ] Use environment variables for secrets
- [ ] Run containers as non-root user
- [ ] Enable firewall rules
- [ ] Use HTTPS in production
- [ ] Implement rate limiting
- [ ] Regular security audits
- [ ] Keep dependencies updated
- [ ] Monitor logs for suspicious activity

### SSL/TLS Configuration

For production, use a reverse proxy like Nginx:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Monitoring & Maintenance

### Health Checks

**Application health:**
```bash
curl http://localhost:7860/
```

**Ollama health:**
```bash
curl http://localhost:11434/api/tags
```

**Docker health:**
```bash
docker-compose ps
docker stats llm-trainer-app
```

### Log Management

**View logs:**
```bash
# Application logs
tail -f logs/app.log

# Error logs
tail -f logs/errors.log

# Docker logs
docker-compose logs -f app
```

**Log rotation** is configured automatically:
- Max size: 10MB per file
- Backup count: 5 files
- Location: `logs/` directory

### Backup Strategy

**1. Configuration backup:**
```bash
# Backup environment file
cp .env .env.backup.$(date +%Y%m%d)

# Backup tracking data
cp config/task_tracking.json config/task_tracking.json.backup.$(date +%Y%m%d)
```

**2. Automated backups:**
```bash
# Add to crontab
0 2 * * * /path/to/backup-script.sh
```

### Updates

**Update application:**
```bash
# Pull latest code
git pull origin main

# Rebuild Docker image
make docker-rebuild

# Or update manually
poetry update
make run
```

**Update dependencies:**
```bash
# Using Dependabot (automated)
# Or manually
poetry update
poetry show --outdated
```

---

## Troubleshooting

### Common Issues

**1. Ollama connection failed:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve

# Check Docker network
docker network inspect llm-trainer-network
```

**2. Out of memory:**
```bash
# Check memory usage
docker stats

# Reduce model size
MODEL_NAME=llama3.2:1b  # Smaller model

# Adjust workers
NUM_WORKERS=2
```

**3. Audio transcription errors:**
```bash
# Check FFmpeg installation
ffmpeg -version

# Install FFmpeg in Docker
docker-compose exec app apt-get install ffmpeg
```

**4. Port already in use:**
```bash
# Find process using port 7860
lsof -i :7860

# Kill process
kill -9 <PID>

# Or use different port
sed -i 's/7860/7861/g' docker-compose.yml
```

### Debug Mode

Enable debug logging:
```bash
# Set environment variable
export LOG_LEVEL=DEBUG

# Or in .env
LOG_LEVEL=DEBUG

# Restart application
make docker-rebuild
```

### Performance Debugging

**Check response times:**
```bash
# Test LLM response time
time curl -X POST http://localhost:7860/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test"}'
```

**Monitor resource usage:**
```bash
# Real-time monitoring
docker stats llm-trainer-app

# Check disk usage
docker system df
```

---

## CI/CD Integration

### GitHub Actions

The repository includes automated CI/CD:

- **Linting:** Ruff code quality checks
- **Type Checking:** MyPy static analysis
- **Testing:** Pytest with coverage reports
- **Security:** Safety vulnerability scans
- **Build:** Docker image creation

### Deployment Pipeline

```yaml
# Production deployment
on:
  push:
    branches: [main]

jobs:
  - lint
  - test
  - build-docker
  - deploy-production
```

---

## Support & Contact

For issues or questions:
- GitHub Issues: [Repository Issues](https://github.com/zubairashfaque/llm_verbal_skills_trainer/issues)
- Documentation: See CONTRIBUTING.md
- Email: support@example.com

---

**Last Updated:** 2025-11-04
**Version:** 0.2.0
