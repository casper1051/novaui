#!/bin/bash

#So the way to launch this UI and not conflict with BotUI is to simply reroute the wombat_launcher.sh start script
#First we should copy the original script so we can revert back if we want to uninstall

echo "Setting up..."
cd /home/kipr/
cp wombat_launcher.sh wombat_launcher_original.sh

#Now we can write the new launch file. ui.py and start_wifi.sh will be started later
echo "Re-writing /home/kipr/wombat_launcher.sh... Find the original at /home/kipr/wombat_launcher_original.sh"
echo -e "#!/bin/bash \nsudo python3 /home/kipr/ui.py & \n/home/kipr/start_wifi.sh &" > wombat_launcher.sh


#Now we make the ui.py file
echo "Fetching main ui file..."
wget https://raw.githubusercontent.com/casper1051/novaui/refs/heads/main/main.py

#Move to the right file place
echo "Moving..."
rm ui.py #Reinstall to update? Remove files already here
mv main.py ui.py

#Now for make_wifi.sh
echo "Fetching wifi AP creation script..."

#TODO: Make client mode
rm start_wifi.sh
wget https://raw.githubusercontent.com/casper1051/novaui/refs/heads/main/start_wifi.sh


echo "Finished"
