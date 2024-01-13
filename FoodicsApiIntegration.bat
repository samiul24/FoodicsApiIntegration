@echo off

set mmddyyyy=%DATE:~4,2%%DATE:~7,2%%DATE:~10,4%

echo Start Sync: %DATE% %TIME% >> Logs\log_%mmddyyyy%.txt

"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Orders.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Transfer_Orders.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Inventory_Categories.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Inventory_Items.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Payment_Methods.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Products.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Modifiers.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Discounts.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Addresses.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Branches.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Categories.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Charges.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Combos.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Coupons.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Customers.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Suppliers.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Delivery_Zones.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Devices.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Drawer_Operations.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Gift_Card_Products.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Gift_Card_Transactions.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\Groups.py"
"C:\Users\api_admin\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\api_admin\Desktop\FoodicsApiIntegration\ApiIntegration\House_Account_Transactions.py"

echo End Sync: %DATE% %TIME% >> Logs\log_%mmddyyyy%.txt