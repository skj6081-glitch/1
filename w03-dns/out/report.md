# Task 2 Report: CDN and Steering

| Site | Chain Length | Final Zone | Third Party? (Actual) | Rule's Verdict |
|---|---|---|---|---|
| www.microsoft.com | 2 | e13678.dscb.akamaiedge.net | Yes | Yes |
| www.netflix.com | 1 | www.prod.ftl.netflix.com | No | No |
| www.adobe.com | 2 | a1319.dscr.akamai.net | Yes | Yes |
| www.cnn.com | 1 | cnn-tls.map.fastly.net | Yes | Yes |
| www.apple.com | 3 | e6858.dsce9.akamaiedge.net | Yes | Yes |
| www.korea.ac.kr | 0 | www.korea.ac.kr | No | No |
| www.stanford.edu | 1 | stanford.netlifyglobalcdn.com | No | Yes |
| www.bbc.co.uk | 2 | bbc.map.fastly.net | Yes | Yes |
| www.spotify.com | 1 | atc.spotify.map.fastly.net | Yes | Yes |
| www.github.com | 1 | github.com | Yes | No |
| www.wikipedia.org | 1 | dyna.wikimedia.org | No | Yes |
| www.nytimes.com | 3 | nytimes.map.fastly.net | Yes | Yes |

## Steering Number
**11 of 11 CDN-hosted sites** answered differently depending on the resolver used.

## Classification Rule & Flaws
**The Rule:** I classified a site as 'Third-party' if the last two labels (e.g., `domain.com`) of the original query and the final CNAME target were different.

**Where it failed:**
- **`www.wikipedia.org`**: The CNAME chain ends at `dyna.wikimedia.org`. Because `wikipedia.org` != `wikimedia.org`, my rule flags it as a Third-Party CDN. However, both belong to the Wikimedia Foundation (First-Party).
- **`www.bbc.co.uk`**: The last two labels are just `co.uk` (the TLD itself). Stripping it this way destroys the actual domain name (`bbc`), making simple label counting completely inaccurate for UK or KR domains.