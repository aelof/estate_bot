# Get python
FROM python:3

# Choose folder instance
WORKDIR /usr/src/app

# Install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy folder instance to container
COPY . .

# Run bootstrap scripts
CMD [ "python", "./bootstrap.py" ]

# Run application
CMD [ "python", "./main.py" ]