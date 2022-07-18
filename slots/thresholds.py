from pylon.core.tools import web, log  # pylint: disable=E0611,E0401
from tools import session_project


class Slot:  # pylint: disable=E1101,R0903
    @web.slot('ui_thresholds_content')
    def content(self, context, slot, payload):
        tests = []
        tests = [each[0] for each in tests]
        with context.app.app_context():
            return self.descriptor.render_template(
                'thresholds/content.html',
                tests=tests
            )

    @web.slot('ui_thresholds_scripts')
    def scripts(self, context, slot, payload):
        from pylon.core.tools import log
        log.info('slot: [%s], payload: %s', slot, payload)
        with context.app.app_context():
            return self.descriptor.render_template(
                'thresholds/scripts.html',
            )

    @web.slot('ui_thresholds_styles')
    def styles(self, context, slot, payload):
        from pylon.core.tools import log
        log.info('slot: [%s], payload: %s', slot, payload)
        with context.app.app_context():
            return self.descriptor.render_template(
                'thresholds/styles.html',
            )
