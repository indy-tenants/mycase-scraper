FROM browserless/chrome

USER root

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install software-properties-common python3.9 python3-pip  -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER blessuser

COPY . /usr/src/mycase-scraper
WORKDIR /usr/src/mycase-scraper

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python3", "./mycase_scraper/scraper.py"]
