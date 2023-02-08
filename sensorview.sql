CREATE VIEW monitoring_sensordata_view AS 
select d.id AS data_id,
h.host, m.metric, d.data, d.created_at
from ((monitoring_sensordata d
join monitoring_sensorhost h on ((d.host_id = h.id)))
join monitoring_sensormetric m on ((d.metric_id = m.id)));