FROM python:3.10

# RUN useradd --create-home --shell /bin/bash temp_user
RUN useradd --create-home temp_user

WORKDIR /home/app

# COPY requirements.txt

# RUN pip install --no-cache-dir -r requirements.txt

USER temp_user

COPY . .

# ENTRYPOINT [ "./app/main.py" ]
CMD ["bash"]