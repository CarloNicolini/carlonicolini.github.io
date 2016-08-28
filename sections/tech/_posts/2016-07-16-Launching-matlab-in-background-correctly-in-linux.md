---
layout: post
title: Launching-matlab-in-background-correctly-in-linux
date: 2016-07-16
categories: tech
---

You want to launch Matlab for a very long script and then disconnect your remote terminal, and when back, not finding bad surprise.

Suppose your script `myeigenvalues.m` is:

    {% highlight matlab %}
    A=randn(1000);
    X=eig(A);
    save{% endhighlight %}
    

1. Create a helper script `helper_myegeinvalues.m` that launches `myeigenvalues.m` script but surrounded by a **try-catch** block like this:

    {% highlight matlab %}
    try
        myeigenvalues;
    catch ME
        disp(ME);
        disp('SCRIPT CRASHED');
        exit;
    end
    disp('SCRIPT RUNNED SUCCESSFULLY');{% endhighlight %}

The try-catch block is needed to avoid leaving Matlab open in idle status if an error occurred once launched as background process.

2. Create another helper bash-script file `helper_myegeinvalues.sh` that runs the script `helper_myegeinvalues.m`

    {% highlight sh %}
    matlab -nodisplay -nodesktop -nosplash -r "helper_myegeinvalues"{% endhighlight %}

3. Make the `helper_myegeinvalues.sh` file executable by issuing 

    {% highlight sh %}
    chmod +x helper_myegeinvalues.sh{% endhighlight %}

4. Run the `helper_myegeinvalues.sh` as a **nohup** command and collect all the output into the file `stdout.txt`

    {% highlight sh %}
    nohup ./helper_myegeinvalues.sh > stdout.txt &{% endhighlight %}

5. You can now leave the process run and stay happy.