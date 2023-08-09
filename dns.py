import argparse
import requests

def main():
    parser = argparse.ArgumentParser(description="使用 Cloudflare 的 DoH 服务查询 DNS 记录")
    parser.add_argument("domain", type=str, help="要查询的域名")
    parser.add_argument("-t", "--type", type=str, help="DNS 记录类型 (A, NS, CNAME, MX, TXT, AAAA, SRV, CAA, HTTPS, SVCB, SPF)")
    parser.add_argument("-d", "--dns", type=str, help="要查询的 DNS 服务器（可选）")
    args = parser.parse_args()

    doh_url = "https://cloudflare-dns.com/dns-query"

    if args.dns:
        doh_url = f"https://{args.dns}/dns-query"

    domain = args.domain
    record_type_input = args.type.upper() if args.type else None

    record_type_map = {
        "A": 1,
        "NS": 2,
        "CNAME": 5,
        "MX": 15,
        "TXT": 16,
        "AAAA": 28,
        "SRV": 33,
        "CAA": 257,
        "HTTPS": 65,
        "SVCB": 64,
        "SPF": 99,
    }

    if record_type_input and record_type_input not in record_type_map:
        print("无效的记录类型")
    else:
        record_type = record_type_input or "A"
        params = {
            "name": domain,
            "type": record_type_map[record_type],
        }

        headers = {
            "Accept": "application/dns-json",
        }

        response = requests.get(doh_url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            answers = data.get("Answer", [])

            for answer in answers:
                print("类型:", answer["type"])
                print("名称:", answer["name"])
                print("TTL:", answer["TTL"])

                if record_type == "A" or record_type == "AAAA":
                    print("数据:", answer.get("data", ""))
                elif record_type == "NS":
                    print("数据: NS 记录:", answer.get("data", ""))
                elif record_type == "CNAME":
                    print("数据: CNAME 记录:", answer.get("data", ""))
                elif record_type == "MX":
                    print("数据: MX 记录:", answer.get("data", ""))
                elif record_type == "TXT":
                    print("数据: TXT 记录:", answer.get("data", ""))
                elif record_type == "SRV":
                    srv_data = answer.get("data", "")
                    srv_parts = srv_data.split()

                    if len(srv_parts) >= 4:
                        priority = srv_parts[0]
                        weight = srv_parts[1]
                        port = srv_parts[2]
                        target = srv_parts[3]

                        print("数据: SRV 记录")
                        print("优先级:", priority)
                        print("权重:", weight)
                        print("端口:", port)
                        print("目标:", target)
                    else:
                        print("无效的 SRV 数据格式")

        else:
            print("错误:", response.status_code)

if __name__ == "__main__":
    main()
