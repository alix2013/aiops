#!/bin/sh
/bin/ollama serve > /tmp/llm.log 2>&1 &
sleep 5

if [ -z "$MODELS" ]; then
    echo "==>MODELS env not set,use default" >> /tmp/m.log
    MODELS="mistral neural-chat"
fi
for m in $MODELS; do
    /bin/ollama pull $m
done

tail -f /tmp/llm.log
