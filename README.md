# DnsLookdesu（ドメインネームシステム見せるです）





只针对SRV和A进行测试

使用方法 ：

`usage: dns [-h] [-t TYPE] [-mc] [-d DNS] domain

使用 Cloudflare 的 DoH 服务查询 DNS 记录

positional arguments:
  domain                要查询的域名

options:
  -h, --help            show this help message and exit
  -t TYPE, --type TYPE  DNS 记录类型 (A, NS, CNAME, MX, TXT, AAAA, SRV, CAA, HTTPS, SVCB, SPF)
  -mc, --minecraft      查询 Minecraft 服务器的 SRV 记录，将自动添加MC前缀
  -d DNS, --dns DNS     要查询的 DNS 服务器（可选），默认为标准 DoH 请求 URL。例如 8.8.8.8 为 'https://8.8.8.8/dns-query'`