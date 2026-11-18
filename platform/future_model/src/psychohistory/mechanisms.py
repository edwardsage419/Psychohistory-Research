"""Application boundary for authenticated, separately approved mechanism runs."""

from . import sources, trajectories
from .degroot import DeGroot
from .plugins import Registry
from .replicator import Replicator
from .v02_execution import RUN_KIND_TRAJECTORY, digest, source_snapshot


registry = Registry()
registry.register(DeGroot())
registry.register(Replicator())


def models():
    return [{**entry, 'research_id': trajectories.RESEARCH[entry['model_id']]}
            for entry in registry.describe()]


class Mechanisms:
    def __init__(self, store, repo):
        self.store = store
        self.repo = repo

    def _source(self, source_id, model_id):
        record = self.store.research_record('sources', source_id)
        if record.get('source_id') != source_id:
            raise ValueError('Source record identity does not match its registration key')
        if record.get('origin') != 'MAIN' or record.get('research_id') != trajectories.RESEARCH[model_id]:
            raise PermissionError('The mechanism requires its pinned MAIN research source')
        return sources.verify(self.repo, record)

    def submit(self, scheduler, model_id, model_version, source_id, parameters, branch_from=None):
        registry.get(model_id, model_version)
        normalized = trajectories.normalize(model_id, model_version, parameters)
        source = self._source(source_id, model_id)
        start = None
        if branch_from is not None:
            parent = self.result(branch_from)['result']
            if (parent['model_id'], parent['model_version'], parent['source']['source_id']) != (
                    model_id, model_version, source_id):
                raise ValueError('Checkpoint belongs to a different mechanism version or source')
            initial_key = 'opinions' if model_id == trajectories.R123 else 'initial'
            if normalized[initial_key] != parent['parameters'][initial_key]:
                raise ValueError('Checkpoint continuation requires the original initial parameter')
            start = {'state': parent['state'], 'snapshot_hash': parent['snapshot']['content_hash']}
        config = {'model_id': model_id, 'model_version': model_version, 'source_id': source_id,
                  'source': source, 'parameters': normalized, 'start': start, 'branch_from': branch_from}
        self.verify_config(config)
        return scheduler.submit_trajectory(config, digest(source_snapshot()))

    def verify_config(self, config):
        model_id = config['model_id']
        expected = trajectories.normalize(model_id, config['model_version'], config['parameters'])
        if expected != config['parameters'] or self._source(config['source_id'], model_id) != config['source']:
            raise ValueError('Trajectory protocol or pinned source changed')
        start = config['start']
        trajectories.validate_start(model_id, start)
        if (start is None) != (config['branch_from'] is None):
            raise ValueError('Trajectory checkpoint and branch lineage differ')
        if start:
            parent = self.result(config['branch_from'])['result']
            if (start != {'state': parent['state'], 'snapshot_hash': parent['snapshot']['content_hash']}
                    or (parent['model_id'], parent['model_version'], parent['source']['source_id']) !=
                    (model_id, config['model_version'], config['source_id'])):
                raise ValueError('Stored checkpoint does not match the completed parent')
            if model_id == trajectories.R132:
                discrete = config['parameters']['method'] == 'eq3'
                if discrete != (parent['time_kind'] == 'discrete-generation'):
                    raise ValueError('Checkpoint and experiment use incompatible time semantics')
            elif parent['state']['state']['time'] + config['parameters']['steps'] > 32:
                raise ValueError('DeGroot continuation exceeds the 32-round limit')

    def run(self, identity):
        run = self.store.get_run(identity)
        if run.get('kind') != RUN_KIND_TRAJECTORY:
            raise KeyError('Unknown mechanism experiment')
        return run

    def result(self, identity):
        run = self.run(identity)
        if run['status'] != 'COMPLETED':
            raise ValueError('No completed trajectory available')
        artifact = self.store.get(run['result_hash'])
        trajectories.validate_result(run, artifact)
        return {'artifact_sha256': run['result_hash'], 'result': artifact}

    def compare(self, left, right, metric='trajectory'):
        lvalue = self.result(left)
        rvalue = self.result(right)
        return {
            **trajectories.compare(lvalue['result'], rvalue['result'], metric),
            'left_artifact_sha256': lvalue['artifact_sha256'],
            'right_artifact_sha256': rvalue['artifact_sha256'],
        }
