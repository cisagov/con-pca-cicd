from lcgit import lcg
import random


def batch_targets(subscription, sub_levels: dict):
    targets = lcgit_list_randomizer(subscription["target_email_list"])
    avg = len(targets) / float(3)

    batches = []
    last = 0.0
    while last < len(targets):
        batches.append(targets[int(last) : int(last + avg)])
        last += avg

    # if less than one target, the final targets will be in the last batches
    # when single targets they should be put in high group
    sub_levels["low"]["targets"] = batches[0]
    sub_levels["moderate"]["targets"] = batches[1]
    sub_levels["high"]["targets"] = batches[2]

    return sub_levels


def lcgit_list_randomizer(object_list):
    """
    Lcgit List Randomizer.

    This uses lcgit from https://github.com/cisagov/lcgit
    to genrate a random list order
    """
    random_list = []
    for item in lcg(object_list):
        random_list.append(item)
    return random_list


def get_target_available_templates(email, templates):
    # TODO: get templates that a target has not been sent
    # if a target has been sent all templates, return all
    return templates


def assign_targets(sub_level):

    for target in sub_level["targets"]:
        available_templates = get_target_available_templates(
            target["email"], sub_level["template_uuids"]
        )
        selected_template = random.choice(available_templates)
        if not sub_level["template_targets"].get(selected_template):
            sub_level["template_targets"][selected_template] = []

        sub_level["template_targets"][selected_template].append(target)

    return sub_level
