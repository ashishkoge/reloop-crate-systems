# Data Dictionary

SQL types below are from `schema.sql`. Raw-source fields retain the supplied text representation where stated.

## `regions`

Operational geography used for hub, customer, supplier, and billing alignment.

| Field | SQL type | Description |
|---|---|---|
| `region_id` | `SMALLINT` | Primary key for this table. |
| `region_code` | `VARCHAR` | Operational attribute. |
| `region_name` | `VARCHAR` | Operational attribute. |
| `country` | `VARCHAR` | Operational attribute. |
| `operational_zone` | `VARCHAR` | Operational attribute. |
| `active_flag` | `BOOLEAN` | Boolean operational indicator. |

## `employees`

Internal employee directory across Operations, Commercial, Finance, and Supply Chain.

| Field | SQL type | Description |
|---|---|---|
| `employee_id` | `INTEGER` | Primary key for this table. |
| `employee_code` | `VARCHAR` | Operational attribute. |
| `first_name` | `VARCHAR` | Operational attribute. |
| `last_name` | `VARCHAR` | Operational attribute. |
| `department` | `VARCHAR` | Operational attribute. |
| `job_title` | `VARCHAR` | Operational attribute. |
| `region_id` | `SMALLINT` | Primary key for this table. |
| `manager_employee_id` | `INTEGER` | Foreign key to the related master or transaction record. |
| `hire_date` | `DATE` | Business or processing date. |
| `employment_status` | `VARCHAR` | Status value as received from the relevant operational process. |
| `work_email` | `VARCHAR` | Operational attribute. |

## `customers`

Commercial customer master records from multiple source processes.

| Field | SQL type | Description |
|---|---|---|
| `customer_id` | `INTEGER` | Primary key for this table. |
| `customer_code` | `VARCHAR` | Operational attribute. |
| `legal_name` | `VARCHAR` | Operational attribute. |
| `trading_name` | `VARCHAR` | Operational attribute. |
| `customer_segment` | `VARCHAR` | Operational attribute. |
| `industry` | `VARCHAR` | Operational attribute. |
| `home_region_id` | `SMALLINT` | Foreign key to the related master or transaction record. |
| `account_manager_id` | `INTEGER` | Foreign key to the related master or transaction record. |
| `primary_email` | `VARCHAR` | Operational attribute. |
| `primary_phone` | `VARCHAR` | Operational attribute. |
| `lifecycle_status` | `VARCHAR` | Status value as received from the relevant operational process. |
| `registered_on` | `DATE` | Business or processing date. |
| `credit_limit` | `NUMERIC(14,2)` | Operational attribute. |
| `tax_id` | `INTEGER` | Foreign key to the related master or transaction record. |
| `record_source` | `VARCHAR` | Operational attribute. |

## `customer_addresses`

Customer billing, delivery, returns, production, and cross-dock sites.

| Field | SQL type | Description |
|---|---|---|
| `address_id` | `INTEGER` | Primary key for this table. |
| `customer_id` | `INTEGER` | Primary key for this table. |
| `region_id` | `SMALLINT` | Primary key for this table. |
| `address_type` | `VARCHAR` | Operational attribute. |
| `site_name` | `VARCHAR` | Operational attribute. |
| `address_line_1` | `VARCHAR` | Operational attribute. |
| `city` | `VARCHAR` | Operational attribute. |
| `postal_code` | `VARCHAR` | Operational attribute. |
| `is_primary` | `BOOLEAN` | Operational attribute. |
| `active_flag` | `BOOLEAN` | Boolean operational indicator. |
| `validated_on` | `DATE` | Business or processing date. |

## `suppliers`

Vendor master, including fabricators, carriers, parts, and sanitation suppliers.

| Field | SQL type | Description |
|---|---|---|
| `supplier_id` | `INTEGER` | Primary key for this table. |
| `supplier_code` | `VARCHAR` | Operational attribute. |
| `supplier_name` | `VARCHAR` | Operational attribute. |
| `supplier_type` | `VARCHAR` | Operational attribute. |
| `home_region_id` | `SMALLINT` | Foreign key to the related master or transaction record. |
| `contact_email` | `VARCHAR` | Operational attribute. |
| `contact_phone` | `VARCHAR` | Operational attribute. |
| `onboarded_on` | `DATE` | Business or processing date. |
| `supplier_status` | `VARCHAR` | Status value as received from the relevant operational process. |
| `standard_lead_days` | `SMALLINT` | Operational attribute. |
| `quality_rating` | `NUMERIC(3,2)` | Operational attribute. |

## `crate_models`

Reusable insulated crate, pallet shipper, divider, and carrier catalog.

| Field | SQL type | Description |
|---|---|---|
| `crate_model_id` | `INTEGER` | Primary key for this table. |
| `sku` | `VARCHAR` | Operational attribute. |
| `model_name` | `VARCHAR` | Operational attribute. |
| `crate_category` | `VARCHAR` | Operational attribute. |
| `temperature_band` | `VARCHAR` | Operational attribute. |
| `material` | `VARCHAR` | Operational attribute. |
| `capacity_liters` | `SMALLINT` | Operational attribute. |
| `base_daily_rental_rate` | `NUMERIC(10,2)` | Monetary amount or rate in the relevant transaction currency. |
| `replacement_cost` | `NUMERIC(12,2)` | Monetary amount or rate in the relevant transaction currency. |
| `primary_supplier_id` | `INTEGER` | Foreign key to the related master or transaction record. |
| `active_flag` | `BOOLEAN` | Boolean operational indicator. |
| `introduced_on` | `DATE` | Business or processing date. |

## `contracts`

Customer commercial agreements and contractual billing parameters.

| Field | SQL type | Description |
|---|---|---|
| `contract_id` | `INTEGER` | Primary key for this table. |
| `contract_number` | `VARCHAR` | Operational attribute. |
| `customer_id` | `INTEGER` | Primary key for this table. |
| `account_manager_id` | `INTEGER` | Foreign key to the related master or transaction record. |
| `contract_tier` | `VARCHAR` | Operational attribute. |
| `contract_status` | `VARCHAR` | Status value as received from the relevant operational process. |
| `start_date` | `DATE` | Business or processing date. |
| `end_date_raw` | `VARCHAR` | Text supplied by the originating process; preserved without normalization. |
| `minimum_monthly_commitment` | `NUMERIC(14,2)` | Operational attribute. |
| `deposit_amount` | `NUMERIC(14,2)` | Monetary amount or rate in the relevant transaction currency. |
| `billing_currency` | `VARCHAR` | Operational attribute. |
| `cancellation_reason` | `VARCHAR` | Operational attribute. |

## `deployment_orders`

Customer request to deploy reusable equipment to a delivery site.

| Field | SQL type | Description |
|---|---|---|
| `order_id` | `BIGINT` | Primary key for this table. |
| `order_number` | `VARCHAR` | Operational attribute. |
| `customer_id` | `INTEGER` | Primary key for this table. |
| `contract_id` | `INTEGER` | Primary key for this table. |
| `delivery_address_id` | `INTEGER` | Foreign key to the related master or transaction record. |
| `fulfillment_region_id` | `SMALLINT` | Foreign key to the related master or transaction record. |
| `created_by_employee_id` | `INTEGER` | Foreign key to the related master or transaction record. |
| `order_date` | `DATE` | Business or processing date. |
| `requested_delivery_date_raw` | `VARCHAR` | Text supplied by the originating process; preserved without normalization. |
| `order_status` | `VARCHAR` | Status value as received from the relevant operational process. |
| `priority_level` | `VARCHAR` | Operational attribute. |
| `customer_po_number` | `VARCHAR` | Operational attribute. |
| `cancellation_reason` | `VARCHAR` | Operational attribute. |
| `order_channel` | `VARCHAR` | Operational attribute. |

## `order_items`

Crate-model line item on a deployment order.

| Field | SQL type | Description |
|---|---|---|
| `order_item_id` | `BIGINT` | Primary key for this table. |
| `order_id` | `BIGINT` | Primary key for this table. |
| `crate_model_id` | `INTEGER` | Primary key for this table. |
| `quantity_ordered` | `INTEGER` | Operational attribute. |
| `quantity_returned` | `INTEGER` | Operational attribute. |
| `daily_rental_days` | `SMALLINT` | Operational attribute. |
| `unit_daily_rate` | `NUMERIC(12,2)` | Monetary amount or rate in the relevant transaction currency. |
| `unit_replacement_cost` | `NUMERIC(12,2)` | Monetary amount or rate in the relevant transaction currency. |
| `discount_pct` | `NUMERIC(5,2)` | Operational attribute. |
| `line_status` | `VARCHAR` | Status value as received from the relevant operational process. |
| `pricing_source` | `VARCHAR` | Operational attribute. |

## `shipments`

Carrier movement created to fulfil an order; orders may split across shipments.

| Field | SQL type | Description |
|---|---|---|
| `shipment_id` | `BIGINT` | Primary key for this table. |
| `shipment_number` | `VARCHAR` | Operational attribute. |
| `order_id` | `BIGINT` | Primary key for this table. |
| `carrier_supplier_id` | `INTEGER` | Foreign key to the related master or transaction record. |
| `origin_region_id` | `SMALLINT` | Foreign key to the related master or transaction record. |
| `destination_region_id` | `SMALLINT` | Foreign key to the related master or transaction record. |
| `coordinator_employee_id` | `INTEGER` | Foreign key to the related master or transaction record. |
| `shipment_status` | `VARCHAR` | Status value as received from the relevant operational process. |
| `dispatch_date` | `DATE` | Business or processing date. |
| `scheduled_arrival_date` | `DATE` | Business or processing date. |
| `actual_arrival_date` | `DATE` | Business or processing date. |
| `tracking_reference` | `VARCHAR` | Operational attribute. |
| `freight_cost` | `NUMERIC(12,2)` | Monetary amount or rate in the relevant transaction currency. |
| `damage_units` | `INTEGER` | Operational attribute. |
| `temperature_excursion_flag` | `BOOLEAN` | Boolean operational indicator. |

## `service_logs`

Service-hub inspection, washing, repair, decommission, or cycle-count event.

| Field | SQL type | Description |
|---|---|---|
| `service_log_id` | `BIGINT` | Primary key for this table. |
| `shipment_id` | `BIGINT` | Primary key for this table. |
| `crate_model_id` | `INTEGER` | Primary key for this table. |
| `service_region_id` | `SMALLINT` | Foreign key to the related master or transaction record. |
| `technician_employee_id` | `INTEGER` | Foreign key to the related master or transaction record. |
| `service_date` | `DATE` | Business or processing date. |
| `service_type` | `VARCHAR` | Operational attribute. |
| `expected_units` | `INTEGER` | Operational attribute. |
| `inspected_units` | `INTEGER` | Operational attribute. |
| `passed_units` | `INTEGER` | Operational attribute. |
| `scrapped_units` | `INTEGER` | Operational attribute. |
| `service_cost` | `NUMERIC(12,2)` | Monetary amount or rate in the relevant transaction currency. |
| `inspection_notes` | `VARCHAR` | Operational attribute. |

## `invoices`

Accounts receivable document with payment and refund fields.

| Field | SQL type | Description |
|---|---|---|
| `invoice_id` | `BIGINT` | Primary key for this table. |
| `invoice_number` | `VARCHAR` | Operational attribute. |
| `external_invoice_ref` | `VARCHAR` | Operational attribute. |
| `customer_id` | `INTEGER` | Primary key for this table. |
| `contract_id` | `INTEGER` | Primary key for this table. |
| `order_id` | `BIGINT` | Primary key for this table. |
| `billing_region_id` | `SMALLINT` | Foreign key to the related master or transaction record. |
| `issued_by_employee_id` | `INTEGER` | Foreign key to the related master or transaction record. |
| `invoice_date` | `DATE` | Business or processing date. |
| `due_date` | `DATE` | Business or processing date. |
| `invoice_status` | `VARCHAR` | Status value as received from the relevant operational process. |
| `subtotal_amount` | `NUMERIC(14,2)` | Monetary amount or rate in the relevant transaction currency. |
| `tax_amount` | `NUMERIC(14,2)` | Monetary amount or rate in the relevant transaction currency. |
| `refund_amount` | `NUMERIC(14,2)` | Monetary amount or rate in the relevant transaction currency. |
| `paid_amount` | `NUMERIC(14,2)` | Monetary amount or rate in the relevant transaction currency. |
| `paid_date` | `DATE` | Business or processing date. |
| `currency` | `VARCHAR` | Operational attribute. |
| `payment_terms` | `VARCHAR` | Operational attribute. |
