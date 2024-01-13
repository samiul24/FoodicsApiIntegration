@echo off

set mmddyyyy=%DATE:~4,2%%DATE:~7,2%%DATE:~10,4%

echo Start Sync: %DATE% %TIME% >> Logs\log_%mmddyyyy%.txt

"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Purchase_Orders.py"

echo End Sync: %DATE% %TIME% >> Logs\log_%mmddyyyy%.txt