# Synapse Web Registration
Simple Synapse registration using Python 2.

This application will enable you to control users registering your Synapse server. You may want to create a private messaging server, unfortunatly you can't because registration is open or has to be manual (using the command line). Thanks to this, you'll be able to accept or deny registrations easily. This application is secure by design and never stores any plaintext password (they are not reversible in any way).

Note that Matrix (the standard used by Synapse) is federated, even if people won't be able to register on your server without your agreement, they will be able to reach you through other servers. The purpose of this application is only to create a restricted registration process on your homeserver.

## Requierements
First perform the following :
```
source ~/.synapse/bin/activate
```

Then install dependancies :
```
pip install flask
pip install flask_recaptcha
```

## Download
Download the application in a relevant folder.
```
git clone https://github.com/ShellCode33/SynapseWebRegistration.git
```
Read and edit the config.py according to your needs.

## Run the server
By default the application will be running on port 1337.
Change current directory :
```
cd SynapseWebRegistration
```
This application is not yet compatible with python3, so please execute it as follow :
```
python2.7 main.py
```

If you want it to be running in the background, you can use :
```
nohup python2.7 main.py &
```

