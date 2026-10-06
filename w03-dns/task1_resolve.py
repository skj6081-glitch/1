#!/usr/bin/env python3
"""Week 3 · Task 1 — Build your own iterative resolver."""
import argparse, subprocess, sys
import dns.message
import dns.query
import dns.rdatatype
import dns.exception
import dns.name

# Root servers. Everything starts here; there is no earlier step.
ROOT_SERVERS = [
    "198.41.0.4",       # a.root-servers.net
    "199.9.14.201",     # b.root-servers.net
    "192.33.4.12",      # c.root-servers.net
]

VERIFY_NAMES = [
    ("www.korea.ac.kr", "stable"),
    ("dns.google", "stable"),
    ("en.wikipedia.org", "stable"),
    ("www.stanford.edu", "stable"),
    ("www.microsoft.com", "cdn"),
]

class Resolver:
    def resolve(self, name, depth=0):
        # R6: 무한 루프 방지 (최대 깊이 제한)
        if depth > 10:
            raise Exception("Max depth exceeded (Loop detected)")

        path = []
        target_name = dns.name.from_text(name)
        current_servers = ROOT_SERVERS.copy()

        while current_servers:
            server_ip = current_servers.pop(0)
            path.append(server_ip)

            # R2: 재귀 쿼리 방지 (+norecurse 역할)
            query = dns.message.make_query(target_name, dns.rdatatype.A)
            query.flags &= ~dns.flags.RD 

            try:
                # R4: 응답 없는 서버 처리 (타임아웃 시 다음 서버로)
                response = dns.query.udp(query, server_ip, timeout=2.0)
            except dns.exception.DNSException:
                continue

            # R1 & R5: Answer 섹션 확인 (A 레코드 또는 CNAME)
            if response.answer:
                a_record = None
                cname_target = None
                
                for rrset in response.answer:
                    if rrset.rdtype == dns.rdatatype.A:
                        a_record = rrset[0].address
                    elif rrset.rdtype == dns.rdatatype.CNAME:
                        cname_target = rrset[0].target.to_text()

                if a_record:
                    return a_record, path
                elif cname_target:
                    # CNAME 처리: 변경된 이름으로 다시 처음부터 걷기 시작
                    addr, sub_path = self.resolve(cname_target, depth + 1)
                    return addr, path + sub_path

            # Authority 섹션 확인 (Delegation)
            if response.authority:
                ns_names = []
                for rrset in response.authority:
                    if rrset.rdtype == dns.rdatatype.NS:
                        for rr in rrset:
                            ns_names.append(rr.target)

                if not ns_names:
                    continue

                # R3: Additional 섹션에서 Glue 레코드 찾기
                glue_ips = []
                for rrset in response.additional:
                    if rrset.rdtype == dns.rdatatype.A and rrset.name in ns_names:
                        for rr in rrset:
                            glue_ips.append(rr.address)

                if glue_ips:
                    # Glue 레코드가 있으면 해당 IP를 다음 서버 후보로 등록
                    current_servers = glue_ips
                else:
                    # Glue 레코드가 없으면 네임서버 자체의 IP를 먼저 Resolve (새로운 walk)
                    for ns_name in ns_names:
                        try:
                            ns_ip, sub_path = self.resolve(ns_name.to_text(), depth + 1)
                            if ns_ip:
                                path.extend(sub_path)
                                current_servers = [ns_ip]
                                break
                        except Exception:
                            continue

        return None, path


# ------------------------------------------------------------------- harness
def dig_answer(name):
    out = subprocess.run(["dig", "+short", name, "A"],
                         capture_output=True, text=True).stdout
    return [l for l in out.split() if l and l[0].isdigit()]

def verify():
    r, failures = Resolver(), 0
    for name, kind in VERIFY_NAMES:
        try:
            addr, path = r.resolve(name)
        except NotImplementedError:
            print("Nothing implemented yet - write Resolver.resolve first.")
            return 1
        except Exception as e:
            print(f"  FAIL  {name:<22} your resolver raised {e!r}")
            failures += 1
            continue
            
        expected = dig_answer(name)
        if addr in expected:
            note = ""
        elif kind == "cdn":
            note = "  <- differs, but this name is CDN-hosted. Explain it."
        else:
            note = "  <- should have matched"
            failures += 1
            
        print(f"  {'FAIL' if note.endswith('matched') else 'ok  '}  {name:<22} "
              f"you={addr:<16} dig={','.join(expected) or '-'}   "
              f"hops={len(path)}{note}")
              
    print(f"\n  {len(VERIFY_NAMES) - failures}/{len(VERIFY_NAMES)} ok")
    return 1 if failures else 0

def main():
    p = argparse.ArgumentParser()
    p.add_argument("name", nargs="?", default="www.korea.ac.kr")
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()

    if a.verify:
        sys.exit(verify())

    addr, path = Resolver().resolve(a.name)
    for i, server in enumerate(path, 1):
        print(f"  {i}. asked {server}")
    print(f"\n  {a.name} -> {addr}")

if __name__ == "__main__":
    main()
