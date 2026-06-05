def init(results_log, trx_name, trx_status, trx_time, run_type):
    results_log.write(str(trx_name))
    results_log.write(",")
    results_log.write(str(trx_status))
    results_log.write(",")
    results_log.write(str(trx_time))
    results_log.write(",")
    results_log.write(str(run_type))
    results_log.write("\n")