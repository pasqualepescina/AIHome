# Use the base Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy your virtual environment into the container
COPY AIHome /app/AIHome

# Install any additional dependencies, if needed
# RUN pip install package_name
# Install any dependencies your application requires from the virtual environment
#RUN AIhome/Scripts/activate.ps1 /app/AIhome/Scripts/activate.ps1

# Copy your Python code into the container
COPY * /app/
# Copy the 'dag' folder into the container
#COPY dags /app/dags

# Specify the command to run when the container starts
CMD ["python", "dags/dag.py"]