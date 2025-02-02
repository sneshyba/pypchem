#!/usr/bin/env python
# coding: utf-8

# # ScheduledFlows
# 
# ## Overview
# The idea of this module is to create an emissions scenario -- a _schedule_ -- that says how much carbon humans put  into the atmosphere in the past, and make projections about future emissions. 
# 
# ## Mathematical background
# The emissions scenario generated here has the form 
# 
# $$
# \epsilon(t) = {exp(kt) \ \sigma_{down}(t)} \ N   \ \ \ \ \ (1)
# $$
# 
# where $\epsilon$ is understood to be a rate of emission of carbon into the atmosphere -- on a per-year basis -- as a function of time, $t$. Let's take this formula apart piece by piece ...
# 
# ### Exponential growth in the early years
# The first term, $exp(kt)$ describes exponential growth. This kind of growth is always parameterized by a growth rate, here given by $k$. Part of your job will be to find a reasonable and defensible range of values for $k$ -- but a reasonable guess is to say that in the last few hundred years, anthropogenic emissions of fossil fuels grew at about the same exponential rate as human population growth, which was roughly $2.5%$ per year, which would correspond to $k=0.025 \ yr^{-1}$. 
# 
# ### Decarbonization by a step-down sigmoid function
# The next term is a step-down sigmoid function, $\sigma_{down}$. This function describes humanity's decarbonization transition. How? Well, it's centered around a transition year, $t_{trans}$. Long before $t_{trans}$), $\sigma_{down}=1$, whereas long after $t_{trans}$), $\sigma_{down}=0$. When the year is exactly the transition year ($t=t_{trans}$), the our sigmoid step-down function takes the value $\sigma_{down}={1\over2}$, which means decarbonization is halfway complete. 
# 
# You might guess that $\sigma_{down}$ requires one more parameter, which concerns how _fast_ the transition occurs. This is specified by a transition time, $\Delta t_{trans}$, which is about the time it takes for $\sigma_{down}$ to get from $0.8$ to $0.2$ (the "80/20" rule). 
# 
# In the example below, we've set $t_{trans}=2035$ and $\Delta t_{trans}=10 \ yr$, but part of your job will be to find a reasonable and defensible range of values for these parameters.
# 
# ### Pegging
# The $N$ in Eq. (1) provides us a way to fix our emissions model so that it's guaranteed to be correct at a least at one year (of our choosing). This is called "pegging." It's convenient to say 
# 
# $$
# N = {\epsilon_o \over {exp(kt_o) \ \sigma_{down}(t_o)}}   \ \ \ \ \ (2)
# $$
# 
# where the pegged year is specified by $t_o$, and the emissions we want to be sure about that year  is specified by $\epsilon_o$. In the example below, we (rather imprecisely) peg the emissions in the year $2020$ to $14 \ GtC/yr$ (so $t_o=2020$ and $\epsilon_o=14 \ GtC/yr$), but part of your job will be to find a reasonable and defensible range of values to peg.
# 
# By the way, with a little mathematical reflection, you'll probably see that this pegging strategy works for any choice of the growth rate, $k$. That's pretty handy because it means that even if we've choose an unrealistic value for $k$, we'll still get the right emission in one particular year -- the pegged year, $t_o$!
# 
# ### Metadata and modularization
# Part of good coding practice is finding ways to save data in a way that is "self-documenting." Like, including the units of your data, or other parameters. Fortunately, the python utility _Pandas_ is very good at saving such data -- so we'll learn a bit about _Pandas_ too.
# 
# Another part of good coding practice is to find ways to re-use code. Here, you'll be doing that using Python _functions_.
# 
# ## Computing skills
# 
# - I can use pandas to write a dataframe to a drive.
# - I can set up functions in python, and am familiar with methodolgies for ensuring they are working.
# 
# 
# ## Climate science skills
# 
# - I can describe how exponential growth is represented mathematically.
# - I can describe how a sigmoid (step) function is represented mathematically.
# - I have a quantitative sense of past carbon emissions.

# In[35]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[36]:


get_ipython().run_line_magic('matplotlib', 'notebook')


# ### The next few cells create a function and tests it. 
# We'll start with the sigmoid _stepup_ function.

# In[37]:


# Define a step-up sigmoid function (from zero to 1) 
def sigmaup(x,center,transitiontime):
  # Generates a sigmoid (smooth step-up) function
  return 1 / (1 + np.exp(-(x-center)*3/transitiontime))


# In[43]:


# Testing the sigma-up function ... first lay out an array of times
t = np.linspace(1980,2100,100)

# Use sigmoid to find y-values for this array
transitionyear = 2040
transitiontime = 10
mysigmaup = sigmaup(t,transitionyear,transitiontime)

# Graph the result
plt.figure()
plt.plot(t,mysigmaup)
plt.xlabel('time (year)')
plt.ylabel('stepup function')
plt.grid()


# ### Pause for analysis
# Take a moment to study the graph you just produced. Does it satisfy the "80/20" rule? What happens if you change $t_{trans}$ and $\Delta t_{trans}$ ... does the curve change appropriately?

# ### Your turn
# Now write (and test) a step-down function.

# In[39]:


### BEGIN SOLUTION 
# Define a step-down sigmoid function (from 1 to 0) 
def sigmadown(x,center,transitiontime):
  # Generates a sigmoid (smooth step-down) function
  return 1 - sigmaup(x,center,transitiontime)
### END SOLUTION


# In[40]:


### BEGIN SOLUTION 
# Use sigmoid to find y-values for this array
transitionyear = 2020
transitiontime = 10
mysigmadown = sigmadown(t,transitionyear,transitiontime)

# Graph the result
plt.figure()
plt.plot(t,mysigmadown)
plt.xlabel('time (year)')
plt.ylabel('stepdown function')
plt.grid()
### END SOLUTION


# ### Evaluating the product of exponential times sigmoid
# Now we're going to check out the form of the function in Eq. (1). Since at the moment, we're really only interested in the shape, we'll pretend $N=1$ (and come back to that later). In the next cell, calculate ${exp(kt) \ \sigma_{down}(t)}$ and graph it. You can use the same exponential and sigmoid functions you've already generated. Name your new variable "myeps".

# In[41]:


### BEGIN SOLUTION
myeps = np.exp*mysigmadown
plt.figure()
plt.plot(t,myeps)
plt.xlabel('time (year)')
plt.grid()
### END SOLUTION


# ### Pause for analysis
# Take a moment to study the graph you just produced. In what year did emissions peak? Was it sooner or later than the transition year, $t_{trans}$? What's the time difference? Just to fix this idea, complete this sentence (in your head): If humanity wanted peak emissions to occur in the year 2050, the sigmoid $t_{trans}$ parameter would need to be:
# 
# 
# 

# 

# ### Getting the right value of $N$

# In[42]:


### BEGIN SOLUTION

eps0 = 14
t0 = 2020
N = eps0/(np.exp(k*t))

### END SOLUTION


# ### Now for the real work: create the emissions scenario
# In the cell below, recreate a scenario

# In[9]:


# Lay out the time period we want to look at
time = np.linspace(1750, 2500, 5000)

# Specify a year that we want to peg the emissions, and the emissions that year
t0 = 2020
eps0 = 14 # This includes actual emissions plus land use changes

# Also specify a year that corresponds to peak emissions
peakemissionsyear = 2040

# The sigmoid function's transion year is 10 years later
transitionyear = peakemissionsyear + 10

# Now for the parameter that controls how fast the transition will occur
transitiontime = 30

# Specify how fast emissions have historically grown 
growthrate = 2.5/100

# Implementing Eq. (1)
first_term = np.exp(time*growthrate)*sigmadown(time,transitionyear,transitiontime)
second_term = eps0/(np.exp(t0*growthrate)*sigmadown(t0,transitionyear,transitiontime))
emissions = first_term * second_term


# In[14]:


# Check the results
plt.figure()
plt.plot(time,emissions)
plt.grid()
plt.xlim(time[0],time[-1])
plt.title('Annual Anthropogenic Emissions')
plt.xlabel('year')
plt.ylabel('GtC/year')


# ### The time lag
# Using the tools for zooming in, verify that the year of peak emissions happened in about the year you expected.

# ### Saving as a _Pandas_ file

# In[12]:


# Create an empty dataframe
Emissionsdf = pd.DataFrame()

# Add the columns we want to it
Emissionsdf.insert(loc=0, column='time', value=time)
Emissionsdf.insert(loc=1, column='emissions', value=emissions)
display(Emissionsdf)

# Assemble a name for our file
filename = 'Peak_emissions_'+str(peakemissionsyear)+'.txt'
print(filename)

# To save it to a drive, change to True
Iwanttosave = False
if Iwanttosave:
  Emissionsdf.to_csv(filename,index=False)


# ### Your turn
# Modify the preceding cell so that the file name has some indication of the transition time as well as the peak emissions year.
# 
# 
