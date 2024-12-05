from flight import Flight
from helper import Queue, Heap

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        self.flights = flights
        self.m = len(flights)
        self.flights_from_city = [[] for _ in range(self.m+1)]
        self.flights_to_city = [[] for _ in range(self.m+1)]
        for flight in flights:
            self.flights_from_city[flight.start_city].append(flight)
            self.flights_to_city[flight.end_city].append(flight)
    
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """

        prev_flight = [None for _ in range(self.m+1)]
        flight_count = [float('inf') for _ in range(self.m+1)]
        least_arrival_time = [float('inf') for _ in range(self.m+1)]

        visited_flights = [False for _ in range(self.m + 1)]
        flight_count[start_city] = 0
        que = Queue()
        for flight in self.flights_from_city[start_city]:
            visited_flights[flight.flight_no] = True
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                que.push(flight.flight_no)

        while not que.is_empty():
            flight_num = que.pop()
            flight = self.flights[flight_num]
            if (flight_count[flight.end_city] > flight_count[flight.start_city] + 1) or (flight_count[flight.end_city] == flight_count[flight.start_city] + 1 and least_arrival_time[flight.end_city] > flight.arrival_time):
                flight_count[flight.end_city] = flight_count[flight.start_city] + 1
                prev_flight[flight.end_city] = flight
                least_arrival_time[flight.end_city] = flight.arrival_time
            for next_flight in self.flights_from_city[flight.end_city]:
                if not visited_flights[next_flight.flight_no] and (next_flight.departure_time >= flight.arrival_time + 20):
                    visited_flights[next_flight.flight_no] = True
                    que.push(next_flight.flight_no)
            
        path = []
        if flight_count[end_city] == float('inf'):
            return path
        curr_city = end_city
        while curr_city != start_city:
            path.append(prev_flight[curr_city])
            curr_city = prev_flight[curr_city].start_city
        path.reverse()
        return path

    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """

        queue = Heap()
        
        if 0 <= start_city <= self.m:
            initial_flights = [
                flight for flight in self.flights_from_city[start_city]
                if flight.departure_time >= t1 and flight.arrival_time <= t2
            ]
        else:
            initial_flights = []
        
        for flight in initial_flights:
            path = [flight]
            queue.push((flight.fare, flight.arrival_time, flight.end_city, path))
        
        if start_city == end_city and t1 <= t2:
            return []
        
        visited = [float('inf')] * (self.m + 1)
        
        while not queue.is_empty():
            total_fare, arrival_time, current_city, path = queue.pop()
            
            if arrival_time > t2:
                continue
            
            if 0 <= current_city <= self.m:
                if total_fare >= visited[current_city]:
                    continue
                visited[current_city] = total_fare
            else:
                continue
            
            if current_city == end_city:
                return path
            
            next_flights = self.flights_from_city[current_city]
            
            for next_flight in next_flights:
                if next_flight.departure_time >= arrival_time + 20:
                    if next_flight.departure_time >= t1 and next_flight.arrival_time <= t2:
                        next_path = path + [next_flight]
                        queue.push((
                            total_fare + next_flight.fare,
                            next_flight.arrival_time,
                            next_flight.end_city,
                            next_path
                        ))
                        
        return []
        
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        heap = Heap()
        
        best_flights = [float('inf')] * (self.m + 1)
        best_fares = [float('inf')] * (self.m + 1)
        best_flights[start_city] = 0
        best_fares[start_city] = 0
        
        for flight in self.flights_from_city[start_city]:
            if flight.departure_time >= t1 and flight.arrival_time <= t2:
                new_num_flights = 1
                new_total_fare = flight.fare
                heap.push((new_num_flights, new_total_fare, flight.end_city, flight.arrival_time, [flight]))
                
                if new_num_flights < best_flights[flight.end_city] or (new_num_flights == best_flights[flight.end_city] and new_total_fare < best_fares[flight.end_city]):
                    best_flights[flight.end_city] = new_num_flights
                    best_fares[flight.end_city] = new_total_fare
        
        if start_city == end_city and t1 <= t2:
            return []
        
        while not heap.is_empty():
            num_flights, total_fare, current_city, arrival_time, path = heap.pop()
            
            if current_city == end_city:
                return path
            
            for next_flight in self.flights_from_city[current_city]:
                if next_flight.departure_time >= arrival_time + 20 and next_flight.arrival_time <= t2:
                    new_num_flights = num_flights + 1
                    new_total_fare = total_fare + next_flight.fare
                    
                    if new_num_flights < best_flights[next_flight.end_city] or (new_num_flights == best_flights[next_flight.end_city] and new_total_fare < best_fares[next_flight.end_city]):
                        best_flights[next_flight.end_city] = new_num_flights
                        best_fares[next_flight.end_city] = new_total_fare
                        new_path = path + [next_flight]
                        heap.push((new_num_flights, new_total_fare, next_flight.end_city, next_flight.arrival_time, new_path))
        
        return []
