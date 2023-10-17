@echo off
echo Start Sync: %DATE% %TIME%
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Inventory_Categories.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Inventory_Items.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Inventory_Transaction.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Orders.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Payment_Methods.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Products.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Purchase_Orders.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Transfer_Orders.py"
echo End Sync: %DATE% %TIME%