# Cron JOBS

### How to Add:

1. Open the cron editor:

   ```bash
   crontab -e
   ```

2. Add the following line at the bottom of the cron file to run the `start.bash` script at system boot:

   ```bash
   @reboot /bin/bash /home/pi/Documents/pi-project/src/cron/start.bash
   ```

   Make sure to adjust the file path if necessary (replace `/home/pi` with your actual home directory if different).

3. Save and exit the editor (usually `Ctrl + O`, then `Enter`, followed by `Ctrl + X`).
