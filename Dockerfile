FROM faucet/python3

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN python3 -m pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "users.py" ]