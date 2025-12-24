@echo off
echo 🚀 Deploying Multi-Currency System...
echo.

echo 📁 Adding files to git...
git add -A

echo 📝 Committing changes...
git commit -m "Add multi-currency support - Enhanced bot and dashboard"

echo 🌐 Pushing to GitHub...
git push origin main

echo.
echo 🎉 Deployment complete!
echo ⏳ Railway will auto-deploy in 2-3 minutes
echo.
pause