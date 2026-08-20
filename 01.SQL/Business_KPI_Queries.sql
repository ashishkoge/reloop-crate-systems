/*==========================================================
Ticket ID: BA-01
KPI: Top Customers by Net Revenue

Business Objective:
Identify the customers generating the highest net revenue
to prioritize key accounts.
==========================================================*/

WITH Customer_Revenue AS (
    SELECT
        c.legal_name AS Customer_Name,
        SUM(i.subtotal_amount - i.refund_amount) AS Net_Revenue
    FROM invoices i
    INNER JOIN customers c
        ON i.customer_id = c.customer_id
    GROUP BY
        c.customer_id,
        c.legal_name
),
Ranked_Customers AS (
    SELECT
        Customer_Name,
        Net_Revenue,
        DENSE_RANK() OVER(ORDER BY Net_Revenue DESC) AS Revenue_Rank
    FROM Customer_Revenue
)
SELECT *
FROM Ranked_Customers
ORDER BY Revenue_Rank
LIMIT 10;

/*==========================================================
Ticket ID: BA-02
KPI: Revenue by Top Crate Models

Business Objective:
Identify the crate models generating the highest net revenue
to understand product performance and support inventory,
sales, and deployment planning.
==========================================================*/

WITH Net_Revenue AS (
    SELECT
        cm.model_name AS Crate_Model,
        SUM(i.subtotal_amount - i.refund_amount) AS Net_Revenue,
        COUNT(DISTINCT oi.order_id) AS Total_Orders
    FROM invoices i
    INNER JOIN deployment_orders d
        ON i.order_id = d.order_id
    INNER JOIN order_items oi
        ON d.order_id = oi.order_id
    INNER JOIN crate_models cm
        ON oi.crate_model_id = cm.crate_model_id
    WHERE i.order_id IS NOT NULL
    GROUP BY
        cm.crate_model_id,
        cm.model_name
),
Crate_Ranked AS (
    SELECT
        Crate_Model,
        Net_Revenue,
        Total_Orders,
        DENSE_RANK() OVER (
            ORDER BY Net_Revenue DESC
        ) AS Revenue_Rank
    FROM Net_Revenue
)
SELECT *
FROM Crate_Ranked
ORDER BY Revenue_Rank
LIMIT 10;

/*==========================================================
Ticket ID: BA-03
KPI: Revenue by Customer Region

Business Objective:
Identify which customer regions generate the highest net
revenue to support regional sales strategy and resource
allocation.
==========================================================*/

WITH Region_Revenue AS (
    SELECT
        r.region_name AS Region_Name,
        SUM(i.subtotal_amount - i.refund_amount) AS Net_Revenue,
        COUNT(DISTINCT c.customer_id) AS Total_Customers
    FROM invoices i
    INNER JOIN customers c
        ON i.customer_id = c.customer_id
    INNER JOIN regions r
        ON c.home_region_id = r.region_id
    GROUP BY
        r.region_id,
        r.region_name
),
Ranked_Region AS (
    SELECT
        Region_Name,
        Net_Revenue,
        Total_Customers,
        DENSE_RANK() OVER(
            ORDER BY Net_Revenue DESC
        ) AS Revenue_Rank
    FROM Region_Revenue
)
SELECT *
FROM Ranked_Region
ORDER BY Revenue_Rank;

/*==========================================================
Ticket ID: BA-04
KPI: Monthly Revenue Trend

Business Objective:
Analyze monthly net revenue trends and measure
Month-over-Month (MoM) revenue growth to identify
business growth patterns and seasonality.
==========================================================*/

WITH Monthly_Revenue AS (
    SELECT
        YEAR(invoice_date) AS Year,
        MONTH(invoice_date) AS Month_No,
        MONTHNAME(invoice_date) AS Month_Name,
        SUM(subtotal_amount - refund_amount) AS Net_Revenue
    FROM invoices
    WHERE invoice_status = 'Paid'
    GROUP BY
        YEAR(invoice_date),
        MONTH(invoice_date),
        MONTHNAME(invoice_date)
),
Previous_Month AS (
    SELECT
        Year,
        Month_No,
        Month_Name,
        Net_Revenue,
        LAG(Net_Revenue) OVER(
            ORDER BY Year, Month_No
        ) AS Previous_Month_Revenue
    FROM Monthly_Revenue
),
Growth AS (
    SELECT
        Year,
        Month_No,
        Month_Name,
        Net_Revenue,
        Previous_Month_Revenue,
        ROUND(
            (
                (Net_Revenue - Previous_Month_Revenue)
                / NULLIF(Previous_Month_Revenue, 0)
            ) * 100,
            2
        ) AS MoM_Growth
    FROM Previous_Month
)
SELECT *
FROM Growth
ORDER BY
    Year,
    Month_No;

/*==========================================================
Ticket ID: BA-05
KPI: Loyal Repeat Customers

Business Objective:
Identify customers who repeatedly place deployment orders.
==========================================================*/

WITH Customer_Details AS (
    SELECT
        cu.legal_name AS Customer_Name,
        COUNT(DISTINCT d.order_id) AS Total_Orders,
        COUNT(DISTINCT d.contract_id) AS Total_Contracts,
        COALESCE(SUM(i.subtotal_amount - i.refund_amount),0) AS Net_Revenue
    FROM deployment_orders d
    INNER JOIN contracts c
        ON d.contract_id = c.contract_id
    INNER JOIN customers cu
        ON c.customer_id = cu.customer_id
    LEFT JOIN invoices i
        ON d.order_id = i.order_id
    GROUP BY
        cu.customer_id,
        cu.legal_name
),
Rank_Loyalty AS (
    SELECT
        Customer_Name,
        Total_Orders,
        Total_Contracts,
        Net_Revenue,
        CASE
            WHEN Total_Orders >= 10 THEN 'Yes'
            ELSE 'No'
        END AS Repeat_Customer,
        DENSE_RANK() OVER(ORDER BY Total_Orders DESC) AS Loyalty_Rank
    FROM Customer_Details
)
SELECT *
FROM Rank_Loyalty
ORDER BY Loyalty_Rank;

/*==========================================================
Ticket ID: BA-06
KPI: Shipment Delay Analysis

Business Objective:
Identify shipments delivered late.
==========================================================*/

WITH Shipment_Data AS (
    SELECT
        s.shipment_number AS Shipment_Number,
        ro.region_name AS Origin_Region,
        rd.region_name AS Destination_Region,
        s.dispatch_date,
        s.actual_arrival_date,
        DATEDIFF(s.actual_arrival_date,s.dispatch_date) AS Transit_Days
    FROM shipments s
    INNER JOIN regions ro
        ON s.origin_region_id=ro.region_id
    INNER JOIN regions rd
        ON s.destination_region_id=rd.region_id
    WHERE s.actual_arrival_date IS NOT NULL
),
Shipment_Status AS (
    SELECT
        Shipment_Number,
        Origin_Region,
        Destination_Region,
        dispatch_date,
        actual_arrival_date,
        Transit_Days,
        CASE
            WHEN Transit_Days>7 THEN 'Late'
            ELSE 'On Time'
        END AS Delivery_Status
    FROM Shipment_Data
)
SELECT *
FROM Shipment_Status;

/*==========================================================
Ticket ID: BA-08
KPI: Customer Segmentation

Business Objective:
Segment customers based on Net Revenue.
==========================================================*/

WITH Customer_Info AS (
    SELECT
        cu.legal_name AS Customer_Name,
        COUNT(DISTINCT d.order_id) AS Total_Orders,
        SUM(i.subtotal_amount-i.refund_amount) AS Net_Revenue
    FROM deployment_orders d
    INNER JOIN invoices i
        ON d.order_id=i.order_id
    INNER JOIN contracts c
        ON d.contract_id=c.contract_id
    INNER JOIN customers cu
        ON c.customer_id=cu.customer_id
    GROUP BY
        cu.customer_id,
        cu.legal_name
),
Customer_Segment AS (
    SELECT
        Customer_Name,
        Total_Orders,
        Net_Revenue,
        DENSE_RANK() OVER(ORDER BY Net_Revenue DESC) AS Customer_Rank,
        CASE
            WHEN Net_Revenue>=500000 THEN 'Platinum'
            WHEN Net_Revenue>=300000 THEN 'Gold'
            WHEN Net_Revenue>=100000 THEN 'Silver'
            ELSE 'Bronze'
        END AS Revenue_Band
    FROM Customer_Info
)
SELECT *
FROM Customer_Segment
ORDER BY Customer_Rank;

/*==========================================================
Ticket ID: BA-09
KPI: Average Rental Days by Crate Model

Business Objective:
Identify which crate models stay longest with customers.
==========================================================*/

WITH Avg_Rental_Day AS (
    SELECT
        cm.model_name AS Model_Name,
        ROUND(AVG(oi.daily_rental_days),2) AS Average_Rental_Days,
        COUNT(DISTINCT oi.order_id) AS Total_Orders
    FROM order_items oi
    INNER JOIN crate_models cm
        ON oi.crate_model_id=cm.crate_model_id
    GROUP BY
        cm.crate_model_id,
        cm.model_name
),
Rank_Model AS (
    SELECT
        Model_Name,
        Average_Rental_Days,
        Total_Orders,
        DENSE_RANK() OVER(ORDER BY Average_Rental_Days DESC) AS Rental_Rank
    FROM Avg_Rental_Day
)
SELECT *
FROM Rank_Model
ORDER BY Rental_Rank;

/*==========================================================
Ticket ID: BA-10
KPI: Profit Margin

Business Objective:
Calculate company profit margin.

Status:
NOT IMPLEMENTED

Reason:
The dataset does not contain complete operational costs
(payroll, rent, depreciation, utilities, etc.).

Calculating Profit Margin would produce misleading results.
==========================================================*/

/*==========================================================
Ticket ID: BA-11
KPI: Revenue by Contract Tier

Business Objective:
Identify which contract tiers generate the highest revenue
to support sales strategy and contract planning.
==========================================================*/

WITH Contract_Revenue AS (
    SELECT 
       c.contract_tier AS Contract_Tier,
       SUM(i.subtotal_amount - i.refund_amount) AS Net_Revenue,
       COUNT(DISTINCT(c.contract_id)) AS Total_Contracts,
       COUNT(DISTINCT(i.customer_id)) AS Total_Customers
	FROM invoices i
    INNER JOIN contracts c
    ON i.contract_id = c.contract_id
    GROUP BY 
      Contract_Tier
),
Tier_Rank AS (
    SELECT
      Contract_Tier,
      Net_Revenue,
      Total_Contracts,
      Total_Customers,
      ROUND( Net_Revenue / NULLIF(Total_Contracts,0),2
       ) AS Average_Contract_Revenue,
      DENSE_RANK() OVER( ORDER BY Net_Revenue DESC ) AS Tiers_Rank,
      ROUND( Net_Revenue * 100 / SUM(Net_Revenue) OVER(),2
       )  AS Revenue_Contribution_Pct
	FROM Contract_Revenue
)
SELECT *
FROM Tier_Rank
ORDER BY Net_Revenue DESC;

/*==========================================================
Ticket ID: BA-12
KPI: Supplier Performance Analysis

Business Objective:
Evaluate supplier performance based on shipment volume,
quality rating, and average freight cost.
==========================================================*/

WITH Supplier_Details AS (
   SELECT 
     s.supplier_id,
     s.supplier_name as Supplier_Name,
     COALESCE(s.quality_rating,0) AS Rating,
     COUNT(DISTINCT(sh.shipment_id)) AS Total_Shipments,
     ROUND(AVG(freight_cost),2) AS Average_Freight_Cost
   FROM shipments sh
   INNER JOIN suppliers s
   ON sh.carrier_supplier_id = s.supplier_id
   GROUP BY 
     s.supplier_id,
     s.supplier_name
),
Supplier_Rank AS (
   SELECT
     Supplier_Name,
     Rating,
     Total_Shipments,
     Average_Freight_Cost,
     DENSE_RANK() OVER( ORDER BY Rating DESC,
                        Average_Freight_Cost ASC) AS Suppliers_Rank
   FROM Supplier_Details
)
SELECT * 
FROM Supplier_Rank;

/*==========================================================
Ticket ID: BA-13
KPI: Deployment Trend Analysis

Business Objective:
Analyze monthly deployment trends to identify business
growth and operational demand using Month-over-Month (MoM)
deployment growth.
==========================================================*/

WITH Deployment_details AS (
  SELECT 
    YEAR( order_date) AS Year,
    MONTH( order_date) AS Month_No,
    MONTHNAME( order_date) AS Month_Name,
    COUNT(order_id) AS Total_Deployments
  FROM deployment_orders
  GROUP BY 
   year,
   Month_No,
   Month_Name
),
Deployment_Trend AS ( 
  SELECT 
   Year,
   Month_No,
   Month_Name,
   Total_Deployments,
   LAG(Total_Deployments) OVER( ORDER BY Year, Month_No ) AS Previous_Month_Deployment
  FROM Deployment_details
),
MoM_Growth AS (
  SELECT
    Year,
    Month_No,
    Month_Name,
    Total_Deployments,
    Previous_Month_Deployment,
    ROUND( (
             (Total_Deployments - Previous_Month_Deployment)
                                /
                 NULLIF(Previous_Month_Deployment,0)
           ) *100,2) AS GROWTH
  FROM Deployment_Trend 
)
SELECT * 
FROM MoM_Growth ;


