import dns.name
import dns.query
import dns.dnssec
import dns.message
import dns.resolver
import dns.rdatatype
import bloomFilter as bloomFilter
import time
import sys
import random

filter = bloomFilter.BloomFilter(50, false_positive_rate=0.01)

def validate_dnssec(domain_url):
    if(filter.query(domain_url)):
        return True
    try:
        # get nameservers for target domain
        response = dns.resolver.resolve(domain_url, dns.rdatatype.NS)
        
        # use the first nameserver
        nsname = response.rrset[0].to_text()  # name
        response = dns.resolver.resolve(nsname, dns.rdatatype.A)
        nsaddr = response.rrset[0].to_text()  # IPv4

        # get DNSKEY for zone
        request = dns.message.make_query(domain_url,
                                         dns.rdatatype.DNSKEY,
                                         want_dnssec=True)
        
        # send the query
        response = dns.query.udp(request, nsaddr)
        
        if response.rcode() != 0:
            # HANDLE QUERY FAILED
            print(f"Query Failed with response code: {response.rcode()}")
            
            if response.rcode() == dns.rcode.NXDOMAIN:
                print("Domain does not exist.")
            elif response.rcode() == dns.rcode.SERVERFAIL:
                print("Server failed to process the query.")
            
            return False

        # answer should contain two RRSET: DNSKEY and RRSIG(DNSKEY)
        answer = response.answer
        #print(answer)
        if len(answer) != 2:
            # SOMETHING WENT WRONG
            #print("Something unexpected happened during the DNS query process")
            return False

        # the DNSKEY should be self-signed, validate it
        name = dns.name.from_text(domain_url)
        dns.dnssec.validate(answer[0], answer[1], {name: answer[0]})
        
        # If validation succeeds, return True
        filter.insert(domain_url)
        return True

    except dns.resolver.NXDOMAIN:
        print("Domain does not exist.")
        return False
    except dns.exception.DNSException as e:
        print(f"DNS Exception: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    
#Experiment Setup:
valid_domains = ['example.com', 'fedoraproject.org', 'ietf.org', 'openssl.org', 'torproject.org']
invalid_domains = ['google.com', 'verisign.com', 'amazon.com', 'usa.gov', 'umass.edu', 'chat.openai.com']
domain_list_to_check = random.choices(valid_domains + invalid_domains, k=30)

# Example usage
for domain in domain_list_to_check:
    start_time = time.time()
    domain_valid = validate_dnssec(domain)
    if domain_valid:
        print(f"{domain} ✔")
    else:
        print(f"{domain} ✖")
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"[{elapsed_time:.6f}] seconds")

print(f"Size of the filter: {filter.size} bits")
print(f"Size saved: {sys.getsizeof(domain_list_to_check)*8 - filter.size} bits")
        
