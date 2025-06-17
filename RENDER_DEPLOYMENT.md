# TechReform Django Deployment on Render

This document provides step-by-step instructions for deploying the TechReform Django application on Render.

## Prerequisites

- Git repository with your Django project
- GitHub, GitLab, or Bitbucket account
- Render account (<https://render.com>)

## Project Structure

Your project should now have these new files:

- `build.sh` - Build script for Render
- `render.yaml` - Infrastructure as Code configuration
- Updated `requirements.txt` with deployment dependencies
- Updated `TechReform/settings.py` with production configurations

## Deployment Methods

### Method 1: Using Infrastructure as Code (Recommended)

1. **Push your code to your repository:**

   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Deploy using Render Dashboard:**
   - Go to the [Render Dashboard](https://dashboard.render.com)
   - Navigate to the [Blueprints page](https://dashboard.render.com/blueprints)
   - Click "New Blueprint Instance"
   - Select your repository and click "Connect"
   - Give your blueprint project a name and click "Apply"

3. **Your application will be deployed with:**
   - A PostgreSQL database named `techreformdb`
   - A web service named `techreform`
   - Automatic environment variables configuration

### Method 2: Manual Deployment

1. **Create a PostgreSQL database:**
   - Go to your Render Dashboard
   - Click "New" → "PostgreSQL"
   - Choose the free plan
   - Name it `techreformdb`
   - Copy the internal database URL

2. **Create a web service:**
   - Click "New" → "Web Service"
   - Connect your repository
   - Select "Python 3" as the language
   - Configure the following settings:
     - Build Command: `./build.sh`
     - Start Command: `python -m gunicorn TechReform.asgi:application -k uvicorn.workers.UvicornWorker`

3. **Add environment variables:**
   - `DATABASE_URL`: Your PostgreSQL internal database URL
   - `SECRET_KEY`: Click "Generate" for a secure random value
   - `WEB_CONCURRENCY`: `4`

## Post-Deployment Steps

1. **Create a Django admin account:**
   - Go to your service dashboard on Render
   - Click "Shell" tab
   - Run: `python manage.py createsuperuser`

2. **Access your application:**
   - Your app will be available at `https://your-service-name.onrender.com`
   - Admin panel: `https://your-service-name.onrender.com/admin/`

## Important Notes

- **Free Tier Limitations:** Render's free tier may have limitations on compute time and will spin down after inactivity
- **Database Backups:** Consider upgrading to paid tiers for automatic backups
- **Custom Domain:** You can add a custom domain in the service settings
- **Static Files:** Handled automatically by WhiteNoise
- **Media Files:** For user uploads, consider using cloud storage like AWS S3

## Environment Variables

The following environment variables are automatically configured:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Django secret key
- `WEB_CONCURRENCY`: Number of worker processes
- `RENDER_EXTERNAL_HOSTNAME`: Your service hostname (auto-configured)
- `RENDER`: Indicates running on Render platform (auto-configured)

## Troubleshooting

1. **Build Fails:**
   - Check the build logs in Render dashboard
   - Ensure all dependencies are in `requirements.txt`
   - Verify `build.sh` has execute permissions

2. **Database Connection Issues:**
   - Verify `DATABASE_URL` environment variable is set
   - Check PostgreSQL service status

3. **Static Files Not Loading:**
   - Ensure `collectstatic` runs successfully during build
   - Check WhiteNoise configuration in settings

4. **Application Errors:**
   - Check application logs in Render dashboard
   - Verify `DEBUG = False` in production
   - Check `ALLOWED_HOSTS` configuration

## Monitoring and Maintenance

- Monitor your application through the Render dashboard
- Set up notifications for deployment failures
- Regularly update dependencies for security patches
- Monitor database usage and performance

## Support

For issues related to:

- **Render Platform:** Check [Render Documentation](<https://render.com/docs>)
- **Django Configuration:** Review [Django Deployment Guide](<https://docs.djangoproject.com/en/stable/howto/deployment/>)
- **This Project:** Check project documentation and issue tracker

---

**Note:** This deployment configuration is optimized for Render's platform. For other cloud providers, you may need to adjust the configuration accordingly.
