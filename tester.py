import dns.name
import dns.query
import dns.dnssec
import dns.message
import dns.resolver
import dns.rdatatype

def validate_dnssec(domain_url):
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
            print("Something unexpected happened during the DNS query process")
            return False

        # the DNSKEY should be self-signed, validate it
        name = dns.name.from_text(domain_url)
        dns.dnssec.validate(answer[0], answer[1], {name: answer[0]})
        
        # If validation succeeds, return True
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

# Example usage
domain_valid = validate_dnssec('fedoraproject.org')
if domain_valid:
    print("Domain has valid DNSSEC.")
else:
    print("Domain does not have valid DNSSEC.")
