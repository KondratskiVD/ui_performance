import json
from typing import Optional, Tuple, List
from pydantic import ValidationError, parse_obj_as
from flask import request
from flask_restful import Resource
from pylon.core.tools import log

from ...models.summary_table_presets import UIPerformanceSummaryTablePreset
from ...models.pd.summary_presets import SummaryPresetsPD

from tools import auth, api_tools


class API(Resource):
    url_params = [
        '<int:project_id>',
        '<int:project_id>/<string:preset_name>',
    ]

    def __init__(self, module):
        self.module = module

    def get(self, project_id: int):
        query = UIPerformanceSummaryTablePreset.query.filter(
            UIPerformanceSummaryTablePreset.project_id == project_id,
        ).all()
        presets = [i.dict() for i in parse_obj_as(List[SummaryPresetsPD], query)]
        return presets, 200

    def post(self, project_id: int):
        try:
            preset = SummaryPresetsPD.validate(request.json).dict()
            preset_db = UIPerformanceSummaryTablePreset(project_id=project_id, **preset)
            preset_db.insert()
            preset = preset_db.to_json()
            return preset, 201
        except ValidationError as e:
            return e.errors(), 400

    def put(self, project_id: int):
        try:
            preset = SummaryPresetsPD.validate(request.json).dict()
            preset_db = UIPerformanceSummaryTablePreset.query.filter(
                UIPerformanceSummaryTablePreset.project_id == project_id,
                UIPerformanceSummaryTablePreset.name == preset['name'],
            ).first()
            preset_db.fields = preset['fields']
            preset_db.commit()
            return preset_db.to_json(), 201
        except ValidationError as e:
            return e.errors(), 400

    def delete(self, project_id: int, preset_name: str):
        if preset_db := UIPerformanceSummaryTablePreset.query.filter(
            UIPerformanceSummaryTablePreset.project_id == project_id,
            UIPerformanceSummaryTablePreset.name == preset_name
            ).one_or_none():
            preset_db.delete()
            preset_db.commit()
        return '', 204
