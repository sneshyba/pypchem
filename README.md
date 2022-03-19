# pypchem
Python code for use in courses in Physical Chemistry

## Installation Notes
Configuring pip on a Manjaro vm. This follows https://jupyterhub.readthedocs.io/en/stable/quickstart.html.

	sudo pacman -Syu python-pip
	sudo pacman -S npm
	sudo npm install -g configurable-http-proxy

Configuring jupyterhub and jupyter notebook on a Manjaro vm. This follows https://jupyterhub.readthedocs.io/en/stable/quickstart.html.

Then, jupyter and nbgrader installation. Some of these are redundant

	sudo python -m pip install jupyterhub
	python -m pip install notebook
	python -m pip install jupyterlab
	python -m pip install jupyter 
	sudo python -m pip install jupyter-client==6.1.12 # This changes the jupyter_client version
	jupyter nbextension install --system --py nbgrader
	jupyter nbextension enable nbgrader --py
	sudo jupyter serverextension enable --sys-prefix --py nbgrader
	sudo jupyter serverextension enable --system --py nbgrader

Regardless, it's useful to know the various ways to query the versions:

	python --version
	jupyter --version
	jupyterhub --version
	nbgrader --version
	jupyter nbextension list

We need a compatible set of versions. The following works (although I don't understand why the notebook version is different for instructor than for the student).

	[instructor@instructor-virtualbox ~]$ jupyter --version
	Selected Jupyter core packages...
	IPython          : 7.32.0
	ipykernel        : 6.4.2
	ipywidgets       : 7.6.5
	jupyter_client   : 6.1.12
	jupyter_core     : 4.9.2
	jupyter_server   : 1.15.4
	jupyterlab       : 3.3.2
	nbclient         : not installed
	nbconvert        : 5.6.1
	nbformat         : 5.2.0
	notebook         : 6.0.0
	qtconsole        : 5.2.2
	traitlets        : 4.3.3

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
	traitlets        : 4.3.3

Setting up nbgrader in the instructor’s account: Create a file, nbgrader_config.py, in two places: the folder where the code will reside, and in the .jupyter folder in the home directory. Contents:

	c = get_config()
	c.CourseDirectory.course_id = “pchem”
	c.CourseDirectory.root = '/home/instructor/pchem’
	c.Exchange.root = '/srv/nbgrader/exchange'
	c.NbGrader.logfile = ‘/home/instructor/pchem/logfile.txt'
	c.ClearSolutions.code_stub = {"python": "# Your code here \n"}

Also set the the folder '/srv/nbgrader/', '/srv/nbgrader/exchange', and '/srv/nbgrader/exchange/pchem', to wide-open privileges. 

Setting up nbgrader in a student’s account. It appears that the student just needs to be added as a system user, e.g.,

	sudo useradd student3 -m
	sudo passwd student3

It seems that .jupyter/nbgrader_config.py is not needed. However, after logging on as a student, it's good to get rid of unwanted nbgrader options,

	jupyter nbextension disable --user create_assignment/main
	jupyter nbextension disable --user formgrader/main --section=tree
	jupyter nbextension disable --user course_list/main --section=tree

Configuring python -- using "sudo" imports for all users

	sudo python -m pip install numpy
	sudo python -m pip install scipy
	sudo python -m pip install sympy
	sudo python -m pip install matplotlib
	sudo python -m pip install pint
	sudo python -m pip install tables
	sudo python -m pip install h5io
	sudo python -m pip install h5py

Processing of student work when you don’t want to use the nbgrader mechanism

1. In the course folder (say pchem), create a folder called “submitted”.
1. In submitted, create a folder called “studentx”.
1. Copy the student-submitted zip file “assignment1” into the studentx folder, and unzip it. Now there should be a folder called assignment1.
1. In jupyter, navigate into submitted/studentx/assignment1/ and open the .ipynb file there (presumably, “assignment1.ipynb”), assign grades & make comments.
1. In formgrader/Manage Assignments, press the “Generate Feedback” button. Now there should appear a new folder in pchem called “feedback”. The feedback for each student should be there.

Installing Mayavi. Probably not all the below are necessary.

	python -m pip install vtk
	python -m pip install mayavi
	python -m pip install ipywidgets
	python -m pip install ipyevents
	jupyter nbextension install --py mayavi --user

Launching a notebook from a terminal window

	jupyter notebook

Launching jupyterhub from a terminal window

	jupyterhub

Setting the time. This follows https://archived.forum.manjaro.org/t/howto-get-your-time-timezone-right-using-manjaro-windows-dual-boot/89359

	sudo timedatectl set-local-rtc 0
	sudo systemctl enable --now systemd-timesyncd
	find /usr/share/zoneinfo/ -maxdepth 1 -type d
	ls /usr/share/zoneinfo/America
	sudo ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

Auto-starting jupyter notebook. This follows https://arcolinux.com/how-to-autostart-any-application-on-any-linux-desktop/. Add file jupyter.desktop to ~./config/autostart, containing this:

	[Desktop Entry]
	Type=Application
	Name=jupyter
	Exec=jupyter notebook
	StartupNotify=false
	Terminal=false

Trying to making the scrolling “natural” (this didn’t work, however). This follows https://www.reddit.com/r/ManjaroLinux/comments/bagymb/natural_scrolling_in_manjaro_i3/. Edit /etc/X11/xorg.conf.d/00-touchpad.conf file, adding 

	Section "InputClass"                 
		...
		Option "Natural Scrolling" "true"
		...
	EndSection

Reporting the version of python from a notebook

	from platform import python_version
	print(python_version())

## Usage notes

### Getting the VM up and running on your laptop

1. Download “pchem” from the google folder and de-compress it. This will take almost 25 Gbytes, temporarily; the decompressed file alone is ~16 Gbytes. 
2. Install VirtualBox (https://www.virtualbox.org/)

### Running a single-user Jupyter Notebook 
1. Use VirtualBox to launch the VM: In the VirtualBox GUI, go to Tools/Add, navigate to the pchem folder you just decompressed, and double-click *pchem.vdbox*. A big green arrow launches it.
2. Once the VM is booted, you’ll find yourself in a Manjaro operating system. Open a terminal window (icon at the top), and enter *jupyter notebook*. That should open up a Firefox window with a jupyter notebook screen. 
3. When you're done, press the *quit* button of any browser windows associated with Juptyter. If the terminal window used to launch jupyter notebook is still busy, ctrl-C a couple of times. 

### Running Jupyterhub with port forwarding
If instead of wanting a single-user jupyter notebook, you want a multi-user jupyterhub environment available on your host machine:
1. With the VM shut down, go to settings/Network/Advanced/Port Forwarding, and enter 8000 in Host Port and Guest Port.
2. Use VirtualBox to launch the VM as before.
3. Once the VM is booted, open a terminal window (icon at the top) as before, but this time enter *sudo jupyterhub -f /etc/jupyterhub/jupyterhub_config.py*. 
4. Unlike the *jupyter notebook* command, *sudo jupyterhub* doesn't launch a browser window automatically. Instead, on a browser of the laptop or desktop that is *hosting* your VM, enter http://localhost:8000 (or just localhost:8000). You can log on as instructor, or student1.
5. When you're done, press the *quit* button of any browser windows associated with Juptyter. Back on the VM, the terminal window used to launch jupyterhub will still be busy, so you have to enter ctrl-C a couple of times to quit out of it.

### Running Jupyterhub with bridge (launched from the terminal)
If instead of a multi-user jupyterhub environment available on your host machine, you want it on a local area network:
1. With the VM shut down, go to settings/Network and choose *Bridged Adapter* to attach to (this overrides the default, NAT). For a name, choose the local Wifi and enter 8000 in Host Port and Guest Port.
3. Boot the VM and find out its IP address, using e.g. the command "ip a" in a terminal window. This address will appear something like this (but with numbers for w, x, y, and z):
	inet w.x.y.z/...
2. Now run jupyterhub:
	sudo jupyterhub -f /etc/jupyterhub/jupyterhub_config.py --ip=0.0.0.0
7. On a browser of a machine on the LAN, enter http://w.x.y.z:8000/hub/login. Now you can log on to jupyter.
8. When you're done, press the *quit* button of any browser windows associated with Juptyter. Back on the VM, the terminal window used to launch jupyterhub will still be busy, so you have to enter ctrl-C a couple of times to quit out of it.

### Running Jupyterhub with bridge (launched on boot)
1. Just like step 1 with launching from the terminal: with the VM shut down, choose *Bridged Adapter* to attach to, etc.
2. On the VM, add *@reboot path-to-jupyterhub -f /etc/jupyterhub/jupyterhub_config.py --ip=0.0.0.0* to the boot file, using crontab:
	sudo EDITOR=nano crontab -e
7. On a browser of a machine on the LAN, enter http://w.x.y.z:8000/hub/login, where the letters correspond to the VM's IP address (see previous item). Now you can log on to jupyter.
8. When you're done, press the *quit* button of any browser windows associated with Juptyter. 

### Shutting down the VM
Find an icon that looks like a circle with a vertical line through part of it, on the upper right; it's just to the left of the time/date. Click that and choose *Shutdown*.

### Getting the IP address as a shell variable
myIP=$(ip a s enp0s3 | awk '/inet / {print$2}'|awk -F'/' '{print $1}')  
echo $myIP

