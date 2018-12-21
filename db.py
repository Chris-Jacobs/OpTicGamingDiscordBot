import variables
import mysql.connector

conn = mysql.connector.connect(host =  variables.localIP, user = variables.dbUser, password = variables.dbPassword, database = "optic_discord")
conn.set_charset_collation('utf8mb4', 'utf8mb4_general_ci')
cur = conn.cursor()


async def getMaxes():
    sql = "select max(id), channel from logs group by channel"
    cur.execute(sql)
    return cur.fetchall()

async def addLog(data):
    sql = ''' INSERT INTO logs (id,user,channel,content,date) VALUES(%s,%s,%s,%s,%s) '''
    cur.execute(sql, data)
    conn.commit()
async def getNew(oldId, channel):
    sql = 'select max(id) from logs where channel = "{channel}" and id < "{oldID}"'.format(channel = channel, oldId = oldId)
    cur.execute(sql)
    return cur.fetchone()
async def getRankings(channels, date):
    channelString = "("
    for channel in channels:
        channelString += "'" + channel.id + "',"
    channelString = channelString[:-1]
    channelString += ")"
    sql = 'select user, count(*) as total from logs where channel in {channels} and date > "{date}"  group by user order by total desc limit 10'.format(channels=channelString, date=date)
    cur.execute(sql)
    rankings = cur.fetchall()
    return rankings
async def getUserInfo(channels, date, user):
    channelString = "("
    for channel in channels:
        channelString += "'" + channel.id + "',"
    channelString = channelString[:-1]
    channelString += ")"
    sql = '''
        SELECT
            rank,
            total
        FROM(
            SELECT
                (@row_number := @row_number + 1) AS rank,
                USER,
                total
            FROM(
                SELECT
                    USER,
                    COUNT(*) AS total
                FROM logs
                WHERE
                    channel in {channels}
                    and date > "{date}"
                GROUP BY
                    USER
                ORDER BY
                    total
                DESC
            ) AS t
        ) AS f
        WHERE
            USER = "{user}"
    '''.format(channels=channelString, date=date, user=user)
    cur.execute("SET @row_number=0")
    cur.execute(sql)
    return cur.fetchone()
