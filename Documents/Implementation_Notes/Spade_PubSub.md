# Implementation of Spade PubSub

we are using ```Prosody``` which is a ```XMPP``` server .
We used ```ejabberd``` but it seems it lacks support where ```Prosody``` is tested with ```Spade python```.


- [Implementation of Spade PubSub](#implementation-of-spade-pubsub)
  - [Installing](#installing)
  - [Configuration](#configuration)
  - [adding users](#adding-users)
  - [User as Admin](#user-as-admin)



## Installing
```shell
  sudo apt update 
  sudo apt install prosody
```





## Configuration 

1. Go to ```/etc/prosody/prosody.cfg.lua```
2. add the localhost binding 
```lua
Host "*"
    c2s_interface = "127.0.0.1"
    s2s_interface = "127.0.0.1"
```
3. add Pubsub components :

```lua
Component "pubsub.localhost" "pubsub"
```
4. add cert and key 

```shell
  # generate key and cert 
  cd /etc/prosody/certs
  openssl genrsa -out localhost.key 2048
  openssl req -x509 -nodes -days 365 -new -key localhost.key -out localhost.crt -subj "/CN=localhost"
  # allow permission
  sudo chown root:prosody /etc/prosody/certs/localhost.key
  sudo chmod 640 /etc/prosody/certs/localhost.key
```

5. restart the prosodyctl 

```shell
  sudo systemctl restart prosodyctl
  # check status 
  sudo systemctl status prosodyctl
```

## adding users 
In order to add users we can use the prosodyctl shell 

1. start the shell 
```shell
  prosodyctl shell
```
2. create user inside the shell 

```shell
user:create("username@localhost","password")
```
3. check user is added  inside the shell 

```shell
  user:list("localhost")
```

## User as Admin 

In order to enable PubSub on the Agents , the Agents must be admin on the XMPP server . 

1. go to ```/etc/prosody/prosody.cfg.lua```

2. find the ``` admin: { }```
3. inside this field add the users 
```lua
  admins = {"username@localhost"}
```
