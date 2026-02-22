# %%
from __future__ import annotations

from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict, Field



# %%

class Hotel(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    hotel_id : str
    name : str
    city : str
    country : str
    stars : int

class Booking_Item(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    hotel: List[Hotel] = Field(default_factory=list)
    total_bookings : float
    unique_customers : float
    total_revenue : float
    average_revenue : float

# %%
class Booking_revenue_status(BaseModel):
    model_config = ConfigDict(from_attributes = True, arbitrary_types_allowed=True)
    hotel : List[Hotel] = Field(default_factory=list)
    status : str
    total_amount : float
    bookings_count : int
    price_strategy : str

class Hotel_prices(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    price_per_night : float

# %%
class Inventory(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    date : date
    allotment_total : int
    allotment_sold : int
    occupancy_rate : float

class Occupancy_rate(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    hotel : List[Hotel] = Field(default_factory=list)
    inventory: List[Inventory] = Field(default_factory=list)
    price_per_night: List[Hotel_prices] = Field(default_factory=list)

# %%
class Revenue_performance(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    hotel: List[Hotel] = Field(default_factory=list)
    daily_bookings: int
    total_amount: int
    average_amount: float
    revenue_segment: str


class Optimized_revenue(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    hotel: List[Hotel] = Field(default_factory=list)
    inventory: List[Inventory] = Field(default_factory=list)
    available: int
    price_per_night: List[Hotel_prices] = Field(default_factory=list)
    recommendation: str
    suggested_price_eur: float

# %%
# FLIGHTS 

class Flight(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    origin : str
    destination : str

class Aircraft(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    model : str
    manufacturer : str
    seats_total : int

class Flight_overview(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    flights : List[Flight] = Field(default_factory=list)
    aircraft : List[Aircraft] = Field(default_factory=list)

# %%
class Flight_prices(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    flights: List[Flight] = Field(default_factory=list)
    min_price : float
    max_price : float
    median_price : float
    popularity_rank : int

class Flight_popularity(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    flights: List[Flight] = Field(default_factory=list)
    cabin_class : str
    average_customer_spend : float  
    popularity_rank : int

class Flight_inventory(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    flight_id: str
    total_fare : int
    average_fare_for_flight : float
    seats_available : int
    average_fare_for_destination : float

# %%
# PAYMENTS

# %%
class Customer(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    customer_id : int
    loyalty_id : str

class Customer_payments(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    value_segment : str
    customer: List[Customer] = Field(default_factory=list)
    average_spent : float
    segment_revenue : float

# %%
class Payments_overview(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    payment_month : int
    method : str
    customer: List[Customer] = Field(default_factory=list)
    booking_type : str
    total_bookings : int
    total_payments : float
    failure_rate_percent : float

# %%
# CUSTOMERS

# %%
class Customer_hotel_preferences(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    hotel : List[Hotel] = Field(default_factory=list)
    customer_id : int
    booking_type : str
    total_bookings : int
    total_revenue : int

class Customer_flight_preferences(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    destination : str
    total_flights : int
    max_price : float
    median_price : float
    customer: List[Customer] = Field(default_factory=list)
    
class Customer_flight_class(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    destination_trips : int
    destination : str
    average_price : float
    customer: List[Customer] = Field(default_factory=list)
    cabin_class : str

# %%
# EVENTS

# %%
class Events(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    event_name : str
    city : str
    customers_assistance : int
    average_price : float
    total_revenue : int

# %%

class Counts(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    hotel_count : int
    flight_count : int
    customer_count : int
    payment_count : int
    events_count : int

# %%
