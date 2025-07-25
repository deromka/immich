#!/bin/bash

IMMICH_URL="http://192.168.2.54:2283/api"
API_KEY="LMaVxA03VIxImcV2mhMSGVFEmQxpA4cagRmPjw0V35Q"

# Check raw response
curl -s -H "x-api-key: $API_KEY" "$IMMICH_URL/asset"
