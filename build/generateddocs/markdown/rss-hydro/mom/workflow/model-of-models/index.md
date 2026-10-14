
# Model of Models workflow (Schema)

`lu.rss-hydro.mom.workflow.model-of-models` *v0.1*

Tested provenance example of a slice of the RSS-Hydro Model of Models flood workflow: GFMS cell attribution, per-watershed aggregation, and GloFAS + GFMS hazard score accumulation.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## Model of Models workflow

Provenance of three activities of the RSS-Hydro Model of Models (MoM) flood workflow, GFMS only.

| Activity | Activity type | Uses | Generates |
|---|---|---|---|
| Cell attribution (optional) | `mom:WatershedCellAttribution` | watershed shapefile, GFMS grid | GFMS cell lookup |
| Per-watershed aggregation | `mom:PerWatershedAggregation` | GFMS file, cell lookup, parameters | per-watershed aggregates |
| Hazard score accumulation | `mom:HazardScoreAccumulation` | aggregates, previous summary, GloFAS file, static tables, parameters | summary with duration, `Final_Attributes`, `Attributes_Clean` |

Each activity is `dcterms:isPartOf` one `mom:WorkflowRun` activity.

Cell attribution runs only when the lookup is missing or outdated; otherwise the lookup
points to the earlier run that built it. The lookup derives from the versioned watershed
shapefile (`mom:watershedFingerprint`) and the GFMS grid (`mom:gridSignature`), which ties each
aggregate to the grid and watersheds it was clipped with. Parameters and static tables ship
with the software version (`dcterms:hasVersion`, `dcterms:isPartOf`).

GFMS and GloFAS files state `mom:dataType`, `dcterms:format`, `mom:dataTime` (time the values
refer to) and `generatedAtTime` (time the file was produced). `rules.shacl` enforces this and
the links between the activities.

## Examples

### Run of 2026-03-02 00:00 UTC, reusing the cell lookup
Usual run; the cell lookup comes from an earlier run. All values are illustrative.
#### json
```json
[
  {
    "id": "run:mom",
    "agentType": "prov:SoftwareAgent",
    "name": "MoMProduction",
    "dcterms:hasVersion": "0.0.1-alpha"
  },
  {
    "id": "run:rss-hydro",
    "agentType": "prov:Organization",
    "name": "RSS-Hydro"
  },
  {
    "id": "run:server",
    "agentType": "prov:Agent",
    "name": "mom-prod-01 (illustrative server)"
  },
  {
    "id": "run:workflow-run",
    "activityType": "mom:WorkflowRun",
    "name": "MoM workflow run, 2026-03-02 00:00",
    "startedAtTime": "2026-03-02T01:05:33Z",
    "endedAtTime": "2026-03-02T01:12:47Z",
    "wasAssociatedWith": [
      "run:mom",
      "run:rss-hydro",
      "run:server"
    ]
  },
  {
    "id": "run:umd",
    "agentType": "prov:Organization",
    "name": "University of Maryland (GFMS)"
  },
  {
    "id": "run:ecmwf",
    "agentType": "prov:Organization",
    "name": "ECMWF / CEMS (GloFAS)"
  },
  {
    "id": "run:watersheds",
    "entityType": "prov:Entity",
    "name": "Watershed_pfaf_id.shp",
    "dcterms:hasVersion": "0.0.0",
    "dcterms:format": "ESRI Shapefile",
    "mom:watershedFingerprint": "a09161ac707ef1d0355e92e730c8fe31e127149b803321bc988b3232058eea17",
    "generatedAtTime": "2026-01-15T00:00:00Z"
  },
  {
    "id": "run:gfms-grid",
    "entityType": "prov:Entity",
    "name": "GFMS Flood_byStor grid",
    "mom:dataType": "GFMS",
    "dcterms:format": "GDAL VRT",
    "mom:gridSignature": "[2880, 800, 0.125, 0.0, -180.0, 0.0, -0.125, 50.0]",
    "dcterms:hasVersion": "0.0.1-alpha",
    "dcterms:isPartOf": "run:mom"
  },
  {
    "id": "run:gfms-cells",
    "entityType": "mom:WatershedCellLookup",
    "name": "gfms_watershed_cells.npz",
    "mom:dataType": "GFMS",
    "dcterms:format": "NumPy .npz cell lookup",
    "mom:watershedFingerprint": "a09161ac707ef1d0355e92e730c8fe31e127149b803321bc988b3232058eea17",
    "generatedAtTime": "2026-03-01T00:15:11Z",
    "wasGeneratedBy": "https://example.org/mom/run/2026030100/cell-attribution",
    "wasDerivedFrom": [
      "run:watersheds",
      "run:gfms-grid"
    ]
  },
  {
    "id": "run:gfms-bin",
    "entityType": "prov:Entity",
    "name": "Flood_byStor_2026030200.bin",
    "dcat:downloadURL": "https://example.org/gfms/Flood_byStor_2026030200.bin",
    "mom:dataType": "GFMS",
    "dcterms:format": "GFMS Flood_byStor binary grid (float32)",
    "mom:gfmsNodataValue": -9999,
    "mom:gridSignature": "[1440, 400, 0.25, 0.0, -180.0, 0.0, -0.25, 50.0]",
    "mom:dataTime": "2026-03-02T00:00:00Z",
    "generatedAtTime": "2026-03-02T01:05:32Z",
    "wasAttributedTo": "run:umd"
  },
  {
    "id": "run:aggregation-parameters",
    "entityType": "prov:Entity",
    "name": "GFMS per-watershed aggregation parameters",
    "dcterms:hasVersion": "0.0.1-alpha",
    "dcterms:isPartOf": "run:mom",
    "mom:gfmsDurationAreaThresholdKm2": 50,
    "mom:gfmsMinFileSizeBytes": 1000000
  },
  {
    "id": "run:aggregation",
    "activityType": "mom:PerWatershedAggregation",
    "name": "GFMS per-watershed aggregation",
    "startedAtTime": "2026-03-02T01:05:33Z",
    "endedAtTime": "2026-03-02T01:05:41Z",
    "used": [
      "run:gfms-bin",
      "run:gfms-cells",
      "run:aggregation-parameters"
    ],
    "generated": "run:gfms-aggregates",
    "wasAssociatedWith": [
      "run:mom",
      "run:rss-hydro",
      "run:server"
    ],
    "dcterms:isPartOf": "run:workflow-run"
  },
  {
    "id": "run:gfms-aggregates",
    "entityType": "prov:Entity",
    "name": "Processing/gfms/Flood_byStor_2026030200.csv (per-watershed aggregates, duration not yet recalculated)",
    "mom:dataType": "GFMS",
    "dcterms:format": "text/csv",
    "mom:dataTime": "2026-03-02T00:00:00Z",
    "generatedAtTime": "2026-03-02T01:05:41Z",
    "wasGeneratedBy": "run:aggregation",
    "wasDerivedFrom": [
      "run:gfms-bin",
      "run:gfms-cells"
    ]
  },
  {
    "id": "run:gfms-summary-prev",
    "entityType": "prov:Entity",
    "name": "GFMS_summary/Flood_byStor_2026030121.csv",
    "mom:dataType": "GFMS",
    "dcterms:format": "text/csv",
    "mom:dataTime": "2026-03-01T21:00:00Z",
    "generatedAtTime": "2026-03-01T01:07:12Z"
  },
  {
    "id": "run:glofas-txt",
    "entityType": "prov:Entity",
    "name": "threspoints_2026030200.txt",
    "dcat:downloadURL": "https://example.org/glofas/threspoints_2026030200.txt",
    "mom:dataType": "GloFAS",
    "dcterms:format": "GloFAS threspoints station table (comma-separated text)",
    "mom:glofasNodataValue": -9999,
    "mom:dataTime": "2026-03-02T00:00:00Z",
    "generatedAtTime": "2026-03-02T00:58:10Z",
    "wasAttributedTo": "run:ecmwf"
  },
  {
    "id": "run:glofas-points",
    "entityType": "prov:Entity",
    "name": "GLOFAS/threspoints_2026030200.csv",
    "mom:dataType": "GloFAS",
    "dcterms:format": "text/csv",
    "mom:glofasNodataValue": -9999,
    "mom:dataTime": "2026-03-02T00:00:00Z",
    "generatedAtTime": "2026-03-02T00:58:12Z",
    "wasDerivedFrom": "run:glofas-txt"
  },
  {
    "id": "run:attributes",
    "entityType": "prov:Entity",
    "name": "data/Attributes.csv",
    "dcterms:format": "text/csv",
    "dcterms:hasVersion": "0.0.1-alpha",
    "dcterms:isPartOf": "run:mom"
  },
  {
    "id": "run:resilience",
    "entityType": "prov:Entity",
    "name": "data/Resilience_Index.csv",
    "dcterms:format": "text/csv",
    "dcterms:hasVersion": "0.0.1-alpha",
    "dcterms:isPartOf": "run:mom"
  },
  {
    "id": "run:weights",
    "entityType": "prov:Entity",
    "name": "data/GFMS_Weightage.csv",
    "dcterms:format": "text/csv",
    "dcterms:hasVersion": "0.0.1-alpha",
    "dcterms:isPartOf": "run:mom"
  },
  {
    "id": "run:hazard-parameters",
    "entityType": "prov:Entity",
    "name": "GloFAS + GFMS hazard score accumulation parameters",
    "dcterms:hasVersion": "0.0.1-alpha",
    "dcterms:isPartOf": "run:mom",
    "mom:gfmsDurationAreaThresholdKm2": 50
  },
  {
    "id": "run:hazard",
    "activityType": "mom:HazardScoreAccumulation",
    "name": "GloFAS + GFMS hazard score accumulation",
    "startedAtTime": "2026-03-02T01:12:40Z",
    "endedAtTime": "2026-03-02T01:12:47Z",
    "used": [
      "run:gfms-aggregates",
      "run:gfms-summary-prev",
      "run:glofas-points",
      "run:attributes",
      "run:resilience",
      "run:weights",
      "run:hazard-parameters"
    ],
    "generated": [
      "run:gfms-summary",
      "run:final-attributes",
      "run:attributes-clean"
    ],
    "wasAssociatedWith": [
      "run:mom",
      "run:rss-hydro",
      "run:server"
    ],
    "dcterms:isPartOf": "run:workflow-run"
  },
  {
    "id": "run:gfms-summary",
    "entityType": "prov:Entity",
    "name": "GFMS_summary/Flood_byStor_2026030200.csv (duration recalculated)",
    "mom:dataType": "GFMS",
    "dcterms:format": "text/csv",
    "mom:dataTime": "2026-03-02T00:00:00Z",
    "generatedAtTime": "2026-03-02T01:12:41Z",
    "wasGeneratedBy": "run:hazard",
    "wasDerivedFrom": [
      "run:gfms-aggregates",
      "run:gfms-summary-prev"
    ]
  },
  {
    "id": "run:final-attributes",
    "entityType": "prov:Entity",
    "name": "GFMS_MoM/Final_Attributes_20260302.csv",
    "dcterms:format": "text/csv",
    "generatedAtTime": "2026-03-02T01:12:47Z",
    "wasGeneratedBy": "run:hazard",
    "wasDerivedFrom": [
      "run:gfms-summary",
      "run:glofas-points",
      "run:attributes",
      "run:resilience",
      "run:weights"
    ]
  },
  {
    "id": "run:attributes-clean",
    "entityType": "prov:Entity",
    "name": "GFMS_MoM/Attributes_Clean_20260302.csv",
    "dcterms:format": "text/csv",
    "generatedAtTime": "2026-03-02T01:12:47Z",
    "wasGeneratedBy": "run:hazard",
    "wasDerivedFrom": "run:final-attributes"
  }
]

```

#### jsonld
```jsonld
{
  "@context": "https://katkatkateryna.github.io/ospd2026_bblocks-template/build/annotated/rss-hydro/mom/workflow/model-of-models/context.jsonld",
  "@graph": [
    {
      "id": "run:mom",
      "agentType": "prov:SoftwareAgent",
      "name": "MoMProduction",
      "dcterms:hasVersion": "0.0.1-alpha"
    },
    {
      "id": "run:rss-hydro",
      "agentType": "prov:Organization",
      "name": "RSS-Hydro"
    },
    {
      "id": "run:server",
      "agentType": "prov:Agent",
      "name": "mom-prod-01 (illustrative server)"
    },
    {
      "id": "run:workflow-run",
      "activityType": "mom:WorkflowRun",
      "name": "MoM workflow run, 2026-03-02 00:00",
      "startedAtTime": "2026-03-02T01:05:33Z",
      "endedAtTime": "2026-03-02T01:12:47Z",
      "wasAssociatedWith": [
        "run:mom",
        "run:rss-hydro",
        "run:server"
      ]
    },
    {
      "id": "run:umd",
      "agentType": "prov:Organization",
      "name": "University of Maryland (GFMS)"
    },
    {
      "id": "run:ecmwf",
      "agentType": "prov:Organization",
      "name": "ECMWF / CEMS (GloFAS)"
    },
    {
      "id": "run:watersheds",
      "entityType": "prov:Entity",
      "name": "Watershed_pfaf_id.shp",
      "dcterms:hasVersion": "0.0.0",
      "dcterms:format": "ESRI Shapefile",
      "mom:watershedFingerprint": "a09161ac707ef1d0355e92e730c8fe31e127149b803321bc988b3232058eea17",
      "generatedAtTime": "2026-01-15T00:00:00Z"
    },
    {
      "id": "run:gfms-grid",
      "entityType": "prov:Entity",
      "name": "GFMS Flood_byStor grid",
      "mom:dataType": "GFMS",
      "dcterms:format": "GDAL VRT",
      "mom:gridSignature": "[2880, 800, 0.125, 0.0, -180.0, 0.0, -0.125, 50.0]",
      "dcterms:hasVersion": "0.0.1-alpha",
      "dcterms:isPartOf": "run:mom"
    },
    {
      "id": "run:gfms-cells",
      "entityType": "mom:WatershedCellLookup",
      "name": "gfms_watershed_cells.npz",
      "mom:dataType": "GFMS",
      "dcterms:format": "NumPy .npz cell lookup",
      "mom:watershedFingerprint": "a09161ac707ef1d0355e92e730c8fe31e127149b803321bc988b3232058eea17",
      "generatedAtTime": "2026-03-01T00:15:11Z",
      "wasGeneratedBy": "https://example.org/mom/run/2026030100/cell-attribution",
      "wasDerivedFrom": [
        "run:watersheds",
        "run:gfms-grid"
      ]
    },
    {
      "id": "run:gfms-bin",
      "entityType": "prov:Entity",
      "name": "Flood_byStor_2026030200.bin",
      "dcat:downloadURL": "https://example.org/gfms/Flood_byStor_2026030200.bin",
      "mom:dataType": "GFMS",
      "dcterms:format": "GFMS Flood_byStor binary grid (float32)",
      "mom:gfmsNodataValue": -9999,
      "mom:gridSignature": "[1440, 400, 0.25, 0.0, -180.0, 0.0, -0.25, 50.0]",
      "mom:dataTime": "2026-03-02T00:00:00Z",
      "generatedAtTime": "2026-03-02T01:05:32Z",
      "wasAttributedTo": "run:umd"
    },
    {
      "id": "run:aggregation-parameters",
      "entityType": "prov:Entity",
      "name": "GFMS per-watershed aggregation parameters",
      "dcterms:hasVersion": "0.0.1-alpha",
      "dcterms:isPartOf": "run:mom",
      "mom:gfmsDurationAreaThresholdKm2": 50,
      "mom:gfmsMinFileSizeBytes": 1000000
    },
    {
      "id": "run:aggregation",
      "activityType": "mom:PerWatershedAggregation",
      "name": "GFMS per-watershed aggregation",
      "startedAtTime": "2026-03-02T01:05:33Z",
      "endedAtTime": "2026-03-02T01:05:41Z",
      "used": [
        "run:gfms-bin",
        "run:gfms-cells",
        "run:aggregation-parameters"
      ],
      "generated": "run:gfms-aggregates",
      "wasAssociatedWith": [
        "run:mom",
        "run:rss-hydro",
        "run:server"
      ],
      "dcterms:isPartOf": "run:workflow-run"
    },
    {
      "id": "run:gfms-aggregates",
      "entityType": "prov:Entity",
      "name": "Processing/gfms/Flood_byStor_2026030200.csv (per-watershed aggregates, duration not yet recalculated)",
      "mom:dataType": "GFMS",
      "dcterms:format": "text/csv",
      "mom:dataTime": "2026-03-02T00:00:00Z",
      "generatedAtTime": "2026-03-02T01:05:41Z",
      "wasGeneratedBy": "run:aggregation",
      "wasDerivedFrom": [
        "run:gfms-bin",
        "run:gfms-cells"
      ]
    },
    {
      "id": "run:gfms-summary-prev",
      "entityType": "prov:Entity",
      "name": "GFMS_summary/Flood_byStor_2026030121.csv",
      "mom:dataType": "GFMS",
      "dcterms:format": "text/csv",
      "mom:dataTime": "2026-03-01T21:00:00Z",
      "generatedAtTime": "2026-03-01T01:07:12Z"
    },
    {
      "id": "run:glofas-txt",
      "entityType": "prov:Entity",
      "name": "threspoints_2026030200.txt",
      "dcat:downloadURL": "https://example.org/glofas/threspoints_2026030200.txt",
      "mom:dataType": "GloFAS",
      "dcterms:format": "GloFAS threspoints station table (comma-separated text)",
      "mom:glofasNodataValue": -9999,
      "mom:dataTime": "2026-03-02T00:00:00Z",
      "generatedAtTime": "2026-03-02T00:58:10Z",
      "wasAttributedTo": "run:ecmwf"
    },
    {
      "id": "run:glofas-points",
      "entityType": "prov:Entity",
      "name": "GLOFAS/threspoints_2026030200.csv",
      "mom:dataType": "GloFAS",
      "dcterms:format": "text/csv",
      "mom:glofasNodataValue": -9999,
      "mom:dataTime": "2026-03-02T00:00:00Z",
      "generatedAtTime": "2026-03-02T00:58:12Z",
      "wasDerivedFrom": "run:glofas-txt"
    },
    {
      "id": "run:attributes",
      "entityType": "prov:Entity",
      "name": "data/Attributes.csv",
      "dcterms:format": "text/csv",
      "dcterms:hasVersion": "0.0.1-alpha",
      "dcterms:isPartOf": "run:mom"
    },
    {
      "id": "run:resilience",
      "entityType": "prov:Entity",
      "name": "data/Resilience_Index.csv",
      "dcterms:format": "text/csv",
      "dcterms:hasVersion": "0.0.1-alpha",
      "dcterms:isPartOf": "run:mom"
    },
    {
      "id": "run:weights",
      "entityType": "prov:Entity",
      "name": "data/GFMS_Weightage.csv",
      "dcterms:format": "text/csv",
      "dcterms:hasVersion": "0.0.1-alpha",
      "dcterms:isPartOf": "run:mom"
    },
    {
      "id": "run:hazard-parameters",
      "entityType": "prov:Entity",
      "name": "GloFAS + GFMS hazard score accumulation parameters",
      "dcterms:hasVersion": "0.0.1-alpha",
      "dcterms:isPartOf": "run:mom",
      "mom:gfmsDurationAreaThresholdKm2": 50
    },
    {
      "id": "run:hazard",
      "activityType": "mom:HazardScoreAccumulation",
      "name": "GloFAS + GFMS hazard score accumulation",
      "startedAtTime": "2026-03-02T01:12:40Z",
      "endedAtTime": "2026-03-02T01:12:47Z",
      "used": [
        "run:gfms-aggregates",
        "run:gfms-summary-prev",
        "run:glofas-points",
        "run:attributes",
        "run:resilience",
        "run:weights",
        "run:hazard-parameters"
      ],
      "generated": [
        "run:gfms-summary",
        "run:final-attributes",
        "run:attributes-clean"
      ],
      "wasAssociatedWith": [
        "run:mom",
        "run:rss-hydro",
        "run:server"
      ],
      "dcterms:isPartOf": "run:workflow-run"
    },
    {
      "id": "run:gfms-summary",
      "entityType": "prov:Entity",
      "name": "GFMS_summary/Flood_byStor_2026030200.csv (duration recalculated)",
      "mom:dataType": "GFMS",
      "dcterms:format": "text/csv",
      "mom:dataTime": "2026-03-02T00:00:00Z",
      "generatedAtTime": "2026-03-02T01:12:41Z",
      "wasGeneratedBy": "run:hazard",
      "wasDerivedFrom": [
        "run:gfms-aggregates",
        "run:gfms-summary-prev"
      ]
    },
    {
      "id": "run:final-attributes",
      "entityType": "prov:Entity",
      "name": "GFMS_MoM/Final_Attributes_20260302.csv",
      "dcterms:format": "text/csv",
      "generatedAtTime": "2026-03-02T01:12:47Z",
      "wasGeneratedBy": "run:hazard",
      "wasDerivedFrom": [
        "run:gfms-summary",
        "run:glofas-points",
        "run:attributes",
        "run:resilience",
        "run:weights"
      ]
    },
    {
      "id": "run:attributes-clean",
      "entityType": "prov:Entity",
      "name": "GFMS_MoM/Attributes_Clean_20260302.csv",
      "dcterms:format": "text/csv",
      "generatedAtTime": "2026-03-02T01:12:47Z",
      "wasGeneratedBy": "run:hazard",
      "wasDerivedFrom": "run:final-attributes"
    }
  ]
}
```

#### ttl
```ttl
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix mom: <https://rss-hydro.lu/ns/mom/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix run: <https://example.org/mom/run/2026030200/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

run:aggregation a mom:PerWatershedAggregation ;
    rdfs:label "GFMS per-watershed aggregation" ;
    dcterms:isPartOf run:workflow-run ;
    prov:endedAtTime "2026-03-02T01:05:41+00:00"^^xsd:dateTime ;
    prov:generated run:gfms-aggregates ;
    prov:startedAtTime "2026-03-02T01:05:33+00:00"^^xsd:dateTime ;
    prov:used run:aggregation-parameters,
        run:gfms-bin,
        run:gfms-cells ;
    prov:wasAssociatedWith run:mom,
        run:rss-hydro,
        run:server .

run:aggregation-parameters a prov:Entity ;
    rdfs:label "GFMS per-watershed aggregation parameters" ;
    dcterms:hasVersion "0.0.1-alpha" ;
    dcterms:isPartOf run:mom ;
    mom:gfmsDurationAreaThresholdKm2 50 ;
    mom:gfmsMinFileSizeBytes 1000000 .

run:attributes-clean a prov:Entity ;
    rdfs:label "GFMS_MoM/Attributes_Clean_20260302.csv" ;
    dcterms:format "text/csv" ;
    prov:generatedAtTime "2026-03-02T01:12:47+00:00"^^xsd:dateTime ;
    prov:wasDerivedFrom run:final-attributes ;
    prov:wasGeneratedBy run:hazard .

run:ecmwf a prov:Organization ;
    rdfs:label "ECMWF / CEMS (GloFAS)" .

run:gfms-grid a prov:Entity ;
    rdfs:label "GFMS Flood_byStor grid" ;
    dcterms:format "GDAL VRT" ;
    dcterms:hasVersion "0.0.1-alpha" ;
    dcterms:isPartOf run:mom ;
    mom:dataType "GFMS" ;
    mom:gridSignature "[2880, 800, 0.125, 0.0, -180.0, 0.0, -0.125, 50.0]" .

run:glofas-txt a prov:Entity ;
    rdfs:label "threspoints_2026030200.txt" ;
    dcterms:format "GloFAS threspoints station table (comma-separated text)" ;
    dcat:downloadURL <https://example.org/glofas/threspoints_2026030200.txt> ;
    prov:generatedAtTime "2026-03-02T00:58:10+00:00"^^xsd:dateTime ;
    prov:wasAttributedTo run:ecmwf ;
    mom:dataTime "2026-03-02T00:00:00+00:00"^^xsd:dateTime ;
    mom:dataType "GloFAS" ;
    mom:glofasNodataValue -9999 .

run:hazard-parameters a prov:Entity ;
    rdfs:label "GloFAS + GFMS hazard score accumulation parameters" ;
    dcterms:hasVersion "0.0.1-alpha" ;
    dcterms:isPartOf run:mom ;
    mom:gfmsDurationAreaThresholdKm2 50 .

run:umd a prov:Organization ;
    rdfs:label "University of Maryland (GFMS)" .

run:watersheds a prov:Entity ;
    rdfs:label "Watershed_pfaf_id.shp" ;
    dcterms:format "ESRI Shapefile" ;
    dcterms:hasVersion "0.0.0" ;
    prov:generatedAtTime "2026-01-15T00:00:00+00:00"^^xsd:dateTime ;
    mom:watershedFingerprint "a09161ac707ef1d0355e92e730c8fe31e127149b803321bc988b3232058eea17" .

run:attributes a prov:Entity ;
    rdfs:label "data/Attributes.csv" ;
    dcterms:format "text/csv" ;
    dcterms:hasVersion "0.0.1-alpha" ;
    dcterms:isPartOf run:mom .

run:final-attributes a prov:Entity ;
    rdfs:label "GFMS_MoM/Final_Attributes_20260302.csv" ;
    dcterms:format "text/csv" ;
    prov:generatedAtTime "2026-03-02T01:12:47+00:00"^^xsd:dateTime ;
    prov:wasDerivedFrom run:attributes,
        run:gfms-summary,
        run:glofas-points,
        run:resilience,
        run:weights ;
    prov:wasGeneratedBy run:hazard .

run:gfms-bin a prov:Entity ;
    rdfs:label "Flood_byStor_2026030200.bin" ;
    dcterms:format "GFMS Flood_byStor binary grid (float32)" ;
    dcat:downloadURL <https://example.org/gfms/Flood_byStor_2026030200.bin> ;
    prov:generatedAtTime "2026-03-02T01:05:32+00:00"^^xsd:dateTime ;
    prov:wasAttributedTo run:umd ;
    mom:dataTime "2026-03-02T00:00:00+00:00"^^xsd:dateTime ;
    mom:dataType "GFMS" ;
    mom:gfmsNodataValue -9999 ;
    mom:gridSignature "[1440, 400, 0.25, 0.0, -180.0, 0.0, -0.25, 50.0]" .

run:gfms-cells a mom:WatershedCellLookup ;
    rdfs:label "gfms_watershed_cells.npz" ;
    dcterms:format "NumPy .npz cell lookup" ;
    prov:generatedAtTime "2026-03-01T00:15:11+00:00"^^xsd:dateTime ;
    prov:wasDerivedFrom run:gfms-grid,
        run:watersheds ;
    prov:wasGeneratedBy <https://example.org/mom/run/2026030100/cell-attribution> ;
    mom:dataType "GFMS" ;
    mom:watershedFingerprint "a09161ac707ef1d0355e92e730c8fe31e127149b803321bc988b3232058eea17" .

run:gfms-summary a prov:Entity ;
    rdfs:label "GFMS_summary/Flood_byStor_2026030200.csv (duration recalculated)" ;
    dcterms:format "text/csv" ;
    prov:generatedAtTime "2026-03-02T01:12:41+00:00"^^xsd:dateTime ;
    prov:wasDerivedFrom run:gfms-aggregates,
        run:gfms-summary-prev ;
    prov:wasGeneratedBy run:hazard ;
    mom:dataTime "2026-03-02T00:00:00+00:00"^^xsd:dateTime ;
    mom:dataType "GFMS" .

run:gfms-summary-prev a prov:Entity ;
    rdfs:label "GFMS_summary/Flood_byStor_2026030121.csv" ;
    dcterms:format "text/csv" ;
    prov:generatedAtTime "2026-03-01T01:07:12+00:00"^^xsd:dateTime ;
    mom:dataTime "2026-03-01T21:00:00+00:00"^^xsd:dateTime ;
    mom:dataType "GFMS" .

run:glofas-points a prov:Entity ;
    rdfs:label "GLOFAS/threspoints_2026030200.csv" ;
    dcterms:format "text/csv" ;
    prov:generatedAtTime "2026-03-02T00:58:12+00:00"^^xsd:dateTime ;
    prov:wasDerivedFrom run:glofas-txt ;
    mom:dataTime "2026-03-02T00:00:00+00:00"^^xsd:dateTime ;
    mom:dataType "GloFAS" ;
    mom:glofasNodataValue -9999 .

run:resilience a prov:Entity ;
    rdfs:label "data/Resilience_Index.csv" ;
    dcterms:format "text/csv" ;
    dcterms:hasVersion "0.0.1-alpha" ;
    dcterms:isPartOf run:mom .

run:weights a prov:Entity ;
    rdfs:label "data/GFMS_Weightage.csv" ;
    dcterms:format "text/csv" ;
    dcterms:hasVersion "0.0.1-alpha" ;
    dcterms:isPartOf run:mom .

run:workflow-run a mom:WorkflowRun ;
    rdfs:label "MoM workflow run, 2026-03-02 00:00" ;
    prov:endedAtTime "2026-03-02T01:12:47+00:00"^^xsd:dateTime ;
    prov:startedAtTime "2026-03-02T01:05:33+00:00"^^xsd:dateTime ;
    prov:wasAssociatedWith run:mom,
        run:rss-hydro,
        run:server .

run:gfms-aggregates a prov:Entity ;
    rdfs:label "Processing/gfms/Flood_byStor_2026030200.csv (per-watershed aggregates, duration not yet recalculated)" ;
    dcterms:format "text/csv" ;
    prov:generatedAtTime "2026-03-02T01:05:41+00:00"^^xsd:dateTime ;
    prov:wasDerivedFrom run:gfms-bin,
        run:gfms-cells ;
    prov:wasGeneratedBy run:aggregation ;
    mom:dataTime "2026-03-02T00:00:00+00:00"^^xsd:dateTime ;
    mom:dataType "GFMS" .

run:hazard a mom:HazardScoreAccumulation ;
    rdfs:label "GloFAS + GFMS hazard score accumulation" ;
    dcterms:isPartOf run:workflow-run ;
    prov:endedAtTime "2026-03-02T01:12:47+00:00"^^xsd:dateTime ;
    prov:generated run:attributes-clean,
        run:final-attributes,
        run:gfms-summary ;
    prov:startedAtTime "2026-03-02T01:12:40+00:00"^^xsd:dateTime ;
    prov:used run:attributes,
        run:gfms-aggregates,
        run:gfms-summary-prev,
        run:glofas-points,
        run:hazard-parameters,
        run:resilience,
        run:weights ;
    prov:wasAssociatedWith run:mom,
        run:rss-hydro,
        run:server .

run:rss-hydro a prov:Organization ;
    rdfs:label "RSS-Hydro" .

run:server a prov:Agent ;
    rdfs:label "mom-prod-01 (illustrative server)" .

run:mom a prov:SoftwareAgent ;
    rdfs:label "MoMProduction" ;
    dcterms:hasVersion "0.0.1-alpha" .


```


### Run of 2026-03-02 00:00 UTC, rebuilding the cell lookup
Same run with cell attribution first. All values are illustrative.
#### json
```json
[
  {
    "id": "run:mom",
    "agentType": "prov:SoftwareAgent",
    "name": "MoMProduction",
    "dcterms:hasVersion": "0.0.1-alpha"
  },
  {
    "id": "run:rss-hydro",
    "agentType": "prov:Organization",
    "name": "RSS-Hydro"
  },
  {
    "id": "run:server",
    "agentType": "prov:Agent",
    "name": "mom-prod-01 (illustrative server)"
  },
  {
    "id": "run:workflow-run",
    "activityType": "mom:WorkflowRun",
    "name": "MoM workflow run, 2026-03-02 00:00",
    "startedAtTime": "2026-03-02T01:01:04Z",
    "endedAtTime": "2026-03-02T01:12:47Z",
    "wasAssociatedWith": [
      "run:mom",
      "run:rss-hydro",
      "run:server"
    ]
  },
  {
    "id": "run:umd",
    "agentType": "prov:Organization",
    "name": "University of Maryland (GFMS)"
  },
  {
    "id": "run:ecmwf",
    "agentType": "prov:Organization",
    "name": "ECMWF / CEMS (GloFAS)"
  },
  {
    "id": "run:watersheds",
    "entityType": "prov:Entity",
    "name": "Watershed_pfaf_id.shp",
    "dcterms:hasVersion": "0.0.0",
    "dcterms:format": "ESRI Shapefile",
    "mom:watershedFingerprint": "a09161ac707ef1d0355e92e730c8fe31e127149b803321bc988b3232058eea17",
    "generatedAtTime": "2026-01-15T00:00:00Z"
  },
  {
    "id": "run:gfms-grid",
    "entityType": "prov:Entity",
    "name": "GFMS Flood_byStor grid",
    "mom:dataType": "GFMS",
    "dcterms:format": "GDAL VRT",
    "mom:gridSignature": "[2880, 800, 0.125, 0.0, -180.0, 0.0, -0.125, 50.0]",
    "dcterms:hasVersion": "0.0.1-alpha",
    "dcterms:isPartOf": "run:mom"
  },
  {
    "id": "run:cell-attribution",
    "activityType": "mom:WatershedCellAttribution",
    "name": "GFMS cell attribution",
    "startedAtTime": "2026-03-02T01:01:04Z",
    "endedAtTime": "2026-03-02T01:04:11Z",
    "used": [
      "run:watersheds",
      "run:gfms-grid"
    ],
    "generated": "run:gfms-cells",
    "wasAssociatedWith": [
      "run:mom",
      "run:rss-hydro",
      "run:server"
    ],
    "dcterms:isPartOf": "run:workflow-run"
  },
  {
    "id": "run:gfms-cells",
    "entityType": "mom:WatershedCellLookup",
    "name": "gfms_watershed_cells.npz",
    "mom:dataType": "GFMS",
    "dcterms:format": "NumPy .npz cell lookup",
    "mom:watershedFingerprint": "a09161ac707ef1d0355e92e730c8fe31e127149b803321bc988b3232058eea17",
    "generatedAtTime": "2026-03-02T01:04:11Z",
    "wasGeneratedBy": "run:cell-attribution",
    "wasDerivedFrom": [
      "run:watersheds",
      "run:gfms-grid"
    ]
  },
  {
    "id": "run:gfms-bin",
    "entityType": "prov:Entity",
    "name": "Flood_byStor_2026030200.bin",
    "dcat:downloadURL": "https://example.org/gfms/Flood_byStor_2026030200.bin",
    "mom:dataType": "GFMS",
    "dcterms:format": "GFMS Flood_byStor binary grid (float32)",
    "mom:gfmsNodataValue": -9999,
    "mom:gridSignature": "[1440, 400, 0.25, 0.0, -180.0, 0.0, -0.25, 50.0]",
    "mom:dataTime": "2026-03-02T00:00:00Z",
    "generatedAtTime": "2026-03-02T01:05:32Z",
    "wasAttributedTo": "run:umd"
  },
  {
    "id": "run:aggregation-parameters",
    "entityType": "prov:Entity",
    "name": "GFMS per-watershed aggregation parameters",
    "dcterms:hasVersion": "0.0.1-alpha",
    "dcterms:isPartOf": "run:mom",
    "mom:gfmsDurationAreaThresholdKm2": 50,
    "mom:gfmsMinFileSizeBytes": 1000000
  },
  {
    "id": "run:aggregation",
    "activityType": "mom:PerWatershedAggregation",
    "name": "GFMS per-watershed aggregation",
    "startedAtTime": "2026-03-02T01:05:33Z",
    "endedAtTime": "2026-03-02T01:05:41Z",
    "used": [
      "run:gfms-bin",
      "run:gfms-cells",
      "run:aggregation-parameters"
    ],
    "generated": "run:gfms-aggregates",
    "wasAssociatedWith": [
      "run:mom",
      "run:rss-hydro",
      "run:server"
    ],
    "dcterms:isPartOf": "run:workflow-run"
  },
  {
    "id": "run:gfms-aggregates",
    "entityType": "prov:Entity",
    "name": "Processing/gfms/Flood_byStor_2026030200.csv (per-watershed aggregates, duration not yet recalculated)",
    "mom:dataType": "GFMS",
    "dcterms:format": "text/csv",
    "mom:dataTime": "2026-03-02T00:00:00Z",
    "generatedAtTime": "2026-03-02T01:05:41Z",
    "wasGeneratedBy": "run:aggregation",
    "wasDerivedFrom": [
      "run:gfms-bin",
      "run:gfms-cells"
    ]
  },
  {
    "id": "run:gfms-summary-prev",
    "entityType": "prov:Entity",
    "name": "GFMS_summary/Flood_byStor_2026030121.csv",
    "mom:dataType": "GFMS",
    "dcterms:format": "text/csv",
    "mom:dataTime": "2026-03-01T21:00:00Z",
    "generatedAtTime": "2026-03-01T01:07:12Z"
  },
  {
    "id": "run:glofas-txt",
    "entityType": "prov:Entity",
    "name": "threspoints_2026030200.txt",
    "dcat:downloadURL": "https://example.org/glofas/threspoints_2026030200.txt",
    "mom:dataType": "GloFAS",
    "dcterms:format": "GloFAS threspoints station table (comma-separated text)",
    "mom:glofasNodataValue": -9999,
    "mom:dataTime": "2026-03-02T00:00:00Z",
    "generatedAtTime": "2026-03-02T00:58:10Z",
    "wasAttributedTo": "run:ecmwf"
  },
  {
    "id": "run:glofas-points",
    "entityType": "prov:Entity",
    "name": "GLOFAS/threspoints_2026030200.csv",
    "mom:dataType": "GloFAS",
    "dcterms:format": "text/csv",
    "mom:glofasNodataValue": -9999,
    "mom:dataTime": "2026-03-02T00:00:00Z",
    "generatedAtTime": "2026-03-02T00:58:12Z",
    "wasDerivedFrom": "run:glofas-txt"
  },
  {
    "id": "run:attributes",
    "entityType": "prov:Entity",
    "name": "data/Attributes.csv",
    "dcterms:format": "text/csv",
    "dcterms:hasVersion": "0.0.1-alpha",
    "dcterms:isPartOf": "run:mom"
  },
  {
    "id": "run:resilience",
    "entityType": "prov:Entity",
    "name": "data/Resilience_Index.csv",
    "dcterms:format": "text/csv",
    "dcterms:hasVersion": "0.0.1-alpha",
    "dcterms:isPartOf": "run:mom"
  },
  {
    "id": "run:weights",
    "entityType": "prov:Entity",
    "name": "data/GFMS_Weightage.csv",
    "dcterms:format": "text/csv",
    "dcterms:hasVersion": "0.0.1-alpha",
    "dcterms:isPartOf": "run:mom"
  },
  {
    "id": "run:hazard-parameters",
    "entityType": "prov:Entity",
    "name": "GloFAS + GFMS hazard score accumulation parameters",
    "dcterms:hasVersion": "0.0.1-alpha",
    "dcterms:isPartOf": "run:mom",
    "mom:gfmsDurationAreaThresholdKm2": 50
  },
  {
    "id": "run:hazard",
    "activityType": "mom:HazardScoreAccumulation",
    "name": "GloFAS + GFMS hazard score accumulation",
    "startedAtTime": "2026-03-02T01:12:40Z",
    "endedAtTime": "2026-03-02T01:12:47Z",
    "used": [
      "run:gfms-aggregates",
      "run:gfms-summary-prev",
      "run:glofas-points",
      "run:attributes",
      "run:resilience",
      "run:weights",
      "run:hazard-parameters"
    ],
    "generated": [
      "run:gfms-summary",
      "run:final-attributes",
      "run:attributes-clean"
    ],
    "wasAssociatedWith": [
      "run:mom",
      "run:rss-hydro",
      "run:server"
    ],
    "dcterms:isPartOf": "run:workflow-run"
  },
  {
    "id": "run:gfms-summary",
    "entityType": "prov:Entity",
    "name": "GFMS_summary/Flood_byStor_2026030200.csv (duration recalculated)",
    "mom:dataType": "GFMS",
    "dcterms:format": "text/csv",
    "mom:dataTime": "2026-03-02T00:00:00Z",
    "generatedAtTime": "2026-03-02T01:12:41Z",
    "wasGeneratedBy": "run:hazard",
    "wasDerivedFrom": [
      "run:gfms-aggregates",
      "run:gfms-summary-prev"
    ]
  },
  {
    "id": "run:final-attributes",
    "entityType": "prov:Entity",
    "name": "GFMS_MoM/Final_Attributes_20260302.csv",
    "dcterms:format": "text/csv",
    "generatedAtTime": "2026-03-02T01:12:47Z",
    "wasGeneratedBy": "run:hazard",
    "wasDerivedFrom": [
      "run:gfms-summary",
      "run:glofas-points",
      "run:attributes",
      "run:resilience",
      "run:weights"
    ]
  },
  {
    "id": "run:attributes-clean",
    "entityType": "prov:Entity",
    "name": "GFMS_MoM/Attributes_Clean_20260302.csv",
    "dcterms:format": "text/csv",
    "generatedAtTime": "2026-03-02T01:12:47Z",
    "wasGeneratedBy": "run:hazard",
    "wasDerivedFrom": "run:final-attributes"
  }
]

```

#### jsonld
```jsonld
{
  "@context": "https://katkatkateryna.github.io/ospd2026_bblocks-template/build/annotated/rss-hydro/mom/workflow/model-of-models/context.jsonld",
  "@graph": [
    {
      "id": "run:mom",
      "agentType": "prov:SoftwareAgent",
      "name": "MoMProduction",
      "dcterms:hasVersion": "0.0.1-alpha"
    },
    {
      "id": "run:rss-hydro",
      "agentType": "prov:Organization",
      "name": "RSS-Hydro"
    },
    {
      "id": "run:server",
      "agentType": "prov:Agent",
      "name": "mom-prod-01 (illustrative server)"
    },
    {
      "id": "run:workflow-run",
      "activityType": "mom:WorkflowRun",
      "name": "MoM workflow run, 2026-03-02 00:00",
      "startedAtTime": "2026-03-02T01:01:04Z",
      "endedAtTime": "2026-03-02T01:12:47Z",
      "wasAssociatedWith": [
        "run:mom",
        "run:rss-hydro",
        "run:server"
      ]
    },
    {
      "id": "run:umd",
      "agentType": "prov:Organization",
      "name": "University of Maryland (GFMS)"
    },
    {
      "id": "run:ecmwf",
      "agentType": "prov:Organization",
      "name": "ECMWF / CEMS (GloFAS)"
    },
    {
      "id": "run:watersheds",
      "entityType": "prov:Entity",
      "name": "Watershed_pfaf_id.shp",
      "dcterms:hasVersion": "0.0.0",
      "dcterms:format": "ESRI Shapefile",
      "mom:watershedFingerprint": "a09161ac707ef1d0355e92e730c8fe31e127149b803321bc988b3232058eea17",
      "generatedAtTime": "2026-01-15T00:00:00Z"
    },
    {
      "id": "run:gfms-grid",
      "entityType": "prov:Entity",
      "name": "GFMS Flood_byStor grid",
      "mom:dataType": "GFMS",
      "dcterms:format": "GDAL VRT",
      "mom:gridSignature": "[2880, 800, 0.125, 0.0, -180.0, 0.0, -0.125, 50.0]",
      "dcterms:hasVersion": "0.0.1-alpha",
      "dcterms:isPartOf": "run:mom"
    },
    {
      "id": "run:cell-attribution",
      "activityType": "mom:WatershedCellAttribution",
      "name": "GFMS cell attribution",
      "startedAtTime": "2026-03-02T01:01:04Z",
      "endedAtTime": "2026-03-02T01:04:11Z",
      "used": [
        "run:watersheds",
        "run:gfms-grid"
      ],
      "generated": "run:gfms-cells",
      "wasAssociatedWith": [
        "run:mom",
        "run:rss-hydro",
        "run:server"
      ],
      "dcterms:isPartOf": "run:workflow-run"
    },
    {
      "id": "run:gfms-cells",
      "entityType": "mom:WatershedCellLookup",
      "name": "gfms_watershed_cells.npz",
      "mom:dataType": "GFMS",
      "dcterms:format": "NumPy .npz cell lookup",
      "mom:watershedFingerprint": "a09161ac707ef1d0355e92e730c8fe31e127149b803321bc988b3232058eea17",
      "generatedAtTime": "2026-03-02T01:04:11Z",
      "wasGeneratedBy": "run:cell-attribution",
      "wasDerivedFrom": [
        "run:watersheds",
        "run:gfms-grid"
      ]
    },
    {
      "id": "run:gfms-bin",
      "entityType": "prov:Entity",
      "name": "Flood_byStor_2026030200.bin",
      "dcat:downloadURL": "https://example.org/gfms/Flood_byStor_2026030200.bin",
      "mom:dataType": "GFMS",
      "dcterms:format": "GFMS Flood_byStor binary grid (float32)",
      "mom:gfmsNodataValue": -9999,
      "mom:gridSignature": "[1440, 400, 0.25, 0.0, -180.0, 0.0, -0.25, 50.0]",
      "mom:dataTime": "2026-03-02T00:00:00Z",
      "generatedAtTime": "2026-03-02T01:05:32Z",
      "wasAttributedTo": "run:umd"
    },
    {
      "id": "run:aggregation-parameters",
      "entityType": "prov:Entity",
      "name": "GFMS per-watershed aggregation parameters",
      "dcterms:hasVersion": "0.0.1-alpha",
      "dcterms:isPartOf": "run:mom",
      "mom:gfmsDurationAreaThresholdKm2": 50,
      "mom:gfmsMinFileSizeBytes": 1000000
    },
    {
      "id": "run:aggregation",
      "activityType": "mom:PerWatershedAggregation",
      "name": "GFMS per-watershed aggregation",
      "startedAtTime": "2026-03-02T01:05:33Z",
      "endedAtTime": "2026-03-02T01:05:41Z",
      "used": [
        "run:gfms-bin",
        "run:gfms-cells",
        "run:aggregation-parameters"
      ],
      "generated": "run:gfms-aggregates",
      "wasAssociatedWith": [
        "run:mom",
        "run:rss-hydro",
        "run:server"
      ],
      "dcterms:isPartOf": "run:workflow-run"
    },
    {
      "id": "run:gfms-aggregates",
      "entityType": "prov:Entity",
      "name": "Processing/gfms/Flood_byStor_2026030200.csv (per-watershed aggregates, duration not yet recalculated)",
      "mom:dataType": "GFMS",
      "dcterms:format": "text/csv",
      "mom:dataTime": "2026-03-02T00:00:00Z",
      "generatedAtTime": "2026-03-02T01:05:41Z",
      "wasGeneratedBy": "run:aggregation",
      "wasDerivedFrom": [
        "run:gfms-bin",
        "run:gfms-cells"
      ]
    },
    {
      "id": "run:gfms-summary-prev",
      "entityType": "prov:Entity",
      "name": "GFMS_summary/Flood_byStor_2026030121.csv",
      "mom:dataType": "GFMS",
      "dcterms:format": "text/csv",
      "mom:dataTime": "2026-03-01T21:00:00Z",
      "generatedAtTime": "2026-03-01T01:07:12Z"
    },
    {
      "id": "run:glofas-txt",
      "entityType": "prov:Entity",
      "name": "threspoints_2026030200.txt",
      "dcat:downloadURL": "https://example.org/glofas/threspoints_2026030200.txt",
      "mom:dataType": "GloFAS",
      "dcterms:format": "GloFAS threspoints station table (comma-separated text)",
      "mom:glofasNodataValue": -9999,
      "mom:dataTime": "2026-03-02T00:00:00Z",
      "generatedAtTime": "2026-03-02T00:58:10Z",
      "wasAttributedTo": "run:ecmwf"
    },
    {
      "id": "run:glofas-points",
      "entityType": "prov:Entity",
      "name": "GLOFAS/threspoints_2026030200.csv",
      "mom:dataType": "GloFAS",
      "dcterms:format": "text/csv",
      "mom:glofasNodataValue": -9999,
      "mom:dataTime": "2026-03-02T00:00:00Z",
      "generatedAtTime": "2026-03-02T00:58:12Z",
      "wasDerivedFrom": "run:glofas-txt"
    },
    {
      "id": "run:attributes",
      "entityType": "prov:Entity",
      "name": "data/Attributes.csv",
      "dcterms:format": "text/csv",
      "dcterms:hasVersion": "0.0.1-alpha",
      "dcterms:isPartOf": "run:mom"
    },
    {
      "id": "run:resilience",
      "entityType": "prov:Entity",
      "name": "data/Resilience_Index.csv",
      "dcterms:format": "text/csv",
      "dcterms:hasVersion": "0.0.1-alpha",
      "dcterms:isPartOf": "run:mom"
    },
    {
      "id": "run:weights",
      "entityType": "prov:Entity",
      "name": "data/GFMS_Weightage.csv",
      "dcterms:format": "text/csv",
      "dcterms:hasVersion": "0.0.1-alpha",
      "dcterms:isPartOf": "run:mom"
    },
    {
      "id": "run:hazard-parameters",
      "entityType": "prov:Entity",
      "name": "GloFAS + GFMS hazard score accumulation parameters",
      "dcterms:hasVersion": "0.0.1-alpha",
      "dcterms:isPartOf": "run:mom",
      "mom:gfmsDurationAreaThresholdKm2": 50
    },
    {
      "id": "run:hazard",
      "activityType": "mom:HazardScoreAccumulation",
      "name": "GloFAS + GFMS hazard score accumulation",
      "startedAtTime": "2026-03-02T01:12:40Z",
      "endedAtTime": "2026-03-02T01:12:47Z",
      "used": [
        "run:gfms-aggregates",
        "run:gfms-summary-prev",
        "run:glofas-points",
        "run:attributes",
        "run:resilience",
        "run:weights",
        "run:hazard-parameters"
      ],
      "generated": [
        "run:gfms-summary",
        "run:final-attributes",
        "run:attributes-clean"
      ],
      "wasAssociatedWith": [
        "run:mom",
        "run:rss-hydro",
        "run:server"
      ],
      "dcterms:isPartOf": "run:workflow-run"
    },
    {
      "id": "run:gfms-summary",
      "entityType": "prov:Entity",
      "name": "GFMS_summary/Flood_byStor_2026030200.csv (duration recalculated)",
      "mom:dataType": "GFMS",
      "dcterms:format": "text/csv",
      "mom:dataTime": "2026-03-02T00:00:00Z",
      "generatedAtTime": "2026-03-02T01:12:41Z",
      "wasGeneratedBy": "run:hazard",
      "wasDerivedFrom": [
        "run:gfms-aggregates",
        "run:gfms-summary-prev"
      ]
    },
    {
      "id": "run:final-attributes",
      "entityType": "prov:Entity",
      "name": "GFMS_MoM/Final_Attributes_20260302.csv",
      "dcterms:format": "text/csv",
      "generatedAtTime": "2026-03-02T01:12:47Z",
      "wasGeneratedBy": "run:hazard",
      "wasDerivedFrom": [
        "run:gfms-summary",
        "run:glofas-points",
        "run:attributes",
        "run:resilience",
        "run:weights"
      ]
    },
    {
      "id": "run:attributes-clean",
      "entityType": "prov:Entity",
      "name": "GFMS_MoM/Attributes_Clean_20260302.csv",
      "dcterms:format": "text/csv",
      "generatedAtTime": "2026-03-02T01:12:47Z",
      "wasGeneratedBy": "run:hazard",
      "wasDerivedFrom": "run:final-attributes"
    }
  ]
}
```

#### ttl
```ttl
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix mom: <https://rss-hydro.lu/ns/mom/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix run: <https://example.org/mom/run/2026030200/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

run:aggregation a mom:PerWatershedAggregation ;
    rdfs:label "GFMS per-watershed aggregation" ;
    dcterms:isPartOf run:workflow-run ;
    prov:endedAtTime "2026-03-02T01:05:41+00:00"^^xsd:dateTime ;
    prov:generated run:gfms-aggregates ;
    prov:startedAtTime "2026-03-02T01:05:33+00:00"^^xsd:dateTime ;
    prov:used run:aggregation-parameters,
        run:gfms-bin,
        run:gfms-cells ;
    prov:wasAssociatedWith run:mom,
        run:rss-hydro,
        run:server .

run:aggregation-parameters a prov:Entity ;
    rdfs:label "GFMS per-watershed aggregation parameters" ;
    dcterms:hasVersion "0.0.1-alpha" ;
    dcterms:isPartOf run:mom ;
    mom:gfmsDurationAreaThresholdKm2 50 ;
    mom:gfmsMinFileSizeBytes 1000000 .

run:attributes-clean a prov:Entity ;
    rdfs:label "GFMS_MoM/Attributes_Clean_20260302.csv" ;
    dcterms:format "text/csv" ;
    prov:generatedAtTime "2026-03-02T01:12:47+00:00"^^xsd:dateTime ;
    prov:wasDerivedFrom run:final-attributes ;
    prov:wasGeneratedBy run:hazard .

run:cell-attribution a mom:WatershedCellAttribution ;
    rdfs:label "GFMS cell attribution" ;
    dcterms:isPartOf run:workflow-run ;
    prov:endedAtTime "2026-03-02T01:04:11+00:00"^^xsd:dateTime ;
    prov:generated run:gfms-cells ;
    prov:startedAtTime "2026-03-02T01:01:04+00:00"^^xsd:dateTime ;
    prov:used run:gfms-grid,
        run:watersheds ;
    prov:wasAssociatedWith run:mom,
        run:rss-hydro,
        run:server .

run:ecmwf a prov:Organization ;
    rdfs:label "ECMWF / CEMS (GloFAS)" .

run:glofas-txt a prov:Entity ;
    rdfs:label "threspoints_2026030200.txt" ;
    dcterms:format "GloFAS threspoints station table (comma-separated text)" ;
    dcat:downloadURL <https://example.org/glofas/threspoints_2026030200.txt> ;
    prov:generatedAtTime "2026-03-02T00:58:10+00:00"^^xsd:dateTime ;
    prov:wasAttributedTo run:ecmwf ;
    mom:dataTime "2026-03-02T00:00:00+00:00"^^xsd:dateTime ;
    mom:dataType "GloFAS" ;
    mom:glofasNodataValue -9999 .

run:hazard-parameters a prov:Entity ;
    rdfs:label "GloFAS + GFMS hazard score accumulation parameters" ;
    dcterms:hasVersion "0.0.1-alpha" ;
    dcterms:isPartOf run:mom ;
    mom:gfmsDurationAreaThresholdKm2 50 .

run:umd a prov:Organization ;
    rdfs:label "University of Maryland (GFMS)" .

run:attributes a prov:Entity ;
    rdfs:label "data/Attributes.csv" ;
    dcterms:format "text/csv" ;
    dcterms:hasVersion "0.0.1-alpha" ;
    dcterms:isPartOf run:mom .

run:final-attributes a prov:Entity ;
    rdfs:label "GFMS_MoM/Final_Attributes_20260302.csv" ;
    dcterms:format "text/csv" ;
    prov:generatedAtTime "2026-03-02T01:12:47+00:00"^^xsd:dateTime ;
    prov:wasDerivedFrom run:attributes,
        run:gfms-summary,
        run:glofas-points,
        run:resilience,
        run:weights ;
    prov:wasGeneratedBy run:hazard .

run:gfms-bin a prov:Entity ;
    rdfs:label "Flood_byStor_2026030200.bin" ;
    dcterms:format "GFMS Flood_byStor binary grid (float32)" ;
    dcat:downloadURL <https://example.org/gfms/Flood_byStor_2026030200.bin> ;
    prov:generatedAtTime "2026-03-02T01:05:32+00:00"^^xsd:dateTime ;
    prov:wasAttributedTo run:umd ;
    mom:dataTime "2026-03-02T00:00:00+00:00"^^xsd:dateTime ;
    mom:dataType "GFMS" ;
    mom:gfmsNodataValue -9999 ;
    mom:gridSignature "[1440, 400, 0.25, 0.0, -180.0, 0.0, -0.25, 50.0]" .

run:gfms-grid a prov:Entity ;
    rdfs:label "GFMS Flood_byStor grid" ;
    dcterms:format "GDAL VRT" ;
    dcterms:hasVersion "0.0.1-alpha" ;
    dcterms:isPartOf run:mom ;
    mom:dataType "GFMS" ;
    mom:gridSignature "[2880, 800, 0.125, 0.0, -180.0, 0.0, -0.125, 50.0]" .

run:gfms-summary a prov:Entity ;
    rdfs:label "GFMS_summary/Flood_byStor_2026030200.csv (duration recalculated)" ;
    dcterms:format "text/csv" ;
    prov:generatedAtTime "2026-03-02T01:12:41+00:00"^^xsd:dateTime ;
    prov:wasDerivedFrom run:gfms-aggregates,
        run:gfms-summary-prev ;
    prov:wasGeneratedBy run:hazard ;
    mom:dataTime "2026-03-02T00:00:00+00:00"^^xsd:dateTime ;
    mom:dataType "GFMS" .

run:gfms-summary-prev a prov:Entity ;
    rdfs:label "GFMS_summary/Flood_byStor_2026030121.csv" ;
    dcterms:format "text/csv" ;
    prov:generatedAtTime "2026-03-01T01:07:12+00:00"^^xsd:dateTime ;
    mom:dataTime "2026-03-01T21:00:00+00:00"^^xsd:dateTime ;
    mom:dataType "GFMS" .

run:glofas-points a prov:Entity ;
    rdfs:label "GLOFAS/threspoints_2026030200.csv" ;
    dcterms:format "text/csv" ;
    prov:generatedAtTime "2026-03-02T00:58:12+00:00"^^xsd:dateTime ;
    prov:wasDerivedFrom run:glofas-txt ;
    mom:dataTime "2026-03-02T00:00:00+00:00"^^xsd:dateTime ;
    mom:dataType "GloFAS" ;
    mom:glofasNodataValue -9999 .

run:resilience a prov:Entity ;
    rdfs:label "data/Resilience_Index.csv" ;
    dcterms:format "text/csv" ;
    dcterms:hasVersion "0.0.1-alpha" ;
    dcterms:isPartOf run:mom .

run:watersheds a prov:Entity ;
    rdfs:label "Watershed_pfaf_id.shp" ;
    dcterms:format "ESRI Shapefile" ;
    dcterms:hasVersion "0.0.0" ;
    prov:generatedAtTime "2026-01-15T00:00:00+00:00"^^xsd:dateTime ;
    mom:watershedFingerprint "a09161ac707ef1d0355e92e730c8fe31e127149b803321bc988b3232058eea17" .

run:weights a prov:Entity ;
    rdfs:label "data/GFMS_Weightage.csv" ;
    dcterms:format "text/csv" ;
    dcterms:hasVersion "0.0.1-alpha" ;
    dcterms:isPartOf run:mom .

run:gfms-aggregates a prov:Entity ;
    rdfs:label "Processing/gfms/Flood_byStor_2026030200.csv (per-watershed aggregates, duration not yet recalculated)" ;
    dcterms:format "text/csv" ;
    prov:generatedAtTime "2026-03-02T01:05:41+00:00"^^xsd:dateTime ;
    prov:wasDerivedFrom run:gfms-bin,
        run:gfms-cells ;
    prov:wasGeneratedBy run:aggregation ;
    mom:dataTime "2026-03-02T00:00:00+00:00"^^xsd:dateTime ;
    mom:dataType "GFMS" .

run:gfms-cells a mom:WatershedCellLookup ;
    rdfs:label "gfms_watershed_cells.npz" ;
    dcterms:format "NumPy .npz cell lookup" ;
    prov:generatedAtTime "2026-03-02T01:04:11+00:00"^^xsd:dateTime ;
    prov:wasDerivedFrom run:gfms-grid,
        run:watersheds ;
    prov:wasGeneratedBy run:cell-attribution ;
    mom:dataType "GFMS" ;
    mom:watershedFingerprint "a09161ac707ef1d0355e92e730c8fe31e127149b803321bc988b3232058eea17" .

run:hazard a mom:HazardScoreAccumulation ;
    rdfs:label "GloFAS + GFMS hazard score accumulation" ;
    dcterms:isPartOf run:workflow-run ;
    prov:endedAtTime "2026-03-02T01:12:47+00:00"^^xsd:dateTime ;
    prov:generated run:attributes-clean,
        run:final-attributes,
        run:gfms-summary ;
    prov:startedAtTime "2026-03-02T01:12:40+00:00"^^xsd:dateTime ;
    prov:used run:attributes,
        run:gfms-aggregates,
        run:gfms-summary-prev,
        run:glofas-points,
        run:hazard-parameters,
        run:resilience,
        run:weights ;
    prov:wasAssociatedWith run:mom,
        run:rss-hydro,
        run:server .

run:workflow-run a mom:WorkflowRun ;
    rdfs:label "MoM workflow run, 2026-03-02 00:00" ;
    prov:endedAtTime "2026-03-02T01:12:47+00:00"^^xsd:dateTime ;
    prov:startedAtTime "2026-03-02T01:01:04+00:00"^^xsd:dateTime ;
    prov:wasAssociatedWith run:mom,
        run:rss-hydro,
        run:server .

run:rss-hydro a prov:Organization ;
    rdfs:label "RSS-Hydro" .

run:server a prov:Agent ;
    rdfs:label "mom-prod-01 (illustrative server)" .

run:mom a prov:SoftwareAgent ;
    rdfs:label "MoMProduction" ;
    dcterms:hasVersion "0.0.1-alpha" .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
description: Provenance chain of one MoM GFMS + GloFAS run. Per-watershed aggregation
  and hazard score accumulation are always present; cell attribution only when the
  cell lookup is (re)built in the same run.
allOf:
- $ref: https://ogcincubator.github.io/bblock-prov-schema/build/annotated/ogc-utils/prov/schema.yaml
contains:
  $ref: https://katkatkateryna.github.io/ospd2026_bblocks-template/build/annotated/rss-hydro/mom/processing-activity/schema.yaml
minContains: 2
x-jsonld-extra-terms:
  mom:dataTime:
    x-jsonld-type: http://www.w3.org/2001/XMLSchema#dateTime
  dcat:downloadURL:
    x-jsonld-type: '@id'
  dcterms:isPartOf:
    x-jsonld-type: '@id'
x-jsonld-prefixes:
  xsd: http://www.w3.org/2001/XMLSchema#
  mom: https://rss-hydro.lu/ns/mom/
  run: https://example.org/mom/run/2026030200/
  dcat: http://www.w3.org/ns/dcat#
  dcterms: http://purl.org/dc/terms/

```

Links to the schema:

* YAML version: [schema.yaml](https://katkatkateryna.github.io/ospd2026_bblocks-template/build/annotated/rss-hydro/mom/workflow/model-of-models/schema.json)
* JSON version: [schema.json](https://katkatkateryna.github.io/ospd2026_bblocks-template/build/annotated/rss-hydro/mom/workflow/model-of-models/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "wasInfluencedBy": {
      "@id": "prov:wasInfluencedBy",
      "@type": "@id"
    },
    "qualifiedInfluence": {
      "@id": "prov:qualifiedInfluence",
      "@type": "@id"
    },
    "hadMember": {
      "@id": "prov:hadMember",
      "@type": "@id"
    },
    "id": "@id",
    "provType": "@type",
    "featureType": "@type",
    "entityType": "@type",
    "has_provenance": {
      "@id": "dct:provenance",
      "@type": "@id"
    },
    "wasGeneratedBy": {
      "@id": "prov:wasGeneratedBy",
      "@type": "@id"
    },
    "wasAttributedTo": {
      "@id": "prov:wasAttributedTo",
      "@type": "@id"
    },
    "wasDerivedFrom": {
      "@id": "prov:wasDerivedFrom",
      "@type": "@id"
    },
    "alternateOf": {
      "@id": "prov:alternateOf",
      "@type": "@id"
    },
    "hadPrimarySource": {
      "@id": "prov:hadPrimarySource",
      "@type": "@id"
    },
    "specializationOf": {
      "@id": "prov:specializationOf",
      "@type": "@id"
    },
    "wasInvalidatedBy": {
      "@id": "prov:wasInvalidatedBy",
      "@type": "@id"
    },
    "wasQuotedFrom": {
      "@id": "prov:wasQuotedFrom",
      "@type": "@id"
    },
    "wasRevisionOf": {
      "@id": "prov:wasRevisionOf",
      "@type": "@id"
    },
    "generatedAtTime": {
      "@id": "prov:generatedAtTime",
      "@type": "xsd:dateTime"
    },
    "invalidatedAtTime": {
      "@id": "prov:invalidatedAtTime",
      "@type": "xsd:dateTime"
    },
    "value": "prov:value",
    "qualifiedPrimarySource": {
      "@id": "prov:qualifiedPrimarySource",
      "@type": "@id"
    },
    "qualifiedQuotation": {
      "@id": "prov:qualifiedQuotation",
      "@type": "@id"
    },
    "qualifiedRevision": {
      "@id": "prov:qualifiedRevision",
      "@type": "@id"
    },
    "atLocation": {
      "@id": "prov:atLocation",
      "@type": "@id"
    },
    "links": {
      "@context": {
        "href": {
          "@type": "@id",
          "@id": "oa:hasTarget"
        },
        "rel": {
          "@context": {
            "@base": "http://www.iana.org/assignments/relation/"
          },
          "@id": "http://www.iana.org/assignments/relation",
          "@type": "@id"
        },
        "type": "dct:type",
        "hreflang": "dct:language",
        "title": "rdfs:label",
        "length": "dct:extent"
      },
      "@id": "rdfs:seeAlso"
    },
    "qualifiedGeneration": {
      "@id": "prov:qualifiedGeneration",
      "@type": "@id"
    },
    "qualifiedInvalidation": {
      "@id": "prov:qualifiedInvalidation",
      "@type": "@id"
    },
    "qualifiedDerivation": {
      "@id": "prov:qualifiedDerivation",
      "@type": "@id"
    },
    "qualifiedAttribution": {
      "@id": "prov:qualifiedAttribution",
      "@type": "@id"
    },
    "activityType": "@type",
    "agentType": "@type",
    "Activity": "prov:Activity",
    "ActivityInfluence": "prov:ActivityInfluence",
    "Agent": "prov:Agent",
    "AgentInfluence": "prov:AgentInfluence",
    "Association": "prov:Association",
    "Attribution": "prov:Attribution",
    "Bundle": "prov:Bundle",
    "Collection": "prov:Collection",
    "Communication": "prov:Communication",
    "Delegation": "prov:Delegation",
    "Derivation": "prov:Derivation",
    "EmptyCollection": "prov:EmptyCollection",
    "End": "prov:End",
    "Entity": "prov:Entity",
    "EntityInfluence": "prov:EntityInfluence",
    "Generation": "prov:Generation",
    "Influence": "prov:Influence",
    "InstantaneousEvent": "prov:InstantaneousEvent",
    "Invalidation": "prov:Invalidation",
    "Location": "prov:Location",
    "Organization": "prov:Organization",
    "Person": "prov:Person",
    "Plan": "prov:Plan",
    "PrimarySource": "prov:PrimarySource",
    "Quotation": "prov:Quotation",
    "Revision": "prov:Revision",
    "Role": "prov:Role",
    "SoftwareAgent": "prov:SoftwareAgent",
    "Start": "prov:Start",
    "Usage": "prov:Usage",
    "ServiceDescription": "prov:ServiceDescription",
    "DirectQueryService": "prov:DirectQueryService",
    "Accept": "prov:Accept",
    "Contribute": "prov:Contribute",
    "Contributor": "prov:Contributor",
    "Copyright": "prov:Copyright",
    "Create": "prov:Create",
    "Creator": "prov:Creator",
    "Modify": "prov:Modify",
    "Publish": "prov:Publish",
    "Publisher": "prov:Publisher",
    "Replace": "prov:Replace",
    "RightsAssignment": "prov:RightsAssignment",
    "RightsHolder": "prov:RightsHolder",
    "Submit": "prov:Submit",
    "Dictionary": "prov:Dictionary",
    "EmptyDictionary": "prov:EmptyDictionary",
    "KeyEntityPair": "prov:KeyEntityPair",
    "Insertion": "prov:Insertion",
    "Removal": "prov:Removal",
    "atTime": {
      "@id": "prov:atTime",
      "@type": "xsd:dateTime"
    },
    "endedAtTime": {
      "@id": "prov:endedAtTime",
      "@type": "xsd:dateTime"
    },
    "startedAtTime": {
      "@id": "prov:startedAtTime",
      "@type": "xsd:dateTime"
    },
    "provenanceUriTemplate": "prov:provenanceUriTemplate",
    "pairKey": {
      "@id": "prov:pairKey",
      "@type": "rdfs:Literal"
    },
    "removedKey": {
      "@id": "prov:removedKey",
      "@type": "rdfs:Literal"
    },
    "actedOnBehalfOf": {
      "@id": "prov:actedOnBehalfOf",
      "@type": "@id"
    },
    "agent": {
      "@id": "prov:agent",
      "@type": "@id"
    },
    "entity": {
      "@id": "prov:entity",
      "@type": "@id"
    },
    "generated": {
      "@id": "prov:generated",
      "@type": "@id"
    },
    "hadActivity": {
      "@id": "prov:hadActivity",
      "@type": "@id"
    },
    "activity": {
      "@id": "prov:activity",
      "@type": "@id"
    },
    "hadGeneration": {
      "@id": "prov:hadGeneration",
      "@type": "@id"
    },
    "hadPlan": {
      "@id": "prov:hadPlan",
      "@type": "@id"
    },
    "hadRole": {
      "@id": "prov:hadRole",
      "@type": "@id"
    },
    "hadUsage": {
      "@id": "prov:hadUsage",
      "@type": "@id"
    },
    "influenced": {
      "@id": "prov:influenced",
      "@type": "@id"
    },
    "influencer": {
      "@id": "prov:influencer",
      "@type": "@id"
    },
    "invalidated": {
      "@id": "prov:invalidated",
      "@type": "@id"
    },
    "qualifiedAssociation": {
      "@id": "prov:qualifiedAssociation",
      "@type": "@id"
    },
    "qualifiedCommunication": {
      "@id": "prov:qualifiedCommunication",
      "@type": "@id"
    },
    "qualifiedDelegation": {
      "@id": "prov:qualifiedDelegation",
      "@type": "@id"
    },
    "qualifiedEnd": {
      "@id": "prov:qualifiedEnd",
      "@type": "@id"
    },
    "qualifiedStart": {
      "@id": "prov:qualifiedStart",
      "@type": "@id"
    },
    "qualifiedUsage": {
      "@id": "prov:qualifiedUsage",
      "@type": "@id"
    },
    "used": {
      "@id": "prov:used",
      "@type": "@id"
    },
    "wasAssociatedWith": {
      "@id": "prov:wasAssociatedWith",
      "@type": "@id"
    },
    "wasEndedBy": {
      "@id": "prov:wasEndedBy",
      "@type": "@id"
    },
    "wasInformedBy": {
      "@id": "prov:wasInformedBy",
      "@type": "@id"
    },
    "wasStartedBy": {
      "@id": "prov:wasStartedBy",
      "@type": "@id"
    },
    "has_anchor": {
      "@id": "prov:has_anchor",
      "@type": "@id"
    },
    "has_query_service": {
      "@id": "prov:has_query_service",
      "@type": "@id"
    },
    "describesService": {
      "@id": "prov:describesService",
      "@type": "@id"
    },
    "pingback": {
      "@id": "prov:pingback",
      "@type": "@id"
    },
    "dictionary": {
      "@id": "prov:dictionary",
      "@type": "@id"
    },
    "derivedByInsertionFrom": {
      "@id": "prov:derivedByInsertionFrom",
      "@type": "@id"
    },
    "derivedByRemovalFrom": {
      "@id": "prov:derivedByRemovalFrom",
      "@type": "@id"
    },
    "insertedKeyEntityPair": {
      "@id": "prov:insertedKeyEntityPair",
      "@type": "@id"
    },
    "hadDictionaryMember": {
      "@id": "prov:hadDictionaryMember",
      "@type": "@id"
    },
    "pairEntity": {
      "@id": "prov:pairEntity",
      "@type": "@id"
    },
    "qualifiedInsertion": {
      "@id": "prov:qualifiedInsertion",
      "@type": "@id"
    },
    "qualifiedRemoval": {
      "@id": "prov:qualifiedRemoval",
      "@type": "@id"
    },
    "asInBundle": {
      "@id": "prov:asInBundle",
      "@type": "@id"
    },
    "mentionOf": {
      "@id": "prov:mentionOf",
      "@type": "@id"
    },
    "name": "rdfs:label",
    "mom:dataTime": {
      "@type": "xsd:dateTime"
    },
    "dcat:downloadURL": {
      "@type": "@id"
    },
    "dcterms:isPartOf": {
      "@type": "@id"
    },
    "prov": "http://www.w3.org/ns/prov#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "dct": "http://purl.org/dc/terms/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "oa": "http://www.w3.org/ns/oa#",
    "mom": "https://rss-hydro.lu/ns/mom/",
    "run": "https://example.org/mom/run/2026030200/",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dcterms": "http://purl.org/dc/terms/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://katkatkateryna.github.io/ospd2026_bblocks-template/build/annotated/rss-hydro/mom/workflow/model-of-models/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/KatKatKateryna/ospd2026_bblocks-template](https://github.com/KatKatKateryna/ospd2026_bblocks-template)
* Path: `_sources/workflow/model-of-models`

