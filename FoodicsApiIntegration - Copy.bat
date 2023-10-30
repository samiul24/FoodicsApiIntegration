@echo off

set mmddyyyy=%DATE:~4,2%%DATE:~7,2%%DATE:~10,4%

echo Start Sync: %DATE% %TIME% >> Logs\log_%mmddyyyy%.txt

"C:\Users\samiul\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\samiul\Desktop\Git Upload\FoodicsApiIntegration\ApiIntegration\Inventory_Categories.py"
"C:\Users\samiul\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\samiul\Desktop\Git Upload\FoodicsApiIntegration\ApiIntegration\Inventory_Items.py"
"C:\Users\samiul\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\samiul\Desktop\Git Upload\FoodicsApiIntegration\ApiIntegration\Inventory_Transaction.py"
"C:\Users\samiul\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\samiul\Desktop\Git Upload\FoodicsApiIntegration\ApiIntegration\Orders.py"
"C:\Users\samiul\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\samiul\Desktop\Git Upload\FoodicsApiIntegration\ApiIntegration\Payment_Methods.py"
"C:\Users\samiul\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\samiul\Desktop\Git Upload\FoodicsApiIntegration\ApiIntegration\Products.py"
"C:\Users\samiul\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\samiul\Desktop\Git Upload\FoodicsApiIntegration\ApiIntegration\Purchase_Orders.py"
"C:\Users\samiul\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\samiul\Desktop\Git Upload\FoodicsApiIntegration\ApiIntegration\Transfer_Orders.py"
"C:\Users\samiul\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\samiul\Desktop\Git Upload\FoodicsApiIntegration\ApiIntegration\Modifiers.py"
"C:\Users\samiul\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\samiul\Desktop\Git Upload\FoodicsApiIntegration\ApiIntegration\Discounts.py"
"C:\Users\samiul\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\samiul\Desktop\Git Upload\FoodicsApiIntegration\ApiIntegration\Addresses.py"
"C:\Users\samiul\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\samiul\Desktop\Git Upload\FoodicsApiIntegration\ApiIntegration\Branches.py"

echo End Sync: %DATE% %TIME% >> Logs\log_%mmddyyyy%.txt
pause