import logging
import fmcapi
import time


def test__ikev1(fmc):
    logging.info(
        "Test IKEv1Policies and IKEv1IpsecProposals."
        "  Post, get, put, delete IKEv1Policies and IKEv1IpsecProposals Objects."
    )

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    ipsec1 = fmcapi.IKEv1IpsecProposals(fmc=fmc)
    ipsec1.name = "_ipsec" + namer
    ipsec1.espEncryption = "AES-128"
    ipsec1.espHash = "SHA"
    ipsec1.post()

    ipsec1.get()
    ipsec1.espEncryption = "AES-192"
    ipsec1.put()

    pol1 = fmcapi.IKEv1Policies(fmc=fmc)
    pol1.name = "_pol" + namer
    pol1.encryption = "3DES"
    pol1.hash = "SHA"
    pol1.priority = "10"
    pol1.diffieHellmanGroup = "5"
    pol1.authenticationMethod = "Preshared Key"
    pol1.lifetimeInSeconds = "3600"
    pol1.post()

    pol1.get()
    pol1.encryption = "AES-128"
    pol1.put()

    ipsec1.delete()
    pol1.delete()

    logging.info("Test IKEv1Policies and IKEv1IpsecProposals classes done.\n")
