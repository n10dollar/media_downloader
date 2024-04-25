def prune_dict(ref_dict, features):
    def construct(ref_dict, construct_dict, split):
        # if [a1, a2, ..., an]
        curr_key = split[0]
        rest_keys = split[1:]

        # check if key exists
        if curr_key not in ref_dict:
            print(f"{curr_key} doesn't exist in ref_dict")
            return

        # base of dict: [a]
        if len(split) == 1:
            construct_dict[split[0]] = ref_dict[split[0]]
            return

        # recurse on sub-dicts
        if curr_key not in construct_dict:
            construct_dict[curr_key] = {}
        construct(ref_dict[curr_key], construct_dict[curr_key], rest_keys)

    pruned_dict = {}
    [construct(ref_dict, pruned_dict, feat.split('.')) for feat in features]

    return pruned_dict


def get_urls(engine, media, choices):
    mappings = {
        "yt": lambda choice: media[choice]['link'],
        "sc": lambda choice: getattr(media[choice], 'permalink_url')
    }

    urls = [mappings[engine](choice) for choice in choices]
    return urls
