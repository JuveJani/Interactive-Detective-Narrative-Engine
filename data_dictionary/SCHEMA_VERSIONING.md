# Schema Versioning Policy

## 1. Purpose

This policy introduces minimal version metadata now so that future formal schemas and software tools can evolve without invalidating existing adventures.

## 2. Required Version Fields

Every adventure root record shall declare:

```yaml
engine_spec_version: "2.0"
data_dictionary_version: "0.3"
adventure_schema_version: "0.1"
```

Individual records may later declare their own schema versions when needed.

## 3. Semantic Version Meaning

Versions use:

```text
MAJOR.MINOR
```

- `MAJOR` changes may break existing adventure data.
- `MINOR` changes add compatible fields, clarifications, or optional behavior.

Patch-level versioning may be added when executable schemas exist.

## 4. Compatibility Rule

An adventure is compatible when:

- its required major schema version is supported;
- all mandatory fields are recognized;
- unknown optional fields can be safely ignored;
- no declared engine requirement is missing.

## 5. Current Scope

Release 0.3 defines the version policy only. Formal JSON Schema files are deferred until after the first playable prototype unless manual validation becomes unreliable during production.
