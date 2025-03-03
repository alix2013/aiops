FROM nvidia/cuda:11.7.1-base-ubuntu22.04

RUN apt-get update && apt-get install -y vim podman python3  python3-pip  python3.10-venv \
  wget curl  pciutils procps net-tools
RUN ln -s /usr/bin/python3 /usr/bin/python
# Set the working directory in the container to /app
WORKDIR /app
# Add the current directory contents into the container at /app
#ADD . /app
#COPY requirements.txt /app
# Install any needed packages specified in requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt

#RUN pip install  --no-cache-dir langchain==0.0.327 chromadb==0.4.15 flask-cors flask==2.3.3 \
#  InstructorEmbedding torch huggingface_hub sentence-transformers gradio openai

RUN pip install  --no-cache-dir --default-timeout=300  langchain==0.0.327 chromadb==0.4.15 flask-cors flask==2.3.3 \
  InstructorEmbedding torch==2.0.1 huggingface_hub==0.17.3 sentence-transformers==2.2.2 gradio openai==0.27.10 \
  gunicorn

#RUN pip install  --no-cache-dir --default-timeout=300  langchain==0.1.8 chromadb==0.4.15 flask-cors flask==2.3.3 \
#  InstructorEmbedding torch==2.0.1 huggingface_hub==0.17.3 sentence-transformers==2.2.2 gradio openai==0.27.10
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

# Run app.py when the container launches
#CMD ["python", "chatUIServer.py"]
#
CMD ["/bin/sh", "startapiserver.sh"]




