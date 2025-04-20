FROM python:3.10

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Expose port and run Flask
CMD ["flask", "run", "--host=0.0.0.0"]
