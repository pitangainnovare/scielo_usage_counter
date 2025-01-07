import unittest
import datetime

from device_detector import DeviceDetector

from scielo_usage_counter import log


class TestLogParser(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.maxDiff = None
        self.lp = log.LogParser(
            mmdb_path='tests/fixtures/map.mmdb',
            robots_path='tests/fixtures/counter-robots.txt'
        )

    def test_action_is_static_file_true(self):
        static_urls = [
            '/img/revistas/rbp/v26n3/a13img02.gif',
            '/img/revistas/pab/v47n8/a19tab02.jpg',
            '/img/revistas/cr/v47n7//1678-4596-cr-47-07-e20161076-gt2.svg',
            '/applications/scielo-org/js/toolbox.js',
            '/applications/scielo-org/css/public/style-es.css',
            '/applications/scielo-org/js/jquery-1.4.2.min.js',
            '/img/revistas/rbgo/v34n1/a07tab02.jpg',
            'http://www.scielo.br/static/css/scielo-bundle-print.css?v=',
            '/favicon.ico?script=sci_arttext&pid=S0102-35862003000500003',
        ]

        for url in static_urls:
            obtained = self.lp.action_is_static_file(url)
            self.assertTrue(obtained)

    def test_action_static_file_false(self):
        not_static_urls = [
            '/scielo.php?script=sci_arttext&pid=S1806-37132013000500595',
            '/scielo.php?script=sci_arttext&pid=S0101-20612008000500011&lng=en&nrm=iso&tlng=pt',
            '/pdf/rbfis/v12n5/en_a09v12n5.pdf',
            '/google_metrics/get_h5_m5.php?issn=1413-6538&callback=jsonp1530327621274',
            '/scielo.php?script=sci_serial&pid=1678-6971&lng=en&nrm=iso',
            '/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=title&fmt=iso.pft&lang=p',
        ]

        for url in not_static_urls:
            obtained = self.lp.action_is_static_file(url)
            self.assertFalse(obtained)

    def test_action_download_true(self):
        download_urls = [
            '/pdf/abo/v64n3/12518.pdf',
            '/img/revistas/bn/v18n2/1676-0611-bn-1676-0611-BN-2017-0395-suppl3-m01.mp4',
            '/pdf/anp/v71n9B/0004-282X-anp-71-09b-693.pdf',
            '/pdf/rbof/v66n6/a02v66n6.pdf',
            '/pdf/brag/v73n3/pt_aop_brag_0136.pdf',
            '/pdf/bjce/v19n2/10670.pdf',
            '/pdf/%0D/jbpneu/v31n5/27160.pdf',
            '/pdf/ca/v22n5/v22n5a09.pdf',
            '/pdf/fb/v28n5/17673.pdf',
            '/pdf/rbefe/v29n3/1981-4690-rbefe-29-03-00439.pdf',
            '/pdf/rod/v58n4/2175-7860-rod-58-04-0743.pdf',
            '/img/revistas/csc/v22n11/1413-8123-csc-22-11-3537.mp3',
            '/img/revistas/csp/links_ing.doc',
        ]

        for url in download_urls:
            obtained = self.lp.action_is_download(url)
            self.assertTrue(obtained)

    def test_action_download_false(self):
        not_download_urls = [
            '/pdf/rbcpol/n6/n6a04',
            '/favicon.ico?script=sci_arttext&pid=S0102-35862003000500003'
            '/cgi-bin/wxis.exe/iah/?IsisScript=iah/iah.xis&base=title&fmt=iso.pft&lang=p'
        ]

        for url in not_download_urls:
            obtained = self.lp.action_is_download(url)
            self.assertFalse(obtained)

    def test_user_agent_is_bot_true(self):
        ua_bots = [
            "LOCKSS cache",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5 (Applebot/0.1; +http://www.apple.com/go/applebot)",
            "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        ]

        for ua in ua_bots:
            obtained = self.lp.user_agent_is_bot(ua)
            self.assertTrue(obtained)

    def test_user_agent_is_bot_false(self):
        not_ua_bots = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/137.2.345735309 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
        ]

        for ua in not_ua_bots:
            obtained = self.lp.user_agent_is_bot(ua)
            self.assertFalse(obtained)

    def test_format_date(self):
        str_date = '4/Nov/2011:00:05:23'
        str_zone = '-0300'
        test_date = datetime.datetime(2011, 11, 4, 3, 5, 23).strftime('%Y-%m-%d %H:%M:%S')
        obtained_date = self.lp.format_date(str_date, str_zone)

        self.assertEqual(test_date, obtained_date)

    def test_has_valid_path_false(self):
        invalid_paths = [
            '/img/revistas/rbp/v26n3/a13img02.gif',
            '/img/revistas/pab/v47n8/a19tab02.jpg',
        ]

        for vp in invalid_paths:
            obtained = self.lp.has_valid_path(vp)
            self.assertFalse(obtained)

    def test_has_valid_path_true(self):
        valid_paths = [
            '/scielo.php?pid=S1981-77462017005002103&script=sci_arttext',
            '/pdf/rem/v63n4/a07v63n4.pdf',
        ]

        for vp in valid_paths:
            obtained = self.lp.has_valid_path(vp)
            self.assertTrue(obtained)

    def test_has_valid_method_true(self):
        http_methods = [
            'GET',
            'HEAD',
        ]

        for m in http_methods:
            obtained = self.lp.has_valid_method(m)
            self.assertTrue(obtained)

    def test_has_valid_method_false(self):
        http_methods = [
            'POST',
            'PUT',
            'PATCH',
            'DELETE',
            'CONNECT',
            'OPTIONS'
        ]

        for m in http_methods:
            obtained = self.lp.has_valid_method(m)
            self.assertFalse(obtained)

    def test_has_valid_status_true(self):
        http_status = [
            '200',
            '304',
        ]

        for s in http_status:
            obtained = self.lp.has_valid_status(s)
            self.assertTrue(obtained)

    def test_has_valid_status_false(self):
        http_status = [
            '100', '101', '102',
            '201', '202', '203', '204', '205', '206', '207', '208', '226',
            '300', '301', '302', '303', '305', '307', '308',
            '400', '401', '402', '403', '404', '405', '406', '407', '408', '409',
            '410', '411', '412', '413', '414', '415', '416', '417', '418',
            '421', '422', '423', '424', '426', '428', '429', '431', '444', '451', '499',
            '500', '501', '502', '503', '504', '505', '506', '507', '508', '510', '511', '599']

        for s in http_status:
            obtained = self.lp.has_valid_status(s)
            self.assertFalse(obtained)

    def test_status_is_redirect_true(self):
        http_status = ['300', '301', '302', '303', '305', '307', '308']

        for s in http_status:
            obtained = self.lp.status_is_redirect(s)
            self.assertTrue(obtained)

    def test_status_is_redirect_false(self):
        http_status = [
            '100', '101', '102',
            '200', '201', '202', '203', '204', '205', '206', '207', '208', '226',
            '304', '400', '401', '402', '403', '404', '405', '406', '407', '408', '409',
            '410', '411', '412', '413', '414', '415', '416', '417', '418',
            '421', '422', '423', '424', '426', '428', '429', '431', '444', '451', '499',
            '500', '501', '502', '503', '504', '505', '506', '507', '508', '510', '511', '599']

        for s in http_status:
            obtained = self.lp.status_is_redirect(s)
            self.assertFalse(obtained)

    def test_status_is_error_true(self):
        http_status = [
            '400', '401', '402', '403', '404', '405', '406', '407', '408', '409',
            '410', '411', '412', '413', '414', '415', '416', '417', '418',
            '421', '422', '423', '424', '426', '428', '429', '431', '444', '451', '499',
            '500', '501', '502', '503', '504', '505', '506', '507', '508', '510', '511', '599']

        for s in http_status:
            obtained = self.lp.status_is_error(s)
            self.assertTrue(obtained)

    def test_status_is_error_false(self):
        http_status = [
            '100', '101', '102',
            '200', '201', '202', '203', '204', '205', '206', '207', '208', '226',
            '304']

        for s in http_status:
            obtained = self.lp.status_is_error(s)
            self.assertFalse(obtained)

    def test_parse_success(self):
        lp = log.LogParser(
            mmdb_path='tests/fixtures/map.mmdb',
            robots_path='tests/fixtures/counter-robots.txt'
        )
        lp.logfile = 'tests/fixtures/usage.log'
        lp.output = 'tests/fixtures/usage.log.processed'
        lp.stats.output = 'tests/fixtures/usage.log.processed.summary'

        data = lp.parse()
        lp.save(data)

        self.assertEqual(lp.stats.ignored_lines_bot, 3)
        self.assertEqual(lp.stats.ignored_lines_invalid_method, 2)
        self.assertEqual(lp.stats.ignored_lines_http_errors, 3)
        self.assertEqual(lp.stats.ignored_lines_http_redirects, 4)
        self.assertEqual(lp.stats.ignored_lines_invalid_client_name, 0)
        self.assertEqual(lp.stats.ignored_lines_invalid_client_version, 0)
        self.assertEqual(lp.stats.ignored_lines_invalid_geolocation, 2)
        self.assertEqual(lp.stats.ignored_lines_invalid_local_datetime, 1)
        self.assertEqual(lp.stats.ignored_lines_invalid_user_agent, 0)
        self.assertEqual(lp.stats.ignored_lines_static_resources, 185)
        self.assertEqual(lp.stats.lines_parsed, 200)
        self.assertEqual(lp.stats.total_imported_lines, 13)
        self.assertEqual(lp.stats.total_ignored_lines, 187)

    def test_parse_success_cub(self):
        lp = log.LogParser(mmdb_path='tests/fixtures/map.mmdb', robots_path='tests/fixtures/counter-robots.txt')
        lp.logfile = 'tests/fixtures/usage.cub.log'
        lp.output = 'tests/fixtures/usage.cub.log.processed'
        lp.stats.output = 'tests/fixtures/usage.cub.log.processed.summary'

        data = lp.parse()
        lp.save(data)

        self.assertEqual(lp.stats.ignored_lines_bot, 16)
        self.assertEqual(lp.stats.ignored_lines_invalid_method, 0)
        self.assertEqual(lp.stats.ignored_lines_http_errors, 0)
        self.assertEqual(lp.stats.ignored_lines_http_redirects, 0)
        self.assertEqual(lp.stats.ignored_lines_invalid_client_name, 0)
        self.assertEqual(lp.stats.ignored_lines_invalid_client_version, 0)
        self.assertEqual(lp.stats.ignored_lines_invalid_geolocation, 0)
        self.assertEqual(lp.stats.ignored_lines_invalid_local_datetime, 0)
        self.assertEqual(lp.stats.ignored_lines_invalid_user_agent, 0)
        self.assertEqual(lp.stats.ignored_lines_static_resources, 36)
        self.assertEqual(lp.stats.lines_parsed, 48)
        self.assertEqual(lp.stats.total_imported_lines, 2)
        self.assertEqual(lp.stats.total_ignored_lines, 46)

    def test_parse_success_esp(self):
        lp = log.LogParser(mmdb_path='tests/fixtures/map.mmdb', robots_path='tests/fixtures/counter-robots.txt')
        lp.logfile = 'tests/fixtures/usage.esp.log'
        lp.output = 'tests/fixtures/usage.esp.log.processed'
        lp.stats.output = 'tests/fixtures/usage.esp.log.processed.summary'

        data = lp.parse()
        lp.save(data)

        self.assertEqual(lp.stats.ignored_lines_bot, 1)
        self.assertEqual(lp.stats.ignored_lines_invalid_method, 0)
        self.assertEqual(lp.stats.ignored_lines_http_errors, 0)
        self.assertEqual(lp.stats.ignored_lines_http_redirects, 0)
        self.assertEqual(lp.stats.ignored_lines_invalid_client_name, 0)
        self.assertEqual(lp.stats.ignored_lines_invalid_client_version, 0)
        self.assertEqual(lp.stats.ignored_lines_invalid_geolocation, 0)
        self.assertEqual(lp.stats.ignored_lines_invalid_local_datetime, 0)
        self.assertEqual(lp.stats.ignored_lines_invalid_user_agent, 0)
        self.assertEqual(lp.stats.ignored_lines_static_resources, 46)
        self.assertEqual(lp.stats.lines_parsed, 64)
        self.assertEqual(lp.stats.total_imported_lines, 17)
        self.assertEqual(lp.stats.total_ignored_lines, 47)

    def test_parse_line_valid(self):
        line = '89.155.0.1 - - [21/May/2021:11:30:37 -0300] "GET /scielo.php?script=sci_arttext&pid=S0102-69092018000300512 HTTP/1.1" 200 44995 "https://www.google.com/" "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/137.2.345735309 Mobile/15E148 Safari/604.1"'
        obtained = self.lp.parse_line(line)
        self.assertListEqual(obtained, [
            '2021-05-21 14:30:37',
            'Google Search App',
            '137.2.345735309',
            '89.155.0.1',
            '38.7599\t-9.15765',
            '/scielo.php?script=sci_arttext&pid=S0102-69092018000300512'
        ])

    def test_parse_line_valid_with_domain(self):
        line = 'scielo.isciii.es 117.64.147.191 - - [12/Feb/2024:04:23:09 +0100] "GET /scielo.php?lng=es&nrm=i&pid=S0213-91112023000100500&script=sci_abstract HTTP/1.1" 200 18575 "-" "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3432.118 Safari/537.36" 90571 364 18950'
        obtained = self.lp.parse_line(line)
        self.assertListEqual(obtained, [
            '2024-02-12 03:23:09',
            'CH',
            '65.0.3432.118',
            '117.64.147.191',
            '30.6007\t117.925',
            '/scielo.php?lng=es&nrm=i&pid=S0213-91112023000100500&script=sci_abstract'
        ])

    def test_parse_line_invalid(self):
        line = '67.205.129.249 - - [21/May/2021:05:05:16 -0300] "GET /scielo.php?download&pid=S0102-86502014000700465&format=EndNote HTTP/1.1" 200 491 "http://www.scielo.br/scielo.php?script=sci_isoref&pid=S0102-86502014000700465&lng=en" "LOCKSS cache"'
        obtained = self.lp.parse_line(line)
        self.assertListEqual(obtained, [])

    def test_device_detector_client_name_valid(self):
        with open('tests/fixtures/user_agents.txt') as fin:
            user_agents = [a.strip() for a in fin]
            obtained_clients_names = set()
            obtained_clients_versions = set()

            for ua in user_agents:
                device = DeviceDetector(ua).parse()
                client_name = self.lp.format_client_name(device)
                client_version = self.lp.format_client_version(device)
                obtained_clients_names.add(client_name)
                obtained_clients_versions.add(client_version)

            self.assertSetEqual(
                obtained_clients_names,
                {'CM', 'CH', 'SF', '"LOCKSS cache"', 'UNK', 'THEN 1 ELSE', 'Google Search App'}
            )

            self.assertSetEqual(
                obtained_clients_versions,
                {'87.0.4280.101', '0', '90.0.4430.212', '137.2.345735309', '88.0.4324.190', '90.0.4430.210', 'UNK'}
            )


class TestStats(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.stats = log.Stats()

    def test_increment(self):
        for attr, v in [
            ('ignored_lines_static_resources', 10),
            ('ignored_lines_bot', 5),
            ('ignored_lines_invalid_method', 4),
            ('ignored_lines_invalid_user_agent', 3),
            ('ignored_lines_invalid_client_name', 1),
            ('ignored_lines_invalid_client_version', 2),
            ('ignored_lines_invalid_geolocation', 20),
            ('ignored_lines_invalid_local_datetime', 1),
            ('ignored_lines_http_redirects', 6),
            ('ignored_lines_http_errors', 3),
            ('total_ignored_lines', 50),
            ('total_imported_lines', 50),
            ('lines_parsed', 100),
        ]:
            for i in range(v):
                self.stats.increment(attr)

        self.assertEqual(self.stats.ignored_lines_static_resources, 10)
        self.assertEqual(self.stats.ignored_lines_invalid_method, 4)
        self.assertEqual(self.stats.ignored_lines_bot, 5)
        self.assertEqual(self.stats.ignored_lines_invalid_user_agent, 3)
        self.assertEqual(self.stats.ignored_lines_invalid_client_name, 1)
        self.assertEqual(self.stats.ignored_lines_invalid_client_version, 2)
        self.assertEqual(self.stats.ignored_lines_invalid_geolocation, 20)
        self.assertEqual(self.stats.ignored_lines_invalid_local_datetime, 1)
        self.assertEqual(self.stats.ignored_lines_http_redirects, 6)
        self.assertEqual(self.stats.ignored_lines_http_errors, 3)
        self.assertEqual(self.stats.total_ignored_lines, 50)
        self.assertEqual(self.stats.total_imported_lines, 50)
        self.assertEqual(self.stats.lines_parsed, 100)
