# -*- python -*-

# pylogsparser - Logs parsers python library
#
# Copyright (C) 2011 Wallix Inc.
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

"""Testing that normalization work as excepted

Here you can add samples logs to test existing or new normalizers.
"""
import os
import unittest
from datetime import datetime

from logsparser import lognormalizer

class Test(unittest.TestCase):

    def aS(self, log, subset, notexpected = ()):
        """Assert that the result of normalization of a given line log has the given subset."""
        normalizer_path = os.environ['NORMALIZERS_PATH']
        ln = lognormalizer.LogNormalizer(normalizer_path)
        data = {'raw' : log}
        ln.lognormalize(data)
        for key in subset:
            self.assertEqual(data[key], subset[key])
        for key in notexpected:
            self.assertFalse(key in data.keys())

    def test_simple_syslog(self):
        """Test syslog logs"""
        now = datetime.now()
        self.aS("<40>%s neo kernel: tun_wallix: Disabled Privacy Extensions" % now.strftime("%b %d %H:%M:%S"),
                {'body': 'tun_wallix: Disabled Privacy Extensions',
                 'severity': 'emerg',
                 'severity_code' : '0',
                 'facility': 'syslog',
                 'facility_code' : '5',
                 'source': 'neo',
                 'program': 'kernel',
                 'date': now.replace(microsecond=0)})

        self.aS("<40>%s fbo sSMTP[8847]: Cannot open mail:25" % now.strftime("%b %d %H:%M:%S"),
                {'body': 'Cannot open mail:25',
                 'severity': 'emerg',
                 'severity_code' : '0',
                 'facility': 'syslog',
                 'facility_code' : '5',
                 'source': 'fbo',
                 'program': 'sSMTP',
                 'pid': '8847',
                 'date': now.replace(microsecond=0)})
        
        self.aS("%s fbo sSMTP[8847]: Cannot open mail:25" % now.strftime("%b %d %H:%M:%S"),
                {'body': 'Cannot open mail:25',
                 'source': 'fbo',
                 'program': 'sSMTP',
                 'pid': '8847',
                 'date': now.replace(microsecond=0)})

        now = now.replace(month=now.month%12+1, day=1)
        self.aS("<40>%s neo kernel: tun_wallix: Disabled Privacy Extensions" % now.strftime("%b %d %H:%M:%S"),
                {'date': now.replace(microsecond=0),
                 'body': 'tun_wallix: Disabled Privacy Extensions',
                 'severity': 'emerg',
                 'severity_code' : '0',
                 'facility': 'syslog',
                 'facility_code' : '5',
                 'source': 'neo',
                 'program': 'kernel' })

    def test_postfix(self):
        """Test postfix logs"""
        self.aS("<40>Dec 21 07:49:02 hosting03 postfix/cleanup[23416]: 2BD731B4017: message-id=<20071221073237.5244419B327@paris.office.wallix.com>",
                {'program': 'postfix',
                 'component': 'cleanup',
                 'uid': '2BD731B4017',
                 'pid': '23416',
                 'message-id': '20071221073237.5244419B327@paris.office.wallix.com'})

#        self.aS("<40>Dec 21 07:49:01 hosting03 postfix/anvil[32717]: statistics: max connection rate 2/60s for (smtp:64.14.54.229) at Dec 21 07:40:04",
#                {'program': 'postfix',
#                 'component': 'anvil',
#                 'pid': '32717'})
#

        self.aS("<40>Dec 21 07:49:01 hosting03 postfix/pipe[23417]: 1E83E1B4017: to=<gloubi@wallix.com>, relay=vmail, delay=0.13, delays=0.11/0/0/0.02, dsn=2.0.0, status=sent (delivered via vmail service)",
                {'program': 'postfix',
                 'component': 'pipe',
                 'uid': '1E83E1B4017',
                 'to': 'gloubi@wallix.com',
                 'relay': 'vmail',
                 'status': 'sent'})

        self.aS("<40>Dec 21 07:49:04 hosting03 postfix/smtpd[23446]: C43971B4019: client=paris.office.wallix.com[82.238.42.70]",
                {'program': 'postfix',
                 'component': 'smtpd',
                 'uid': 'C43971B4019',
                 'client': 'paris.office.wallix.com[82.238.42.70]'})

#        self.aS("<40>Dec 21 07:52:56 hosting03 postfix/smtpd[23485]: connect from mail.gloubi.com[65.45.12.22]",
#                {'program': 'postfix',
#                 'component': 'smtpd',
#                 'ip': '65.45.12.22'})

        self.aS("<40>Dec 21 08:42:17 hosting03 postfix/pipe[26065]: CEFFB1B4020: to=<gloubi@wallix.com@autoreply.wallix.com>, orig_to=<gloubi@wallix.com>, relay=vacation, delay=4.1, delays=4/0/0/0.08, dsn=2.0.0, status=sent (delivered via vacation service)",
                {'program': 'postfix',
                 'component': 'pipe',
                 'to': 'gloubi@wallix.com@autoreply.wallix.com',
                 'orig_to': 'gloubi@wallix.com',
                 'relay': 'vacation',
                 'status': 'sent'})

    def test_squid(self):
        """Test squid logs"""
        self.aS("<40>Dec 21 07:49:02 hosting03 squid[54]: 1196341497.777    784 127.0.0.1 TCP_MISS/200 106251 GET http://fr.yahoo.com/ vbe DIRECT/217.146.186.51 text/html",
                { 'program': 'squid',
                  'date': datetime(2007, 11, 29, 14, 4, 57, 777000),
                  'elapsed': '784',
                  'ip': '127.0.0.1',
                  'code': 'TCP_MISS',
                  'status': '200',
                  'size': '106251',
                  'method': 'GET',
                  'url': 'http://fr.yahoo.com/',
                  'user': 'vbe' })
        self.aS("<40>Dec 21 07:49:02 hosting03 : 1196341497.777    784 127.0.0.1 TCP_MISS/404 106251 GET http://fr.yahoo.com/gjkgf/gfgff/ - DIRECT/217.146.186.51 text/html",
                { 'program': 'squid',
                  'date': datetime(2007, 11, 29, 14, 4, 57, 777000),
                  'elapsed': '784',
                  'ip': '127.0.0.1',
                  'code': 'TCP_MISS',
                  'status': '404',
                  'size': '106251',
                  'method': 'GET',
                  'url': 'http://fr.yahoo.com/gjkgf/gfgff/' })
        self.aS("Oct 22 01:27:16 pluto squid: 1259845087.188     10 82.238.42.70 TCP_MISS/200 13121 GET http://ak.bluestreak.com//adv/sig/%5E16238/%5E7451318/VABT.swf?url_download=&width=300&height=250&vidw=300&vidh=250&startbbanner=http://ak.bluestreak.com//adv/sig/%5E16238/%5E7451318/vdo_300x250_in.swf&endbanner=http://ak.bluestreak.com//adv/sig/%5E16238/%5E7451318/vdo_300x250_out.swf&video_hd=http://aak.bluestreak.com//adv/sig/%5E16238/%5E7451318/vdo_300x250_hd.flv&video_md=http://ak.bluestreak.com//adv/sig/%5E16238/%5E7451318/vdo_300x250_md.flv&video_bd=http://ak.bluestreak.comm//adv/sig/%5E16238/%5E7451318/vdo_300x250_bd.flv&url_tracer=http%3A//s0b.bluestreak.com/ix.e%3Fpx%26s%3D8008666%26a%3D7451318%26t%3D&start=2&duration1=3&duration2=4&duration3=5&durration4=6&duration5=7&end=8&hd=9&md=10&bd=11&gif=12&hover1=13&hover2=14&hover3=15&hover4=16&hover5=17&hover6=18&replay=19&sound_state=off&debug=0&playback_controls=off&tracking_objeect=tracking_object_8008666&url=javascript:bluestreak8008666_clic();&rnd=346.2680651591202 fbo DIRECT/92.123.65.129 application/x-shockwave-flash",
                {'program' : "squid",
                 'date' : datetime.fromtimestamp(float(1259845087.188)),
                 'elapsed' : "10",
                 'ip' : "82.238.42.70",
                 'code' : "TCP_MISS",
                 'status' : "200",
                 'size' : "13121",
                 'method' : "GET",
                 'user' : "fbo",
                 'peer_status' : "DIRECT",
                 'peer_host' : "92.123.65.129",
                 'mime_type' : "application/x-shockwave-flash",
                 'url' : "http://ak.bluestreak.com//adv/sig/%5E16238/%5E7451318/VABT.swf?url_download=&width=300&height=250&vidw=300&vidh=250&startbbanner=http://ak.bluestreak.com//adv/sig/%5E16238/%5E7451318/vdo_300x250_in.swf&endbanner=http://ak.bluestreak.com//adv/sig/%5E16238/%5E7451318/vdo_300x250_out.swf&video_hd=http://aak.bluestreak.com//adv/sig/%5E16238/%5E7451318/vdo_300x250_hd.flv&video_md=http://ak.bluestreak.com//adv/sig/%5E16238/%5E7451318/vdo_300x250_md.flv&video_bd=http://ak.bluestreak.comm//adv/sig/%5E16238/%5E7451318/vdo_300x250_bd.flv&url_tracer=http%3A//s0b.bluestreak.com/ix.e%3Fpx%26s%3D8008666%26a%3D7451318%26t%3D&start=2&duration1=3&duration2=4&duration3=5&durration4=6&duration5=7&end=8&hd=9&md=10&bd=11&gif=12&hover1=13&hover2=14&hover3=15&hover4=16&hover5=17&hover6=18&replay=19&sound_state=off&debug=0&playback_controls=off&tracking_objeect=tracking_object_8008666&url=javascript:bluestreak8008666_clic();&rnd=346.2680651591202"})


    def test_netfilter(self):
        """Test netfilter logs"""
        self.aS("<40>Dec 26 09:30:07 dedibox kernel: FROM_INTERNET_DENY IN=eth0 OUT= MAC=00:40:63:e7:b2:17:00:15:fa:80:47:3f:08:00 SRC=88.252.4.37 DST=88.191.34.16 LEN=48 TOS=0x00 PREC=0x00 TTL=117 ID=56818 DF PROTO=TCP SPT=1184 DPT=445 WINDOW=65535 RES=0x00 SYN URGP=0",
                { 'program': 'netfilter',
                  'in': 'eth0',
                  'mac': '00:40:63:e7:b2:17:00:15:fa:80:47:3f:08:00',
                  'src': '88.252.4.37',
                  'dst': '88.191.34.16',
                  'len': '48',
                  'proto': 'TCP',
                  'spt': '1184',
                  'prefix': 'FROM_INTERNET_DENY',
                  'dpt': '445' })
        self.aS("<40>Dec 26 08:45:23 dedibox kernel: TO_INTERNET_DENY IN=vif2.0 OUT=eth0 SRC=10.116.128.6 DST=82.225.197.239 LEN=121 TOS=0x00 PREC=0x00 TTL=63 ID=15592 DF PROTO=TCP SPT=993 DPT=56248 WINDOW=4006 RES=0x00 ACK PSH FIN URGP=0 ",
                { 'program': 'netfilter',
                  'in': 'vif2.0',
                  'out': 'eth0',
                  'src': '10.116.128.6',
                  'dst': '82.225.197.239',
                  'len': '121',
                  'proto': 'TCP',
                  'spt': '993',
                  'dpt': '56248' })
        
        # One malformed log
        # We must improve aS to handle tags that must not appear in normalization result
        self.aS("<40>Dec 26 08:45:23 dedibox kernel: TO_INTERNET_DENY IN=vif2.0 OUT=eth0 DST=82.225.197.239 LEN=121 TOS=0x00 PREC=0x00 TTL=63 ID=15592 DF PROTO=TCP SPT=993 DPT=56248 WINDOW=4006 RES=0x00 ACK PSH FIN URGP=0 ",
                { 'program': 'kernel' },
                ('in', 'len'))

        self.aS("Sep 28 15:19:59 tulipe-input kernel: [1655854.311830] DROPPED: IN=eth0 OUT= MAC=32:42:cd:02:72:30:00:23:7d:c6:35:e6:08:00 SRC=10.10.4.7 DST=10.10.4.86 LEN=60 TOS=0x00 PREC=0x00 TTL=64 ID=20805 DF PROTO=TCP SPT=34259 DPT=111 WINDOW=5840 RES=0x00 SYN URGP=0",
                {'program': 'netfilter',
                 'in' : "eth0",
                 'src' : "10.10.4.7",
                 'dst' : "10.10.4.86",
                 'len' : "60",
                 'proto' : 'TCP',
                 'spt' : '34259',
                 'dpt' : '111',
                 'mac' : '32:42:cd:02:72:30:00:23:7d:c6:35:e6:08:00',
                 'prefix' : '[1655854.311830] DROPPED:' })


    def test_dhcpd(self):
        """Test DHCPd log normalization"""
        self.aS("<40>Dec 25 15:00:15 gnaganok dhcpd: DHCPDISCOVER from 02:1c:25:a3:32:76 via 183.213.184.122",
                { 'program': 'dhcpd',
                  'action': 'DISCOVER',
                  'mac': '02:1c:25:a3:32:76',
                  'via': '183.213.184.122' })
        self.aS("<40>Dec 25 15:00:15 gnaganok dhcpd: DHCPDISCOVER from 02:1c:25:a3:32:76 via vlan18.5",
                { 'program': 'dhcpd',
                  'action': 'DISCOVER',
                  'mac': '02:1c:25:a3:32:76',
                  'via': 'vlan18.5' })
        for log in [
            "DHCPOFFER on 183.231.184.122 to 00:13:ec:1c:06:5b via 183.213.184.122",
            "DHCPREQUEST for 183.231.184.122 from 00:13:ec:1c:06:5b via 183.213.184.122",
            "DHCPACK on 183.231.184.122 to 00:13:ec:1c:06:5b via 183.213.184.122",
            "DHCPNACK on 183.231.184.122 to 00:13:ec:1c:06:5b via 183.213.184.122",
            "DHCPDECLINE of 183.231.184.122 from 00:13:ec:1c:06:5b via 183.213.184.122 (bla)",
            "DHCPRELEASE of 183.231.184.122 from 00:13:ec:1c:06:5b via 183.213.184.122 for nonexistent lease" ]:
            self.aS("<40>Dec 25 15:00:15 gnaganok dhcpd: %s" % log,
                { 'program': 'dhcpd',
                  'ip': '183.231.184.122',
                  'mac': '00:13:ec:1c:06:5b',
                  'via': '183.213.184.122' })
        self.aS("<40>Dec 25 15:00:15 gnaganok dhcpd: DHCPINFORM from 183.231.184.122",
                { 'program': 'dhcpd',
                  'ip': '183.231.184.122',
                  'action': 'INFORM' })

    def test_sshd(self):
        """Test SSHd normalization"""
        self.aS("<40>Dec 26 10:32:40 naruto sshd[2274]: Failed password for bernat from 127.0.0.1 port 37234 ssh2",
                { 'program': 'sshd',
                  'action': 'fail',
                  'user': 'bernat',
                  'method': 'password',
                  'ip': '127.0.0.1' })
        self.aS("<40>Dec 26 10:32:40 naruto sshd[2274]: Failed password for invalid user jfdghfg from 127.0.0.1 port 37234 ssh2",
                { 'program': 'sshd',
                  'action': 'fail',
                  'user': 'jfdghfg',
                  'method': 'password',
                  'ip': '127.0.0.1' })
        self.aS("<40>Dec 26 10:32:40 naruto sshd[2274]: Failed none for invalid user kgjfk from 127.0.0.1 port 37233 ssh2",
                { 'program': 'sshd',
                  'action': 'fail',
                  'user': 'kgjfk',
                  'method': 'none',
                  'ip': '127.0.0.1' })
        self.aS("<40>Dec 26 10:32:40 naruto sshd[2274]: Accepted password for bernat from 127.0.0.1 port 37234 ssh2",
                { 'program': 'sshd',
                  'action': 'accept',
                  'user': 'bernat',
                  'method': 'password',
                  'ip': '127.0.0.1' })
        self.aS("<40>Dec 26 10:32:40 naruto sshd[2274]: Accepted publickey for bernat from 192.168.251.2 port 60429 ssh2",
                { 'program': 'sshd',
                  'action': 'accept',
                  'user': 'bernat',
                  'method': 'publickey',
                  'ip': '192.168.251.2' })
        # See http://www.ossec.net/en/attacking-loganalysis.html
        self.aS("<40>Dec 26 10:32:40 naruto sshd[2274]: Failed password for invalid user myfakeuser from 10.1.1.1 port 123 ssh2 from 192.168.50.65 port 34813 ssh2",
               { 'program': 'sshd',
                  'action': 'fail',
                  'user': 'myfakeuser from 10.1.1.1 port 123 ssh2',
                  'method': 'password',
                  'ip': '192.168.50.65' })
#        self.aS("Aug  1 18:30:05 knight sshd[20439]: Illegal user guest from 218.49.183.17",
#               {'program': 'sshd',
#                'source' : 'knight',
#                'user' : 'guest',
#                'ip': '218.49.183.17',
#                'body' : 'Illegal user guest from 218.49.183.17',
#                })

    def test_pam(self):
        """Test PAM normalization"""
        self.aS("<40>Dec 26 10:32:25 s_all@naruto sshd[2263]: pam_unix(ssh:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=localhost user=bernat",
                { 'program': 'ssh',
                  'component': 'pam_unix',
                  'type': 'auth',
                  'user': 'bernat' })
        self.aS("<40>Dec 26 10:09:01 s_all@naruto CRON[2030]: pam_unix(cron:session): session opened for user root by (uid=0)",
                { 'program': 'cron',
                  'component': 'pam_unix',
                  'type': 'session',
                  'user': 'root' })
        self.aS("<40>Dec 26 10:32:25 s_all@naruto sshd[2263]: pam_unix(ssh:auth): check pass; user unknown",
                { 'program': 'ssh',
                  'component': 'pam_unix',
                  'type': 'auth' })
        # This one should be better handled
        self.aS("<40>Dec 26 10:32:25 s_all@naruto sshd[2263]: pam_unix(ssh:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=localhost",
                { 'program': 'ssh',
                  'component': 'pam_unix',
                  'type': 'auth' })

    def test_lea(self):
        """Test LEA normalization"""
        self.aS("Oct 22 01:27:16 pluto lea: loc=7803|time=1199716450|action=accept|orig=fw1|i/f_dir=inbound|i/f_name=PCnet1|has_accounting=0|uuid=<47823861,00000253,7b040a0a,000007b6>|product=VPN-1 & FireWall-1|__policy_id_tag=product=VPN-1 & FireWall-1[db_tag={9F95C344-FE3F-4E3E-ACD8-60B5194BAAB4};mgmt=fw1;date=1199701916;policy_name=Standard]|src=naruto|s_port=36973|dst=fw1|service=941|proto=tcp|rule=1",
                {'program' : 'lea',
                 'id' : "7803",
                 'action' : "accept",
                 'src' : "naruto",
                 'spt' : "36973",
                 'dst' : "fw1",
                 'dpt' : "941",
                 'protocol' : "tcp",
                 'product' : "VPN-1 & FireWall-1",
                 'dir' : "inbound",
                 'interface' : "PCnet1" })

    def test_apache(self):
        """Test Apache normalization"""
        # Test Common Log Format (CLF) "%h %l %u %t \"%r\" %>s %O"
        self.aS("""Oct 22 01:27:16 pluto apache: 127.0.0.1 - - [20/Jul/2009:00:29:39 +0300] "GET /index/helper/test HTTP/1.1" 200 889""",
                {'program' : "apache",
                 'remote_host' : "127.0.0.1",
                 'request' : 'GET /index/helper/test HTTP/1.1',
                 'response_size' : "889",
                 'date' : datetime(2009, 7, 20, 0, 29, 39), 
                 'body' : '127.0.0.1 - - [20/Jul/2009:00:29:39 +0300] "GET /index/helper/test HTTP/1.1" 200 889'})

        # Test "combined" log format  "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\""
        self.aS('Oct 22 01:27:16 pluto apache: 10.10.4.4 - - [04/Dec/2009:16:23:13 +0100] "GET /tulipe.core.persistent.persistent-module.html HTTP/1.1" 200 2937 "http://10.10.4.86/toc.html" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20090910 Ubuntu/9.04 (jaunty) Shiretoko/3.5.3"',
                {'program' : "apache",
                 'remote_host' : "10.10.4.4",
                 'remote_logname' : "-",
                 'remote_user' : "-",
                 'date' : datetime(2009, 12, 4, 16, 23, 13),
                 'request' : 'GET /tulipe.core.persistent.persistent-module.html HTTP/1.1',
                 'final_request_status' : "200",
                 'response_size' : "2937",
                 'request_header_Referer_contents' : "http://10.10.4.86/toc.html",
                 'request_header_Useragent_contents' : "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20090910 Ubuntu/9.04 (jaunty) Shiretoko/3.5.3",
                 'body' : '10.10.4.4 - - [04/Dec/2009:16:23:13 +0100] "GET /tulipe.core.persistent.persistent-module.html HTTP/1.1" 200 2937 "http://10.10.4.86/toc.html" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.3) Gecko/20090910 Ubuntu/9.04 (jaunty) Shiretoko/3.5.3"'})

        # Test "vhost_combined" log format "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\""
        #TODO: Update apache normalizer to handle this format.


    def test_bind9(self):
        """Test Bind9 normalization"""
        self.aS("Oct 22 01:27:16 pluto named: client 192.168.198.130#4532: bad zone transfer request: 'www.abc.com/IN': non-authoritative zone (NOTAUTH)",
                {'msg_type' : "zone_transfer_bad",
                 'zone' : "www.abc.com",
                 'client_ip' : '192.168.198.130',
                 'class' : 'IN',
                 'program' : 'named'})
        self.aS("Oct 22 01:27:16 pluto named: general: notice: client 10.10.4.4#39583: query: tpf.qa.ifr.lan IN SOA +",
                {'msg_type' : "client_query",
                 'domain' : "tpf.qa.ifr.lan",
                 'category' : "general",
                 'severity' : "notice",
                 'class' : "IN",
                 'client_ip' : "10.10.4.4",
                 'program' : 'named'})
        self.aS("Oct 22 01:27:16 pluto named: createfetch: 126.92.194.77.zen.spamhaus.org A",
                {'msg_type' : "fetch_request",
                 'domain' : "126.92.194.77.zen.spamhaus.org",
                 'program' : 'named'})

if __name__ == "__main__":
    unittest.main()
