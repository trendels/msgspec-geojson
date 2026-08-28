import json
from typing import Any

import msgspec.json
from msgspec import Struct

from msgspec_geojson import (
    Feature,
    FeatureCollection,
    GeoJSON,
    Geometry,
    LineString,
    Point,
    Polygon,
)

rfc7946_example_1 = """
  {
       "type": "FeatureCollection",
       "features": [{
           "type": "Feature",
           "geometry": {
               "type": "Point",
               "coordinates": [102.0, 0.5]
           },
           "properties": {
               "prop0": "value0"
           }
       }, {
           "type": "Feature",
           "geometry": {
               "type": "LineString",
               "coordinates": [
                   [102.0, 0.0],
                   [103.0, 1.0],
                   [104.0, 0.0],
                   [105.0, 1.0]
               ]
           },
           "properties": {
               "prop0": "value0",
               "prop1": 0.0
           }
       }, {
           "type": "Feature",
           "geometry": {
               "type": "Polygon",
               "coordinates": [
                   [
                       [100.0, 0.0],
                       [101.0, 0.0],
                       [101.0, 1.0],
                       [100.0, 1.0],
                       [100.0, 0.0]
                   ]
               ]
           },
           "properties": {
               "prop0": "value0",
               "prop1": {
                   "this": "that"
               }
           }
       }]
   }
"""

rfc7946_example_2 = """
   {
       "type": "Feature",
       "bbox": [-10.0, -10.0, 10.0, 10.0],
       "geometry": {
           "type": "Polygon",
           "coordinates": [
               [
                   [-10.0, -10.0],
                   [10.0, -10.0],
                   [10.0, 10.0],
                   [-10.0, -10.0]
               ]
           ]
       },
       "properties": null
   }
"""


def test_decode_example_featurecollection():
    obj = msgspec.json.decode(rfc7946_example_1, type=GeoJSON)

    assert obj == FeatureCollection[Geometry, dict[str, Any]](
        features=[
            Feature(
                Point((102.0, 0.5)),
                {"prop0": "value0"},
            ),
            Feature(
                LineString([
                    (102.0, 0.0),
                    (103.0, 1.0),
                    (104.0, 0.0),
                    (105.0, 1.0),
                ]),
                {"prop0": "value0", "prop1": 0.0},
            ),
            Feature(
                Polygon([
                    [
                        (100.0, 0.0),
                        (101.0, 0.0),
                        (101.0, 1.0),
                        (100.0, 1.0),
                        (100.0, 0.0),
                    ]
                ]),
                {"prop0": "value0", "prop1": {"this": "that"}},
            ),
        ],
    )


def test_encode_example_featurecollection():
    obj = FeatureCollection[Geometry, dict[str, Any]](
        features=[
            Feature(
                Point((102.0, 0.5)),
                {"prop0": "value0"},
            ),
            Feature(
                LineString([
                    (102.0, 0.0),
                    (103.0, 1.0),
                    (104.0, 0.0),
                    (105.0, 1.0),
                ]),
                {"prop0": "value0", "prop1": 0.0},
            ),
            Feature(
                Polygon([
                    [
                        (100.0, 0.0),
                        (101.0, 0.0),
                        (101.0, 1.0),
                        (100.0, 1.0),
                        (100.0, 0.0),
                    ]
                ]),
                {"prop0": "value0", "prop1": {"this": "that"}},
            ),
        ],
    )
    serialized = msgspec.json.encode(obj).decode()

    assert json.loads(serialized) == json.loads(rfc7946_example_1)


def test_decode_2d_bbox():
    obj = msgspec.json.decode(rfc7946_example_2, type=Feature[Polygon, None])

    assert obj == Feature(
        Polygon([
            [
                (-10.0, -10.0),
                (10.0, -10.0),
                (10.0, 10.0),
                (-10.0, -10.0),
            ]
        ]),
        bbox=(-10.0, -10.0, 10.0, 10.0),
    )


def test_encode_2d_bbox():
    obj = Feature[Polygon, None](
        Polygon([
            [
                (-10.0, -10.0),
                (10.0, -10.0),
                (10.0, 10.0),
                (-10.0, -10.0),
            ]
        ]),
        bbox=(-10.0, -10.0, 10.0, 10.0),
    )
    serialized = msgspec.json.encode(obj).decode()

    assert json.loads(serialized) == json.loads(rfc7946_example_2)


def test_decode_id():
    obj = msgspec.json.decode(
        """{"type": "Feature", "id": 1, "geometry": null, "properties": null}""",
        type=Feature[None, None],
    )

    assert obj == Feature(id=1)


def test_encode_id():
    obj = Feature[None, None](id=1)
    serialized = msgspec.json.encode(obj).decode()

    assert json.loads(serialized) == json.loads(
        """{"type": "Feature", "id": 1, "geometry": null, "properties": null}"""
    )


def test_decode_featurecollection_points():
    fc_json = """
    {"type": "FeatureCollection",
     "features": [
        {"type": "Feature",
         "geometry": {"type": "Point", "coordinates": [0.0, 0.0]},
         "properties": {"id": 1, "name": "origin"}
        },
        {"type": "Feature",
         "geometry": {"type": "Point", "coordinates": [1.0, 1.0]},
         "properties": {"id": 2, "name": "some place"}
        }
     ]
    }
    """

    class PoiProperties(Struct):
        id: int
        name: str

    obj = msgspec.json.decode(fc_json, type=FeatureCollection[Point, PoiProperties])

    assert obj == FeatureCollection([
        Feature(Point((0, 0)), PoiProperties(1, "origin")),
        Feature(Point((1, 1)), PoiProperties(2, "some place")),
    ])


def test_encode_featurecollection_points():
    class PoiProperties(Struct):
        id: int
        name: str

    obj: FeatureCollection[Point, PoiProperties] = FeatureCollection([
        Feature(Point((0, 0)), PoiProperties(1, "origin")),
        Feature(Point((1, 1)), PoiProperties(2, "some place")),
    ])
    serialized = msgspec.json.encode(obj).decode()

    assert json.loads(serialized) == json.loads("""
    {"type": "FeatureCollection",
     "features": [
        {"type": "Feature",
         "geometry": {"type": "Point", "coordinates": [0.0, 0.0]},
         "properties": {"id": 1, "name": "origin"}
        },
        {"type": "Feature",
         "geometry": {"type": "Point", "coordinates": [1.0, 1.0]},
         "properties": {"id": 2, "name": "some place"}
        }
     ]
    }
    """)
