# %%
import connect
import pandas as pd
import query
import pandas.io.sql as psql

%load_ext autoreload
%autoreload 2

# %%
conn = connect.get_connection()

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

qc_o = query.Customers.customer_loyalty()
qc_cf = query.Customers.customer_flight_preferences()
qc_fc =query.Customers.customer_class_flight()

# %%
# EVENTS QUERIES
qe_e = query.Events.events()

# %%
def execute_query_to_dataframe(query, params=None):
    conn = None
    try:
        conn = connect.get_connection()
        df = psql.read_sql_query(query, conn, params=params)
        print(f"""\n✅ Query executed. {len(df)} filas obtenidas""")
        return df
        
    except Exception as e:
        print(f"❌ Query error: {e}")
        raise


