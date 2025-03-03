#!/bin/sh

if [ -n "$OCP_LOGIN_TOKEN" ] && [ -n "$OCP_API_SERVER" ]; then     
  oc login --token=$OCP_LOGIN_TOKEN --server=$OCP_API_SERVER  --insecure-skip-tls-verify=true
fi

touch /tmp/apiserver.log
nohup python apiserver.py >> /tmp/apiserver.log 2>&1 &
tail -f /tmp/apiserver.log

#if [ -z "$PORT" ]; then
#    PORT=5001
#fi
#if [ -z "$WORKERS" ]; then
#    WORKERS=1
#fi
#if [ -z "$TIMEOUT" ]; then
#    TIMEOUT=300
#fi
#gunicorn -w $WORKERS --timeout $TIMEOUT  -b 0.0.0.0:$PORT apiserver:app


