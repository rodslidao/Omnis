FROM sherensberk/python_opencv:0.0.1
WORKDIR /usr/src/app/omis-lib
COPY ./omnis-lib ./
RUN pip install -r requirements.txt
RUN pip install .
WORKDIR /usr/src/app
RUN rm -rf ./omis-lib


