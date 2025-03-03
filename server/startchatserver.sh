#!/bin/sh

if [ -n "$OCP_LOGIN_TOKEN" ] && [ -n "$OCP_API_SERVER" ]; then  
  oc login --token=$OCP_LOGIN_TOKEN --server=$OCP_API_SERVER  --insecure-skip-tls-verify=true
fi

python chatUIServer.py

