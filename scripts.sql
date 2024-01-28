select count(1)
from yellow_taxi_trips ytd
where lpep_pickup_datetime::date = '2019-09-18'
;


select lpep_pickup_datetime::date, max(trip_distance)
from yellow_taxi_data ytd
group by 1
order by 2 desc
;


select z."Borough", sum(total_amount) as sm
from yellow_taxi_data ytd
join zones z 
    on ytd."PULocationID" = z."LocationID" 
where lpep_pickup_datetime::date = '2019-09-18'
group by 1
having sum(total_amount) >=50000
;


select z1."Zone", z2."Zone", max(tip_amount) as max_tip
from yellow_taxi_data ytd
join zones z1
    on ytd."PULocationID" = z1."LocationID"
    and z1."Zone" = 'Astoria'
join zones z2
    on ytd."DOLocationID" = z2."LocationID"
where date_trunc('month', lpep_pickup_datetime::date) = '2019-09-01'
group by 1,2
order by max_tip desc
;
