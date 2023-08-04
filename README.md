# pypchem
Python code for use in courses in Physical Chemistry

## Installation Notes
*Configuring pip on a Manjaro vm*  
This follows https://jupyterhub.readthedocs.io/en/stable/quickstart.html.

	sudo pacman -Syu python-pip
	sudo pacman -S npm
	sudo npm install -g configurable-http-proxy


*Jupyter and nbgrader installation*  
Some of these might be redundant.

	sudo python -m pip install jupyterhub
	python -m pip install notebook
	python -m pip install jupyter 
	sudo python -m pip install jupyter-client==7.0.0 # This changes the jupyter_client version
	jupyter nbextension install --system --py nbgrader
	jupyter nbextension enable nbgrader --py
	sudo jupyter serverextension enable --sys-prefix --py nbgrader
	sudo jupyter serverextension enable --system --py nbgrader
	
	(python -m pip install jupyterlab will install jupyterlab, but I don't recommend doing so if one always wants the "classic" interface)



*Querying the installed versions*  

	python --version
	jupyter --version
	jupyterhub --version
	nbgrader --version
	jupyter nbextension list


*Version compatibility*  
The following versions work -- many are default. I don't understand why the students' notebook version is different from the instructor's version, but it doesn't seem to hurt anything.

	[instructor@instructor-virtualbox ~]$ jupyter --version
	Selected Jupyter core packages...
	IPython          : 7.32.0
	ipykernel        : 6.4.2
	ipywidgets       : 7.6.5
	jupyter_client   : 7.0.0
	jupyter_core     : 4.9.2
	jupyter_server   : 1.15.4
	jupyterlab       : 3.3.2
	nbclient         : 0.6.1
	nbconvert        : 7.0.0
	nbformat         : 5.2.0
	notebook         : 6.4.12
	qtconsole        : 5.2.2
	traitlets        : 5.3.0

	[student4@instructor-virtualbox ~]$ jupyter --version
	Selected Jupyter core packages...
	IPython          : 7.32.0
	ipykernel        : 6.4.2
	ipywidgets       : 7.6.5
	jupyter_client   : 6.1.12
	jupyter_core     : 4.9.2
	jupyter_server   : not installed
	jupyterlab       : not installed
	nbclient         : not installed
	nbconvert        : 5.6.1
	nbformat         : 5.2.0
	notebook         : 6.4.10
	qtconsole        : 5.2.2
	traitlets        : 5.3.0

Other configuration settings can be show using

	pip list jupyter-console

*Tailoring the ngrader configuration*  
I used commands like the following to tailor these:

	pip install jupyter-client==7.0.0
	pip install traitlets==5.3.0
	pip install nbgrader==0.7.0
	
Here, it seems a key setting is the nbgrader version. 


*Configuring python*  
Using "sudo" imports for all users.

	sudo python -m pip install numpy
	sudo python -m pip install scipy
	sudo python -m pip install sympy
	sudo python -m pip install matplotlib
	sudo python -m pip install pint
	sudo python -m pip install tables
	sudo python -m pip install h5io
	sudo python -m pip install h5py


*The exchange directory*  
Before setting up nbgrader, it is necessary to loosen the protections of folder '/srv/nbgrader/', '/srv/nbgrader/exchange', and '/srv/nbgrader/exchange/pchem'. I set them to wide-open (777) privileges. 


*Setting up nbgrader in the instructor’s account*  

Create a file, nbgrader_config.py, in two places: the folder where the code will reside, and in the .jupyter folder in the home directory. Contents of both should be something along the lines of

	c = get_config()
	c.CourseDirectory.course_id = “pchem”
	c.CourseDirectory.root = '/home/instructor/pchem’
	c.Exchange.root = '/srv/nbgrader/exchange'
	c.NbGrader.logfile = ‘/home/instructor/pchem/logfile.txt'
	c.ClearSolutions.code_stub = {"python": "# Your code here \n"}

The "course" tab in nbgrader doesn't seem to do much, so to disable it one can use

	jupyter nbextension disable --user course_list/main --section=tree


*Setting up nbgrader in student accounts*  
Students need an account on the system,

	sudo useradd student1 -m; sudo passwd student1

 or
	ns=studentname
 	sudo useradd $ns -m; echo "$ns:$ns" | sudo chpasswd
	
Then, after logging on (e.g., as student1), it's good to get rid of unwanted nbgrader options,

	jupyter nbextension disable --user create_assignment/main
	jupyter nbextension disable --user formgrader/main --section=tree
	jupyter nbextension disable --user course_list/main --section=tree

or, to do these last three all at once, 

	jupyter nbextension disable --user create_assignment/main; jupyter nbextension disable --user formgrader/main --section=tree; jupyter nbextension disable --user course_list/main --section=tree


It seems that student accounts do not require .jupyter/nbgrader_config.py. 

*To expand the hard drive space on a virtual machine*

1. Turn off the VM. 
1. In the Virtualbox GUI, go to File>Virtual Media Manager, select the hard disk to resize, and under “Attributes” adjust the “Size” slider (or type desired size into text box on right). Click “Apply.”
1. Restart the VM and log on. Open the GParted gui, and select the partition to be resized (typically /dev/sda1) using Menu bar- Partition>Resize/Move>. Then type the new size, or slide the bar on top to set the target size for the partition. Click “Resize” to apply the partitioning changes, from the menu bar, click Edit > Apply All Operations.
1. A warning about potential data loss willl show- Click ‘okay”, then you can close gparted.

*Processing student work with nbgrader using the regular nbgrader pipeline*  
Go to *Formgrader/Collect*, click on the number underneath *Submissions* (if non-zero), and follow the instructions provided.


*Processing student work with nbgrader without using the regular nbgrader pipeline*  
If an instructor wants to manually bring student work into the nbgrader environment (instead of using the regular nbgrader pipeline),

1. In the course folder (say pchem), create a folder called “submitted”.
1. In submitted, create a folder called “studentx”.
1. Copy the student-submitted zip file “assignment1” into the studentx folder, and unzip it. Now there should be a folder called assignment1.
1. In jupyter, navigate into submitted/studentx/assignment1/ and open the .ipynb file there (presumably, “assignment1.ipynb”), assign grades & make comments.
1. In formgrader/Manage Assignments, press the “Generate Feedback” button. Now there should appear a new folder in pchem called “feedback”. The feedback for each student should be there.

## VM-specific notes

*Getting the VM*  
1. Download “pchem” from the google folder and de-compress it. This will take almost 25 Gbytes, temporarily; the decompressed file alone is ~16 Gbytes. 
2. Install VirtualBox (https://www.virtualbox.org/)
3. Use VirtualBox to launch the VM: In the VirtualBox GUI, go to Tools/Add, navigate to the pchem folder you just decompressed, and double-click *pchem.vdbox*. A big green arrow launches it.


*Launching jupyter, etc., from the terminal window*  
Once the VM is booted, you’ll find yourself in a Manjaro operating system. Open a terminal window (icon at the top), and enter

	jupyter notebook 
	
to launch just a notebook; a Firefox window with a jupyter notebook screen should open up. When you're done, press the *quit* button of any browser windows associated with Juptyter. If the terminal window used to launch jupyter notebook is still busy, ctrl-C a couple of times. 

To launch Jupyterhub, open a terminal window (icon at the top), and enter

	jupyterhub 
	
This will launch a single-user version of jupyterhub. You'll have to open a Firefox window and enter localhost to get into it.


*Running Jupyterhub with port forwarding*  
If instead of wanting a single-user jupyter notebook, you want a multi-user jupyterhub environment available on your host machine:
1. With the VM shut down, go to settings/Network/Advanced/Port Forwarding, and enter 8000 in Host Port and Guest Port.
2. Use VirtualBox to launch the VM as before.
3. Once the VM is booted, open a terminal window (icon at the top) as before, but this time enter 

	sudo jupyterhub -f /etc/jupyterhub/jupyterhub_config.py 

4. Unlike the *jupyter notebook* command, *sudo jupyterhub* doesn't launch a browser window automatically. Instead, on a browser of the laptop or desktop that is *hosting* your VM, enter http://localhost:8000 (or just localhost:8000). You can log on as instructor, or student1.
5. When you're done, press the *quit* button of any browser windows associated with Juptyter. Back on the VM, the terminal window used to launch jupyterhub will still be busy, so you have to enter ctrl-C a couple of times to quit out of it.

*As related note, a way to make Jupyterhub on a VM avaliable without needing the VM's IP address* 
In virtualbox, go to Settings/Network/Adaptor 1/, then select *NAT* in the dropdown *Attached to:*. Selecting *Advanced*, click on *Port Forwarding*. In the *Port Forwarding Rules* window, the *Name* can be anything you make up, the *Protocol* should be *TCP*, the *Host Port* should be a number that the host doesn't use (like 9000), and the *Guest Port* should be 8000. Now, suppose your host has IP address 10.150.1.100.  Then to get to the VM’s Jupyterhub, you’d enter into the browser window something like this:

	10.150.1.100:9000/

or 

	http://10.150.1.100:9000/



*Running Jupyterhub with bridge (autoboot not previously set up)*
The following steps are for when autoboot has not already been set up; you'll see that there's a lot in common with the autoboot process, but with two additional steps.
1. With the VM shut down, go to settings/Network and choose *Bridged Adapter* to attach to (this overrides the default, NAT). For a name, choose the local Wifi (or enp0s25 on the 7610). Then boot the VM and make a note of its IP address, using e.g. the command "ip a" in a terminal window. This address will appear something like *inet w.x.y.z/...* (but with numbers for w, x, y, and z). 
1. Launch Jupyterhub from a VM terminal window using
	sudo jupyterhub -f /etc/jupyterhub/jupyterhub_config.py --ip=0.0.0.0
4. On a browser of a machine on the LAN, enter http://w.x.y.z:8000/hub/login, where the letters correspond to the VM's IP address you made a note of before, and follow the prompts. 
5. When you're done, press the *quit* button of any browser windows associated with Juptyter. 
6. Go back to the VM window where you launched Jupyterhub and enter ctrl-C a couple of times, to stop Jupyterhub.


*Setting up autoboot*  
In the VM, one adds the line *@reboot path-to-jupyterhub -f /etc/jupyterhub/jupyterhub_config.py --ip=0.0.0.0* to the boot file, using crontab:

	sudo EDITOR=nano crontab -e


*Running Jupyterhub with bridge (autoboot previously set up)*  
The following steps are for when autoboot has already been set up; for system commands that do that setting up, see the next item.
1. With the VM shut down, go to settings/Network and choose *Bridged Adapter* to attach to (this overrides the default, NAT). For a name, choose the local Wifi (or enp0s25 on the 7610). Then boot the VM and make a note of its IP address, using e.g. the command "ip a" in a terminal window. This address will appear something like *inet w.x.y.z/...* (but with numbers for w, x, y, and z). 
4. On a browser of a machine on the LAN, enter http://w.x.y.z:8000/hub/login, where the letters correspond to the VM's IP address you made a note of before, and follow the prompts. 
5. When you're done, press the *quit* button of any browser windows associated with Juptyter. 


*Shutting down the VM*  
Find an icon that looks like a circle with a vertical line through part of it, on the upper right; it's just to the left of the time/date. Click that and choose *Shutdown*.


*Launching the VM as a detached process*  
This is based on https://superuser.com/questions/135498/run-virtualbox-in-background-without-a-window. After logging on to the host, cd to the folder that contains the .vdi, and issue this command (here, assuming pchem.vdi):

	VBoxHeadless --startvm pchem &
	
The "&" makes this a detached process, so one can log off th host and the VM will keep running. 

*Shutting down a detached VM*  
If Jupyterhub is running, then log on to it, open a terminal window from there, and say  

 	sudo shutdown now

If Jupyterhub is not available, then one can shut down the "headless" process using top on the host.


## Other notes

*Getting the IP address as a shell variable*  

	myIP=$(ip a s enp0s3 | awk '/inet / {print$2}'|awk -F'/' '{print $1}')  
	echo $myIP


*Installing Mayavi*  
Probably not all the below are necessary.

	python -m pip install vtk
	python -m pip install mayavi
	python -m pip install ipywidgets
	python -m pip install ipyevents
	jupyter nbextension install --py mayavi --user


*Trying to making the scrolling “natural” (this didn’t work, however)*  
This follows https://www.reddit.com/r/ManjaroLinux/comments/bagymb/natural_scrolling_in_manjaro_i3/. Edit /etc/X11/xorg.conf.d/00-touchpad.conf file, adding 

	Section "InputClass"                 
		...
		Option "Natural Scrolling" "true"
		...
	EndSection


*Setting the time*  
This follows https://archived.forum.manjaro.org/t/howto-get-your-time-timezone-right-using-manjaro-windows-dual-boot/89359

	sudo timedatectl set-local-rtc 0
	sudo systemctl enable --now systemd-timesyncd
	find /usr/share/zoneinfo/ -maxdepth 1 -type d
	ls /usr/share/zoneinfo/America
	sudo ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime


*Auto-starting jupyter notebook on login*  
This follows https://arcolinux.com/how-to-autostart-any-application-on-any-linux-desktop/. Add file jupyter.desktop to ~./config/autostart, containing this:

	[Desktop Entry]
	Type=Application
	Name=jupyter
	Exec=jupyter notebook
	StartupNotify=false
	Terminal=false


*Reporting the version of python from a notebook*  
	from platform import python_version
	print(python_version())


*Before installing virtualbox on Manjaro*  

	uname -r

*Installing virtualbox on Manjaro*  

	sudo pacman -Syu virtualbox

*When the screen locks but can't be unlocked*

	Switch to virtual terminal using Ctrl+Alt+F2
	Log in and execute loginctl unlock-session 3
	Then log out with Ctrl-D
	Switch back to the running session with Ctrl+Alt+F1
