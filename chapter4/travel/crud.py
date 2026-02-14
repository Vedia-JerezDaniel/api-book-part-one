# %%
import connect
import pandas as pd
import query
import pandas.io.sql as psql
import logging


# %%
# conn = connect.get_connection()

# %%
# BOOKING QUERIES

qb_r = query.Booking.revenue("CONFIRMED")
qb_rs = query.Booking.revenue_by_status()
qb_or = query.Booking.occupancy_rate()
qb_rp = query.Booking.revenue_performance('CONFIRMED')
qb_op = query.Booking.optimized_revenue()

# %%
# FLIGHT QUERIES

qf_o = query.Flights.flights_overview()
qf_p = query.Flights.flight_prices()
qf_fp = query.Flights.flight_popularity()
qf_fi = query.Flights.flight_inventory()

# %%
# PAYMENT QUERIES

qp_c = query.Payments.customer_payments()
qp_o = query.Payments.payments_overview()

# %%
# CUSTOMER QUERIES

qc_o = query.Customers.customer_hotel_preferences()
qc_cf = query.Customers.customer_flight_preferences()
qc_fc =query.Customers.customer_class_flight()

# %%
# EVENTS QUERIES
qe_e = query.Events.events()

# QUERY ANALYTICS
qc_hco = "SELECT COUNT(*) FROM travel.hotels"
qc_fco = "SELECT COUNT(*) FROM travel.flights"
qc_cco = "SELECT COUNT(*) FROM travel.customers"
qc_pco = "SELECT COUNT(DISTINCT(customer_id)) FROM travel.payments"
qc_eco = "SELECT COUNT(DISTINCT(customer_id)) FROM travel.events"

# %%
def execute_query_to_dataframe(query, params=None):
    conn = None
    try:
        conn = connect.get_connection()
        df = psql.read_sql_query(query, conn, params=params)
        logging.info(f"✅ Query executed. {len(df)} filas obtenidas")
        return df
        
    except Exception as e:
        logging.error(f"❌ Query error: {e}")
        raise


