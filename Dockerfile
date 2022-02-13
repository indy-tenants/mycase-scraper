FROM browserless/chrome

# Use root to install dependencies
USER root

RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install python3.9 -y
RUN apt install python3-pip -y
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
RUN update-alternatives --set python /usr/bin/python3.9
RUN python -m pip install --upgrade pip

# Switch back to normal user to run script
USER blessuser
COPY . /usr/src/mycase-scraper
RUN pip install -r /usr/src/mycase-scraper/requirements.txt
RUN /usr/bin/python3.9 /usr/src/mycase-scraper/mycase_scraper/scraper.py
