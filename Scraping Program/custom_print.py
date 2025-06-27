def cprint(text, surpress=False, end_para=None, flush_para=False):
    if surpress is False:
        if end_para is None:
            print(text, flush=flush_para)
        else:
            print(text, end=end_para, flush=flush_para)