from ...models.reports import UIReport
from flask import request

from tools import api_tools, LokiLogFetcher


class API(api_tools.APIBase):
    url_params = [
        '<int:project_id>',
        '<string:mode>/<int:project_id>',
    ]

    def get(self, project_id: int, **kwargs):

        report_uid = request.args.get("report_id", None)

        if not report_uid:
            return {"message": ""}, 404

        project = self.module.context.rpc_manager.call.project_get_or_404(project_id=project_id)
        websocket_base_url = LokiLogFetcher.from_project(project).get_websocket_url(project)

        logs_limit = 10000000000

        logs_query = '{report_id="%s",project="%s"}' % (report_uid, project_id)

        return {'websocket_url': f"{websocket_base_url}?query={logs_query}&start=0&limit={logs_limit}"}, 200
