import logging
import fmcapi
import time


def test__ikev2(fmc):
    logging.info(
        "Test IKEv2Policies and IKEv2IpsecProposals."
        "  Post, get, put, delete IKEv2Policies and IKEv2IpsecProposals Objects."
    )

    starttime = str(int(time.time()))
    namer = f"_fmcapi_test_{starttime}"

    encryption_list = ["AES", "AES-192", "AES-256", "NULL"]
    integrity_list1 = ["NULL", "SHA-1", "SHA-256", "SHA-384", "SHA-512"]
    ipsec_integrity_list1 = ["NULL", "SHA", "SHA-256", "SHA-384", "SHA-512"]
    # 'NULL' is invalid for prf_integrity.  Should generate a warning log and ignore that type.
    prf_integrity_list1 = ["NULL", "SHA", "SHA-256", "SHA-384", "SHA-512"]

    ipsec1 = fmcapi.IKEv2IpsecProposals(fmc=fmc)
    ipsec1.name = "_ipsec" + namer
    ipsec1.encryption(action="add", algorithms=encryption_list)
    ipsec1.hash(action="add", algorithms=integrity_list1)
    ipsec1.post()

    ipsec1.get()
    # Try to add a duplicate
    ipsec1.encryption(action="add", algorithms=["AES-192"])
    ipsec1.hash(action="add", algorithms=["SHA-1"])

    ipsec1.encryption(action="remove", algorithms=["NULL"])
    ipsec1.hash(action="remove", algorithms=["NULL"])
    ipsec1.put()

    # None of the algorithms can contain an empty list
    ipsec1.get()
    ipsec1.encryption(action="clear")
    ipsec1.hash(action="clear")
    ipsec1.encryption(action="add", algorithms=["AES-192"])
    ipsec1.hash(action="add", algorithms=["SHA-1"])
    ipsec1.put()

    pol1 = fmcapi.IKEv2Policies(fmc=fmc)
    pol1.name = "_pol" + namer
    pol1.priority = "10"
    pol1.diffieHellmanGroups = ["2", "5"]
    pol1.encryption(action="add", algorithms=encryption_list)
    pol1.hash(action="add", algorithms=ipsec_integrity_list1)
    pol1.prf_hash(action="add", algorithms=prf_integrity_list1)
    pol1.lifetimeInSeconds = "3600"
    pol1.post()

    pol1.get()
    # Try to add a duplicate
    pol1.encryption(action="add", algorithms=["AES-192"])
    pol1.hash(action="add", algorithms=["NULL"])
    pol1.prf_hash(action="add", algorithms=["SHA"])

    pol1.encryption(action="remove", algorithms=["NULL"])
    pol1.hash(action="remove", algorithms=["NULL"])
    pol1.prf_hash(action="remove", algorithms=["SHA"])
    pol1.put()

    # None of the algorithms can contain an empty list
    pol1.get()
    pol1.encryption(action="clear")
    pol1.hash(action="clear")
    pol1.prf_hash(action="clear")
    pol1.encryption(action="add", algorithms=["AES-192"])
    pol1.hash(action="add", algorithms=["NULL"])
    pol1.prf_hash(action="add", algorithms=["SHA"])
    pol1.put()

    ipsec1.delete()
    pol1.delete()

    logging.info("Test IKEv2Policies and IKEv2IpsecProposals classes done.\n")
