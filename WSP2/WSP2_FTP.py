import ftplib
from Info import Info

class WSP2_FTP:
    server = "192.168.0.2"
    user = "pi"
    password = "H411#9se5"
    info = Info()
    ftp_local_list = [info.websiteinfo_filename, info.extTemp24hr_filename, info.extRH24hr_filename, info.press24hr_filename,
    info.rain24hr_filename, info.uv24hr_filename, info.vis24hr_filename, info.index_filename, info.gauges_filename,
    info.monthlyrecord_filename, info.record_filename, info.thismonth_filename, info.thisyear_filename, info.today_filename,
    info.trends_filename, info.yesterday_filename, info.wind24hr_filename, info.dir24hr_filename, info.intTemp24hr_filename,
    info.intRH24hr_filename, info.rainrate24hr_filename]

    ftp_remote_list = [info.websiteinfo_filename, "/images/" + info.extTemp24hr_filename, "/images/" + info.extRH24hr_filename,
    "/images/" + info.press24hr_filename,
    "/images/" + info.rain24hr_filename, "/images/" + info.uv24hr_filename, "/images/" + info.vis24hr_filename,
    info.index_filename, info.gauges_filename,
    info.monthlyrecord_filename, info.record_filename, info.thismonth_filename, info.thisyear_filename, info.today_filename,
    info.trends_filename, info.yesterday_filename, "/images/" + info.wind24hr_filename, "/images/" + info.dir24hr_filename,
    "/images/" + info.intTemp24hr_filename,
    "/images/" + info.intRH24hr_filename,
    "/images/" + info.rainrate24hr_filename]

    def do_ftp(self):
        print("Doing FTP")
        session = ftplib.FTP(self.server, self.user, self.password)
        # file = open("websitedata.json", "rb")
        # session.storbinary("STOR websitedata.json", file)
        # file.close()
        # file = open("extTemp24hr.png", "rb")
        # session.storbinary("STOR extTemp24hr.png", file)
        # file.close()
        length = len(self.ftp_local_list)
        for i in range(length):
            print("FTP: " + self.ftp_local_list[i])
            ftp_command = "STOR " + self.ftp_remote_list[i]
            file = open(self.ftp_local_list[i], "rb")
            session.storbinary(ftp_command, file)
            file.close()
        session.quit()
        print("FTP Done.")