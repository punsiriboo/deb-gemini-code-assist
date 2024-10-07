# BigQuery Casvas Prompt for Data Analysis

## ALL TABLES:
1. distribution_centers: Information about various distribution centers
2. events: Records of events, possibly related to website visits, customer interactions
3. inventory_items: Details about items in the inventory, possibly including quantities and locations.
4. order_items: Information about items included in orders.
5. orders: Details about customer orders, including order dates, statuses, and associated users.
6. products: Information about products, such as names, descriptions, and prices.
7. users: Details about users, including customer information.

## Orders
Prompts:
| Query Prompt | Visualization Prompts |
| - | - |
|Find cancel rate based on gender| -|
| For all order, find ratio of each order status | Stacked bar chart by month |
| For each month, find total_revenue, total_items, total_purchasers, total_orders where the order not Cancelled or Returned| Line chart by month |
|For Shipped Orders, find average, min, max, lead time in day before Shipped| - |

## Distribution Centers
- Summary product category in each DC

## Events
- count total users group by trafic source , country 
- สรุปจำนวน event จาก trafic source , ทุก event_type, browsrer

## Products
| Query Prompt | Visualization Prompts |
| - | - |
|Top 10 Average, min, max profit from each category |Bar chrat|

## User
| Query Prompt | Visualization Prompts |
| - | - |
| Summarize total user by traffice_source, gender and city |-|

## Order Items + Product 
| Query Prompt | Visualization Prompts |
| - | - |
| Analyze which product category have order sale volume and frequency | - |
| product category sales| - |
| Product category cancellation and return | - |


### References:
- Medium: https://medium.com/@chisomnnamani/the-look-e-commerce-data-analysis-28342b8da868
