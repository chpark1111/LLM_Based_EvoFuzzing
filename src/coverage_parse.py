import coverage
import parse
import string

def coverage_func(arg_list, mode):
    if mode == "max":
        max_output = 0
        for arg in arg_list:
            cov = coverage.Coverage() 
            cov.start()
            try:
                p = parse.Parser(arg, {a:ord(a) for a in string.ascii_lowercase if a != 'e'})
                p.getValue()
                cov.stop()
                cov.save()
                report_output = cov.report()
            except Exception as e:
                cov.stop()
                cov.save()
                report_output = cov.report()
            if report_output > max_output:
                max_output = report_output
        return max_output 
    elif mode == "median":
        median_output = 0
        for arg in arg_list:
            cov = coverage.Coverage() 
            cov.start()
            try:
                p = parse.Parser(arg, {a:ord(a) for a in string.ascii_lowercase if a != 'e'})
                p.getValue()
                cov.stop()
                cov.save()
                report_output = cov.report()
            except Exception as e:
                cov.stop()
                cov.save()
                report_output = cov.report()
            median_output += report_output 
        return median_output / len(arg_list)
    elif mode == "total":
        median_output = 0
        cov = coverage.Coverage()
        cov.start()
        for arg in arg_list:
            try:
                p = parse.Parser(arg, {a:ord(a) for a in string.ascii_lowercase if a != 'e'})
                p.getValue()
            except Exception as e:
                c = 5
        cov.stop()
        cov.save() 
        report_output = cov.report() 
        return report_output
    else:
        raise ValueError("Error")
