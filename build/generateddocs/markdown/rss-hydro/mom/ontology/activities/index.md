
# MoM workflow activity types (Model)

`lu.rss-hydro.mom.ontology.activities` *v0.1*

Activity and entity types emitted by the RSS-Hydro Model of Models flood workflow, as subclasses of prov:Activity and prov:Entity.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

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


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/KatKatKateryna/ospd2026_bblocks-template](https://github.com/KatKatKateryna/ospd2026_bblocks-template)
* Path: `_sources/ontology/activities`

