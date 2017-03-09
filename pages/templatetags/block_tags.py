from django import template

from contact.forms import ContactForm

register = template.Library()

CONTENT_TEMPLATES = {
    'A': 'pages/blocks/accordion.html',
    'T': 'pages/blocks/text.html',
    'C': 'pages/blocks/contact.html',
    'I': 'pages/blocks/info.html',
    'H': 'pages/blocks/checkbox.html',
}


def blockmaker(block):
    return {
        'block': block,
        'content_template': CONTENT_TEMPLATES[block.blocktype]
    }

register.inclusion_tag('pages/blocks/block.html')(blockmaker)


@register.simple_tag
def get_depth(tree):
    # get the maximum depth for each tree
    depth_map = {}
    for node in tree:
        try:
            if depth_map[node.tree_id] < node.level:
                depth_map[node.tree_id] = node.level
        except KeyError:
            depth_map[node.tree_id] = node.level

    return depth_map


@register.filter
def is_penultimate_level(depth_map, node):
    return depth_map[node.tree_id] == node.level + 1
