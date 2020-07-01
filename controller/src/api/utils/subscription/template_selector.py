"""Tempalte Selector Util."""
# Standard Python Libraries
import logging

# Third-Party Libraries
from api.manager import TemplateManager
from api.utils.tag.tags import get_tags
from api.utils.template.personalize import personalize_template
from api.utils.template.templates import get_email_templates

logger = logging.getLogger()


def get_num_templates_per_batch(diversity_level="moderate"):
    """Get_num_templates_per_batch."""
    numbers = {"high": 8, "moderate": 5, "low": 3}
    return numbers.get(diversity_level, 5)


def get_relevant_templates(templates, subscription, template_count: int):
    """Get_relevant_templates."""
    template_manager = TemplateManager()

    # formats templates for alogrithm
    template_data = {
        t.get("template_uuid"): t.get("descriptive_words") for t in templates
    }

    logger.info(f"Template Data: length - {len(template_data)}")

    # gets order of templates ranked from best to worst
    relevant_templates = template_manager.get_templates(
        url=subscription.get("url"),
        keywords=subscription.get("keywords"),
        template_data=template_data,
    )
    logger.info(f"{relevant_templates} {len(relevant_templates)}")
    return relevant_templates[:template_count]


def batch_templates(templates, num_per_batch, sub_levels: dict):
    """Batch_templates."""
    batches = [
        templates[x : x + num_per_batch]
        for x in range(0, len(templates), num_per_batch)
    ]

    logger.info(f"template_batches={len(batches)}")

    sub_levels["high"]["template_uuids"] = batches[0]
    sub_levels["moderate"]["template_uuids"] = batches[1]
    sub_levels["low"]["template_uuids"] = batches[2]

    return sub_levels


def personalize_templates(customer, subscription, templates, sub_levels: dict):
    """Personalize_templates."""
    # Gets list of tags for personalizing
    tags = get_tags()

    for k in sub_levels.keys():
        # Get actual list of template data
        personalize_list = list(
            filter(
                lambda x: x["template_uuid"] in sub_levels[k]["template_uuids"],
                templates,
            )
        )

        # Send to manager function for personalizing
        personalized_data = personalize_template(
            customer_info=customer,
            template_data=personalize_list,
            sub_data=subscription,
            tag_list=tags,
        )

        # Assign
        sub_levels[k]["personalized_templates"] = personalized_data

    return sub_levels


def personalize_template_batch(customer, subscription, sub_levels: dict):
    """Personalize_template_batch."""
    # Gets list of available email templates
    templates = get_email_templates()

    logger.info(f"Template Count = {len(templates)}")

    # Determines how many templates are available in each batch
    templates_per_batch = get_num_templates_per_batch()
    logger.info(f"{templates_per_batch}")

    # Gets needed amount of relevant templates
    relevant_templates = get_relevant_templates(
        templates, subscription, 3 * templates_per_batch
    )
    logger.info(f"{relevant_templates}")

    # Batches templates
    sub_levels = batch_templates(relevant_templates, templates_per_batch, sub_levels)
    logger.info(f"{sub_levels}")

    # Personalize Templates
    sub_levels = personalize_templates(customer, subscription, templates, sub_levels)
    logger.info(f"{sub_levels}")

    return sub_levels
