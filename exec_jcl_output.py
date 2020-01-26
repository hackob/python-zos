import ftplib
import time

job_list = []
job_log  = []

with open('jclfile.jcl', 'rb') as jcl_file:
    with ftplib.FTP() as ftp:
        ftp.set_debuglevel(0)
        job_is_running = False
        job_ended      = False
        joblog_file_name = 'TEST'
        ftp_message = ftp.connect(host='0.0.0.0', port=21)
        ftp_message = ftp.login(user='_user-name_', passwd='password')
        ftp_message = ftp.sendcmd("SITE FILEtype=JES")
        ftp_message = ftp.storlines(f"STOR jcl.jcl", jcl_file)
        ftp_message = ftp_message.split('\n')
        for ftp_message_line in ftp_message:
            if '250-It is known to JES' in ftp_message_line:
                job_is_running = True
                job_id = ftp_message_line.strip()[-8:]
                joblog_file_name = f"{joblog_file_name}_JOBLOG_{job_id}.txt"
                break
        while job_is_running:
            ftp.dir(job_list.append)
            for job in job_list:
                if job_id in job and 'OUTPUT' in job:
                    job_is_running = False
                    job_ended      = True
            time.sleep(1)
        if job_ended:
            ftp.retrlines(f"RETR {job_id}.X", job_log.append)