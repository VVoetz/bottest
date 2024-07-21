import schedule
import time
import aex

def my_action():
    # Define the action to perform
    print("Performing action at", time.strftime("%Y-%m-%d %H:%M:%S"))
    aex.get_winners_losers()

# Schedule the action to run at a specific time
schedule.every().day.at("13:38").do(my_action)  # Example: Run at 10:00 AM every day

# Run the scheduler loop
while True:
    schedule.run_pending()
    time.sleep(1)  # Optional: Adjust the sleep time as needed to control the frequency of checking for scheduled tasks
