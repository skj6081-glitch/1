# Week 3 DNS Observation Report

## Task 1
* Successfully implemented the iterative resolver, passing all target resolutions including `www.korea.ac.kr` (in 3 hops) and `www.microsoft.com` (in 10 hops).
* The resolver correctly starts its path at the root server hints and properly handles iterative queries across TLD and authoritative name servers.

## Task 2
* Successfully generated `chains.json` and `report.md` for 12 CDN-hosted sites, incorporating the required table, third-party verdicts, and steering numbers.
* Utilized the official Kurose & Ross textbook Wireshark lab trace (Path B) since local packet capturing was bypassed.

## Task 3
* Implemented the local DNS cache (`YourCache`), achieving a **72.5% hit rate** and reducing upstream queries from 1000 down to **275**.
* The local cache successfully shortened the simulation time from 20.0s to **5.5s** while maintaining zero stale answers and satisfying all cache floor and expiration constraints.