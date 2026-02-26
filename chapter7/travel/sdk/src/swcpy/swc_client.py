import logging
from typing import List, Type, TypeVar

import backoff
import httpx

try:
    from . import swc_config as config
    from .schemas import (
        Booking_Item,
        Booking_revenue_status,
        Counts,
        Customer_flight_class,
        Customer_flight_preferences,
        Customer_hotel_preferences,
        Customer_payments,
        Events,
        Flight_inventory,
        Flight_overview,
        Flight_popularity,
        Flight_prices,
        Occupancy_rate,
        Optimized_revenue,
        Payments_overview,
        Revenue_performance,
    )
except ImportError:
    import swc_config as config
    from schemas import (
        Booking_Item,
        Booking_revenue_status,
        Counts,
        Customer_flight_class,
        Customer_flight_preferences,
        Customer_hotel_preferences,
        Customer_payments,
        Events,
        Flight_inventory,
        Flight_overview,
        Flight_popularity,
        Flight_prices,
        Occupancy_rate,
        Optimized_revenue,
        Payments_overview,
        Revenue_performance,
    )

logger = logging.getLogger(__name__)
T = TypeVar("T")


class SWCClient:
    """Interacts with the Sports World Central API."""

    HEALTH_CHECK_ENDPOINT = "/"
    LIST_BOOKING_ITEM_ENDPOINT = "/v0/booking_items/"
    LIST_BOOKING_REVENUE_STATUS_ENDPOINT = "/v0/booking_revenue_status/"
    LIST_BOOKING_OCCUPANCY_RATE_ENDPOINT = "/v0/booking_occupancy_rate/"
    LIST_REVENUE_PERFORMANCE_ENDPOINT = "/v0/revenue_performance/"
    LIST_OPTIMIZED_REVENUE_ENDPOINT = "/v0/optimized_revenue/"
    LIST_FLIGHT_OVERVIEW_ENDPOINT = "/v0/flight_overview/"
    LIST_FLIGHT_PRICES_ENDPOINT = "/v0/flight_prices/"
    LIST_FLIGHT_POPULARITY_ENDPOINT = "/v0/flight_popularity/"
    LIST_FLIGHT_INVENTORY_ENDPOINT = "/v0/flight_inventory/"
    LIST_CUSTOMER_PAYMENTS_ENDPOINT = "/v0/customer_payments/"
    LIST_PAYMENTS_OVERVIEW_ENDPOINT = "/v0/payments_overview/"
    LIST_CUSTOMER_HOTEL_PREFERENCES_ENDPOINT = "/v0/customer_hotel_preferences/"
    LIST_CUSTOMER_FLIGHT_PREFERENCES_ENDPOINT = "/v0/customer_flight_preferences/"
    LIST_CUSTOMER_FLIGHT_CLASS_ENDPOINT = "/v0/customer_flight_class/"
    LIST_EVENTS_ENDPOINT = "/v0/events/"
    GET_COUNTS_ENDPOINT = "/v0/counts/"

    BULK_FILE_BASE_URL = (
        "https://raw.githubusercontent.com/[github ID]"
        + "/portfolio-project/main/bulk/"
    )

    def __init__(self, input_config: config.SWCConfig):
        self.swc_base_url = input_config.swc_base_url
        self.backoff = input_config.swc_backoff
        self.backoff_max_time = input_config.swc_backoff_max_time
        self.bulk_file_format = input_config.swc_bulk_file_format

        self.BULK_FILE_NAMES = {
            "booking_items": "booking_items_data",
            "booking_revenue_status": "booking_revenue_status_data",
            "booking_occupancy_rate": "booking_occupancy_rate_data",
            "revenue_performance": "revenue_performance_data",
            "optimized_revenue": "optimized_revenue_data",
            "flight_overview": "flight_overview_data",
            "flight_prices": "flight_prices_data",
            "flight_popularity": "flight_popularity_data",
            "flight_inventory": "flight_inventory_data",
            "customer_payments": "customer_payments_data",
            "payments_overview": "payments_overview_data",
            "customer_hotel_preferences": "customer_hotel_preferences_data",
            "customer_flight_preferences": "customer_flight_preferences_data",
            "customer_flight_class": "customer_flight_class_data",
            "events": "events_data",
        }

        if self.backoff:
            self.call_api = backoff.on_exception(
                wait_gen=backoff.expo,
                exception=(httpx.RequestError, httpx.HTTPStatusError),
                max_time=self.backoff_max_time,
                jitter=backoff.random_jitter,
            )(self.call_api)

        suffix = ".parquet" if self.bulk_file_format.lower() == "parquet" else ".csv"
        self.BULK_FILE_NAMES = {
            key: f"{value}{suffix}" for key, value in self.BULK_FILE_NAMES.items()
        }

    def call_api(self, api_endpoint: str, api_params: dict = None) -> httpx.Response:
        """Makes an API call and raises on HTTP errors."""
        if api_params:
            api_params = {k: v for k, v in api_params.items() if v is not None}

        try:
            with httpx.Client(base_url=self.swc_base_url) as client:
                response = client.get(api_endpoint, params=api_params)
                response.raise_for_status()
                return response
        except httpx.HTTPStatusError as e:
            logger.error(
                "HTTP status error occurred: %s %s",
                e.response.status_code,
                e.response.text,
            )
            raise
        except httpx.RequestError as e:
            logger.error("Request error occurred: %s", str(e))
            raise

    def _list_resource(self, endpoint: str, schema: Type[T], **params) -> List[T]:
        response = self.call_api(endpoint, params)
        payload = response.json()
        return [schema(**item) for item in payload]

    def _get_bulk_file(self, resource_key: str) -> bytes:
        file_path = self.BULK_FILE_BASE_URL + self.BULK_FILE_NAMES[resource_key]
        response = httpx.get(file_path, follow_redirects=True)
        response.raise_for_status()
        return response.content

    def get_health_check(self) -> httpx.Response:
        return self.call_api(self.HEALTH_CHECK_ENDPOINT)

    def list_booking_items(
        self, status: str = "CONFIRMED", limit: int = 100
    ) -> List[Booking_Item]:
        return self._list_resource(
            self.LIST_BOOKING_ITEM_ENDPOINT,
            Booking_Item,
            status=status,
            limit=limit,
        )

    def list_booking_revenue_status(
        self, limit: int = 100
    ) -> List[Booking_revenue_status]:
        return self._list_resource(
            self.LIST_BOOKING_REVENUE_STATUS_ENDPOINT,
            Booking_revenue_status,
            limit=limit,
        )

    def list_booking_occupancy_rate(self, limit: int = 100) -> List[Occupancy_rate]:
        return self._list_resource(
            self.LIST_BOOKING_OCCUPANCY_RATE_ENDPOINT,
            Occupancy_rate,
            limit=limit,
        )

    def list_revenue_performance(self, limit: int = 100) -> List[Revenue_performance]:
        return self._list_resource(
            self.LIST_REVENUE_PERFORMANCE_ENDPOINT,
            Revenue_performance,
            limit=limit,
        )

    def list_optimized_revenue(self, limit: int = 100) -> List[Optimized_revenue]:
        return self._list_resource(
            self.LIST_OPTIMIZED_REVENUE_ENDPOINT,
            Optimized_revenue,
            limit=limit,
        )

    def list_flight_overview(self, limit: int = 100) -> List[Flight_overview]:
        return self._list_resource(
            self.LIST_FLIGHT_OVERVIEW_ENDPOINT,
            Flight_overview,
            limit=limit,
        )

    def list_flight_prices(self, limit: int = 100) -> List[Flight_prices]:
        return self._list_resource(
            self.LIST_FLIGHT_PRICES_ENDPOINT,
            Flight_prices,
            limit=limit,
        )

    def list_flight_popularity(self, limit: int = 100) -> List[Flight_popularity]:
        return self._list_resource(
            self.LIST_FLIGHT_POPULARITY_ENDPOINT,
            Flight_popularity,
            limit=limit,
        )

    def list_flight_inventory(self, limit: int = 100) -> List[Flight_inventory]:
        return self._list_resource(
            self.LIST_FLIGHT_INVENTORY_ENDPOINT,
            Flight_inventory,
            limit=limit,
        )

    def list_customer_payments(self, limit: int = 100) -> List[Customer_payments]:
        return self._list_resource(
            self.LIST_CUSTOMER_PAYMENTS_ENDPOINT,
            Customer_payments,
            limit=limit,
        )

    def list_payments_overview(self, limit: int = 100) -> List[Payments_overview]:
        return self._list_resource(
            self.LIST_PAYMENTS_OVERVIEW_ENDPOINT,
            Payments_overview,
            limit=limit,
        )

    def list_customer_hotel_preferences(
        self, limit: int = 100
    ) -> List[Customer_hotel_preferences]:
        return self._list_resource(
            self.LIST_CUSTOMER_HOTEL_PREFERENCES_ENDPOINT,
            Customer_hotel_preferences,
            limit=limit,
        )

    def list_customer_flight_preferences(
        self, limit: int = 100
    ) -> List[Customer_flight_preferences]:
        return self._list_resource(
            self.LIST_CUSTOMER_FLIGHT_PREFERENCES_ENDPOINT,
            Customer_flight_preferences,
            limit=limit,
        )

    def list_customer_flight_class(self, limit: int = 100) -> List[Customer_flight_class]:
        return self._list_resource(
            self.LIST_CUSTOMER_FLIGHT_CLASS_ENDPOINT,
            Customer_flight_class,
            limit=limit,
        )

    def list_events(self, limit: int = 100) -> List[Events]:
        return self._list_resource(self.LIST_EVENTS_ENDPOINT, Events, limit=limit)

    def get_counts(self) -> Counts:
        response = self.call_api(self.GET_COUNTS_ENDPOINT)
        return Counts(**response.json())

    def get_bulk_booking_items_file(self) -> bytes:
        return self._get_bulk_file("booking_items")

    def get_bulk_booking_revenue_status_file(self) -> bytes:
        return self._get_bulk_file("booking_revenue_status")

    def get_bulk_booking_occupancy_rate_file(self) -> bytes:
        return self._get_bulk_file("booking_occupancy_rate")

    def get_bulk_revenue_performance_file(self) -> bytes:
        return self._get_bulk_file("revenue_performance")

    def get_bulk_optimized_revenue_file(self) -> bytes:
        return self._get_bulk_file("optimized_revenue")

    def get_bulk_flight_overview_file(self) -> bytes:
        return self._get_bulk_file("flight_overview")

    def get_bulk_flight_prices_file(self) -> bytes:
        return self._get_bulk_file("flight_prices")

    def get_bulk_flight_popularity_file(self) -> bytes:
        return self._get_bulk_file("flight_popularity")

    def get_bulk_flight_inventory_file(self) -> bytes:
        return self._get_bulk_file("flight_inventory")

    def get_bulk_customer_payments_file(self) -> bytes:
        return self._get_bulk_file("customer_payments")

    def get_bulk_payments_overview_file(self) -> bytes:
        return self._get_bulk_file("payments_overview")

    def get_bulk_customer_hotel_preferences_file(self) -> bytes:
        return self._get_bulk_file("customer_hotel_preferences")

    def get_bulk_customer_flight_preferences_file(self) -> bytes:
        return self._get_bulk_file("customer_flight_preferences")

    def get_bulk_customer_flight_class_file(self) -> bytes:
        return self._get_bulk_file("customer_flight_class")

    def get_bulk_events_file(self) -> bytes:
        return self._get_bulk_file("events")
