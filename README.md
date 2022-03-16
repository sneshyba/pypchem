# pypchem
Python code for use in courses in Physical Chemistry

## Installation Notes
Configuring pip on a Manjaro vm. This follows https://jupyterhub.readthedocs.io/en/stable/quickstart.html.

	sudo pacman -Syu python-pip
	sudo pacman -S npm
	sudo npm install -g configurable-http-proxy

Configuring jupyterhub and jupyter notebook on a Manjaro vm. This follows https://jupyterhub.readthedocs.io/en/stable/quickstart.html.

Then, jupyter and nbgrader installation. But we need a compatible set of versions. Here's one

	python version 3.10.2
	nbgrader version 0.6.2 
	jupyter notebook version 6.0.0
	jupyter client version 5.3.1
	jupyter traitlets version 4.3.3

How do we implement this?

	python -m pip install jupyterhub
	python -m pip install jupyter --version==6.4.4
	python -m pip install jupyter-client==5.3.1
	python -m pip install notebook
	python -m pip install jupyterlab
	python -m pip install jupyter-client==6.1.12
	jupyter nbextension install --system --py nbgrader --version==0.6.2
	jupyter nbextension enable nbgrader --py
	
	
Here are ways to query the versions:

	python --version
	jupyter --version
	jupyterhub --version
	nbgrader --version
	jupyter nbextension list
	

These are old notes:

	python -m pip install jupyterhub
	python -m pip install jupyterlab notebook

	sudo python -m pip install nbgrader
	sudo nbextension enable --system --py nbgrader
	sudo jupyter nbextension install --system --py nbgrader
	sudo jupyter nbextension enable --system --py nbgrader
	sudo jupyter serverextension enable --system --py nbgrader

	sudo python -m pip install nbgrader
	sudo python -m pip install --upgrade jupyterthemes
	sudo python -m pip install jupyter-client==6.1.12
	sudo jupyter nbextension install --py nbgrader
	sudo jupyter nbextension install --user —-py nbgrader
	sudo jupyter nbextension enable nbgrader --py
	sudo jupyter nbextension enable —-user —-py nbgrader
	sudo jupyter nbextension enable --system --py nbgrader
	sudo jupyter serverextension enable --user --py nbgrader
	sudo jupyter serverextension enable --system --py nbgrader
	jupyter nbextension list

Setting up nbgrader in an instructor’s account. Create a file, nbgrader_config.py, in two places: the folder where the code will reside, and in the .jupyter folder in the home directory. Contents:

	c = get_config()
	c.CourseDirectory.course_id = “pchem”
	c.CourseDirectory.root = '/home/instructor/pchem’
	c.Exchange.root = '/srv/nbgrader/exchange'
	c.NbGrader.logfile = ‘/home/instructor/pchem/logfile.txt'
	c.ClearSolutions.code_stub = {"python": "# Your code here \n"}

Also set the the folder '/srv/nbgrader/exchange' to wide-open privileges. 

Setting up nbgrader in a student’s account

After logging on as a student (not sure how much of this is essential); it’s useful to pack this into a script file, like addstudent_nbgrader, if there are a lot of students.

	jupyter nbextension install --user --py nbgrader
	jupyter nbextension enable nbgrader --user --py
	jupyter serverextension enable --user --py nbgrader
	jupyter nbextension disable --user create_assignment/main
	jupyter nbextension disable --user formgrader/main --section=tree
	jupyter nbextension disable --user course_list/main --section=tree
	jupyter nbextension list


Configuring python -- using "sudo" imports for all users (I think)

	sudo python -m pip install numpy
	sudo python -m pip install scipy
	sudo python -m pip install sympy
	sudo python -m pip install matplotlib
	sudo python -m pip install pint
	sudo python -m pip install tables
	sudo python -m pip install h5io
	sudo python -m pip install h5py


To enable a jupyterhub user (instructor) to be admin

	sudo usermod -a -G jupyter_admins instructor


To add admin privileges for a user

	sudo nano /etc/jupyterhub/jupyterhub_config.py


Processing of student work when you don’t want to use the nbgrader mechanism

	1)	In the course folder (say pchem), create a folder called “submitted”.
	2)	In submitted, create a folder called “studentx”.
	3)	Copy the student-submitted zip file “assignment1” into the studentx folder, and unzip it. Now there should be a folder called assignment1.
	4)	In jupyter, navigate into submitted/studentx/assignment1/ and open the .ipynb file there (presumably, “assignment1.ipynb”), assign grades & make comments.
	5)	In formgrader/Manage Assignments, press the “Generate Feedback” button. Now there should appear a new folder in pchem called “feedback”. The feedback for each student should be there.


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


