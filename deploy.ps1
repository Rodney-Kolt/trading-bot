Write-Host "🚀 Deploying Multi-Currency System..." -ForegroundColor Green
Write-Host ""

Write-Host "📁 Adding files to git..." -ForegroundColor Yellow
git add -A

Write-Host "📝 Committing changes..." -ForegroundColor Yellow
git commit -m "Add multi-currency support - Enhanced bot and dashboard"

Write-Host "🌐 Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "🎉 Deployment complete!" -ForegroundColor Green
Write-Host "⏳ Railway will auto-deploy in 2-3 minutes" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to continue"