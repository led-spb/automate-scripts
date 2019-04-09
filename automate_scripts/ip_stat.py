import ipinfo
import sqlite3


class StatisticsAggregator(object):
    def __init__(self, db_filename='ip_stat.db', api_token=''):
        self._init_database(db_filename)
        self.ipinfo = ipinfo.getHandler(access_token=api_token)
        pass

    def _init_database(self, db_filename):
        scripts = [
            'create table if not exists ip_address('
            '   ip           varchar2(15),'
            '   country      varchar2(5),'
            '   country_name varchar2(50),'
            '   org          varchar2(50),'
            '   hostname     varchar2(500),'
            '   resolved char(1),'
            ''
            '   primary key (ip)'
            ');',

            'create table if not exists counters('
            '   ip      varchar2(15),'
            '   action  varchar2(20),'
            '   updated datetime,'
            '   value   integer,'
            ''
            '   primary key (ip, action),'
            '   foreign key (ip) references ip_address(ip)'
            ');'
        ]

        self.db = sqlite3.connect(db_filename, isolation_level=None)
        for script in scripts:
            try:
                self.db.executescript(script)
            except sqlite3.Error, e:
                pass
        pass

    def add_ip(self, ip):
        cur = self.db.execute('select * from ip_address where ip=?', (ip,))
        row = cur.fetchone()
        if row is None:
            row = (ip, )
            self.db.execute('insert into ip_address(ip) values (?)', row)
        return row

    def aggregate_ip(self, ip, action):
        self.add_ip(ip)
        cur = self.db.execute('select ifnull(max(value)+1, 1) from counters where ip=? and action=?', (ip, action))
        row = cur.fetchone()
        self.db.execute("replace into counters(ip, action, updated, value) values (?, ?, datetime('now'), ?);", (ip, action, row[0]))
        pass

    def resolve_all(self, limit=100):
        cur = self.db.execute('select ip from ip_address where resolved is null limit ?', (limit, ))
        resolve = [x[0] for x in cur.fetchall()]
        for ip in resolve:
            self.resolve(ip)
        print resolve

    def resolve(self, ip):
        try:
            info = self.ipinfo.getDetails(ip)
            info = info.details
            params = (
                info['country'] if 'country' in info else None,
                info['country_name'] if 'country_name' in info else None,
                info['org'] if 'org' in info else None,
                info['hostname'] if 'hostname' in info else None,
                ip
            )
            self.db.execute(
                "update ip_address"
                "   set country=?,"
                "       country_name=?,"
                "       org=?,"
                "       hostname=?,"
                "       resolved='Y'"
                "where ip=?",
                params
            )
        except RuntimeError, e:
            pass
        pass


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', default='ip_stat.db')
    parser.add_argument('--token', default='')
    parser.add_argument('-s', '--skip_resolve', action='store_true', default=False)
    parser.add_argument('action')

    args = parser.parse_args()
    aggregator = StatisticsAggregator(db_filename=args.database, api_token=args.token)
    for line in sys.stdin:
        ip = line.split(' ')[0].strip()
        aggregator.aggregate_ip(ip, args.action)

    if not args.skip_resolve:
        aggregator.resolve_all()
        pass
    pass


if __name__ == '__main__':
    main()