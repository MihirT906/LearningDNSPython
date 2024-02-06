# LearningDNSPython
In this project, I have created a script to check if a domain is DNSSEC valid, and also incorporated a bloom filter to store the valid DNSECC domains. This reduces lookup time, while requiring minimum space considerations. 
Running the code gives the following output:
```
example.com ✔
[0.134844] seconds
torproject.org ✖
[0.269991] seconds
fedoraproject.org ✔
[0.111781] seconds
usa.gov ✔
[0.206279] seconds
google.com ✖
[0.086854] seconds
fedoraproject.org ✔
[0.000009] seconds
google.com ✖
[0.090687] seconds
example.com ✔
[0.000014] seconds
ietf.org ✔
[0.061337] seconds
DNS Exception: The DNS response does not contain an answer to the question: chat.openai.com. IN NS
chat.openai.com ✖
[0.022738] seconds
verisign.com ✔
[0.068730] seconds
usa.gov ✔
[0.000011] seconds
torproject.org ✖
[1.534741] seconds
ietf.org ✔
[0.000033] seconds
fedoraproject.org ✔
[0.000017] seconds
usa.gov ✔
[0.000015] seconds
usa.gov ✔
[0.000012] seconds
ietf.org ✔
[0.000013] seconds
usa.gov ✔
[0.000012] seconds
ietf.org ✔
[0.000013] seconds
DNS Exception: The DNS response does not contain an answer to the question: chat.openai.com. IN NS
chat.openai.com ✖
[0.023859] seconds
umass.edu ✖
[0.078464] seconds
torproject.org ✖
[0.352761] seconds
DNS Exception: The DNS response does not contain an answer to the question: chat.openai.com. IN NS
chat.openai.com ✖
[0.024148] seconds
fedoraproject.org ✔
[0.000015] seconds
DNS Exception: The DNS response does not contain an answer to the question: chat.openai.com. IN NS
chat.openai.com ✖
[0.020330] seconds
amazon.com ✖
[0.070639] seconds
google.com ✖
[0.070657] seconds
fedoraproject.org ✔
[0.000013] seconds
torproject.org ✖
[0.174575] seconds
Size of the filter: 479 bits
Size saved: 2017 bits

```
Here, a tick mark indicates that the corresponding domain is DNSSEC valid and cross indicates that the DNSSEC is invalid
Notice the time saved during redundant lookups. 
Also notice the amount of size saved in comparison to storing all the lookups

OBJECTIVE: The purpose of this Python script is to validate DNSSEC (Domain Name System Security Extensions) for a randomly selected list of domains. To enhance efficiency, the script employs a Bloom filter to quickly determine whether a domain has undergone DNSSEC validation before. While this introduces the possibility of false positives, it significantly reduces the time required for subsequent validations.
ANALYSIS: The trade-off lies in the space requirement of the Bloom filter. Despite the potential for false positives, the overall advantage is a notable reduction in validation time. False positives, while not impacting accuracy, might incur additional time in certain cases. In summary, the script leverages the benefits of a Bloom filter to minimize storage space while providing a substantial time-saving advantage, acknowledging the trade-offs involved.
CHALLENGES: Commonly, these systems are implemented on servers, but relying on server-based storage for the list of valid DNSSEC introduces scalability challenges. The approach becomes less scalable as the number of domains increases, and any modifications to the system can lead to complications. Security is a pivotal concern in DNSSEC, aiming to thwart attacks such as DNS spoofing. However, storing the list centrally on a server increases the vulnerability to potential spoofing incidents, contradicting the core objective of DNSSEC.

