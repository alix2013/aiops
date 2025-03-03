# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app
# Add the current directory contents into the container at /app
#ADD . /app
#COPY requirements.txt /app
# Install any needed packages specified in requirements.txt
#RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN pip install  --no-cache-dir langchain chromadb flask-cors flask \
  InstructorEmbedding torch huggingface_hub sentence-transformers gradio openai

COPY chatUIServer.py /app
COPY .env /app
COPY ./DB_Fusion/ /app/DB_Fusion/
COPY llmbase.py /app 
COPY apiserver.py /app 
COPY actiontool.py /app 
COPY startchatserver.sh /app
COPY startapiserver.sh /app
COPY ./oc /app
COPY ./ocAI /app
RUN chmod a+x /app/oc 
RUN chmod a+x /app/ocAI 
RUN ln -s /app/oc /app/kubectl
ENV SENTENCE_TRANSFORMERS_HOME ./cache
ENV PATH="$PATH:/app"
ENV KUBECONFIG=/app/kubeconfig
RUN touch /app/kubeconfig
## for openshift permission
RUN chgrp -R 0 /app
# # Set the permissions so that all users can read and write.
RUN chmod -R g=u /app
#
# Run app.py when the container launches
#CMD ["python", "chatUIServer.py"]
CMD ["/bin/sh", "startapiserver.sh"]


