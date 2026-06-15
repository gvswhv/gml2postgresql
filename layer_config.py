# -*- coding: utf-8 -*-
"""
layer_config.py – XPlanung layer definitions for GML2PostgreSQL

Each entry maps a GML layer name to its target database table, the attribute
columns to extract, additional plan-level fields read from the GML header, and
the expected geometry type.

Layers whose GML tag may carry mixed geometry types (point / line / polygon)
are listed under MULTI_GEOMETRY_LAYERS.  The processing logic dispatches each
feature to the correct suffixed table (_po, _li, _py) at runtime.
"""

# ---------------------------------------------------------------------------
# Layers with fixed, single geometry type
# ---------------------------------------------------------------------------

SINGLE_GEOMETRY_LAYERS = {
    "BP_GemeinbedarfsFlaeche": {
        "table": "BP_GemeinbedarfsFlaeche",
        "columns": ["gml_id", "zweckbestimmung", "bauweise", "bebauungsArt"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_GemeinschaftsanlagenFlaeche": {
        "table": "BP_GemeinschaftsanlagenFlaeche",
        "columns": ["gml_id", "zweckbestimmung"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_GewaesserFlaeche": {
        "table": "BP_GewaesserFlaeche",
        "columns": ["gml_id", "zweckbestimmung"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_GruenFlaeche": {
        "table": "BP_GruenFlaeche",
        "columns": ["gml_id", "zweckbestimmung", "nutzungsform"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_Immissionsschutz_li": {
        "table": "BP_Immissionsschutz_li",
        "columns": ["gml_id", "laermpegelbereich", "typ", "technVorkehrung"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "LINESTRING",
    },
    "BP_Immissionsschutz_py": {
        "table": "BP_Immissionsschutz_py",
        "columns": ["gml_id", "laermpegelbereich", "typ", "technVorkehrung"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_LandwirtschaftsFlaeche": {
        "table": "BP_LandwirtschaftsFlaeche",
        "columns": ["gml_id", "zweckbestimmung"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_NebenanlagenFlaeche": {
        "table": "BP_NebenanlagenFlaeche",
        "columns": ["gml_id", "zweckbestimmung"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_NichtUeberbaubareGrundstuecksflaeche": {
        "table": "BP_NichtUeberbaubareGrundstuecksflaeche",
        "columns": ["gml_id", "nutzung"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_SchutzPflegeEntwicklungsFlaeche": {
        "table": "BP_SchutzPflegeEntwicklungsFlaeche",
        "columns": ["gml_id", "ziel"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_SchutzPflegeEntwicklungsMassnahme": {
        "table": "BP_SchutzPflegeEntwicklungsMassnahme",
        "columns": ["gml_id", "ziel", "massnahme"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_StrassenVerkehrsFlaeche": {
        "table": "BP_StrassenVerkehrsFlaeche",
        "columns": ["gml_id", "nutzungsform"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_UeberbaubareGrundstuecksFlaeche": {
        "table": "BP_UeberbaubareGrundstuecksFlaeche",
        "columns": [
            "gml_id",
            "bauweise",
            "bebauungsArt",
            "bebauungVordereGrenze",
            "bebauungRueckwaertigeGrenze",
            "bebauungSeitlicheGrenze",
        ],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_VerkehrsflaecheBesondererZweckbestimmung_py": {
        "table": "BP_VerkehrsflaecheBesondererZweckbestimmung_py",
        "columns": ["gml_id", "zweckbestimmung", "detaillierteZweckbestimmung", "nutzungsform"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_WaldFlaeche": {
        "table": "BP_WaldFlaeche",
        "columns": [
            "gml_id",
            "zweckbestimmung",
            "detaillierteZweckbestimmung",
            "eigentumsart",
            "betreten",
        ],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_WasserwirtschaftsFlaeche": {
        "table": "BP_WasserwirtschaftsFlaeche",
        "columns": ["gml_id", "zweckbestimmung", "detaillierteZweckbestimmung"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "POLYGON",
    },
    "BP_BauGrenze": {
        "table": "BP_BauGrenze",
        "columns": ["gml_id", "rechtscharakter"],
        "extra_fields": ["inkrafttretensDatum", "nummer"],
        "geometry_type": "LINESTRING",
    },
}

# ---------------------------------------------------------------------------
# Layers whose features may carry point, line, or polygon geometry.
# Each base name maps to the three possible suffixed target tables.
# ---------------------------------------------------------------------------

MULTI_GEOMETRY_LAYERS = {
    "BP_AnpflanzungBindungErhaltung": {
        "_po": {
            "table": "BP_AnpflanzungBindungErhaltung_po",
            "columns": ["gml_id", "massnahme", "gegenstand"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POINT",
        },
        "_li": {
            "table": "BP_AnpflanzungBindungErhaltung_li",
            "columns": ["gml_id", "massnahme", "gegenstand"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "LINESTRING",
        },
        "_py": {
            "table": "BP_AnpflanzungBindungErhaltung_py",
            "columns": ["gml_id", "massnahme", "gegenstand"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POLYGON",
        },
    },
    "BP_BaugebietsTeilFlaeche": {
        "_po": {
            "table": "BP_BaugebietsTeilFlaeche_po",
            "columns": [
                "gml_id",
                "allgArtDerBaulNutzung",
                "besondereArtDerBaulNutzung",
                "sondernutzung",
                "abweichungBauNVO",
                "bauweise",
                "bebauungsArt",
                "bebauungVordereGrenze",
                "bebauungRueckwaertigeGrenze",
                "bebauungSeitlicheGrenze",
            ],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POINT",
        },
        "_li": {
            "table": "BP_BaugebietsTeilFlaeche_li",
            "columns": [
                "gml_id",
                "allgArtDerBaulNutzung",
                "besondereArtDerBaulNutzung",
                "sondernutzung",
                "abweichungBauNVO",
                "bauweise",
                "bebauungsArt",
                "bebauungVordereGrenze",
                "bebauungRueckwaertigeGrenze",
                "bebauungSeitlicheGrenze",
            ],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "LINESTRING",
        },
        "_py": {
            "table": "BP_BaugebietsTeilFlaeche_py",
            "columns": [
                "gml_id",
                "allgArtDerBaulNutzung",
                "besondereArtDerBaulNutzung",
                "sondernutzung",
                "abweichungBauNVO",
                "bauweise",
                "bebauungsArt",
                "bebauungVordereGrenze",
                "bebauungRueckwaertigeGrenze",
                "bebauungSeitlicheGrenze",
            ],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POLYGON",
        },
    },
    "BP_GenerischesObjekt": {
        "_po": {
            "table": "BP_GenerischesObjekt_po",
            "columns": ["gml_id", "zweckbestimmung"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POINT",
        },
        "_li": {
            "table": "BP_GenerischesObjekt_li",
            "columns": ["gml_id", "zweckbestimmung"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "LINESTRING",
        },
        "_py": {
            "table": "BP_GenerischesObjekt_py",
            "columns": ["gml_id", "zweckbestimmung"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POLYGON",
        },
    },
    "BP_Immissionsschutz": {
        "_li": {
            "table": "BP_Immissionsschutz_li",
            "columns": ["gml_id", "laermpegelbereich", "typ", "technVorkehrung"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "LINESTRING",
        },
        "_py": {
            "table": "BP_Immissionsschutz_py",
            "columns": ["gml_id", "laermpegelbereich", "typ", "technVorkehrung"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POLYGON",
        },
    },
    "BP_VerEntsorgung": {
        "_po": {
            "table": "BP_VerEntsorgung_po",
            "columns": ["gml_id", "zweckbestimmung", "detaillierteZweckbestimmung"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POINT",
        },
        "_li": {
            "table": "BP_VerEntsorgung_li",
            "columns": ["gml_id", "zweckbestimmung", "detaillierteZweckbestimmung"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "LINESTRING",
        },
        "_py": {
            "table": "BP_VerEntsorgung_py",
            "columns": ["gml_id", "zweckbestimmung", "detaillierteZweckbestimmung"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POLYGON",
        },
    },
    "BP_VerkehrsflaecheBesondererZweckbestimmung": {
        "_po": {
            "table": "BP_VerkehrsflaecheBesondererZweckbestimmung_po",
            "columns": ["gml_id", "zweckbestimmung", "detaillierteZweckbestimmung", "nutzungsform"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POINT",
        },
        "_py": {
            "table": "BP_VerkehrsflaecheBesondererZweckbestimmung_py",
            "columns": ["gml_id", "zweckbestimmung", "detaillierteZweckbestimmung", "nutzungsform"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POLYGON",
        },
    },
    "BP_Wegerecht": {
        "_po": {
            "table": "BP_Wegerecht_po",
            "columns": ["gml_id", "typ"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POINT",
        },
        "_li": {
            "table": "BP_Wegerecht_li",
            "columns": ["gml_id", "typ"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "LINESTRING",
        },
        "_py": {
            "table": "BP_Wegerecht_py",
            "columns": ["gml_id", "typ"],
            "extra_fields": ["inkrafttretensDatum", "nummer"],
            "geometry_type": "POLYGON",
        },
    },
}

# Geometry-type suffix → canonical target type string
SUFFIX_TO_GEOMETRY_TYPE = {
    "_po": "POINT",
    "_li": "LINESTRING",
    "_py": "POLYGON",
}
