"""No implicit time, uncertainty or unit conversion."""
import json
from .contracts import canonical, validate_record, uncertainty

class PopulationAdapter:
    adapter_id, version = 'binary-population-prevalence','1.0.0'
    def adapt(self, record):
        validate_record(record)
        states=record['payload'].get('states',[])
        if record['record_type']!='individual.states' or record['units']!='binary' or not states or len(states)!=len(record['subject_ref']) or any(type(x)!=int or x not in (0,1) for x in states):
            raise ValueError('Incompatible state/unit/identity or missing values')
        result=json.loads(canonical(record))
        result.update(record_type='group.exposure',units='proportion',payload={'prevalence':sum(states)/len(states)},
                      uncertainty=uncertainty('UNKNOWN',target='unobserved real group effect'))
        result['provenance']['adapter']={'id':self.adapter_id,'version':self.version}
        return validate_record(result)
