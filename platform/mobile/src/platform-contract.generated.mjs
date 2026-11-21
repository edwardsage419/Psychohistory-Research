// Generated from Platform v0.5 by scripts/export-contract.py.
export const stateSchema = {
  "$defs": {
    "CompletionMass": {
      "additionalProperties": false,
      "properties": {
        "duration": {
          "type": "decimal",
          "ge": 0
        },
        "probability": {
          "type": "decimal",
          "ge": 0,
          "le": 1
        }
      },
      "required": [
        "duration",
        "probability"
      ],
      "type": "object"
    },
    "Constraint": {
      "additionalProperties": false,
      "properties": {
        "id": {
          "pattern": "^[a-zA-Z0-9_-]{1,48}$",
          "type": "string"
        },
        "label": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "unit": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "operator": {
          "enum": [
            ">=",
            ">",
            "<=",
            "<"
          ],
          "type": "string"
        },
        "threshold": {
          "type": "decimal"
        },
        "source": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        },
        "horizon": {
          "anyOf": [
            {
              "maxLength": 400,
              "minLength": 1,
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "required": [
        "id",
        "label",
        "unit",
        "operator",
        "threshold"
      ],
      "type": "object"
    },
    "Cutoff": {
      "additionalProperties": false,
      "properties": {
        "at": {
          "type": "decimal",
          "ge": 0
        },
        "inclusive": {
          "type": "boolean"
        },
        "kind": {
          "enum": [
            "fact",
            "estimate",
            "assumption",
            "synthetic",
            "unknown"
          ],
          "type": "string"
        },
        "source": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        }
      },
      "required": [
        "at",
        "inclusive",
        "kind"
      ],
      "type": "object"
    },
    "EvidenceItem": {
      "additionalProperties": false,
      "properties": {
        "id": {
          "pattern": "^[a-zA-Z0-9_-]{1,48}$",
          "type": "string"
        },
        "label": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "kind": {
          "enum": [
            "fact",
            "estimate",
            "assumption",
            "synthetic",
            "unknown"
          ],
          "type": "string"
        },
        "source": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        },
        "verification": {
          "default": "unverified",
          "enum": [
            "user_supplied",
            "user_confirmed",
            "unverified"
          ],
          "type": "string"
        },
        "scope": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        }
      },
      "required": [
        "id",
        "label",
        "kind"
      ],
      "type": "object"
    },
    "InformationInput": {
      "additionalProperties": false,
      "properties": {
        "signals": {
          "items": {
            "$ref": "#/$defs/Signal"
          },
          "maxItems": 24,
          "type": "array"
        },
        "prior": {
          "$ref": "#/$defs/ProbabilityRow"
        },
        "likelihoods": {
          "maxProperties": 24,
          "patternProperties": {
            "^[a-zA-Z0-9_-]{1,48}$": {
              "$ref": "#/$defs/ProbabilityRow"
            }
          },
          "type": "object"
        },
        "cost": {
          "anyOf": [
            {
              "$ref": "#/$defs/Quantity"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "actions_by_signal": {
          "maxProperties": 24,
          "patternProperties": {
            "^[a-zA-Z0-9_-]{1,48}$": {
              "$ref": "#/$defs/SignalActions"
            }
          },
          "type": "object"
        },
        "unrestricted_actions": {
          "default": false,
          "type": "boolean"
        },
        "action_source": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        },
        "parameter_domain": {
          "default": "unknown",
          "enum": [
            "unknown",
            "rectangle",
            "constrained"
          ],
          "type": "string"
        },
        "parameter_domain_source": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        },
        "timing_basis": {
          "anyOf": [
            {
              "maxLength": 400,
              "minLength": 1,
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "fixed_policy": {
          "maxProperties": 24,
          "patternProperties": {
            "^[a-zA-Z0-9_-]{1,48}$": {
              "pattern": "^[a-zA-Z0-9_-]{1,48}$",
              "type": "string"
            }
          },
          "type": "object"
        },
        "verification_source": {
          "anyOf": [
            {
              "maxLength": 400,
              "minLength": 1,
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "type": "object"
    },
    "Investigation": {
      "additionalProperties": false,
      "properties": {
        "mode": {
          "enum": [
            "deterministic",
            "joint",
            "conditional"
          ],
          "type": "string"
        },
        "cost": {
          "anyOf": [
            {
              "$ref": "#/$defs/TimeValue"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "duration": {
          "anyOf": [
            {
              "$ref": "#/$defs/TimeValue"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "kind": {
          "default": "unknown",
          "enum": [
            "fact",
            "estimate",
            "assumption",
            "synthetic",
            "unknown"
          ],
          "type": "string"
        },
        "source": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        },
        "joint": {
          "items": {
            "$ref": "#/$defs/JointMass"
          },
          "maxItems": 384,
          "type": "array"
        },
        "completion_by_state": {
          "maxProperties": 24,
          "patternProperties": {
            "^[a-zA-Z0-9_-]{1,48}$": {
              "items": {
                "$ref": "#/$defs/CompletionMass"
              },
              "maxItems": 24,
              "type": "array"
            }
          },
          "type": "object"
        }
      },
      "required": [
        "mode"
      ],
      "type": "object"
    },
    "JointMass": {
      "additionalProperties": false,
      "properties": {
        "duration": {
          "type": "decimal",
          "ge": 0
        },
        "probability": {
          "type": "decimal",
          "ge": 0,
          "le": 1
        },
        "scenario_id": {
          "pattern": "^[a-zA-Z0-9_-]{1,48}$",
          "type": "string"
        },
        "signal_id": {
          "pattern": "^[a-zA-Z0-9_-]{1,48}$",
          "type": "string"
        }
      },
      "required": [
        "duration",
        "probability",
        "scenario_id",
        "signal_id"
      ],
      "type": "object"
    },
    "Objective": {
      "additionalProperties": false,
      "properties": {
        "id": {
          "pattern": "^[a-zA-Z0-9_-]{1,48}$",
          "type": "string"
        },
        "label": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "unit": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "direction": {
          "enum": [
            "max",
            "min"
          ],
          "type": "string"
        }
      },
      "required": [
        "id",
        "label",
        "unit",
        "direction"
      ],
      "type": "object"
    },
    "Option": {
      "additionalProperties": false,
      "properties": {
        "id": {
          "pattern": "^[a-zA-Z0-9_-]{1,48}$",
          "type": "string"
        },
        "label": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "measurements": {
          "maxProperties": 24,
          "patternProperties": {
            "^[a-zA-Z0-9_-]{1,48}$": {
              "$ref": "#/$defs/Quantity"
            }
          },
          "type": "object"
        },
        "scores": {
          "maxProperties": 16,
          "patternProperties": {
            "^[a-zA-Z0-9_-]{1,48}$": {
              "$ref": "#/$defs/Quantity"
            }
          },
          "type": "object"
        }
      },
      "required": [
        "id",
        "label"
      ],
      "type": "object"
    },
    "PreferenceSnapshot": {
      "additionalProperties": false,
      "properties": {
        "values": {
          "items": {
            "$ref": "#/$defs/PreferenceValue"
          },
          "maxItems": 16,
          "minItems": 1,
          "type": "array"
        },
        "applicability": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "provenance": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "adopted_version_id": {
          "anyOf": [
            {
              "pattern": "^[a-f0-9]{32}$",
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "required": [
        "values",
        "applicability",
        "provenance"
      ],
      "type": "object"
    },
    "PreferenceValue": {
      "additionalProperties": false,
      "properties": {
        "label": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "value": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        }
      },
      "required": [
        "label",
        "value"
      ],
      "type": "object"
    },
    "Probability": {
      "additionalProperties": false,
      "properties": {
        "lower": {
          "anyOf": [
            {
              "type": "decimal",
              "ge": 0,
              "le": 1
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "upper": {
          "anyOf": [
            {
              "type": "decimal",
              "ge": 0,
              "le": 1
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "kind": {
          "enum": [
            "fact",
            "estimate",
            "assumption",
            "synthetic",
            "unknown"
          ],
          "type": "string"
        },
        "source": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        }
      },
      "required": [
        "kind"
      ],
      "type": "object"
    },
    "ProbabilityRow": {
      "maxProperties": 24,
      "patternProperties": {
        "^[a-zA-Z0-9_-]{1,48}$": {
          "$ref": "#/$defs/Probability"
        }
      },
      "type": "object"
    },
    "Proposal": {
      "additionalProperties": false,
      "properties": {
        "field": {
          "enum": [
            "objectives",
            "options",
            "deadline",
            "constraints",
            "preferences"
          ],
          "type": "string"
        },
        "value": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "source": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        }
      },
      "required": [
        "field",
        "value",
        "source"
      ],
      "type": "object"
    },
    "Quantity": {
      "additionalProperties": false,
      "properties": {
        "lower": {
          "anyOf": [
            {
              "type": "decimal"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "upper": {
          "anyOf": [
            {
              "type": "decimal"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "unit": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "kind": {
          "enum": [
            "fact",
            "estimate",
            "assumption",
            "synthetic",
            "unknown"
          ],
          "type": "string"
        },
        "source": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        },
        "horizon": {
          "anyOf": [
            {
              "maxLength": 400,
              "minLength": 1,
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "required": [
        "unit",
        "kind"
      ],
      "type": "object"
    },
    "Reversibility": {
      "additionalProperties": false,
      "properties": {
        "description": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "kind": {
          "enum": [
            "fact",
            "estimate",
            "assumption",
            "synthetic",
            "unknown"
          ],
          "type": "string"
        },
        "source": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        }
      },
      "required": [
        "description",
        "kind"
      ],
      "type": "object"
    },
    "Scenario": {
      "additionalProperties": false,
      "properties": {
        "id": {
          "pattern": "^[a-zA-Z0-9_-]{1,48}$",
          "type": "string"
        },
        "label": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        "utilities": {
          "maxProperties": 24,
          "patternProperties": {
            "^[a-zA-Z0-9_-]{1,48}$": {
              "$ref": "#/$defs/Quantity"
            }
          },
          "type": "object"
        },
        "kind": {
          "enum": [
            "fact",
            "estimate",
            "assumption",
            "synthetic",
            "unknown"
          ],
          "type": "string"
        },
        "source": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        },
        "probability": {
          "anyOf": [
            {
              "type": "decimal",
              "ge": 0,
              "le": 1
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "required": [
        "id",
        "label",
        "kind"
      ],
      "type": "object"
    },
    "Signal": {
      "additionalProperties": false,
      "properties": {
        "id": {
          "pattern": "^[a-zA-Z0-9_-]{1,48}$",
          "type": "string"
        },
        "label": {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        }
      },
      "required": [
        "id",
        "label"
      ],
      "type": "object"
    },
    "SignalActions": {
      "additionalProperties": false,
      "properties": {
        "option_ids": {
          "items": {
            "pattern": "^[a-zA-Z0-9_-]{1,48}$",
            "type": "string"
          },
          "maxItems": 24,
          "type": "array"
        },
        "kind": {
          "enum": [
            "fact",
            "estimate",
            "assumption",
            "synthetic",
            "unknown"
          ],
          "type": "string"
        },
        "source": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        }
      },
      "required": [
        "kind"
      ],
      "type": "object"
    },
    "TimeValue": {
      "additionalProperties": false,
      "properties": {
        "lower": {
          "anyOf": [
            {
              "type": "decimal",
              "ge": 0
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "upper": {
          "anyOf": [
            {
              "type": "decimal",
              "ge": 0
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "kind": {
          "default": "unknown",
          "enum": [
            "fact",
            "estimate",
            "assumption",
            "synthetic",
            "unknown"
          ],
          "type": "string"
        },
        "source": {
          "default": "",
          "maxLength": 400,
          "type": "string"
        }
      },
      "type": "object"
    },
    "TimingAction": {
      "additionalProperties": false,
      "properties": {
        "cutoff": {
          "anyOf": [
            {
              "$ref": "#/$defs/Cutoff"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "switching_cost": {
          "anyOf": [
            {
              "$ref": "#/$defs/TimeValue"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "delay_losses": {
          "maxProperties": 24,
          "patternProperties": {
            "^[a-zA-Z0-9_-]{1,48}$": {
              "$ref": "#/$defs/TimeValue"
            }
          },
          "type": "object"
        },
        "reversibility": {
          "anyOf": [
            {
              "$ref": "#/$defs/Reversibility"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "type": "object"
    },
    "TimingInput": {
      "additionalProperties": false,
      "properties": {
        "confirmed": {
          "default": false,
          "type": "boolean"
        },
        "time_unit": {
          "anyOf": [
            {
              "maxLength": 400,
              "minLength": 1,
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "time_origin": {
          "anyOf": [
            {
              "maxLength": 400,
              "minLength": 1,
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "horizon": {
          "anyOf": [
            {
              "$ref": "#/$defs/Cutoff"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "decision_deadline": {
          "anyOf": [
            {
              "$ref": "#/$defs/Cutoff"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "desired_time": {
          "anyOf": [
            {
              "$ref": "#/$defs/TimeValue"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "predicted_completion": {
          "anyOf": [
            {
              "$ref": "#/$defs/TimeValue"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "wait_duration": {
          "anyOf": [
            {
              "$ref": "#/$defs/TimeValue"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "actions": {
          "maxProperties": 24,
          "patternProperties": {
            "^[a-zA-Z0-9_-]{1,48}$": {
              "$ref": "#/$defs/TimingAction"
            }
          },
          "type": "object"
        },
        "status_quo_option_id": {
          "anyOf": [
            {
              "pattern": "^[a-zA-Z0-9_-]{1,48}$",
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "fallback_option_id": {
          "anyOf": [
            {
              "pattern": "^[a-zA-Z0-9_-]{1,48}$",
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "investigation": {
          "anyOf": [
            {
              "$ref": "#/$defs/Investigation"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        }
      },
      "type": "object"
    },
    "UnderstandingReceipt": {
      "additionalProperties": false,
      "properties": {
        "mode": {
          "enum": [
            "GUIDED_CONFIRMATION",
            "PROVISIONAL_PROVIDER",
            "PROVIDER_FAILED"
          ],
          "type": "string"
        },
        "provider_id": {
          "anyOf": [
            {
              "maxLength": 400,
              "minLength": 1,
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "provider_version": {
          "anyOf": [
            {
              "maxLength": 400,
              "minLength": 1,
              "type": "string"
            },
            {
              "type": "null"
            }
          ],
          "default": null
        },
        "suggestions": {
          "items": {
            "$ref": "#/$defs/Proposal"
          },
          "maxItems": 22,
          "type": "array"
        }
      },
      "required": [
        "mode"
      ],
      "type": "object"
    },
    "Weight": {
      "additionalProperties": false,
      "properties": {
        "lower": {
          "type": "decimal"
        },
        "upper": {
          "type": "decimal"
        }
      },
      "required": [
        "lower",
        "upper"
      ],
      "type": "object"
    }
  },
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "const": "1.0.0",
      "default": "1.0.0",
      "type": "string"
    },
    "decision_id": {
      "pattern": "^[a-f0-9]{32}$",
      "type": "string"
    },
    "revision": {
      "maximum": 1000000,
      "minimum": 1,
      "type": "integer"
    },
    "question": {
      "maxLength": 6000,
      "type": "string",
      "minLength": 1
    },
    "understanding_receipt": {
      "anyOf": [
        {
          "$ref": "#/$defs/UnderstandingReceipt"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "confirmed": {
      "default": false,
      "type": "boolean"
    },
    "deadline": {
      "anyOf": [
        {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "constraints_confirmed": {
      "default": false,
      "type": "boolean"
    },
    "objectives": {
      "items": {
        "$ref": "#/$defs/Objective"
      },
      "maxItems": 16,
      "type": "array"
    },
    "constraints": {
      "items": {
        "$ref": "#/$defs/Constraint"
      },
      "maxItems": 24,
      "type": "array"
    },
    "options": {
      "items": {
        "$ref": "#/$defs/Option"
      },
      "maxItems": 24,
      "type": "array"
    },
    "weights_confirmed": {
      "default": false,
      "type": "boolean"
    },
    "weights": {
      "maxProperties": 16,
      "patternProperties": {
        "^[a-zA-Z0-9_-]{1,48}$": {
          "$ref": "#/$defs/Weight"
        }
      },
      "type": "object"
    },
    "score_basis": {
      "anyOf": [
        {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "score_dependence": {
      "default": "unknown",
      "enum": [
        "unknown",
        "rectangle",
        "shared_additive"
      ],
      "type": "string"
    },
    "score_dependence_source": {
      "anyOf": [
        {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "score_transform": {
      "default": "unknown",
      "enum": [
        "unknown",
        "identity",
        "clip_01"
      ],
      "type": "string"
    },
    "shared_offset_dependence": {
      "default": "unknown",
      "enum": [
        "unknown",
        "rectangle"
      ],
      "type": "string"
    },
    "shared_offsets": {
      "maxProperties": 16,
      "patternProperties": {
        "^[a-zA-Z0-9_-]{1,48}$": {
          "$ref": "#/$defs/Weight"
        }
      },
      "type": "object"
    },
    "scenarios": {
      "items": {
        "$ref": "#/$defs/Scenario"
      },
      "maxItems": 24,
      "type": "array"
    },
    "scenario_basis": {
      "anyOf": [
        {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "scenario_dependence": {
      "default": "unknown",
      "enum": [
        "unknown",
        "rectangle",
        "constrained"
      ],
      "type": "string"
    },
    "scenario_dependence_source": {
      "anyOf": [
        {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "precision_radius": {
      "anyOf": [
        {
          "type": "decimal",
          "ge": 0
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "reference_option_id": {
      "anyOf": [
        {
          "pattern": "^[a-zA-Z0-9_-]{1,48}$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "workflow_version": {
      "const": "0.5.0",
      "default": "0.5.0",
      "type": "string"
    },
    "intent": {
      "anyOf": [
        {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "evidence": {
      "items": {
        "$ref": "#/$defs/EvidenceItem"
      },
      "maxItems": 40,
      "type": "array"
    },
    "information": {
      "anyOf": [
        {
          "$ref": "#/$defs/InformationInput"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "timing": {
      "anyOf": [
        {
          "$ref": "#/$defs/TimingInput"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "preferences": {
      "anyOf": [
        {
          "$ref": "#/$defs/PreferenceSnapshot"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "intended_option_id": {
      "anyOf": [
        {
          "pattern": "^[a-zA-Z0-9_-]{1,48}$",
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    },
    "plan_note": {
      "anyOf": [
        {
          "maxLength": 400,
          "minLength": 1,
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null
    }
  },
  "required": [
    "decision_id",
    "revision",
    "question"
  ],
  "type": "object"
};
export const modelCards = [
  {
    "model_id": "c028_interval_feasibility",
    "version": "1.0.0",
    "title": "C028 区间硬约束",
    "applicability": "用户确认单调硬约束和有限候选行动。",
    "inputs": "候选方案、每项硬约束阈值与区间，或用户明确确认无硬约束。",
    "outputs": "每项 CERTAIN_PASS、CERTAIN_FAIL、POSSIBLE 或 UNKNOWN，及整体可行性。",
    "units": "阈值与上下界同单位、同时间范围。",
    "assumptions": "可信闭区间。阈值为单调不等式，多个条件使用逻辑与。",
    "uncertainty": "逻辑界限，无概率含义。",
    "sources": [
      "research/decision_methods/C028_INTERVAL_HARD_CONSTRAINT_FEASIBILITY_2026-11-20.md"
    ],
    "failure_conditions": "未知边界、单位或时间冲突、来源缺失、未确认底线。",
    "replay": "tests/test_decision_hub.py 的等号、单位、未知、合取与来源用例。",
    "baseline": "用区间中点比较阈值，可把跨阈值区间误标为确定可行。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "5909e1ae58dbfcb0d14d00c0561726ecb35e1028"
  },
  {
    "model_id": "comparability",
    "version": "1.0.0",
    "title": "目标得分可比性",
    "applicability": "至少两个通过硬约束筛查的方案，已列明目标方向与单位。",
    "inputs": [
      "通过筛查的方案",
      "目标与单位",
      "得分区间、证据类型和来源"
    ],
    "outputs": [
      "逐方案逐目标的可比性检查",
      "数据缺口"
    ],
    "units": "沿用各目标的单位。",
    "assumptions": "同一目标采用同一观察口径。跨目标加权需额外确认效用刻度。",
    "uncertainty": "缺失、未知证据或单位不一致均显示待核对。",
    "sources": [
      "research/decision_methods/C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md"
    ],
    "failure_conditions": "缺少可行方案或目标时无法比较。",
    "replay": "按目标逐项复核得分区间、单位和来源。",
    "baseline": "逐一并列查看各目标原始记录。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "5909e1ae58dbfcb0d14d00c0561726ecb35e1028"
  },
  {
    "model_id": "pareto",
    "version": "1.0.0",
    "title": "Pareto 支配比较",
    "applicability": "通过硬约束的方案可按各目标独立比较。",
    "inputs": [
      "目标方向",
      "可核对的得分或区间"
    ],
    "outputs": [
      "保证支配关系",
      "未被证明支配的方案集合"
    ],
    "units": "每个目标沿用自身单位。",
    "assumptions": "若所有目标均保证不差且至少一个目标保证更好，则形成支配。共同误差使用名义点值进行这一层的比较。",
    "uncertainty": "得分区间端点用于保守支配判断。重叠或证据缺口可使比较待定。",
    "sources": [
      "research/decision_methods/C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md"
    ],
    "failure_conditions": "指标口径或单位不一致时，相应比较待定。",
    "replay": "按目标方向核对两方案的最差和最好得分。",
    "baseline": "列出各目标上的优劣。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "5909e1ae58dbfcb0d14d00c0561726ecb35e1028"
  },
  {
    "model_id": "weight_sensitivity",
    "version": "1.0.0",
    "title": "已确认权重的敏感性",
    "applicability": "用户确认共同基数刻度、补偿和权重含义，比较固定名义分数。",
    "inputs": [
      "目标方向和点得分",
      "用户确认的权重上下界",
      "共同效用刻度依据"
    ],
    "outputs": [
      "精确效用差区间",
      "严格领先条件",
      "边界权重组合"
    ],
    "units": "共同效用单位。",
    "assumptions": "加权可加，权重非负且和为 1。",
    "uncertainty": "权重以可行集合表达，得分固定为名义值。",
    "sources": [
      "research/decision_methods/C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md"
    ],
    "failure_conditions": "未确认权重或共同刻度，权重区间不可行，或得分未知或为区间。",
    "replay": "按效用差系数顺序将剩余权重分配到上界，复算极值。",
    "baseline": "在任一确认的单组权重下比较固定得分。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "5909e1ae58dbfcb0d14d00c0561726ecb35e1028"
  },
  {
    "model_id": "c034_joint_robustness",
    "version": "1.0.0",
    "title": "C034 权重与得分联合稳健性",
    "applicability": "两个越高越好的共同基数效用目标，已确认权重和联合误差结构及变换。",
    "inputs": [
      "点得分或矩形区间",
      "用户确认的权重范围",
      "误差结构和依据",
      "得分变换",
      "共同偏移区间"
    ],
    "outputs": [
      "效用差界与严格偏好条件",
      "可证实的边界情形",
      "条件性信息缺口"
    ],
    "units": "共同效用单位。",
    "assumptions": "权重范围与得分误差集合可任意组合。共同偏移后的得分若截断至 0–1，则检查转折点。矩形区间使用变换后的效用。",
    "uncertainty": "外界包含零时，相关信息不足。精确区间包含零时，无法证明任一方严格领先。",
    "sources": [
      "research/decision_methods/C034_WEIGHT_SCORE_JOINT_ROBUSTNESS_CERTIFICATE_2026-11-20.md",
      "research/decision_methods/C034_ADDENDUM_SHARED_SCORE_ERROR_CANCELLATION_2026-11-20.md",
      "research/decision_methods/C034_ADDENDUM_CLIPPING_BREAKS_SHARED_ERROR_CANCELLATION_2026-11-20.md",
      "research/decision_methods/C004_DYNAMIC_UTILITY_MULTI_OBJECTIVE_ROBUST_2026-10-27.md"
    ],
    "failure_conditions": "依据不足、变换未知、量尺不可比、权重不可行或误差超出所列模型时，联合证据待定。",
    "replay": "矩形误差比较对立端点，恒等变换抵消共同偏移，截断检查端点和转折点并对权重取极值。",
    "baseline": "固定名义得分的权重比较，以及逐目标的 Pareto 比较。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "5909e1ae58dbfcb0d14d00c0561726ecb35e1028"
  },
  {
    "model_id": "C029",
    "version": "1.0.0",
    "title": "情景最小最大后悔值",
    "applicability": "通过硬约束且已确认同一时限、效用量尺及完整点值的有限情景比较。",
    "inputs": [
      "可行方案",
      "情景",
      "各情景的点值效用",
      "用户选择的参照方案（可选）"
    ],
    "outputs": [
      "后悔值矩阵",
      "最小最大后悔方案",
      "各情景最优方案",
      "最大最小效用基线",
      "参照方案的条件性预知增益"
    ],
    "units": "用户确认的共用效用单位。",
    "assumptions": [
      "效用越高越好。",
      "比较基于所列固定情景，结论取决于情景覆盖。"
    ],
    "uncertainty": "不需要情景概率。只在承诺前完全预知情景、且允许改选的假设下显示逐情景效用增益。",
    "sources": [
      "research/decision_methods/C029_SCENARIO_MINIMAX_REGRET_INFORMATION_BOUNDARY_2026-11-20.md"
    ],
    "failure_conditions": [
      "缺失点值、来源或共同单位",
      "情景、时限或效用尺度未确认",
      "依硬约束通过的方案为空"
    ],
    "replay": "逐情景计算可行方案的最大效用，再减去各方案效用，对每个方案取情景最大值。",
    "baseline": "比较各方案最小效用，并在指定参照时计算对该方案的逐情景增益。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "5909e1ae58dbfcb0d14d00c0561726ecb35e1028"
  },
  {
    "model_id": "C030",
    "version": "1.0.0",
    "title": "区间情景后悔值",
    "applicability": "效用可表示为共用标尺上的闭区间，且区间内至少存在一个联合可行取值。",
    "inputs": [
      "可行方案",
      "情景",
      "闭区间效用",
      "区间依赖关系及来源"
    ],
    "outputs": [
      "后悔值区间矩阵",
      "最大后悔值区间",
      "最小上界方案",
      "严格分离的比较"
    ],
    "units": "用户确认的共用效用单位。",
    "assumptions": [
      "效用越高越好。",
      "矩形独立性决定各极值能否分别达到。"
    ],
    "uncertainty": "仅在声明有来源的矩形独立性下报告可达极值。其他情况为保守外界，区间接触时严格排序仍为 UNKNOWN。",
    "sources": [
      "research/decision_methods/C030_INTERVAL_BOUNDED_SCENARIO_REGRET_2026-11-20.md",
      "research/decision_methods/C029_SCENARIO_MINIMAX_REGRET_INFORMATION_BOUNDARY_2026-11-20.md"
    ],
    "failure_conditions": [
      "缺失、倒置或不可比的效用区间",
      "情景、来源、时限或效用尺度未确认",
      "不存在一致的联合取值"
    ],
    "replay": "排除自身，分别比较对手下界与自身上界、对手上界与自身下界，再以零截断并跨情景取最大值。",
    "baseline": "假设每个效用取区间中点，计算 C029 作为比较。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "5909e1ae58dbfcb0d14d00c0561726ecb35e1028"
  },
  {
    "model_id": "C031",
    "version": "1.0.0",
    "title": "后悔值排序的效用精度阈值",
    "applicability": "两个及以上可行方案有可比较的情景效用中心，并给出假设统一半径。",
    "inputs": [
      "效用点数据作为中心",
      "假设统一半径",
      "区间依赖关系及来源"
    ],
    "outputs": [
      "最大后悔值区间",
      "最小上界方案",
      "严格分离阈值",
      "适用时的合成反例"
    ],
    "units": "统一半径与后悔值采用共用效用单位。",
    "assumptions": [
      "所有情景的效用单元格按同一个非负半径展开。",
      "充要结论仅适用于来源卡的原始矩形合成几何与半径范围。"
    ],
    "uncertainty": "按区间外界给出严格比较的充分条件。阈值衡量假设效用精度，合成反例依赖声明的矩形联合取值。",
    "sources": [
      "research/decision_methods/C031_REGRET_PRECISION_THRESHOLD_SYNTHETIC_2026-11-20.md",
      "research/decision_methods/C031_ADDENDUM_SHARP_THRESHOLD_COUNTEREXAMPLE_2026-11-20.md",
      "research/decision_methods/C030_INTERVAL_BOUNDED_SCENARIO_REGRET_2026-11-20.md"
    ],
    "failure_conditions": [
      "缺失或不可比的点值中心",
      "负或缺失半径",
      "通过硬约束的方案少于两个"
    ],
    "replay": "由中心加减统一半径得到区间。按 C030 计算，再求领先方案上界严格低于各对手下界的半径范围。",
    "baseline": "以点值中心计算 C029，留存所有并列候选。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "5909e1ae58dbfcb0d14d00c0561726ecb35e1028"
  },
  {
    "model_id": "voi_point",
    "version": "1.0.0",
    "title": "点值调查信息价值",
    "applicability": "有限互斥状态和调查信号，有明确来源的概率、行动集合、可比较的点效用和调查成本。",
    "inputs": [
      "先验和条件信号概率",
      "通过硬约束的立即行动和调查后行动",
      "效用、时限和成本的证据"
    ],
    "outputs": [
      "立即行动",
      "信号后行动及概率",
      "EVSI、完全信息上界与调查净优势"
    ],
    "units": "概率为比例，效用和调查成本采用确认的同一量纲。",
    "assumptions": "调查在行动前完成，无等待损失。行动受限时显示相对免费基线的调查收益差。",
    "uncertainty": "仅比较当前问题的期望效用。不为区间参数补造分布。用户提交的核对声明不等于系统独立核验，条件计算与合成演示分别标明。",
    "sources": [
      "research/decision_methods/VOI_IMPERFECT_BINARY_SIGNAL_METHOD_CARD_2026-11-20.md",
      "research/decision_methods/VOI_ASYMMETRIC_BINARY_SIGNAL_EXTENSION_2026-11-20.md",
      "research/decision_methods/VOI_REVERSED_BINARY_SIGNAL_LABEL_INVARIANCE_2026-11-20.md",
      "research/decision_methods/VOI_ASYMMETRIC_SIGNAL_PRIOR_SWITCH_INTERVAL_2026-11-20.md",
      "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md"
    ],
    "failure_conditions": "缺少来源或行动，归一化冲突，效用或成本不可比较，时序未确认，或超出声明的参数范围。",
    "replay": "根据先验和条件信号概率计算联合概率，逐信号最大化联合效用。",
    "baseline": "同一参数点下，从全部通过硬约束的立即行动中选取期望效用最大的免费行动。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "f6115556ecf3ee6eed8f96b043497a51e5f1bf9a",
    "depends_on": [
      "c028_interval_feasibility@1.0.0"
    ]
  },
  {
    "model_id": "voi_oracle_bounds",
    "version": "1.0.0",
    "title": "按参数各自最优的调查优势区间",
    "applicability": "有限互斥状态和调查信号，有明确来源的概率、行动集合、可比较的点效用和调查成本。",
    "inputs": [
      "先验和条件信号概率",
      "通过硬约束的立即行动和调查后行动",
      "效用、时限和成本的证据"
    ],
    "outputs": [
      "精确净优势上下界",
      "可复算的极值见证"
    ],
    "units": "概率为比例，效用和调查成本采用确认的同一量纲。",
    "assumptions": "有据的概率行间直积与行内归一化。每个参数点允许选不同调查策略。",
    "uncertainty": "仅比较当前问题的期望效用。不为区间参数补造分布。用户提交的核对声明不等于系统独立核验，条件计算与合成演示分别标明。",
    "sources": [
      "research/decision_methods/VOI_PRIOR_INTERVAL_ROBUST_COST_2026-11-21.md",
      "research/decision_methods/VOI_IMPERFECT_BINARY_SIGNAL_METHOD_CARD_2026-11-20.md",
      "research/decision_methods/VOI_ASYMMETRIC_BINARY_SIGNAL_EXTENSION_2026-11-20.md",
      "research/decision_methods/VOI_REVERSED_BINARY_SIGNAL_LABEL_INVARIANCE_2026-11-20.md",
      "research/decision_methods/VOI_ASYMMETRIC_SIGNAL_PRIOR_SWITCH_INTERVAL_2026-11-20.md",
      "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md"
    ],
    "failure_conditions": "缺少来源或行动，归一化冲突，效用或成本不可比较，时序未确认，或超出声明的参数范围。",
    "replay": "将参数区间写成联合概率的线性约束，按立即行动和信号行动的切换面分段求界。",
    "baseline": "同一参数点下，从全部通过硬约束的立即行动中选取期望效用最大的免费行动。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "f6115556ecf3ee6eed8f96b043497a51e5f1bf9a",
    "depends_on": [
      "c028_interval_feasibility@1.0.0"
    ]
  },
  {
    "model_id": "voi_fixed_policy",
    "version": "1.0.0",
    "title": "固定调查规则的逐参数优势",
    "applicability": "有限互斥状态和调查信号，有明确来源的概率、行动集合、可比较的点效用和调查成本。",
    "inputs": [
      "先验和条件信号概率",
      "通过硬约束的立即行动和调查后行动",
      "效用、时限和成本的证据"
    ],
    "outputs": [
      "固定规则",
      "精确净优势上下界",
      "对各免费行动的最小优势"
    ],
    "units": "概率为比例，效用和调查成本采用确认的同一量纲。",
    "assumptions": "事前确认同一可执行映射，参数变化时规则保持固定。",
    "uncertainty": "仅比较当前问题的期望效用。不为区间参数补造分布。用户提交的核对声明不等于系统独立核验，条件计算与合成演示分别标明。",
    "sources": [
      "research/decision_methods/VOI_FIXED_POLICY_UNIFORM_DOMINANCE_2026-11-21.md",
      "research/decision_methods/VOI_JOINT_SIGNAL_QUALITY_ROBUST_FIXED_POLICY_2026-11-21.md"
    ],
    "failure_conditions": "缺少来源或行动，归一化冲突，效用或成本不可比较，时序未确认，或超出声明的参数范围。",
    "replay": "按立即行动的切换面分段，以同一调查规则计算各参数点的净优势。",
    "baseline": "同一参数点下，从全部通过硬约束的立即行动中选取期望效用最大的免费行动。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "f6115556ecf3ee6eed8f96b043497a51e5f1bf9a",
    "depends_on": [
      "c028_interval_feasibility@1.0.0"
    ]
  },
  {
    "model_id": "voi_maximin",
    "version": "1.0.0",
    "title": "确定性规则的最大最小调查优势",
    "applicability": "有限互斥状态和调查信号，有明确来源的概率、行动集合、可比较的点效用和调查成本。",
    "inputs": [
      "先验和条件信号概率",
      "通过硬约束的立即行动和调查后行动",
      "效用、时限和成本的证据"
    ],
    "outputs": [
      "完整确定性映射集合",
      "每项规则最坏净优势",
      "含并列的最优规则"
    ],
    "units": "概率为比例，效用和调查成本采用确认的同一量纲。",
    "assumptions": "事前承诺确定性映射，目标为最大化最小逐参数优势。",
    "uncertainty": "仅比较当前问题的期望效用。不为区间参数补造分布。用户提交的核对声明不等于系统独立核验，条件计算与合成演示分别标明。",
    "sources": [
      "research/decision_methods/VOI_FOUR_SIGNAL_POLICIES_MAXIMIN_CERTIFICATE_2026-11-21.md",
      "research/decision_methods/VOI_JOINT_SIGNAL_QUALITY_ROBUST_FIXED_POLICY_2026-11-21.md"
    ],
    "failure_conditions": "缺少来源或行动，归一化冲突，效用或成本不可比较，时序未确认，或超出声明的参数范围。",
    "replay": "枚举可执行确定性策略和概率行端点，用多重仿射比较精确求各规则最坏优势。",
    "baseline": "同一参数点下，从全部通过硬约束的立即行动中选取期望效用最大的免费行动。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "f6115556ecf3ee6eed8f96b043497a51e5f1bf9a",
    "depends_on": [
      "c028_interval_feasibility@1.0.0"
    ]
  },
  {
    "model_id": "voi_randomized_certificate",
    "version": "1.0.0",
    "title": "固定随机规则的上下界证书",
    "applicability": "有限互斥状态和调查信号，有明确来源的概率、行动集合、可比较的点效用和调查成本。",
    "inputs": [
      "先验和条件信号概率",
      "通过硬约束的立即行动和调查后行动",
      "效用、时限和成本的证据"
    ],
    "outputs": [
      "确定性下界",
      "随机规则上界见证",
      "覆盖的策略范围和证书状态"
    ],
    "units": "概率为比例，效用和调查成本采用确认的同一量纲。",
    "assumptions": "随机化只依赖所见信号，所有概率在事前固定，期望效用对混合行动线性。",
    "uncertainty": "仅比较当前问题的期望效用。不为区间参数补造分布。用户提交的核对声明不等于系统独立核验，条件计算与合成演示分别标明。",
    "sources": [
      "research/decision_methods/VOI_RANDOMIZED_SIGNAL_POLICY_MINIMAX_BOUND_2026-11-21.md",
      "research/decision_methods/VOI_FOUR_SIGNAL_POLICIES_MAXIMIN_CERTIFICATE_2026-11-21.md"
    ],
    "failure_conditions": "缺少来源或行动，归一化冲突，效用或成本不可比较，时序未确认，或超出声明的参数范围。",
    "replay": "比较确定性最大最小值与单点最优响应上界。仅在上下界相等时认证精确值。",
    "baseline": "同一参数点下，从全部通过硬约束的立即行动中选取期望效用最大的免费行动。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "f6115556ecf3ee6eed8f96b043497a51e5f1bf9a",
    "depends_on": [
      "c028_interval_feasibility@1.0.0"
    ]
  },
  {
    "model_id": "timing_actions",
    "version": "1.0.0",
    "title": "立即行动、等待与维持现状",
    "applicability": "时机已确认、使用共同起点和分析时域，按所列情景对比可执行方案。",
    "inputs": [
      "有来源的期限与时间变量",
      "可行方案的情景效用",
      "实际换转成本",
      "情景内延迟损失"
    ],
    "outputs": [
      "情景效用与未被支配的策略",
      "时间可行性",
      "现状标签与可逆性依据"
    ],
    "units": "输入指定的时间单位及共同效用量尺。",
    "assumptions": [
      "延迟损失按情景与动作单独计量，固定等待期间无新信息。",
      "明确填有时机规则的方案沿用共同时域与共同截止，并应用已填报的单独截止。"
    ],
    "uncertainty": "没有概率时逐情景比较，列出 UNKNOWN 并保留实际换转费用。",
    "sources": [
      "research/decision_methods/C009_OPTION_VALUE_INFORMATION_REVERSIBILITY_2026-11-01.md",
      "research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PERSONAL_COMPLETION_TIME_FORECAST_BOUNDARY_2026-11-21.md",
      "research/decision_methods/SAMUELSON_ZECKHAUSER_1988_STATUS_QUO_FRAMING_AUDIT_2026-11-20.md",
      "research/decision_methods/TVERSKY_SHAFIR_1992_CONFLICT_DEFERRAL_OPTION_SET_BOUNDARY_2026-11-21.md"
    ],
    "failure_conditions": "硬约束可行性、效用、行动时机或来源不明时，对应策略待核对。",
    "replay": "在共享时间轴上检查每个动作的期限，逐情景从效用扣除换转成本及随时间增加的延迟损失。",
    "baseline": "以相同标签和真实成本逐情景比较立即采取的行动。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "f6115556ecf3ee6eed8f96b043497a51e5f1bf9a",
    "depends_on": [
      "c028_interval_feasibility@1.0.0"
    ],
    "candidate_scope": "structural"
  },
  {
    "model_id": "timing_investigation",
    "version": "1.0.0",
    "title": "有截止期限的调查信息价值",
    "applicability": "调查完成才观察到时长与信号，有限概率已注明来源，给定可执行范围与共用效用标尺。",
    "inputs": [
      "固定调查费",
      "确定时长、联合概率或基于证据的条件因式分解",
      "行动窗口与情景延迟损失"
    ],
    "outputs": [
      "立即行动基线",
      "观察后最优行动",
      "净调查价值",
      "确定时长的优势边界"
    ],
    "units": "输入指定的时间单位及共同效用量尺。",
    "assumptions": [
      "调查前承诺，调查中途不可取消。固定成本与每个动作的线性机会损失分开计量。",
      "条件模式明确使用给定情景后的完成时间与信号条件独立。依赖关系未知时需直接联合证据。",
      "调查完成后先观察完成时刻与信号。默认考虑通过硬约束与期限检查的所有行动，并应用已填报的信号后限制。"
    ],
    "uncertainty": "保留合成与有来源的证据类型。正概率分支没有可执行行动时，净值为 UNKNOWN。",
    "sources": [
      "research/decision_methods/VOI_DELAY_DEADLINE_OPPORTUNITY_COST_2026-11-21.md",
      "research/decision_methods/VOI_RANDOM_COMPLETION_TIME_DEADLINE_2026-11-21.md",
      "research/decision_methods/VOI_COMPLETION_TIME_STATE_DEPENDENCE_DEADLINE_2026-11-21.md"
    ],
    "failure_conditions": "概率、时间口径或效用来源缺失，或决策者不能在行动前观察到完成时刻和信号。",
    "replay": "按观察到的时间与信号分组枚举联合事件，逐组筛除到期行动，比较后验加权效用并扣除调查费。",
    "baseline": "在同一情景边际概率下，比较不调查且立即执行的最优行动。",
    "evidence": "SYNTHETIC_ENGINEERING_CANDIDATE",
    "permissions": "本地计算。链接为项目研究记录。",
    "source_baseline": "f6115556ecf3ee6eed8f96b043497a51e5f1bf9a",
    "depends_on": [
      "c028_interval_feasibility@1.0.0"
    ],
    "candidate_scope": "structural"
  }
];
export const casefoldOverrides = {
  "µ": "μ",
  "ß": "ss",
  "ŉ": "ʼn",
  "ſ": "s",
  "ǰ": "ǰ",
  "ͅ": "ι",
  "ΐ": "ΐ",
  "ΰ": "ΰ",
  "ς": "σ",
  "ϐ": "β",
  "ϑ": "θ",
  "ϕ": "φ",
  "ϖ": "π",
  "ϰ": "κ",
  "ϱ": "ρ",
  "ϵ": "ε",
  "և": "եւ",
  "Ꭰ": "Ꭰ",
  "Ꭱ": "Ꭱ",
  "Ꭲ": "Ꭲ",
  "Ꭳ": "Ꭳ",
  "Ꭴ": "Ꭴ",
  "Ꭵ": "Ꭵ",
  "Ꭶ": "Ꭶ",
  "Ꭷ": "Ꭷ",
  "Ꭸ": "Ꭸ",
  "Ꭹ": "Ꭹ",
  "Ꭺ": "Ꭺ",
  "Ꭻ": "Ꭻ",
  "Ꭼ": "Ꭼ",
  "Ꭽ": "Ꭽ",
  "Ꭾ": "Ꭾ",
  "Ꭿ": "Ꭿ",
  "Ꮀ": "Ꮀ",
  "Ꮁ": "Ꮁ",
  "Ꮂ": "Ꮂ",
  "Ꮃ": "Ꮃ",
  "Ꮄ": "Ꮄ",
  "Ꮅ": "Ꮅ",
  "Ꮆ": "Ꮆ",
  "Ꮇ": "Ꮇ",
  "Ꮈ": "Ꮈ",
  "Ꮉ": "Ꮉ",
  "Ꮊ": "Ꮊ",
  "Ꮋ": "Ꮋ",
  "Ꮌ": "Ꮌ",
  "Ꮍ": "Ꮍ",
  "Ꮎ": "Ꮎ",
  "Ꮏ": "Ꮏ",
  "Ꮐ": "Ꮐ",
  "Ꮑ": "Ꮑ",
  "Ꮒ": "Ꮒ",
  "Ꮓ": "Ꮓ",
  "Ꮔ": "Ꮔ",
  "Ꮕ": "Ꮕ",
  "Ꮖ": "Ꮖ",
  "Ꮗ": "Ꮗ",
  "Ꮘ": "Ꮘ",
  "Ꮙ": "Ꮙ",
  "Ꮚ": "Ꮚ",
  "Ꮛ": "Ꮛ",
  "Ꮜ": "Ꮜ",
  "Ꮝ": "Ꮝ",
  "Ꮞ": "Ꮞ",
  "Ꮟ": "Ꮟ",
  "Ꮠ": "Ꮠ",
  "Ꮡ": "Ꮡ",
  "Ꮢ": "Ꮢ",
  "Ꮣ": "Ꮣ",
  "Ꮤ": "Ꮤ",
  "Ꮥ": "Ꮥ",
  "Ꮦ": "Ꮦ",
  "Ꮧ": "Ꮧ",
  "Ꮨ": "Ꮨ",
  "Ꮩ": "Ꮩ",
  "Ꮪ": "Ꮪ",
  "Ꮫ": "Ꮫ",
  "Ꮬ": "Ꮬ",
  "Ꮭ": "Ꮭ",
  "Ꮮ": "Ꮮ",
  "Ꮯ": "Ꮯ",
  "Ꮰ": "Ꮰ",
  "Ꮱ": "Ꮱ",
  "Ꮲ": "Ꮲ",
  "Ꮳ": "Ꮳ",
  "Ꮴ": "Ꮴ",
  "Ꮵ": "Ꮵ",
  "Ꮶ": "Ꮶ",
  "Ꮷ": "Ꮷ",
  "Ꮸ": "Ꮸ",
  "Ꮹ": "Ꮹ",
  "Ꮺ": "Ꮺ",
  "Ꮻ": "Ꮻ",
  "Ꮼ": "Ꮼ",
  "Ꮽ": "Ꮽ",
  "Ꮾ": "Ꮾ",
  "Ꮿ": "Ꮿ",
  "Ᏸ": "Ᏸ",
  "Ᏹ": "Ᏹ",
  "Ᏺ": "Ᏺ",
  "Ᏻ": "Ᏻ",
  "Ᏼ": "Ᏼ",
  "Ᏽ": "Ᏽ",
  "ᏸ": "Ᏸ",
  "ᏹ": "Ᏹ",
  "ᏺ": "Ᏺ",
  "ᏻ": "Ᏻ",
  "ᏼ": "Ᏼ",
  "ᏽ": "Ᏽ",
  "ᲀ": "в",
  "ᲁ": "д",
  "ᲂ": "о",
  "ᲃ": "с",
  "ᲄ": "т",
  "ᲅ": "т",
  "ᲆ": "ъ",
  "ᲇ": "ѣ",
  "ᲈ": "ꙋ",
  "ẖ": "ẖ",
  "ẗ": "ẗ",
  "ẘ": "ẘ",
  "ẙ": "ẙ",
  "ẚ": "aʾ",
  "ẛ": "ṡ",
  "ẞ": "ss",
  "ὐ": "ὐ",
  "ὒ": "ὒ",
  "ὔ": "ὔ",
  "ὖ": "ὖ",
  "ᾀ": "ἀι",
  "ᾁ": "ἁι",
  "ᾂ": "ἂι",
  "ᾃ": "ἃι",
  "ᾄ": "ἄι",
  "ᾅ": "ἅι",
  "ᾆ": "ἆι",
  "ᾇ": "ἇι",
  "ᾈ": "ἀι",
  "ᾉ": "ἁι",
  "ᾊ": "ἂι",
  "ᾋ": "ἃι",
  "ᾌ": "ἄι",
  "ᾍ": "ἅι",
  "ᾎ": "ἆι",
  "ᾏ": "ἇι",
  "ᾐ": "ἠι",
  "ᾑ": "ἡι",
  "ᾒ": "ἢι",
  "ᾓ": "ἣι",
  "ᾔ": "ἤι",
  "ᾕ": "ἥι",
  "ᾖ": "ἦι",
  "ᾗ": "ἧι",
  "ᾘ": "ἠι",
  "ᾙ": "ἡι",
  "ᾚ": "ἢι",
  "ᾛ": "ἣι",
  "ᾜ": "ἤι",
  "ᾝ": "ἥι",
  "ᾞ": "ἦι",
  "ᾟ": "ἧι",
  "ᾠ": "ὠι",
  "ᾡ": "ὡι",
  "ᾢ": "ὢι",
  "ᾣ": "ὣι",
  "ᾤ": "ὤι",
  "ᾥ": "ὥι",
  "ᾦ": "ὦι",
  "ᾧ": "ὧι",
  "ᾨ": "ὠι",
  "ᾩ": "ὡι",
  "ᾪ": "ὢι",
  "ᾫ": "ὣι",
  "ᾬ": "ὤι",
  "ᾭ": "ὥι",
  "ᾮ": "ὦι",
  "ᾯ": "ὧι",
  "ᾲ": "ὰι",
  "ᾳ": "αι",
  "ᾴ": "άι",
  "ᾶ": "ᾶ",
  "ᾷ": "ᾶι",
  "ᾼ": "αι",
  "ι": "ι",
  "ῂ": "ὴι",
  "ῃ": "ηι",
  "ῄ": "ήι",
  "ῆ": "ῆ",
  "ῇ": "ῆι",
  "ῌ": "ηι",
  "ῒ": "ῒ",
  "ΐ": "ΐ",
  "ῖ": "ῖ",
  "ῗ": "ῗ",
  "ῢ": "ῢ",
  "ΰ": "ΰ",
  "ῤ": "ῤ",
  "ῦ": "ῦ",
  "ῧ": "ῧ",
  "ῲ": "ὼι",
  "ῳ": "ωι",
  "ῴ": "ώι",
  "ῶ": "ῶ",
  "ῷ": "ῶι",
  "ῼ": "ωι",
  "ꭰ": "Ꭰ",
  "ꭱ": "Ꭱ",
  "ꭲ": "Ꭲ",
  "ꭳ": "Ꭳ",
  "ꭴ": "Ꭴ",
  "ꭵ": "Ꭵ",
  "ꭶ": "Ꭶ",
  "ꭷ": "Ꭷ",
  "ꭸ": "Ꭸ",
  "ꭹ": "Ꭹ",
  "ꭺ": "Ꭺ",
  "ꭻ": "Ꭻ",
  "ꭼ": "Ꭼ",
  "ꭽ": "Ꭽ",
  "ꭾ": "Ꭾ",
  "ꭿ": "Ꭿ",
  "ꮀ": "Ꮀ",
  "ꮁ": "Ꮁ",
  "ꮂ": "Ꮂ",
  "ꮃ": "Ꮃ",
  "ꮄ": "Ꮄ",
  "ꮅ": "Ꮅ",
  "ꮆ": "Ꮆ",
  "ꮇ": "Ꮇ",
  "ꮈ": "Ꮈ",
  "ꮉ": "Ꮉ",
  "ꮊ": "Ꮊ",
  "ꮋ": "Ꮋ",
  "ꮌ": "Ꮌ",
  "ꮍ": "Ꮍ",
  "ꮎ": "Ꮎ",
  "ꮏ": "Ꮏ",
  "ꮐ": "Ꮐ",
  "ꮑ": "Ꮑ",
  "ꮒ": "Ꮒ",
  "ꮓ": "Ꮓ",
  "ꮔ": "Ꮔ",
  "ꮕ": "Ꮕ",
  "ꮖ": "Ꮖ",
  "ꮗ": "Ꮗ",
  "ꮘ": "Ꮘ",
  "ꮙ": "Ꮙ",
  "ꮚ": "Ꮚ",
  "ꮛ": "Ꮛ",
  "ꮜ": "Ꮜ",
  "ꮝ": "Ꮝ",
  "ꮞ": "Ꮞ",
  "ꮟ": "Ꮟ",
  "ꮠ": "Ꮠ",
  "ꮡ": "Ꮡ",
  "ꮢ": "Ꮢ",
  "ꮣ": "Ꮣ",
  "ꮤ": "Ꮤ",
  "ꮥ": "Ꮥ",
  "ꮦ": "Ꮦ",
  "ꮧ": "Ꮧ",
  "ꮨ": "Ꮨ",
  "ꮩ": "Ꮩ",
  "ꮪ": "Ꮪ",
  "ꮫ": "Ꮫ",
  "ꮬ": "Ꮬ",
  "ꮭ": "Ꮭ",
  "ꮮ": "Ꮮ",
  "ꮯ": "Ꮯ",
  "ꮰ": "Ꮰ",
  "ꮱ": "Ꮱ",
  "ꮲ": "Ꮲ",
  "ꮳ": "Ꮳ",
  "ꮴ": "Ꮴ",
  "ꮵ": "Ꮵ",
  "ꮶ": "Ꮶ",
  "ꮷ": "Ꮷ",
  "ꮸ": "Ꮸ",
  "ꮹ": "Ꮹ",
  "ꮺ": "Ꮺ",
  "ꮻ": "Ꮻ",
  "ꮼ": "Ꮼ",
  "ꮽ": "Ꮽ",
  "ꮾ": "Ꮾ",
  "ꮿ": "Ꮿ",
  "ﬀ": "ff",
  "ﬁ": "fi",
  "ﬂ": "fl",
  "ﬃ": "ffi",
  "ﬄ": "ffl",
  "ﬅ": "st",
  "ﬆ": "st",
  "ﬓ": "մն",
  "ﬔ": "մե",
  "ﬕ": "մի",
  "ﬖ": "վն",
  "ﬗ": "մխ"
};
