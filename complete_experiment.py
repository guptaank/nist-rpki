import os

def replaceTextInLine(s_base, replace_str, conf_asn):
    '''
    Replace the string after "sbase" with string "replace_str"
    in the file "conf_asn"
    '''
    cmd = 'sed -i -e "/'+s_base+'/ s/'+s_base+'.*/'+replace_str+'/" '+conf_asn
    #print cmd
    os.system(cmd)



def configureBGP(as_list, conf_base, prefix_dict, peer_dict):
    '''
    * Two clients (A1 & A2) (What are the ASNs we can use?)
    * Create a basic bgpd.conf for each client (define MUX for each client)
    * Configure the set of prefixes they announce (Which prefixes have ROA?)
    '''
    for asn in as_list:
        '''
        ASN:
        router bgp 47065 ---> replace with ASN of the client
        Prefix:
        !  network 184.164.240.0/24 --> replace with prefix we want to advertisee
        For each Peer:
        ! neighbor 10.193.0.1 remote-as 47065 ---> ASN of advertising client
        ! neighbor 10.193.0.1 description WISC ---> remote MUX's name
        ! neighbor 10.193.0.1 route-map WISC out ---> remote MUX's name
        '''
        conf_asn = "bgpd_"+str(asn)+".conf"
        cmd = "cp "+conf_base+" "+conf_asn
        os.system(cmd)

        # Replace ASN
        s_base = 'router bgp '
        replace_str = s_base+str(asn)
        replaceTextInLine(s_base, replace_str, conf_asn)

        # Replace prefixes
        for prefix in prefix_dict[asn]:
            prefix = prefix.replace("/", "\/")
            s_base = '!  network 184.164.240.0\/24'
            replace_str = '  network '+str(prefix)
            replaceTextInLine(s_base, replace_str, conf_asn)

        # Replace Peers
        for peer in peer_dict[asn]:
            (id, ip) = peer
            # line 1
            s_base = '! neighbor '+str(ip)+' remote-as 47065'
            replace_str = ' neighbor '+str(ip)+' remote-as 47065'
            replaceTextInLine(s_base, replace_str, conf_asn)
            # line 2
            s_base = '! neighbor '+str(ip)+' description '+id
            replace_str = ' neighbor '+str(ip)+' description '+id
            replaceTextInLine(s_base, replace_str, conf_asn)
            #line 3
            s_base = '! neighbor '+str(ip)+' route-map '+id+' out'
            replace_str = ' neighbor '+str(ip)+' route-map '+id+' out'
            replaceTextInLine(s_base, replace_str, conf_asn)


if __name__ == '__main__':
    as_list = [100,200]
    prefix_dict = {100:["184.164.240.0/24"], 200:["184.164.241.0/24"]}
    conf_base = "bgpd_sample.conf"
    peer_dict = {100:[("UW", "10.194.0.1")], 200:[("WISC", "10.193.0.1")]}
    configureBGP(as_list, conf_base, prefix_dict, peer_dict)

    #run_experiment1()
    #run_experiment2()
    #run_experiment3()
