#!/usr/bin/env python3

import json


def add_ua(my_dict, ua):
    """
    Sets/increments the count of how many times a user_agent has been seen

    Args:
        my_dict(dict): the dictionary you are using to track this
            user_agent
        ua(str): the user_agent seen

    Returns:
        my_dict(dict): key and value pairs of user_agent and count
    """
    if ua in my_dict:
        my_dict[ua] += 1
    else:
        my_dict[ua] = 1

    return my_dict


def search_json(my_json):
    """
    Look for bad things in the json fields

    Args:
        my_json(json): the json containing all the data

    Returns:
        All of these are a key and then a value of count thanks to add_ua()

        ua_dict(dict): all of the user_agents seen
        bad_ua_dict(dict): known bad user_agents
        bad_hosts(dict): known bad hosts
    """
    ua_dict = {}
    bad_ua_dict = {}
    bad_hosts = {}

    #                 Match       Fields
    bad_traffic = { "<script": ["uri", "user_agent", "host"], # XSS
                    "etc/passwd": ["uri", "user_agent", "host"], # LFI
                    "SELECT": ["uri", "user_agent", "host"], # SQLi
                    "ssrf": ["uri", "user_agent", "host"], # SSRF
                    "bin/": ["user_agent"], # Shellshock
                  }

    for obj in my_json:
        ua_dict = add_ua(ua_dict, obj["user_agent"])
        for bstr, fields in bad_traffic.items():
            for field in fields:
                if bstr in obj[field]:
                    # we'll be pivoting on user_agent
                    bad_hosts[obj["id.orig_h"]] = obj["user_agent"]
                    bad_ua_dict = add_ua(bad_ua_dict, obj["user_agent"])
 
    return ua_dict, bad_ua_dict, bad_hosts


def find_doubles(bad_ua_dict, ua_dict):
    """
    We noticed a pattern when manually pivoting on the known bad traffic.
    A 'bad' UA (fairly obvious mispellings, etc), would only be used one
    extra time

    Args:
        bad_ua_dict(dict): known bad user agents and their count

    Returns:
        final_bad_ua(list): our final list of bad IPs based on user_agent
    """
    final_bad_ua = []
    for bua in bad_ua_dict:
        if ua_dict[bua] == 2:
            final_bad_ua.append(bua)

    return final_bad_ua


def ua_pivot(my_json, bad_hosts, final_bad_ua):
    """
    Now that we have our known real bad UAs, we cycle back through the json

    Args:
        my_json(json): the json containing all the data
        bad_hosts(dict): known bad hosts
        final_bad_ua(list): our final list of bad IPs based on user_agent

    Returns:
        bad_hosts(dict): known bad hosts
    """
    for obj in my_json:
        if obj["user_agent"] in final_bad_ua:
            bad_hosts[obj["id.orig_h"]] = obj["user_agent"]

    return bad_hosts


def main():
    with open("http.log", "r") as logf:
        my_json = json.load(logf)

    ua_dict, bad_ua_dict, bad_hosts = search_json(my_json)
    final_bad_ua = find_doubles(bad_ua_dict, ua_dict)
    bad_hosts = ua_pivot(my_json, bad_hosts, final_bad_ua)

    # Plus the original attacker (whose UA violates the =2 rule)
    bad_hosts[
        "42.103.246.130"
    ] = "don't care, but we did find it based on it's history via UA manually"

    print(", ".join(bad_hosts))


if __name__ == "__main__":
    main()
