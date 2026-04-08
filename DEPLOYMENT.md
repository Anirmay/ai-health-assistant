# Deployment Guide - AI Health Assistant

## Quick Deploy to Railway

### Prerequisites
- Railway.app account (free tier available)
- Git installed

### Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd ai-health-assistant
   ```

2. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

3. **Deploy backend**
   ```bash
   cd backend
   railway init
   railway up
   ```

4. **Deploy frontend**
   ```bash
   cd ../frontend
   npm run build
   railway init
   railway up
   ```

## Deploy to Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps for Backend

1. **Create Heroku app**
   ```bash
   heroku create ai-health-assistant-backend
   ```

2. **Add buildpacks**
   ```bash
   heroku buildpacks:add heroku/python
   heroku buildpacks:add https://github.com/jontewks/heroku-buildpack-tesseract.git
   ```

3. **Set environment variables**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
   heroku config:set DATABASE_URL=postgresql://...  # If using PostgreSQL
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### Steps for Frontend

1. **Build frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Netlify / Vercel / GitHub Pages**
   - Netlify: `npm install -g netlify-cli && netlify deploy`
   - Vercel: `npm install -g vercel && vercel`

## Environment Variables

Create `.env` file in backend directory:

```
FLASK_ENV=production
DATABASE_URL=your-database-url
CORS_ORIGINS=https://yourdomain.com
OPENAI_API_KEY=your-api-key
```

## Database Migration

For production PostgreSQL:

```bash
flask db upgrade
```

## Testing Deployment

1. **Health check endpoint**
   ```bash
   curl https://your-api-url/api/health
   ```

2. **Frontend**
   - Visit your deployed frontend URL
   - Test symptom checker
   - Test medicine detector
   - Check history page

## Monitoring

- Check Heroku logs: `heroku logs --tail`
- Check Railway logs: `railway logs`
- Enable error reporting in production

## Production Checklist

- [ ] Set SECRET_KEY to a secure value
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set appropriate CORS_ORIGINS
- [ ] Set DEBUG=False
- [ ] Configure logging
- [ ] Set up SSL certificates
- [ ] Enable rate limiting
- [ ] Configure backups for database
