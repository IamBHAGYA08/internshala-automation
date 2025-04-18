# Step 1: Use the official Python image as the base image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements.txt into the container
COPY requirements.txt /app/

# Step 4: Install the dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the entire project into the container
COPY . /app/

# Step 6: Expose the port the app runs on
EXPOSE 5000

# Step 7: Define the command to run the app
CMD ["python", "run.py"]
