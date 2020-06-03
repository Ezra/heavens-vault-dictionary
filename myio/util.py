''' non-io utilities for myio '''


def toggle_prefix(text, prefix):
    ''' If the string starts with the prefix,
    remove it. Otherwise, insert it.
    '''
    if text.startswith(prefix):
        # 3.8: slice off prefix
        # 3.9: removeprefix()
        result = text[len(prefix):]
    else:
        result = prefix + text
    return result
