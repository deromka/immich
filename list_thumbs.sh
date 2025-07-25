#!/bin/bash

IMMICH_URL="http://192.168.2.54:2283/api"
API_KEY="LMaVxA03VIxImcV2mhMSGVFEmQxpA4cagRmPjw0V35Q"

docker run --rm curlimages/curl:latest \
  curl -s -X GET "$IMMICH_URL/asset" \
  -H "x-api-key: $API_KEY" \
  -H "Accept: application/json" \
  | jq '.[] | select(.originalFileName | contains("-thumbnail.webp")) | {id: .id, fileName: .originalFileName, createdAt: .createdAt}'
