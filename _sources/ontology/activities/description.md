## MoM workflow activity types

Activity types of the MoM flood workflow (subclasses of `mom:Geoprocessing`, itself a
`prov:Activity`), candidate entries for the OSPD process-type register, plus the entity type,
properties, workflow run type (`mom:WorkflowRun`) and alert levels (`mom:AlertLevels`) the
MoM profile uses.

| Term | Generic operation |
|---|---|
| `mom:WatershedCellAttribution` | zonal masking (grid cells to zones) |
| `mom:PerWatershedAggregation` | zonal statistics |
| `mom:HazardScoreAccumulation` | index composition and classification |
