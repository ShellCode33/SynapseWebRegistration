# Synapse Web Registration
Simple Synapse registration using Python.

This application will enable you to control users registering your Synapse server. You may want to create a private messaging server, unfortunatly you can't because registration is open or has to be manual. Thanks to this, you'll be able to accept or deny registrations easily. This application is secured by design and never stores any plaintext password (nor reversible).

Note that Matrix (the standard used by Synapse) is federated, even if people won't be able to register on your server without your agreement, they will be able to reach you through other servers. The purpose of this application is only to create a restricted registration process on your homeserver.
