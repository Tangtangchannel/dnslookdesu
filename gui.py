import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QWidget, \
    QHBoxLayout, QComboBox, QCheckBox, QMessageBox


class DNSQueryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("DNSLookdesu")
        self.setGeometry(100, 100, 600, 400)

        self.domain_label = QLabel("域名:")
        self.domain_input = QLineEdit()

        self.type_label = QLabel("记录类型:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["A", "NS", "CNAME", "MX", "TXT", "AAAA", "SRV", "CAA", "HTTPS", "SVCB", "SPF"])

        self.minecraft_checkbox = QCheckBox("Minecraft服务器查询（忽略记录类型）")

        self.query_button = QPushButton("查询")
        self.query_button.clicked.connect(self.performQuery)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.domain_label)
        layout.addWidget(self.domain_input)
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)
        layout.addWidget(self.minecraft_checkbox)
        layout.addWidget(self.query_button)
        layout.addWidget(self.result_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def performQuery(self):
        domain = self.domain_input.text()
        record_type = self.type_combo.currentText()
        minecraft = self.minecraft_checkbox.isChecked()

        result = self.performDnsQuery(domain, record_type, minecraft)

        self.result_text.clear()
        self.result_text.append(result)

    def performDnsQuery(self, domain, record_type, minecraft):
        doh_url = "https://cloudflare-dns.com/dns-query"

        srv_domain = domain
        record_type_input = record_type
        record_type = record_type_input.upper() if record_type_input else None

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

        if minecraft:
            srv_domain = f"_minecraft._tcp.{domain}"
            record_type = "SRV"

        if record_type == "SRV":
            params = {
                "name": srv_domain,
                "type": record_type_map[record_type],
            }
        else:
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
            result_str = ""

            if not answers:
                    error_message = "未查询到记录。"
                    QMessageBox.critical(self, "错误", error_message)
                    return ""
            for answer in answers:
                result_str += "类型: {}\n".format(answer["type"])
                result_str += "名称: {}\n".format(answer["name"])
                result_str += "TTL: {}\n".format(answer["TTL"])

                if record_type == "A" or record_type == "AAAA":
                    result_str += "数据: {}\n".format(answer.get("data", ""))
                elif record_type == "NS":
                    result_str += "数据: NS 记录: {}\n".format(answer.get("data", ""))
                elif record_type == "CNAME":
                    result_str += "数据: CNAME 记录: {}\n".format(answer.get("data", ""))
                elif record_type == "MX":
                    result_str += "数据: MX 记录: {}\n".format(answer.get("data", ""))
                elif record_type == "TXT":
                    result_str += "数据: TXT 记录: {}\n".format(answer.get("data", ""))
                elif record_type == "SRV":
                    srv_data = answer.get("data", "")
                    srv_parts = srv_data.split()

                    if len(srv_parts) >= 4:
                        priority = srv_parts[0]
                        weight = srv_parts[1]
                        port = srv_parts[2]
                        target = srv_parts[3]

                        result_str += "数据: SRV 记录\n"
                        result_str += "优先级: {}\n".format(priority)
                        result_str += "权重: {}\n".format(weight)
                        result_str += "端口: {}\n".format(port)
                        result_str += "目标: {}\n".format(target)
                    else:
                        result_str += "无效的 SRV 数据格式\n"
        else:
            result_str = "错误: {}\n".format(response.status_code)




        return result_str

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DNSQueryApp()
    window.show()
    sys.exit(app.exec_())
