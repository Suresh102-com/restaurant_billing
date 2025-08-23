-A simple Streamlit-based Restaurant Billing Application that allows restaurants to manage menus, take customer orders, calculate totals, and process payments in a clean UI.

-(Image 1)->
![image alt](https://github.com/Suresh102-com/restaurant_billing/blob/d049d4998ab13198e4e25ff9bbfe9f3d55babbb0/screenshot1.png)

-📋 Menu Management: Default menu loaded; items displayed in the sidebar.

🧑‍🤝‍🧑 Order Modes: Supports both Dine-In (with table number) and Takeaway (with customer name).

➕ Add Items: Select menu items with quantities and add them to the current order.

💰 Billing: Automatic calculation of subtotals and running total.

📥 Export Bill: Download the bill as a CSV file.

🧹 Clear Order: Reset the cart anytime.

✅ Confirm Order: Move to the payment page.

💳 Payment Options: Choose Cash, Card, or UPI.

🗄️ Database Integration: Saves completed orders via db_utils.save_order()

-Tech Stack->

Python 3.8+

Streamlit (UI framework)

Pandas (data handling)

sqlite3 (data store)

-✅ Future Enhancements

Upload custom menu from CSV.

Add admin dashboard to view past orders.

Integrate real payment gateway (Razorpay/Stripe/Paytm).

Multi-user login support.



-(Image 2)->

![image alt](-(Image 1)->
![image alt](https://github.com/Suresh102-com/restaurant_billing/blob/d049d4998ab13198e4e25ff9bbfe9f3d55babbb0/screenshot2.png))


