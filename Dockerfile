FROM continuumio/miniconda3:22.11.1
# Copy files into image
COPY . /structures_ws
# Define working directory
WORKDIR /structures_ws
# TODO Load conda environment
# RUN conda create -n test python=3.10.10
RUN conda env create -n django -f environment.yml
# Add conda activate line to .bashrc
RUN echo "conda activate django" >> ~/.bashrc
# Update shell command (used by RUN)
SHELL ["/bin/bash", "-lc"]
# Initialize migrations
RUN python manage.py makemigrations
# Make migrations
RUN python manage.py migrate
# Create superuser (admin)
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=damiano.orcid@mailinator.com
RUN python manage.py createsuperuser --noinput
## Fill database
#RUN python manage.py runscript update_files
# Expose port 8000
EXPOSE 8000
# TODO Define command to be executed on activation
CMD ["/bin/bash", "-lc", "python manage.py runserver 0.0.0.0:8000"]
