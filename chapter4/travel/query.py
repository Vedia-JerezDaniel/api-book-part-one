
class Booking:
    
    def revenue(status):
    # Status: PENDING_PAYMENT, TICKETED, CANCELLED, CONFIRMED
        query = """
        SELECT h.hotel_id, h.name, h.city, h.country,
            COUNT(DISTINCT b.booking_id) as total_bookings,
            COUNT(DISTINCT b.customer_id) as unique_customers,
            SUM(b.total_amount) as total_revenue,
            ROUND(AVG(b.total_amount), 2) as average_revenue
        FROM travel.hotels h
        LEFT JOIN travel.bookings b ON h.hotel_id = b.hotel_id
            AND b.status = %(status)s
            and b.booking_type = 'HOTEL'
        GROUP BY h.hotel_id, h.name, h.city, h.country
        ORDER BY total_revenue DESC
        """

        return query
    
    def revenue_by_status():
        query = """
            WITH daily_prices AS (
            SELECT 
                hp.hotel_id,
                AVG(hp.price_per_night) as avg_daily_price_eur
            FROM travel.hotel_prices hp
            GROUP BY hp.hotel_id
            ),
            daily_bookings AS (
                SELECT 
                    b.hotel_id, b.status, 
                    COUNT(*) as bookings_count,
                    AVG(b.total_amount) as avg_price_per_night_eur
                FROM travel.bookings b
                GROUP BY b.hotel_id, b.status
            )
            SELECT 
                h.name, h.city, db.status,
                dp.avg_daily_price_eur as listed_price,
                db.avg_price_per_night_eur as total_amount,
                db.bookings_count,
                CASE 
                    WHEN db.avg_price_per_night_eur > dp.avg_daily_price_eur * 1.1
                        THEN 'PREMIUM_BOOKING'
                    WHEN db.avg_price_per_night_eur < dp.avg_daily_price_eur * 0.9
                        THEN 'DISCOUNTED'
                    ELSE 'MARKET_RATE'
                END as pricing_strategy,
                ROUND((db.avg_price_per_night_eur - dp.avg_daily_price_eur) / dp.avg_daily_price_eur * 100, 2) 
                    as price_variance_percent
            FROM daily_prices dp
            JOIN daily_bookings db ON dp.hotel_id = db.hotel_id 
            JOIN travel.hotels h ON dp.hotel_id = h.hotel_id
            ORDER BY h.name DESC
        """

        return query

    def occupancy_rate():
        query = """
        SELECT 
            h.hotel_id,
            h.name,
            h.city,
            i.date,
            i.allotment_total,
            i.allotment_sold,
            ROUND(i.allotment_sold::DECIMAL / i.allotment_total * 100, 2) as occupancy_rate,
            hp.price_per_night as price_per_night,
            AVG(i.allotment_sold) OVER (
                PARTITION BY h.hotel_id 
                ORDER BY i.date 
                ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING
            ) as avg_last_3_days,
            LAG(i.allotment_sold) OVER (
                PARTITION BY h.hotel_id 
                ORDER BY i.date
            ) as prev_day_sold,
            CASE 
                WHEN LAG(i.allotment_sold) OVER (
                    PARTITION BY h.hotel_id 
                    ORDER BY i.date
                ) > 0
                THEN ROUND(
                    (i.allotment_sold - LAG(i.allotment_sold) OVER (
                        PARTITION BY h.hotel_id 
                        ORDER BY i.date
                    )) / LAG(i.allotment_sold) OVER (
                        PARTITION BY h.hotel_id 
                        ORDER BY i.date
                    )::DECIMAL * 100, 
                    2
                )
                ELSE NULL
            END as daily_growth_percent    
        FROM travel.inventory i
        JOIN travel.hotels h ON i.hotel_id = h.hotel_id
        LEFT JOIN travel.hotel_prices hp ON i.hotel_id = hp.hotel_id 
            AND i.date = hp.date
        group by h.city,h.hotel_id,i.date,i.allotment_total,i.allotment_sold,hp.price_per_night
        ORDER BY h.hotel_id, i.date
        """

        return query
    

    def revenue_performance(status):
    # Status: PENDING_PAYMENT, TICKETED, CANCELLED, CONFIRMED
        query = """
        WITH daily_revenue AS (
            SELECT 
                b.hotel_id,
                COUNT(b.booking_id) as daily_bookings,
                SUM(b.total_amount) as total_amount,
                AVG(b.total_amount) as average_amount
            FROM travel.bookings as b
            WHERE b.status = %(status)s
            GROUP BY b.hotel_id
            ),
            hotel_summary AS (
                SELECT 
                    h.hotel_id,
                    h.name,
                    h.city,
                    h.stars
                FROM travel.hotels h
                GROUP BY h.hotel_id, h.name, h.city, h.stars
            ),
            ranked_hotels AS (
                SELECT *,
                    ROW_NUMBER() OVER (ORDER BY total_amount DESC) as revenue_rank,
                    percent_rank() OVER (ORDER BY total_amount) as revenue_percentage
                FROM hotel_summary h
                left join daily_revenue dr ON h.hotel_id = dr.hotel_id
            )
        SELECT *,
            CASE 
                WHEN revenue_percentage >= 0.8 THEN 'TOP_20%'
                WHEN revenue_percentage >= 0.5 THEN 'MIDDLE_50%'
                ELSE 'BOTTOM_30%'
            END as revenue_segment
        FROM ranked_hotels
        ORDER BY revenue_rank
        """

        return query

    def optimized_revenue():
        query = """
            SELECT 
            i.hotel_id,
            h.name,
            i.date,
            i.allotment_total,
            i.allotment_sold,
            (i.allotment_total - i.allotment_sold) as available,
            hp.price_per_night ,
            CASE 
                WHEN (i.allotment_total - i.allotment_sold) <= 2 
                    THEN 'INCREASE PRICE +20%'
                WHEN (i.allotment_total - i.allotment_sold) >= 10
                    THEN 'SPECIAL OFFER -15%'
                WHEN (i.allotment_total - i.allotment_sold) = i.allotment_total 
                    THEN 'LAST BOOKING -30%'
                ELSE 'SAME PRICE'
            END as recommendation,
            CASE 
                WHEN (i.allotment_total - i.allotment_sold) <= 2 
                    THEN ROUND(hp.price_per_night * 1.2 , 2)
                WHEN (i.allotment_total - i.allotment_sold) >= 10
                    THEN ROUND(hp.price_per_night * 0.85 , 2)
                WHEN (i.allotment_total - i.allotment_sold) = i.allotment_total 
                    THEN ROUND(hp.price_per_night * 0.7 , 2)
                ELSE ROUND(hp.price_per_night , 2)
            END as suggested_price_eur,
            ROUND(
                CASE 
                    WHEN (i.allotment_total - i.allotment_sold) <= 2 
                        THEN hp.price_per_night * 1.2 * (i.allotment_total - i.allotment_sold)
                    WHEN (i.allotment_total - i.allotment_sold) >= 10
                        THEN hp.price_per_night * 0.85 * (i.allotment_total - i.allotment_sold)
                    WHEN (i.allotment_total - i.allotment_sold) = i.allotment_total 
                        THEN hp.price_per_night * 0.7 * (i.allotment_total - i.allotment_sold)
                    ELSE hp.price_per_night * (i.allotment_total - i.allotment_sold)
                END , 
                2
            ) as potential_revenue_eur
        FROM travel.inventory i
        JOIN travel.hotels h ON i.hotel_id = h.hotel_id
        LEFT JOIN travel.hotel_prices hp ON i.hotel_id = hp.hotel_id 
        ORDER BY i.date, h.name
        """

        return query
    
class Flights:
    def flights_overview():
        query = """
        SELECT 
            f.origin,
            f.destination,
            a.model,
            a.manufacturer,
            a.seats_total
        FROM travel.flights f
        LEFT JOIN travel.aircraft a ON f.aircraft_code = a.aircraft_code
        ORDER BY f.departure_ts
        """

        return query
    
    def flight_prices():
        query = """
        SELECT 
    f.origin,
    f.destination,
    COUNT(DISTINCT f.flight_id) as total_flights,
    MIN(p.total_fare) as min_price,
        MAX(p.total_fare) as max_price,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_fare) as median_price,
        ROW_NUMBER() OVER (ORDER BY COUNT(DISTINCT f.flight_id) DESC) as popularity_rank
    FROM travel.flights f
    JOIN travel.booking_items b ON f.flight_id = b.flight_id
    JOIN travel.prices p ON p.price_id = b.price_id 
    GROUP BY  f.origin, f.destination
    order by popularity_rank, median_price
        """

        return query
    
    def flight_popularity():
        query = """
        WITH customer_route_preferences AS (
        SELECT 
        b.cabin_class as cabin_class, 
        f.origin,
        f.destination,
        COUNT(DISTINCT f.flight_id) as flights_taken,
        AVG(p.total_fare) as avg_spent
        FROM travel.booking_items b
        JOIN travel.flights f ON b.flight_id = f.flight_id
        LEFT JOIN travel.prices p ON p.price_id = b.price_id
        GROUP BY f.origin, f.destination, b.cabin_class 
    ),
        route_popularity AS (
            SELECT 
                origin, 
                destination,
                cabin_class,
                SUM(flights_taken) as total_flights_taken,
                AVG(avg_spent) as avg_customer_spend,
                ROW_NUMBER() OVER (ORDER BY SUM(flights_taken) DESC) as booking_rank
            FROM customer_route_preferences
            GROUP BY origin, destination, cabin_class
        )
        SELECT 
            rp.origin,
            rp.destination, rp.cabin_class,
            avg(rp.avg_customer_spend) as average_customer_spend,
            avg(rp.booking_rank) as popularity_rank
        FROM route_popularity rp
        LEFT JOIN customer_route_preferences crp ON rp.origin = crp.origin 
            AND rp.destination = crp.destination
        group by rp.origin , rp.destination, rp.cabin_class
        """

        return query
        
    def flight_inventory():
        query = """
        WITH inventory_status AS (
        SELECT 
            f.flight_id, f.origin, f.destination, p.inventory_id, p.price_id, 
            f.flight_number,
            f.departure_ts,
            fi.fare_family_id,
            fi.seats_available,
            AVG(p.total_fare) as total_fare,
            round(AVG(p.total_fare) OVER (PARTITION BY f.flight_id),2) as average_fare_for_flight,
            round(AVG(p.total_fare) OVER (PARTITION BY f.destination),2) as average_fare_for_destination
        FROM travel.flights f
        JOIN travel.flight_inventory fi ON f.flight_id = fi.flight_id
        LEFT JOIN travel.prices p ON fi.inventory_id = p.inventory_id
        GROUP BY f.flight_id, f.flight_number, f.departure_ts, 
                fi.fare_family_id, fi.seats_available, p.total_fare, p.inventory_id, p.price_id 
        )
        SELECT 
            ia.flight_id, ia.inventory_id, ia.price_id,
            ia.origin,
            ia.destination, ia.total_fare,
            ia.average_fare_for_flight, sum(ia.seats_available) seats_available, 
            ia.average_fare_for_destination, 
            SUM(CASE WHEN total_fare < average_fare_for_flight THEN 1 ELSE 0 END) 
                as below_avg_price,
            SUM(CASE WHEN total_fare > average_fare_for_flight THEN 1 ELSE 0 END) 
                as above_avg_price,
            ROUND(
                SUM(CASE WHEN total_fare < average_fare_for_flight THEN 1 ELSE 0 END)::DECIMAL 
                / COUNT(DISTINCT ia.flight_id)*10, 2) as percent_below_avg
        FROM inventory_status as ia
        GROUP BY ia.flight_id, ia.total_fare, ia.average_fare_for_flight,
        ia.average_fare_for_destination,ia.origin,
        ia.destination,  ia.inventory_id, ia.price_id
        """

        return query
    
class Payments:
    def customer_payments():
        query = """
        WITH customer_spending AS (
        SELECT 
            c.customer_id,
            c.loyalty_id ,
            COUNT(DISTINCT p.payment_id) as total_payments,
            SUM(p.amount) as total_spent_eur,
            AVG(p.amount) as avg_payment_eur
        FROM travel.customers c
		LEFT JOIN travel.payments p ON c.customer_id = p.customer_id
            where p.status = 'CONFIRMED' 
        GROUP BY c.customer_id
        ),
        customer_segments AS (
            SELECT 
                *,
                NTILE(5) OVER (ORDER BY total_spent_eur DESC) as spending_quintile,
                CASE 
                    WHEN total_spent_eur > 1000 THEN 'VIP'
                    WHEN total_spent_eur > 500 THEN 'PREMIUM'
                    WHEN total_spent_eur > 100 THEN 'REGULAR'
                    ELSE 'NEW'
                END as value_segment
            FROM customer_spending
        )
        SELECT 
            value_segment, customer_id, loyalty_id,
            ROUND(AVG(avg_payment_eur), 2) as average_spent,
            ROUND(SUM(total_spent_eur), 2) as segment_revenue,
            ROUND(SUM(total_spent_eur) / SUM(SUM(total_spent_eur)) OVER () * 100, 2) 
                as revenue_percentage
        FROM customer_segments
        GROUP BY value_segment, customer_id, loyalty_id
        ORDER BY segment_revenue DESC
        """

        return query
    
    def payments_overview():
        query = """
        SELECT 
            DATE_PART('month', p.created_at) as payment_month,
            CASE 
                WHEN DATE_PART('month', p.created_at) = 1 THEN 'JANUARY'
                WHEN DATE_PART('month', p.created_at) = 2 THEN 'FEBRUARY'
            END as payment_month,
            p.method, p.customer_id, b.booking_type,
            COUNT(DISTINCT p.payment_id) as total_payments,
            COUNT(DISTINCT b.booking_id) as total_bookings,
            SUM(p.amount) as total_payments,
            SUM(b.total_amount) as total_bookings,
            AVG(DATE_PART('day', p.created_at - b.created_at)) as avg_days_to_pay,
            ROUND(SUM(CASE WHEN p.status = 'FAILED' THEN 1 ELSE 0 END)::DECIMAL 
                / COUNT(*) * 100, 2) as failure_rate_percent
        FROM travel.payments p
        JOIN travel.customers c ON p.customer_id = c.customer_id
        JOIN travel.bookings b ON c.customer_id = b.customer_id 
        GROUP BY DATE_PART('month', p.created_at), p.method, p.customer_id, b.booking_type
        ORDER BY payment_month DESC, total_payments DESC;
        """
        return query
    
    
class Customers:
    def customer_hotel_preferences():
        query = """
        SELECT 
        h.name, h.city, h.country, b.customer_id, b.booking_type, 
            COUNT(DISTINCT b.booking_id) as total_bookings,
            SUM(b.total_amount) as total_revenue
        FROM travel.hotels h
        LEFT JOIN travel.bookings b ON h.hotel_id = b.hotel_id
            AND b.status = 'CONFIRMED'
        GROUP BY 
        h.name, h.city, h.country, b.customer_id, b.booking_type  
        ORDER BY total_revenue DESC
        """
        
        return query

    def customer_flight_preferences():
        query = """
       SELECT 
            f.destination,
            COUNT(DISTINCT f.flight_id) as total_flights,
            MAX(p.total_fare) as max_price,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY total_fare) as median_price,
            b.customer_id, c.loyalty_id
        FROM travel.flights f
        JOIN travel.booking_items b ON f.flight_id = b.flight_id
        JOIN travel.prices p ON p.price_id = b.price_id
        JOIN travel.customers c ON c.customer_id = b.customer_id
        GROUP BY f.destination, b.customer_id, c.loyalty_id
        order by b.customer_id
        """

        return query
    
    def customer_class_flight():
        query = """
        SELECT 
            count(f.destination) as destination_trips, f.destination,
            AVG(p.total_fare) as average_price,
            b.customer_id, b.cabin_class 
        FROM travel.flights f
        JOIN travel.booking_items b ON f.flight_id = b.flight_id
        JOIN travel.prices p ON p.price_id = b.price_id 
        GROUP BY  f.destination, b.customer_id, b.cabin_class 
        order by count desc
        """
        
        return query
    
class Events:
    def events():
        query = """
        select event_name, e.city,
        count(e.customer_id ) as customers_assistance, 
        avg(e.price_event) as average_price,
        sum(e.price_event) as total_revenue
        from travel.events e
        group by e.event_name, city
        """     
        return query