import requests

# 设置 Cloudflare 的 DoH URL
doh_url = "https://cloudflare-dns.com/dns-query"

print("输入请求域名")
satou_host = input()

# 定义不同记录类型的映射关系
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

# 获取用户输入的记录类型
print("输入记录类型（A、NS、CNAME等）：")
record_type_input = input()
record_type = record_type_input.upper()

# 检查记录类型是否有效
if record_type not in record_type_map:
    print("无效的记录类型")
else:
    # 构建 DoH 查询参数
    params = {
        "name": satou_host,
        "type": record_type_map[record_type],
    }

    # 设置请求头
    headers = {
        "Accept": "application/dns-json",
    }

    # 发起 GET 请求并获取响应
    response = requests.get(doh_url, params=params, headers=headers)

    # 解析 JSON 响应
    if response.status_code == 200:
        data = response.json()
        answers = data.get("Answer", [])

        for answer in answers:
            print("Type:", answer["type"])
            print("Name:", answer["name"])
            print("TTL:", answer["TTL"])

            # 根据记录类型处理数据
            if record_type == "A" or record_type == "AAAA":
                print("Data:", answer.get("data", ""))
            elif record_type == "NS":
                print("Data: NS record:", answer.get("data", ""))
            elif record_type == "CNAME":
                print("Data: CNAME record:", answer.get("data", ""))
            elif record_type == "MX":
                print("Data: MX record:", answer.get("data", ""))
            elif record_type == "TXT":
                print("Data: TXT record:", answer.get("data", ""))
            elif record_type == "SRV":
                srv_data = answer.get("data", "")
                srv_parts = srv_data.split()

                if len(srv_parts) >= 4:
                    priority = srv_parts[0]
                    weight = srv_parts[1]
                    port = srv_parts[2]
                    target = srv_parts[3]

                    print("Data: SRV record")
                    print("Priority:", priority)
                    print("Weight:", weight)
                    print("Port:", port)
                    print("Target:", target)
                else:
                    print("Invalid SRV data format")

    else:
        print("Error:", response.status_code)
