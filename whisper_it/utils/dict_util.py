from collections import defaultdict


def get_target_lang(lang_results: defaultdict):
    lang_results_sorted = sorted(lang_results.items(), key=lambda x: x[1], reverse=True)
    target_lang = lang_results_sorted[0][0]
    return target_lang
