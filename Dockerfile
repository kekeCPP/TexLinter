FROM python:3.10

RUN useradd --create-home temp_user

WORKDIR /home/app

# COPY requirements.txt

# RUN pip install --no-cache-dir -r requirements.txt

USER temp_user

COPY . .

CMD ["bash"]