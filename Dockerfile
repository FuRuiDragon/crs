# init a base image
FROM python:3.10

ENV OPENAI_API_KEY=""
ENV LISTEN_PORT=5000

# update pio to minimize dependency errors
RUN pip install --upgrade pip

# Create app working directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

# run pip to install the dependencies
RUN pip install -r requirements.txt


# Bundle app source
COPY . .

EXPOSE 5000
CMD [ "python3", "app.py","--host=0.0.0.0"]