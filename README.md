Gemel SDN
=========

![Gemel](https://a2-images.myspacecdn.com/images04/12/bf743f21408a4ec8938448a10700602d/full.jpg)

This repository contains scrtipts for provisioning and managing resources on Gemel. The componenets are:

VNet
----
Convenient scripts for adding/removing hosts to/from virtual networks.

Set-up
------
Notes and scripting for setting up the SDN from scratch on GCP.

Provision
---------
Scripts used for instantiating new virtual machines and setting up OVS and connections on them

Snort
---------
Scripts used for installing Snort and Barnyard2 and setting up a MySQL database used by Snort

Getting Started
---------------

TODOs before using the scripts:

* [Add your public key as a project-wide metadata](https://cloud.google.com/compute/docs/storing-retrieving-metadata#projectwide) to the project so you can use the SSH and SCP command freely
* [Obtain a service account key JSON file](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) from GCP (to be used with provision/gcp-login.sh)
* [Intall GCloud CLI](https://devopscube.com/setup-google-cloud-clisdk/) tool on your system.
* `apt install jq xmllint`
* `pip install beautifulsoup4`
* For OS X, run `brew install coreutils`

See [wiki](https://github.com/simorgh-project/gemel-sdn/wiki/) for more info.

