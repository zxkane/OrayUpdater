OrayUpdater
===========

Automatically register current IP to dynamic DNS service hosted on oray.com


## Usage

* Specify your hostname, username and password via program arguments

> usage: updater.py [-h] [-f] [-s HOSTNAME] [-u USERNAME] [-p PASSWORD]
> 
> 
> optional arguments:
> 
>   -h, --help            *show this help message and exit*
>   
>   -f, --force           *force updating IP address of ddns*
>   
>   -s HOSTNAME, --hostname HOSTNAME
>                         *hostname to be updated*
>                         
>   -u USERNAME, --username USERNAME
>                         *username of Oray.com*
>                         
>   -p PASSWORD, --password PASSWORD
>                         *password of Oray.com*

* Create a **.orayupdater.cfg** file in your home directory, write your hostname, username and password in it. For example,

```cfg
[OrayUpdator]
Username=myname
Hostname=myname.gicp.net
Password=passw0rd
```