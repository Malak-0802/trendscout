# Script de test multi-produits pour Trendscout

$products = @(
    "iPhone 15 Pro",
    "Nike Air Max",
    "Balenciaga Sneakers",
    "Crocs",
    "Levi's Jeans",
    "Y2K Cargo Pants",
    "Luxury Watch",
    "Streetwear Hoodie"
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TRENDSCOUT SCRAPING TEST - MULTI PRODUCTS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$results = @()

foreach ($product in $products) {
    Write-Host "Testing: $product" -ForegroundColor Green
    
    try {
        $body = @{
            product_name = $product
            category = "Fashion"
            season = "2024"
        } | ConvertTo-Json
        
        $response = Invoke-WebRequest -Uri "http://localhost:8000/api/analyze-trend" `
          -Method POST `
          -Headers @{"Content-Type"="application/json"} `
          -Body $body `
          -TimeoutSec 30
        
        $data = $response.Content | ConvertFrom-Json
        
        Write-Host "  SUCCESS!" -ForegroundColor Green
        Write-Host "  Sentiment: $($data.sentiment_score)/100" -ForegroundColor Yellow
        Write-Host "  Adoption: $($data.catwalk_adoption)%" -ForegroundColor Yellow
        Write-Host "  Prediction: $($data.prediction)" -ForegroundColor Magenta
        Write-Host "  Reviews: $($data.review_count)" -ForegroundColor Blue
        
        $results += @{
            Product = $product
            Sentiment = $data.sentiment_score
            Adoption = $data.catwalk_adoption
            Prediction = $data.prediction
            Reviews = $data.review_count
        }
        
    } catch {
        Write-Host "  ERROR: $($_)" -ForegroundColor Red
    }
    
    Write-Host ""
    Start-Sleep -Seconds 2
}

# Resume
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Total products tested: $($results.Count)" -ForegroundColor Yellow
Write-Host ""

if ($results.Count -gt 0) {
    $results | Format-Table -AutoSize
}

Write-Host ""
Write-Host "Test completed!" -ForegroundColor Green