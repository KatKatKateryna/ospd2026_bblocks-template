## MoM workflow activity types

Step types of the MoM flood workflow (subclasses of `prov:Activity`), candidate entries for
the OSPD process-type register, plus the entity type and properties the MoM profile uses, and the alert levels
(`mom:AlertLevels`, MoMProduction 0.0.1-alpha).

| Term | MoMProduction code |
|---|---|
| `mom:WatershedCellAttribution` | `gfms_cells.py` `build()` |
| `mom:PerWatershedAggregation` | `GFMS_tool.py` `GFMS_extract_by_watershed()` |
| `mom:HazardScoreAccumulation` | `GFMS_tool.py` `GFMS_fix_duration()`, `GFMS_MoM.py` `flood_severity()` |
