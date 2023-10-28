@echo off

set mmddyyyy=%DATE:~4,2%%DATE:~7,2%%DATE:~10,4%

echo Start Sync: %DATE% %TIME% >> Logs\log_%mmddyyyy%.txt

"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Inventory_Categories.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Inventory_Items.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Inventory_Transaction.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Orders.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Payment_Methods.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Products.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Purchase_Orders.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Transfer_Orders.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Modifiers.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Discounts.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Addresses.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Branches.py"

echo End Sync: %DATE% %TIME% >> Logs\log_%mmddyyyy%.txt