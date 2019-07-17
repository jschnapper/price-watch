#!/home/ec2-user/pricewatch/bin/python3
from bs4 import BeautifulSoup
import boto3
from botocore.exceptions import ClientError
import requests
import time

# Item URL on Amazon
urls = {
  "kindle": "https://www.amazon.com/All-new-Kindle-Paperwhite-Waterproof-Storage/dp/B07CXG6C9W?smid=ATVPDKIKX0DER&pf_rd_p=c6ec48a9-d8ac-42b3-b63e-12257d2e8873&pf_rd_r=HQQGTN8E06V4NW8BB4Z9"
}
# Price to watch for
deal = {
  "kindle": 10000
}

def send_email(item, price, url):
  # Replace sender@example.com with your "From" address.
  # This address must be verified with Amazon SES.
  SENDER = "price watch <sender@example.com>"

  # Replace recipient@example.com with a "To" address. If your account 
  # is still in the sandbox, this address must be verified.
  RECIPIENT = "recipient@example.com"

  # Specify a configuration set. If you do not want to use a configuration
  # set, comment the following variable, and the 
  # ConfigurationSetName=CONFIGURATION_SET argument below.
  CONFIGURATION_SET = "price_watch"

  # If necessary, replace us-east-1 with the AWS Region you're using for Amazon SES.
  AWS_REGION = "us-east-1"

  # The subject line for the email.
  SUBJECT = item + " price drop to $" + str(price)

  # The email body for recipients with non-HTML email clients.
  BODY_TEXT = (item + " price dropped to $" + str(price) + " check the link: " + url)
              
  # The HTML body of the email.
  BODY_HTML = """<html>
  <head></head>
  <body>
    <h1{item} price has dropped to {price}</h1>
    <p>Check it out <a href="{url}">here</a></p>
  </body>
  </html>
              """.format(item=item, price=price, url=url)            

  # The character encoding for the email.
  CHARSET = "UTF-8"

  # Create a new SES resource and specify a region.
  client = boto3.client('ses',region_name=AWS_REGION)

  # Try to send the email.
  try:
      #Provide the contents of the email.
      response = client.send_email(
          Destination={
              'ToAddresses': [
                  RECIPIENT,
              ],
          },
          Message={
              'Body': {
                  'Html': {
                      'Charset': CHARSET,
                      'Data': BODY_HTML,
                  },
                  'Text': {
                      'Charset': CHARSET,
                      'Data': BODY_TEXT,
                  },
              },
              'Subject': {
                  'Charset': CHARSET,
                  'Data': SUBJECT,
              },
          },
          Source=SENDER,
          # If you are not using a configuration set, comment or delete the
          # following line
          ConfigurationSetName=CONFIGURATION_SET,
      )
  # Display an error if something goes wrong.	
  except ClientError as e:
      print(e.response['Error']['Message'])
  else:
      print("Email sent! Message ID:"),
      print(response['MessageId'])

def watch_price():
  for item, url in urls.items():
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    is_deal = soup.find(id="priceblock_dealprice")
    if (is_deal):
      price = float(soup.find(id="priceblock_dealprice").contents[0][1:])
      if (price < deal[item]):
        send_email(item, price, url)
        print("email sent")

# Checks every hour
def main():
  while True:
    watch_price()
    # Change if desired, value in seconds
    time.sleep(3600)

if __name__ == "__main__":
  main()


