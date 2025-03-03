# Use an official Python runtime as a parent image
FROM python:3.10-slim
# Set the working directory in the container to /app
WORKDIR /app

RUN pip install  --no-cache-dir  slack_sdk requests python-dotenv 

COPY apiclient.py /app
COPY slack.env /app
COPY slack_aibot.py /app

ENV PATH="$PATH:/app"

## for openshift permission
RUN chgrp -R 0 /app
# # Set the permissions so that all users can read and write.
RUN chmod -R g=u /app
#
# Run app.py when the container launches
CMD ["python", "slack_aibot.py"]
#CMD ["/bin/sh", "startapiserver.sh"]


