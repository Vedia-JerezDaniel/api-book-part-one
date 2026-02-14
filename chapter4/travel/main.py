"""FastAPI program - Chapter 4/Travel"""

from fastapi import Depends, FastAPI, HTTPException
# from sqlalchemy.orm import Session
# from datetime import date

import crud, schemas
# from connect import SessionLocal


app = FastAPI()

# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@app.get("/")
async def root():
    return {"message": "API health check successful"}

# BOOKING
@app.get("/v0/booking_item/", response_model=list[schemas.Booking_Item])
def read_booking_item(status: str = 'CONFIRMED'):
    query = crud.qb_r
    params = {"status": status}
    df = crud.execute_query_to_dataframe(query, params)
    
    records = df.to_dict(orient='records')
    return [schemas.Booking_Item(**row) for row in records]


@app.get("/v0/booking_revenue_status/", response_model=list[schemas.Booking_revenue_status])
def read_booking_revenue_status():
    query = crud.qb_rs
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Booking_revenue_status(**row) for row in records]


@app.get("/v0/booking_occupancy_rate/", response_model=list[schemas.Occupancy_rate])
def read_booking_occupancy_rate():
    query = crud.qb_or
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Occupancy_rate(**row) for row in records]


@app.get("/v0/revenue_performance/", response_model=list[schemas.Revenue_performance])
def read_booking_revenue_performance(status: str = 'CONFIRMED'):
    query = crud.qb_rp
    params = {"status": status}
    df = crud.execute_query_to_dataframe(query, params)
    
    records = df.to_dict(orient='records')
    return [schemas.Revenue_performance(**row) for row in records]


@app.get("/v0/optimized_revenue/", response_model=list[schemas.Optimized_revenue])
def read_booking_optimized_revenue():
    query = crud.qb_op
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Optimized_revenue(**row) for row in records]


# FLIGHTS
@app.get("/v0/flight_overview/", response_model=list[schemas.Flight_overview])
def read_flight_overview():
    query = crud.qf_o
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Flight_overview(**row) for row in records]


@app.get("/v0/flight_prices/", response_model=list[schemas.Flight_prices])
def read_flight_prices():
    query = crud.qf_p
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Flight_prices(**row) for row in records]


@app.get("/v0/flight_popularity/", response_model=list[schemas.Flight_popularity])
def read_flight_popularity():
    query = crud.qf_fp
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Flight_popularity(**row) for row in records]

@app.get("/v0/flight_inventory/", response_model=list[schemas.Flight_inventory])
def read_flight_inventory():
    query = crud.qf_fi
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Flight_inventory(**row) for row in records]


# PAYMENTS
@app.get("/v0/customer_payments/", response_model=list[schemas.Customer_payments])
def read_customer_payments():
    query = crud.qp_c
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Customer_payments(**row) for row in records]

@app.get("/v0/payments_overview/", response_model=list[schemas.Payments_overview])
def read_payments_overview():
    query = crud.qp_o
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Payments_overview(**row) for row in records]

# CUSTOMERS
@app.get("/v0/customer_hotel_preferences/", response_model=list[schemas.Customer_hotel_preferences])
def read_customer_hotel_preferences():
    query = crud.qc_o
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Customer_hotel_preferences(**row) for row in records]

@app.get("/v0/customer_flight_preferences/", response_model=list[schemas.Customer_flight_preferences])
def read_customer_flight_preferences():
    query = crud.qc_cf
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Customer_flight_preferences(**row) for row in records]

@app.get("/v0/customer_flight_class/", response_model=list[schemas.Customer_flight_class])
def read_customer_flight_class():
    query = crud.qc_fc
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Customer_flight_class(**row) for row in records]

# EVENTS
@app.get("/v0/events/", response_model=list[schemas.Events])
def read_events():
    query = crud.qe_e
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Events(**row) for row in records]

# COUNT ANALYTICS
@app.get("/v0/counts/", response_model=schemas.Counts)
def get_count():
    counts = schemas.Counts(
    hotel_count = crud.execute_query_to_dataframe(crud.qc_hco).iat[0,0],
    flight_count = crud.execute_query_to_dataframe(crud.qc_fco).iat[0,0],
    customer_count = crud.execute_query_to_dataframe(crud.qc_cco).iat[0,0],
    payment_count = crud.execute_query_to_dataframe(crud.qc_pco).iat[0,0],
    events_count = crud.execute_query_to_dataframe(crud.qc_eco).iat[0,0]
    )
    return counts
