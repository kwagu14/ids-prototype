Some scripts used in an IDS prototype
-------------------------------------

- application: contains files related to the iot process
- classifier: contains files used by the classification server
- docker: contains custom images/configurations for docker containers used in the prototype
- mem-forensics: contains everything needed for periodic mem-forensics
- secureboot: contains scripts that mimic the secure boot mechanism of RO-IoT
- networking: contains all of the network code used on the IoT devices; some are mqtt scripts, one is a client used for transfering bin files

This system mimics the RO-IoT recovery mechanism. It is meant to run on a Rasberry Pi 4 Device. 

Since the Raspberry Pi 4 does not have ARM TrustZone features required of RO-IoT, the concept is mimicked through the use of containers. 

One container contains all IDS functions and models the TEE. 

The other container contains the IoT process and any other untrusted programs and models the regular IoT environment/OS/firmware

This solution is ok for the proof-of-concept but should not be used in the final product. In the real world, malware will not infect a single container on the system. It will instead infect the entire host. In the final implementation, we need to use a chip that has ARM TrustZone so that we can implement IDS functions correctly in the TEE. 


