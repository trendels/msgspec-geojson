from msgspec import Struct
from msgspec.json import schema_components

from msgspec_geojson import Feature, FeatureCollection, Geometry, Point


class PoiProperties(Struct):
    name: str
    kind: str


def test_geometry_schema():
    _, components = schema_components([Geometry])

    assert list(components) == [
        "Point",
        "MultiPoint",
        "LineString",
        "MultiLineString",
        "Polygon",
        "MultiPolygon",
        "GeometryCollection",
    ]

    assert components["Point"] == {
        "type": "object",
        "title": "Point",
        "description": "A GeoJSON Point Geometry",
        "properties": {
            "type": {"enum": ["Point"]},
            "coordinates": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "prefixItems": [{"type": "number"}, {"type": "number"}],
                "items": False,
            },
        },
        "required": ["type", "coordinates"],
    }

    assert components["MultiPoint"] == {
        "type": "object",
        "title": "MultiPoint",
        "description": "A GeoJSON MultiPoint Geometry",
        "properties": {
            "type": {"enum": ["MultiPoint"]},
            "coordinates": {
                "type": "array",
                "items": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "prefixItems": [{"type": "number"}, {"type": "number"}],
                    "items": False,
                },
            },
        },
        "required": ["type", "coordinates"],
    }

    assert components["LineString"] == {
        "type": "object",
        "title": "LineString",
        "description": "A GeoJSON LineString Geometry",
        "properties": {
            "type": {"enum": ["LineString"]},
            "coordinates": {
                "type": "array",
                "items": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "prefixItems": [{"type": "number"}, {"type": "number"}],
                    "items": False,
                },
            },
        },
        "required": ["type", "coordinates"],
    }

    assert components["MultiLineString"] == {
        "type": "object",
        "title": "MultiLineString",
        "description": "A GeoJSON MultiLineString Geometry",
        "properties": {
            "type": {"enum": ["MultiLineString"]},
            "coordinates": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "minItems": 2,
                        "maxItems": 2,
                        "prefixItems": [{"type": "number"}, {"type": "number"}],
                        "items": False,
                    },
                },
            },
        },
        "required": ["type", "coordinates"],
    }

    assert components["Polygon"] == {
        "type": "object",
        "title": "Polygon",
        "description": "A GeoJSON Polygon Geometry",
        "properties": {
            "type": {"enum": ["Polygon"]},
            "coordinates": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "minItems": 2,
                        "maxItems": 2,
                        "prefixItems": [{"type": "number"}, {"type": "number"}],
                        "items": False,
                    },
                },
            },
        },
        "required": ["type", "coordinates"],
    }

    assert components["MultiPolygon"] == {
        "type": "object",
        "title": "MultiPolygon",
        "description": "A GeoJSON MultiPolygon Geometry",
        "properties": {
            "type": {"enum": ["MultiPolygon"]},
            "coordinates": {
                "type": "array",
                "items": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "minItems": 2,
                            "maxItems": 2,
                            "prefixItems": [{"type": "number"}, {"type": "number"}],
                            "items": False,
                        },
                    },
                },
            },
        },
        "required": ["type", "coordinates"],
    }


def test_schema_components_for_typed_feature():
    schemas, components = schema_components([Feature[Point, PoiProperties]])

    assert schemas == ({"$ref": "#/$defs/Feature_Point__PoiProperties_"},)
    assert list(components) == [
        "Feature_Point__PoiProperties_",
        "Point",
        "PoiProperties",
    ]
    assert components["Feature_Point__PoiProperties_"] == {
        "type": "object",
        "title": "Feature[Point, PoiProperties]",
        "description": "A GeoJSON Feature",
        "properties": {
            "type": {"enum": ["Feature"]},
            "geometry": {"$ref": "#/$defs/Point"},
            "properties": {"$ref": "#/$defs/PoiProperties"},
            "id": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
            "bbox": {
                "type": "array",
                "minItems": 4,
                "maxItems": 4,
                "prefixItems": [
                    {"type": "number"},
                    {"type": "number"},
                    {"type": "number"},
                    {"type": "number"},
                ],
                "items": False,
            },
        },
        "required": ["type", "geometry", "properties"],
    }


def test_schema_components_for_typed_featurecollection():
    schemas, components = schema_components([FeatureCollection[Point, PoiProperties]])

    assert schemas == ({"$ref": "#/$defs/FeatureCollection_Point__PoiProperties_"},)
    assert list(components) == [
        "FeatureCollection_Point__PoiProperties_",
        "Feature_Point__PoiProperties_",
        "Point",
        "PoiProperties",
    ]
    assert components["FeatureCollection_Point__PoiProperties_"] == {
        "type": "object",
        "title": "FeatureCollection[Point, PoiProperties]",
        "description": "A GeoJSON FeatureCollection",
        "properties": {
            "type": {"enum": ["FeatureCollection"]},
            "features": {
                "type": "array",
                "items": {"$ref": "#/$defs/Feature_Point__PoiProperties_"},
            },
            "bbox": {
                "type": "array",
                "minItems": 4,
                "maxItems": 4,
                "prefixItems": [
                    {"type": "number"},
                    {"type": "number"},
                    {"type": "number"},
                    {"type": "number"},
                ],
                "items": False,
            },
        },
        "required": ["type", "features"],
    }
