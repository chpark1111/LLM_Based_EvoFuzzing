import coverage
import parse
import string
import subprocess

def coverage_func(arg_list, mode):
    if mode == "max":
        max_value = 0
        for arg in arg_list:
            value = measure_coverage(str(arg))
            if max_value < value:
                max_value = value 
        return max_value
    
    elif mode == "median":
        median = 0
        for arg in arg_list:
            value = measure_coverage(str(arg))
            median += value 
        return median / len(arg_list)

    elif mode == "total":
        total = measure_coverage(arg_list, mode="total")
        return total


def measure_coverage(arg, mode=None):

    if mode == "total":
        cov = coverage.Coverage() 
        cov.start()
        for args in arg:
            try:
                p = parse.Parser(str(args), {a:ord(a) for a in string.ascii_lowercase if a != 'e'})
                p.getValue()

            except Exception as e:
                a = 1
        cov.stop()
        cov.save()
        report_output = cov.report()
        return report_output
    else:
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

        return report_output