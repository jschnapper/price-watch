# Price watch

A quick python script to watch amazon prices for certain deals that utilizes AWS (EC2 and SES) for FREE

### How to watch an item
1. Add the Amazon item url with an appropriate key-name to the `urls` dictionary
2. Add the same key-name to the `deal` dictionary with a value that matches the most you would want to pay for the item
3. Verify your email on AWS SES
4. Add this verified email under `SENDER` in `send_email`
5. Replace `recipient@example.com` with the email you want to receive the notification (does not have to be verified)
6. Spin up an EC2 (can be free tier, t2.micro) and add the `price_watch.py` to it
7. Start up a `virtualenv` or `venv` in the ec2 and `pip install beautifulsoup4`, `pip install requests`, and `pip install boto3`, and then start the virtual environment
8. I used linux screen to keep the script running even when I'm not on the instance, which is why I use `time.sleep([val])` in `main`, but you can opt for CRON and take out the `time.sleep`
9. Adjust the frequency of how often you'd like to scan the item price
10. Run the script! 
