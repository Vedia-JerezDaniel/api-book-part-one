"""FastAPI program - Chapter 4/Travel"""

from fastapi import Depends, FastAPI, HTTPException, Query
# from sqlalchemy.orm import Session
# from datetime import date

import crud, schemas
# from connect import SessionLocal

with open('chapter5/travel/requirements.txt', 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)

content = open('chapter5/travel/description.txt').read()


app = FastAPI(description=content,
    title="WanderData Travel API",
    version="0.1")


@app.get("/",
    summary="Check to see if the WanderData Travel API is running",
    description="""Use this endpoint to check if the API is running""",
    response_description="A JSON record with a message in it. If the API is running A message will appears successfully.",
    operation_id="v0_health_check",
    tags=["analytics"],)
async def root():
    return {"message": "API health check successful"}

# BOOKING
@app.get(
    "/v0/booking_item/", 
    response_model=list[schemas.Booking_Item],
    summary="Get booking items",
    description="""Returns list of hotels bookings and revenue. Default status is 'CONFIRMED'. Other options include 'CANCELLED' and 'PENDING'.""",
    response_description="A list of hotels booking with hotel name, bookings number, customer count, and total revenue.",
    operation_id="v0_get_booking_items",
    tags=["booking"],)
def read_booking_item(status: str = Query(default='CONFIRMED',
    description="""Filter bookings by status. Default is 'CONFIRMED'. 
    Other options include 'CANCELLED' and 'PENDING'.""")):
    query = crud.qb_r
    params = {"status": status}
    df = crud.execute_query_to_dataframe(query, params)
    
    records = df.to_dict(orient='records')
    return [schemas.Booking_Item(**row) for row in records]


@app.get("/v0/booking_revenue_status/", 
         response_model=list[schemas.Booking_revenue_status],
         summary="Get booking revenue by its status, price and pricing recommendation",
         description="""Returns booking revenue status records with status, total revenue, and pricing recommendation.""",
         response_description="A list of booking revenue status records with status and total revenue.",
         operation_id="v0_get_booking_revenue_status",
         tags=["booking"],)
def read_booking_revenue_status():
    query = crud.qb_rs
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Booking_revenue_status(**row) for row in records]


@app.get("/v0/booking_occupancy_rate/",
         response_model=list[schemas.Occupancy_rate],
         summary="Get Hotel occupancy rate",
         description="""Returns the occupancy rate for each booking by day and price.""",
         response_description="A list of occupancy rate records with Hotel ID, price, and occupancy rate.",
         operation_id="v0_get_booking_occupancy_rate",
         tags=["booking"],)
def read_booking_occupancy_rate():
    query = crud.qb_or
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Occupancy_rate(**row) for row in records]


@app.get("/v0/revenue_performance/", 
         response_model=list[schemas.Revenue_performance],
         summary="Get Hotel revenue performance",
         description="""Returns the revenue performance for each hotel, daily bookings and amount .""",
         response_description="A list of revenue performance records with hotel name, daily bookings, and total revenue.",
         operation_id="v0_get_booking_revenue_performance",
         tags=["booking"],)
def read_booking_revenue_performance(status: str = Query(default='CONFIRMED',
    description="""Filter bookings by status. Default is 'CONFIRMED'. 
    Other options include 'CANCELLED' and 'PENDING'.""")):
    query = crud.qb_rp
    params = {"status": status}
    df = crud.execute_query_to_dataframe(query, params)
    
    records = df.to_dict(orient='records')
    return [schemas.Revenue_performance(**row) for row in records]


@app.get("/v0/optimized_revenue/", 
         response_model=list[schemas.Optimized_revenue],
         summary="Get Hotels booking revenue",
         description="""Returns a list of hotels with occupancy rate, price, and optimized revenue.""",
         response_description="A list of optimized revenue records with hotel name, occupancy rate, price, and optimized revenue.",
         operation_id="v0_get_booking_optimized_revenue",
         tags=["booking"],)
def read_booking_optimized_revenue():
    query = crud.qb_op
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Optimized_revenue(**row) for row in records]


# FLIGHTS
@app.get("/v0/flight_overview/",
            response_model=list[schemas.Flight_overview],
            summary="Get flight overview",
            description="""Returns an overview of all flights.""",
            response_description="A list of flight overview records with flight ID, origin, aircraft model and total seats.",
            operation_id="v0_get_flight_overview",
            tags=["flight"],)
def read_flight_overview():
    query = crud.qf_o
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Flight_overview(**row) for row in records]


@app.get("/v0/flight_prices/", 
         response_model=list[schemas.Flight_prices],
         summary="Get flight prices",
         description="""Returns the prices for all flights.""",
         response_description="A list of flight price records with destination, and price statistics.",
         operation_id="v0_get_flight_prices",
         tags=["flight"],)
def read_flight_prices():
    query = crud.qf_p
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Flight_prices(**row) for row in records]


@app.get("/v0/flight_popularity/", 
         response_model=list[schemas.Flight_popularity],
         summary="Get flight popularity",
         description="""Returns the popularity for all flights, cabin class and prices.""",
         response_description="A list of flight popularity records with destination, cabin class, and popularity.",
         operation_id="v0_get_flight_popularity",
         tags=["flight"],)
def read_flight_popularity():
    query = crud.qf_fp
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Flight_popularity(**row) for row in records]

@app.get("/v0/flight_inventory/",
         response_model=list[schemas.Flight_inventory],
         summary="Get flight inventory",
         description="""Returns the inventory for all flights, price statistics and seats available for each flight.""",
         response_description="A list of flight inventory records with flight ID and summary inventory.",
         operation_id="v0_get_flight_inventory",
         tags=["flight"],)
def read_flight_inventory():
    query = crud.qf_fi
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Flight_inventory(**row) for row in records]


# PAYMENTS
@app.get("/v0/customer_payments/", 
         response_model=list[schemas.Customer_payments],
         summary="Get customer payments",
         description="""Returns the payments for all customers classified by expenditure segment: new, regular, premium, VIP.""",
         response_description="A list of customer payment records with customer ID, expenditure segment, and total payment amount.",
         operation_id="v0_get_customer_payments",
         tags=["payment"],)
def read_customer_payments():
    query = crud.qp_c
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Customer_payments(**row) for row in records]

@app.get("/v0/payments_overview/", 
         response_model=list[schemas.Payments_overview],
         summary="Get payments overview",
         description="""Returns an overview of all payments by customer, payment type, amount, booking type and failure rate.""",
         response_description="A list of payment overview records with customer ID, payment type, amount, booking type and failure rate.",
         operation_id="v0_get_payments_overview",
         tags=["payment"],)
def read_payments_overview():
    query = crud.qp_o
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Payments_overview(**row) for row in records]

# CUSTOMERS
@app.get("/v0/customer_hotel_preferences/", 
         response_model=list[schemas.Customer_hotel_preferences],
         summary="Get customer  preferences",
         description="""Returns the destination preferences for all customers, number of bookings and average price for each destination.""",
         response_description="A list of customer destination preference with number of visits and price.",
         operation_id="v0_get_customer_hotel_preferences",
         tags=["customer"],)
def read_customer_hotel_preferences():
    query = crud.qc_o
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Customer_hotel_preferences(**row) for row in records]

@app.get("/v0/customer_flight_preferences/", 
         response_model=list[schemas.Customer_flight_preferences],
         summary="Get customer flight preferences",
         description="""Returns the flight preferences for all customers with summary prices.""",
         response_description="A list of customer flight preference records with customer ID, flight ID, and summary price.",
         operation_id="v0_get_customer_flight_preferences",
         tags=["customer"],)
def read_customer_flight_preferences():
    query = crud.qc_cf
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Customer_flight_preferences(**row) for row in records]

@app.get("/v0/customer_flight_class/", 
         response_model=list[schemas.Customer_flight_class],
         summary="Get customer flight class",
         description="""Returns the flight class for all customers in the system.""",
         response_description="A list of customer flight class records with customer ID and average price.",
         operation_id="v0_get_customer_flight_class",
         tags=["customer"],)
def read_customer_flight_class():
    query = crud.qc_fc
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Customer_flight_class(**row) for row in records]

# EVENTS
@app.get("/v0/events/", 
         response_model=list[schemas.Events],
         summary="Get events",
         description="""Returns all events in the system.""",
         response_description="A list of event records with event name, assistance count, and revenue.",
         operation_id="v0_get_events",
         tags=["event"],)
def read_events():
    query = crud.qe_e
    df = crud.execute_query_to_dataframe(query)
    
    records = df.to_dict(orient='records')
    return [schemas.Events(**row) for row in records]

# COUNT ANALYTICS
@app.get("/v0/counts/", 
         response_model=schemas.Counts,
         summary="Get counts",
         description="""Returns the counts of all tables entities in the system.""",
         response_description="A counts object with hotel, flight, customer, payment, and events counts.",
         operation_id="v0_get_counts",
         tags=["count"],)
def get_count():
    counts = schemas.Counts(
    hotel_count = crud.execute_query_to_dataframe(crud.qc_hco).iat[0,0],
    flight_count = crud.execute_query_to_dataframe(crud.qc_fco).iat[0,0],
    customer_count = crud.execute_query_to_dataframe(crud.qc_cco).iat[0,0],
    payment_count = crud.execute_query_to_dataframe(crud.qc_pco).iat[0,0],
    events_count = crud.execute_query_to_dataframe(crud.qc_eco).iat[0,0]
    )
    return counts
