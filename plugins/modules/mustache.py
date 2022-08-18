#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from pystache import Renderer

DOCUMENTATION = '''
module: mustache
short_description: mustache templating
description:
  - The mustache module purpose is to parse an mustache template with variables and output the compiled template
author:
  - "kael_k - D'Alcamo Kael (kael-k on gh)"
options:
  template:
    description:
      - mustache template to render
    required: true
    type: str
  values:
    description:
      - values to provide for template rendering
    type: dict
    required: true
  strict:
    description:
      - strict validation on missing tag
    default: false
    type: bool
requirements:
  - python pystache~=0.5.4
'''

EXAMPLES = '''
# Render an "Hello world!"
- kael_k.ansible_mustache.mustache:
    template: "{{ greetings }} {{ target }}!"
    values:
        greetings: Hello
        target: world

# Since is strict validation on missing tag is enabled and
# target is not defined in values, this task will fail
- kael_k.ansible_mustache.mustache:
    template: "{{ greetings }} {{ target }}!"
    strict: true
    values:
        greetings: Hello
'''

RETURN = '''
success:
    description: check if template was compiled successfully
    returned: always
    type: bool
rendered_template:
    description: contains the output of the template rendering
    returned: only if success is True
    type: str
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        template=dict(type='str', required=True),
        values=dict(type='dict', required=True),
        strict=dict(type='bool', default=False)
    )

    result = dict(
        changed=False,
        success=False
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    try:
        renderer = Renderer(missing_tags="strict" if module.params['strict'] else None)
        result['rendered_template'] = renderer.render(module.params['template'], module.params['values'])
        result['success'] = True
    except Exception as e:
        result['exception'] = e
        module.fail_json(msg='Error during template rendering', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
