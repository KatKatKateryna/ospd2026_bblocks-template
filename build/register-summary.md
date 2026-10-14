# RSS-Hydro Model of Models Building Blocks

Provenance building blocks for the RSS-Hydro Model of Models (MoM) flood prediction workflow,
profiled for the OGC Open Science Persistent Demonstrator (OSPD) 2026.


W3C PROV profile and activity vocabulary for a minimal slice of the MoM workflow:
GFMS per-watershed cell attribution, GFMS per-watershed aggregation, and GloFAS + GFMS
hazard score accumulation.


## Building Blocks

### `lu.rss-hydro.mom.processing-activity` — Processing activity provenance

**Type:** schema

Generic W3C PROV profile of one geospatial processing activity.

### `lu.rss-hydro.mom.ontology.activities` — MoM workflow activity types

**Type:** model

Activity and entity types emitted by the RSS-Hydro Model of Models flood workflow, as subclasses of prov:Activity and prov:Entity.

### `lu.rss-hydro.mom.workflow.model-of-models` — Model of Models workflow

**Type:** schema

Tested provenance example of a slice of the RSS-Hydro Model of Models flood workflow: GFMS cell attribution, per-watershed aggregation, and GloFAS + GFMS hazard score accumulation.

