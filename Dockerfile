FROM python:3.10

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update
# Installing Unzip
RUN apt-get install -yqq unzip

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# Set display port as an environment variable
ENV DISPLAY=:99


# RUN apt-get install -y xclip xvfb
# RUN apt-get update && apt-get install -y xclip
# ENV DISPLAY=:99
# RUN nohup bash -c "Xvfb :99 -screen 0 1280x720x16 &"

# Magic happens
RUN apt-get install -y google-chrome-stable
# set work directory
WORKDIR /usr/src/app/
# copy project
COPY . /usr/src/app/
RUN pip install --upgrade pip
# install dependencies
RUN pip install --user --upgrade selenium
RUN pip install --user --upgrade webdriver-manager
RUN pip install --user --upgrade psycopg2
# run app
CMD ["python", "parser_1.py"]