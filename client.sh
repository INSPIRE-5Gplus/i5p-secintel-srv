#!/usr/bin/env bash


curl -X GET -H "Content-Type: application/json" http://127.0.0.1:4455/monitoring_action/a
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:4455/monitoring_action

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:4455/monitoring_action/a -d'{"action_id" : "a","action_type" : "MONITOR_IDS","element_ip" : "10.55.0.13:8080","notify_violation" : "policy_manager", "debug" : "True"}'

curl -X DELETE -H "Content-Type: application/json" http://127.0.0.1:4455/monitoring_action/a



#ACTING AS IDS:

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:4455/telemetry/a -d'{"id":1234, "trust" : 0}'

